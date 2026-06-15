#!/usr/bin/env python3
"""
Mexico SVI Tool — Data Download and Processing Script
Run this locally (macOS/Linux) to download all Tier 1–3 data sources,
filter to Guerrero (12), Oaxaca (20), Chiapas (07), and join into a
master municipality table keyed by CVE_GEO.

Output: data/processed/master_municipalities.csv
        data/processed/municipalities.geojson  (if geopandas available)

Requirements: pip install pandas openpyxl requests geopandas
"""

import os, sys, zipfile, io, re
import pandas as pd
import requests

RAW   = os.path.join(os.path.dirname(__file__), "raw")
PROC  = os.path.join(os.path.dirname(__file__), "processed")
os.makedirs(RAW, exist_ok=True)
os.makedirs(PROC, exist_ok=True)

TARGET_STATES = {"07": "Chiapas", "12": "Guerrero", "20": "Oaxaca"}

def download(url, dest, desc=""):
    if os.path.exists(dest):
        print(f"  [skip] {desc or dest} already downloaded")
        return
    print(f"  Downloading {desc or url}...")
    r = requests.get(url, timeout=120, stream=True)
    r.raise_for_status()
    with open(dest, "wb") as f:
        for chunk in r.iter_content(65536):
            f.write(chunk)
    print(f"  Saved → {dest}")


# ─────────────────────────────────────────────
# TIER 1A: CONAPO Marginalization Index 2020
# ─────────────────────────────────────────────
def get_conapo():
    print("\n[1/5] CONAPO Marginalization Index 2020")
    url  = "https://conapo.segob.gob.mx/work/models/CONAPO/Datos_Abiertos/Municipio/IMM_2020.xls"
    dest = os.path.join(RAW, "IMM_2020.xls")
    download(url, dest, "CONAPO IMM 2020")

    df = pd.read_excel(dest, header=0, dtype=str)
    # Standardise column names (CONAPO uses Spanish with accents)
    df.columns = [c.strip().upper()
                    .replace("Á","A").replace("É","E").replace("Í","I")
                    .replace("Ó","O").replace("Ú","U").replace("Ñ","N")
                  for c in df.columns]
    print("  CONAPO columns:", list(df.columns)[:10], "...")

    # Build CVE_GEO = zero-padded state (2) + municipio (3)
    # CONAPO usually has CVE_ENT and CVE_MUN or similar
    cve_col = next((c for c in df.columns if "CVE" in c and "ENT" in c), None)
    mun_col = next((c for c in df.columns if "CVE" in c and "MUN" in c), None)
    if cve_col and mun_col:
        df["CVE_GEO"] = df[cve_col].str.zfill(2) + df[mun_col].str.zfill(3)
    else:
        # Try CLAVE_MUN style (some versions use 5-digit combined)
        geo_col = next((c for c in df.columns if "CLAVE" in c or "CVE_GEO" in c), None)
        if geo_col:
            df["CVE_GEO"] = df[geo_col].str.zfill(5)

    df = df[df["CVE_GEO"].str[:2].isin(TARGET_STATES.keys())]

    # Keep relevant columns — find them dynamically
    keep = {"CVE_GEO"}
    for target in ["INDICE", "GRADO", "LUGAR"]:
        matches = [c for c in df.columns if target in c]
        keep.update(matches)
    df = df[sorted(keep, key=lambda c: list(df.columns).index(c))]

    # Rename for clarity
    rename = {}
    for c in df.columns:
        if "INDICE" in c and "MARG" in c:  rename[c] = "CONAPO_IMM"
        elif "GRADO" in c and "MARG" in c: rename[c] = "CONAPO_GRADO"
        elif "LUGAR" in c:                 rename[c] = "CONAPO_LUGAR_NAC"
    df = df.rename(columns=rename)
    print(f"  → {len(df)} municipalities in target states")
    return df


# ─────────────────────────────────────────────
# TIER 1B: CONEVAL Social Lag Index 2020
# ─────────────────────────────────────────────
def get_coneval():
    print("\n[2/5] CONEVAL Social Lag Index 2020")
    # Try the main download URL (may change — check coneval.org.mx if 404)
    url  = "https://www.coneval.org.mx/Medicion/IRS/Documents/IRS_2020_municipios.xlsx"
    dest = os.path.join(RAW, "IRS_2020_municipios.xlsx")
    download(url, dest, "CONEVAL IRS 2020")

    df = pd.read_excel(dest, dtype=str)
    df.columns = [c.strip().upper()
                    .replace("Á","A").replace("É","E").replace("Í","I")
                    .replace("Ó","O").replace("Ú","U").replace("Ñ","N")
                  for c in df.columns]
    print("  CONEVAL columns:", list(df.columns)[:10], "...")

    cve_col = next((c for c in df.columns if "CVE" in c and ("GEO" in c or "MUN" in c or "MPIO" in c)), None)
    if cve_col:
        df["CVE_GEO"] = df[cve_col].str.zfill(5)
    df = df[df["CVE_GEO"].str[:2].isin(TARGET_STATES.keys())]

    keep = {"CVE_GEO"}
    for target in ["REZAGO", "INDICE", "GRADO"]:
        keep.update(c for c in df.columns if target in c)
    df = df[sorted(keep, key=lambda c: list(df.columns).index(c))]

    rename = {}
    for c in df.columns:
        if "INDICE" in c: rename[c] = "CONEVAL_IRS"
        elif "GRADO" in c: rename[c] = "CONEVAL_GRADO"
    df = df.rename(columns=rename)
    print(f"  → {len(df)} municipalities in target states")
    return df


