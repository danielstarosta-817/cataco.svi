#!/usr/bin/env python3
"""
upgrade_seismic_from_usgs.py
────────────────────────────────────────────────────────────────────────
Replace the embedded earthquake catalog in index.html with real USGS data.

PREREQUISITES
  pip install requests pandas

USAGE
  python upgrade_seismic_from_usgs.py

The script:
  1. Downloads M4.5+ earthquakes 1990-2025 from USGS FDSN API for the
     Guerrero-Oaxaca-Chiapas bounding box (14-19.5°N, 103.5-93°W)
  2. Computes distance-weighted seismic exposure for each of the 775
     municipalities (inverse-distance^1.5 with magnitude^1.5 weighting)
  3. Adds trench-proximity baseline
  4. Normalizes to 0-1
  5. Injects new pseismic values + recomputes physS + sviS in index.html

OUTPUT
  Updates: <index.html path>/index.html
  Backup:  <index.html path>/index.html.bak
"""

import requests
import pandas as pd
import math
import re
import json
import shutil
import os
from datetime import datetime

# ─── PATHS ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_HTML  = os.path.join(SCRIPT_DIR, '..', 'index.html')
CACHE_CSV   = os.path.join(SCRIPT_DIR, 'usgs_earthquakes_cache.csv')

# ─── PARAMETERS ──────────────────────────────────────────────────────────
MIN_MAG    = 4.5
START_DATE = "1990-01-01"
END_DATE   = "2025-12-31"
MIN_LAT, MAX_LAT     = 14.0, 19.5
MIN_LON, MAX_LON     = -103.5, -93.0

# physS formula weights
W_HURR, W_SEIS, W_FLOOD, W_SLIDE = 1.3, 1.2, 1.0, 0.8
W_TOTAL = W_HURR + W_SEIS + W_FLOOD + W_SLIDE   # 4.3

# Middle America Trench approximation (lat, lon pairs)
TRENCH = [
    (18.8,-104.5),(18.2,-103.5),(17.5,-102.5),(16.8,-101.5),
    (16.0,-100.5),(15.5,-99.5),(15.2,-98.5),(15.0,-97.5),
    (14.8,-96.5),(14.7,-95.5),(14.6,-94.5),(14.4,-93.5),
    (14.0,-92.5),(13.8,-91.5),(13.5,-90.5),
]


def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2-lat1)
    dl = math.radians(lon2-lon1)
    a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return R * 2 * math.asin(math.sqrt(a))


def dist_to_trench_km(lat, lng):
    return min(haversine_km(lat, lng, t[0], t[1]) for t in TRENCH)


def download_usgs_catalog():
    """Download M4.5+ earthquake catalog from USGS FDSN API."""
    if os.path.exists(CACHE_CSV):
        print(f"  Loading cached catalog: {CACHE_CSV}")
        return pd.read_csv(CACHE_CSV)

    print("  Downloading from USGS FDSN API...")
    # API limit is 20,000 per request — fetch in two halves if needed
    base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "csv",
        "starttime": START_DATE,
        "endtime": END_DATE,
        "minmagnitude": MIN_MAG,
        "minlatitude": MIN_LAT,
        "maxlatitude": MAX_LAT,
        "minlongitude": MIN_LON,
        "maxlongitude": MAX_LON,
        "orderby": "time-asc",
        "limit": 20000,
    }
    r = requests.get(base_url, params=params, timeout=120)
    r.raise_for_status()

    from io import StringIO
    df = pd.read_csv(StringIO(r.text))
    df.to_csv(CACHE_CSV, index=False)
    print(f"  Downloaded {len(df)} events → cached to {CACHE_CSV}")
    return df


def compute_seismic_exposure(munis, eq_df):
    """
    Compute seismic exposure for each municipality.

    Model:
        exposure_i = sum_j( mag_j^1.5 / max(dist_km(i,j), 25)^1.5 )
                   + trench_bonus_i

    where trench_bonus_i = 0.6 * exp(-dist_to_trench_km_i / 250)
    """
    # Build epicenter list
    eq_pts = list(zip(
        eq_df['latitude'].values,
        eq_df['longitude'].values,
        eq_df['mag'].values,
    ))
    print(f"  Computing exposure for {len(munis)} municipalities using {len(eq_pts)} events...")

    raw = {}
    for i, m in enumerate(munis):
        if i % 100 == 0:
            print(f"    {i}/{len(munis)} ...", end='\r')
        lat, lng = m['lat'], m['lng']

        eq_exp = sum(
            (mag**1.5) / max(haversine_km(lat, lng, eq_lat, eq_lng), 25.0)**1.5
            for eq_lat, eq_lng, mag in eq_pts
            if not (math.isnan(eq_lat) or math.isnan(eq_lng) or math.isnan(mag))
        )
        d_trench = dist_to_trench_km(lat, lng)
        trench_bonus = 0.6 * math.exp(-d_trench / 250.0)

        raw[m['id']] = eq_exp + trench_bonus * 50

    print(f"    {len(munis)}/{len(munis)} done.       ")
    return raw


def normalize(raw_dict, p_lo=0.02, p_hi=0.96):
    """Normalize raw exposure values to [0.05, 1.0]."""
    vals = sorted(raw_dict.values())
    n = len(vals)
    lo = vals[int(n * p_lo)]
    hi = vals[int(n * p_hi)]
    span = hi - lo
    return {k: round(max(0.05, min(1.0, (v - lo) / span)), 4) for k, v in raw_dict.items()}


def update_html(index_html_path, pseismic):
    """Inject new seismic scores + recompute physS, sviS in index.html."""
    with open(index_html_path) as f:
        html = f.read()

    # Back up original
    bak = index_html_path + '.bak'
    shutil.copy2(index_html_path, bak)
    print(f"  Backup: {bak}")

    # Parse MUNICIPIOS
    mun_match = re.search(r'(var MUNICIPIOS=)(\[.*?\]);', html, re.DOTALL)
    if not mun_match:
        raise ValueError("Could not find MUNICIPIOS array in index.html")
    prefix = mun_match.group(1)
    munis = json.loads(mun_match.group(2))

    # Update pseismic
    for m in munis:
        if m['id'] in pseismic:
            m['pseismic'] = pseismic[m['id']]

    # Recompute physS
    for m in munis:
        ph = m.get('phurricane', 0.0)
        ps = m['pseismic']
        pf = m.get('pflood', 0.0)
        pl = m.get('pslide', 0.0)
        m['physS'] = round(max(0.0, min(1.0, (ph*W_HURR + ps*W_SEIS + pf*W_FLOOD + pl*W_SLIDE) / W_TOTAL)), 4)

    # Recompute sviS
    raw_svi = [m['physS'] + m['socS']**2 * 1.2 for m in munis]
    mn_r, mx_r = min(raw_svi), max(raw_svi)
    for m, r in zip(munis, raw_svi):
        m['sviS'] = round((r - mn_r) / (mx_r - mn_r), 4)

    # Serialize and inject
    def compact(obj):
        return json.dumps(obj, ensure_ascii=False, separators=(',', ':'))

    new_json = '[' + ','.join(compact(m) for m in munis) + ']'
    new_html = html[:mun_match.start()] + prefix + new_json + ';' + html[mun_match.end():]

    with open(index_html_path, 'w') as f:
        f.write(new_html)

    print(f"  Updated: {index_html_path}  ({len(new_html):,} bytes)")
    return munis


def main():
    print(f"\n{'='*60}")
    print("SVI-MEX Seismic Score Upgrader (USGS FDSN Edition)")
    print(f"{'='*60}\n")

    # Load municipality centroids from index.html
    index_html_path = os.path.realpath(INDEX_HTML)
    print(f"Reading: {index_html_path}")
    with open(index_html_path) as f:
        html = f.read()

    mun_match = re.search(r'var MUNICIPIOS=(\[.*?\]);', html, re.DOTALL)
    munis = json.loads(mun_match.group(1))
    print(f"Municipalities: {len(munis)}\n")

    # Download USGS catalog
    print("Step 1: Earthquake catalog")
    try:
        eq_df = download_usgs_catalog()
        # Validate
        eq_df = eq_df.dropna(subset=['latitude', 'longitude', 'mag'])
        eq_df = eq_df[eq_df['mag'] >= MIN_MAG]
        print(f"  {len(eq_df)} valid events  (M{eq_df['mag'].min():.1f}–M{eq_df['mag'].max():.1f})")
    except Exception as e:
        print(f"  ERROR downloading: {e}")
        print("  Falling back to embedded catalog (run without internet connection)")
        return

    # Compute exposure
    print("\nStep 2: Computing exposure")
    raw = compute_seismic_exposure(munis, eq_df)

    # Normalize
    print("\nStep 3: Normalizing")
    pseismic = normalize(raw)
    vals = list(pseismic.values())
    print(f"  Range: {min(vals):.4f} – {max(vals):.4f}  mean={sum(vals)/len(vals):.4f}")

    # Inject
    print("\nStep 4: Updating index.html")
    updated_munis = update_html(index_html_path, pseismic)

    # Spot-check
    print("\nSpot check:")
    checks = ['Acapulco','Tapachula','Tuxtla','Tehuantepec','Huatulco','Taxco']
    for m in updated_munis:
        if any(k.lower() in m['n'].lower() for k in checks):
            print(f"  {m['n']:40s} ps={m['pseismic']:.4f} physS={m['physS']:.4f} sviS={m['sviS']:.4f}")

    print(f"\n✓ Done — {datetime.now().strftime('%Y-%m-%d %H:%M')}")


if __name__ == '__main__':
    main()