# ─────────────────────────────────────────────
# TIER 1C: INEGI Census 2020 — ITER tables
# Key variables: population, indigenous language, housing materials,
# disability, single-parent HH, avg occupants/room
# ─────────────────────────────────────────────
def get_inegi_iter():
    print("\n[3/5] INEGI Census 2020 ITER tables (Chiapas, Guerrero, Oaxaca)")
    iter_base = "https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/iter/iter_{state}_cpv2020_csv.zip"

    ITER_VARS = {
        # Variable name in ITER file : rename
        "POBTOT":   "POB_TOTAL",          # total population
        "POBFEM":   "POB_FEM",            # female population
        "P3YM_HLI": "PCT_HABLA_INDIG",   # speaks indigenous language (3+)
        "PHOG_IND": "PCT_HOG_INDIG",      # indigenous households
        "GRAPROES": "ESCOLARIDAD_PROM",   # avg schooling years
        "PCON_DISC":"PCT_DISCAPACIDAD",   # with disability
        "VPH_PISOTI":"PCT_PISO_TIERRA",   # earthen floor
        "VPH_S_ELEC":"PCT_SIN_ELEC",      # no electricity
        "VPH_AGUAFV":"PCT_SIN_AGUA",      # no piped water
        "VPH_NODREN":"PCT_SIN_DRENAJE",   # no sewerage
        "VIVTOT":   "VIV_TOTAL",          # total dwellings
        "OCUPVIVPAR":"VIV_OCUPADAS",      # occupied dwellings
        "PROM_OCUP": "PROM_OCUP_CUARTO",  # avg occupants per room
    }

    all_frames = []
    for state_code in ["07", "12", "20"]:
        url  = iter_base.format(state=state_code)
        dest = os.path.join(RAW, f"iter_{state_code}_cpv2020.zip")
        download(url, dest, f"ITER state {state_code}")

        with zipfile.ZipFile(dest) as z:
            # ITER files have the CSV named like ITER_07XLSX.csv or similar
            csv_names = [n for n in z.namelist() if n.upper().endswith(".CSV")]
            if not csv_names:
                print(f"  WARNING: no CSV found in {dest}")
                continue
            csv_name = csv_names[0]
            with z.open(csv_name) as f:
                raw_df = pd.read_csv(f, dtype=str, encoding="latin-1", low_memory=False)

        # Filter to municipality-level rows only (NOM_LOC == "Total del municipio")
        if "NOM_LOC" in raw_df.columns:
            mun_df = raw_df[raw_df["NOM_LOC"].str.contains("Total del municipio", na=False)].copy()
        elif "NIVEL_GEO" in raw_df.columns:
            mun_df = raw_df[raw_df["NIVEL_GEO"] == "Municipio"].copy()
        else:
            # Fallback: rows where LOC code == 0
            mun_df = raw_df[raw_df.get("LOC", raw_df.get("CLOC", pd.Series())).astype(str).str.strip().isin(["0","0000",""])].copy()

        mun_df["CVE_GEO"] = state_code + mun_df.get("MUN", mun_df.get("CLAVE_MUN", pd.Series())).str.zfill(3)

        # Select and rename variables
        available = {k: v for k, v in ITER_VARS.items() if k in mun_df.columns}
        cols = ["CVE_GEO"] + list(available.keys())
        sub = mun_df[[c for c in cols if c in mun_df.columns]].rename(columns=available)

        # Derive key percentages where raw counts are present
        for pct_col in ["PCT_HABLA_INDIG", "PCT_HOG_INDIG", "PCT_DISCAPACIDAD",
                        "PCT_PISO_TIERRA", "PCT_SIN_ELEC", "PCT_SIN_AGUA", "PCT_SIN_DRENAJE"]:
            if pct_col in sub.columns and "POB_TOTAL" in sub.columns:
                sub[pct_col] = pd.to_numeric(sub[pct_col], errors="coerce")
                sub["POB_TOTAL_N"] = pd.to_numeric(sub.get("POB_TOTAL", 0), errors="coerce")
                # Already a % in ITER? Check magnitude
                if sub[pct_col].dropna().max() > 1.5:
                    # Raw count — divide by population
                    if "VIV" in pct_col:
                        sub[pct_col] = sub[pct_col] / pd.to_numeric(sub.get("VIV_OCUPADAS", sub["POB_TOTAL_N"].replace(0, float("nan"))), errors="coerce")
                    else:
                        sub[pct_col] = sub[pct_col] / sub["POB_TOTAL_N"].replace(0, float("nan"))

        all_frames.append(sub)
        print(f"  State {state_code}: {len(sub)} municipalities")

    if all_frames:
        df = pd.concat(all_frames, ignore_index=True)
        print(f"  → {len(df)} total")
        return df
    return pd.DataFrame()


# ─────────────────────────────────────────────
# TIER 1D: SESNSP Homicide Rates
# ─────────────────────────────────────────────
def get_sesnsp():
    print("\n[4/5] SESNSP Homicide data 2022–2024")
    # SESNSP publishes monthly incidencia delictiva CSV
    url  = "https://drive.google.com/uc?export=download&id=1GwXxlv4AGSY6zxZQQLOFBXzRrv0llNO5"
    dest = os.path.join(RAW, "sesnsp_homicidios.csv")
    download(url, dest, "SESNSP homicidios municipales")

    try:
        df = pd.read_csv(dest, dtype=str, encoding="latin-1", low_memory=False)
        df.columns = [c.strip().upper()
                        .replace("Á","A").replace("É","E").replace("Í","I")
                        .replace("Ó","O").replace("Ú","U").replace("Ñ","N")
                      for c in df.columns]

        # Filter to homicidio doloso; sum 2022–2024; divide by population
        hom = df[df.get("SUBTIPO_DELITO","").str.contains("HOMICIDIO", na=False)].copy()

        # Year columns are typically named by year-month: ENE_2022, FEB_2022, etc.
        year_cols = [c for c in hom.columns if re.match(r"[A-Z]{3}_202[234]", c)]
        hom["HOMICIDIOS_SUM"] = hom[year_cols].apply(pd.to_numeric, errors="coerce").sum(axis=1)

        # Aggregate to municipality using CVE_MUN or similar
        cve_col = next((c for c in hom.columns if "CVE" in c and "MUN" in c), None)
        ent_col = next((c for c in hom.columns if "CVE" in c and "ENT" in c), None)
        if cve_col and ent_col:
            hom["CVE_GEO"] = hom[ent_col].str.zfill(2) + hom[cve_col].str.zfill(3)
            agg = hom.groupby("CVE_GEO")["HOMICIDIOS_SUM"].sum().reset_index()
            agg = agg[agg["CVE_GEO"].str[:2].isin(TARGET_STATES.keys())]
            agg = agg.rename(columns={"HOMICIDIOS_SUM": "HOMICIDIOS_2022_2024"})
            print(f"  → {len(agg)} municipalities with homicide data")
            return agg
    except Exception as e:
        print(f"  WARNING: SESNSP processing failed — {e}")
        print("  Manual download: https://www.gob.mx/sesnsp/acciones-y-programas/incidencia-delictiva-87005")
    return pd.DataFrame()


# ─────────────────────────────────────────────
# TIER 1E: CENAPRED Hazard Indices
# ─────────────────────────────────────────────
def get_cenapred():
    print("\n[5/5] CENAPRED Atlas Nacional de Riesgos indices")
    # Main downloadable dataset from datos.gob.mx
    url  = "https://datos.gob.mx/busca/api/3/action/package_show?id=indice-de-peligro-a-nivel-municipal"
    dest = os.path.join(RAW, "cenapred_meta.json")
    download(url, dest, "CENAPRED metadata")

    try:
        import json
        with open(dest) as f:
            meta = json.load(f)
        resources = meta.get("result", {}).get("resources", [])
        for r in resources:
            fmt = r.get("format", "").upper()
            if fmt in ("CSV", "XLSX", "XLS"):
                dl_url = r["url"]
                dl_dest = os.path.join(RAW, f"cenapred_peligros.{fmt.lower()}")
                download(dl_url, dl_dest, f"CENAPRED peligros ({fmt})")
                if fmt == "CSV":
                    df = pd.read_csv(dl_dest, dtype=str, encoding="latin-1")
                else:
                    df = pd.read_excel(dl_dest, dtype=str)
                df.columns = [c.strip().upper() for c in df.columns]
                # Build CVE_GEO
                cve = next((c for c in df.columns if "CVE" in c), None)
                if cve:
                    df["CVE_GEO"] = df[cve].str.zfill(5)
                    df = df[df["CVE_GEO"].str[:2].isin(TARGET_STATES.keys())]
                    # Keep hazard index columns
                    haz_cols = [c for c in df.columns if any(t in c for t in
                                ["SISMICO","CICLONIC","INUNDACION","DESLIZA","PELIGRO","INDICE"])]
                    df = df[["CVE_GEO"] + haz_cols]
                    print(f"  → {len(df)} municipalities with CENAPRED data, columns: {haz_cols[:6]}")
                    return df
    except Exception as e:
        print(f"  WARNING: CENAPRED processing failed — {e}")
        print("  Manual: http://www.atlasnacionalderiesgos.gob.mx/ → Descarga de datos")
    return pd.DataFrame()


# ─────────────────────────────────────────────
# JOIN ALL SOURCES
# ─────────────────────────────────────────────
def build_master():
    print("\n" + "="*60)
    print("Building master municipality table")
    print("="*60)

    frames = {}

    try: frames["conapo"] = get_conapo()
    except Exception as e: print(f"  CONAPO failed: {e}")

    try: frames["coneval"] = get_coneval()
    except Exception as e: print(f"  CONEVAL failed: {e}")

    try: frames["inegi"] = get_inegi_iter()
    except Exception as e: print(f"  INEGI ITER failed: {e}")

    try: frames["sesnsp"] = get_sesnsp()
    except Exception as e: print(f"  SESNSP failed: {e}")

    try: frames["cenapred"] = get_cenapred()
    except Exception as e: print(f"  CENAPRED failed: {e}")

    # Start from CONAPO as the backbone (has all municipalities)
    master = frames.get("conapo", pd.DataFrame())
    if master.empty:
        print("ERROR: CONAPO download failed — cannot build master table without backbone")
        sys.exit(1)

    for name, df in frames.items():
        if name == "conapo" or df.empty:
            continue
        before = len(master)
        master = master.merge(df, on="CVE_GEO", how="left")
        print(f"  Merged {name}: {before} → {len(master)} rows")

    # Add state name column
    master["NOM_ENT"] = master["CVE_GEO"].str[:2].map(TARGET_STATES)

    # Sort
    master = master.sort_values(["CVE_GEO"]).reset_index(drop=True)

    out = os.path.join(PROC, "master_municipalities.csv")
    master.to_csv(out, index=False)
    print(f"\n✓ Master table saved: {out}")
    print(f"  {len(master)} municipalities × {len(master.columns)} columns")
    print(f"  Columns: {list(master.columns)}")
    return master


# ─────────────────────────────────────────────
# OPTIONAL: BUILD GEOJSON (requires geopandas)
# ─────────────────────────────────────────────
def build_geojson(master):
    print("\n[Optional] Building GeoJSON with joined attributes")
    try:
        import geopandas as gpd

        shp_url  = "https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/geografia/marcogeo/889463807469_mg.zip"
        shp_dest = os.path.join(RAW, "mg_municipios_2020.zip")
        download(shp_url, shp_dest, "INEGI Marco Geoestadístico 2020 (municipalities)")

        with zipfile.ZipFile(shp_dest) as z:
            z.extractall(os.path.join(RAW, "mg_municipios"))

        # Find the municipalities .shp file
        import glob
        shps = glob.glob(os.path.join(RAW, "mg_municipios", "**", "*muni*.shp"), recursive=True)
        if not shps:
            shps = glob.glob(os.path.join(RAW, "mg_municipios", "**", "*.shp"), recursive=True)
        if not shps:
            print("  No shapefile found in archive")
            return

        gdf = gpd.read_file(shps[0])
        gdf.columns = [c.strip().upper() for c in gdf.columns]

        # Build CVE_GEO in geodataframe
        cve_col = next((c for c in gdf.columns if "CVE" in c and ("GEO" in c or "MUN" in c)), None)
        if cve_col:
            gdf["CVE_GEO"] = gdf[cve_col].str.zfill(5)
        gdf = gdf[gdf["CVE_GEO"].str[:2].isin(TARGET_STATES.keys())]

        # Join attributes
        gdf = gdf.merge(master.drop(columns=["NOM_ENT"], errors="ignore"), on="CVE_GEO", how="left")

        # Reproject to WGS84 for Leaflet
        gdf = gdf.to_crs(epsg=4326)

        out = os.path.join(PROC, "municipalities.geojson")
        gdf.to_file(out, driver="GeoJSON")
        print(f"  ✓ GeoJSON saved: {out}  ({len(gdf)} features)")

    except ImportError:
        print("  geopandas not installed — skipping GeoJSON. Run: pip install geopandas")
    except Exception as e:
        print(f"  GeoJSON build failed: {e}")


if __name__ == "__main__":
    master = build_master()
    build_geojson(master)
    print("\nDone. Check data/processed/ for outputs.")
    print("If any downloads failed, check the manual download links printed above.")
