#!/usr/bin/env python3
"""
Mexico SVI Tool — Raw Data Processing Script
Run after fetch_all_data.sh completes.
Reads data/raw/, filters to Guerrero/Oaxaca/Chiapas, joins on CVE_GEO,
and outputs:
  data/processed/master_municipalities.csv
  data/processed/municipalities.geojson  (if geopandas installed)

pip install pandas openpyxl geopandas
"""

import os, sys, json, zipfile, glob, re, warnings
import pandas as pd
warnings.filterwarnings("ignore")

RAW  = os.path.join(os.path.dirname(__file__), "raw")
PROC = os.path.join(os.path.dirname(__file__), "processed")
os.makedirs(PROC, exist_ok=True)

TARGET = {"07": "Chiapas", "12": "Guerrero", "20": "Oaxaca"}

def norm_cols(df):
    """Normalise column names: strip, upper, remove accents."""
    rep = {"Á":"A","É":"E","Í":"I","Ó":"O","Ú":"U","Ü":"U","Ñ":"N"," ":"_"}
    cols = []
    for c in df.columns:
        c = str(c).strip().upper()
        for a, b in rep.items():
            c = c.replace(a, b)
        cols.append(c)
    df.columns = cols
    return df

def pad_geo(df, ent_col, mun_col):
    df["CVE_GEO"] = df[ent_col].astype(str).str.strip().str.zfill(2) + \
                    df[mun_col].astype(str).str.strip().str.zfill(3)
    return df

def filter_states(df):
    return df[df["CVE_GEO"].str[:2].isin(TARGET.keys())].copy()


# ─────────────────────────────────────────────
# 1. CONAPO Marginalization
# ─────────────────────────────────────────────
def load_conapo():
    path = os.path.join(RAW, "IMM_2020.xls")
    if not os.path.exists(path):
        print("  [skip] CONAPO — file not found"); return pd.DataFrame()
    try:
        df = pd.read_excel(path, dtype=str)
    except Exception:
        df = pd.read_excel(path, dtype=str, engine="xlrd")
    df = norm_cols(df)
    print(f"  CONAPO raw cols: {list(df.columns)}")

    # Find entity/municipality code columns
    ent = next((c for c in df.columns if re.search(r"CVE.?ENT|ENTIDAD", c)), None)
    mun = next((c for c in df.columns if re.search(r"CVE.?MUN|MUNICIPIO", c) and "NOM" not in c), None)
    geo = next((c for c in df.columns if re.search(r"CVE.?GEO|CLAVE_MUN", c)), None)

    if geo:
        df["CVE_GEO"] = df[geo].astype(str).str.strip().str.zfill(5)
    elif ent and mun:
        df = pad_geo(df, ent, mun)
    else:
        print("  ERROR: cannot identify CVE columns in CONAPO data")
        print(f"  Available: {list(df.columns)}")
        return pd.DataFrame()

    df = filter_states(df)

    # Standardise key columns
    rename = {}
    for c in df.columns:
        if re.search(r"INDICE.*MARG|IM_2020", c): rename[c] = "CONAPO_IMM"
        elif re.search(r"GRADO.*MARG", c):         rename[c] = "CONAPO_GRADO"
        elif re.search(r"LUGAR.*NAC", c):           rename[c] = "CONAPO_LUGAR_NAC"
        elif re.search(r"NOM.*MUN", c):             rename[c] = "NOM_MUN"
        elif re.search(r"NOM.*ENT", c):             rename[c] = "NOM_ENT_CONAPO"
    df = df.rename(columns=rename)

    keep = ["CVE_GEO"] + [c for c in ["NOM_MUN","NOM_ENT_CONAPO","CONAPO_IMM","CONAPO_GRADO","CONAPO_LUGAR_NAC"]
                          if c in df.columns]
    print(f"  CONAPO: {len(df)} municipalities, cols: {keep}")
    return df[keep]


# ─────────────────────────────────────────────
# 2. CONEVAL Social Lag
# ─────────────────────────────────────────────
def load_coneval():
    path = os.path.join(RAW, "IRS_2020_municipios.xlsx")
    if not os.path.exists(path):
        print("  [skip] CONEVAL — file not found"); return pd.DataFrame()
    df = pd.read_excel(path, dtype=str)
    df = norm_cols(df)
    print(f"  CONEVAL raw cols: {list(df.columns)}")

    ent = next((c for c in df.columns if re.search(r"CVE.?ENT|ENTIDAD", c) and "NOM" not in c), None)
    mun = next((c for c in df.columns if re.search(r"CVE.?MUN|MUNICIPIO", c) and "NOM" not in c), None)
    geo = next((c for c in df.columns if re.search(r"CVE.?GEO|CVE_MUN", c)), None)

    if geo:
        df["CVE_GEO"] = df[geo].astype(str).str.strip().str.zfill(5)
    elif ent and mun:
        df = pad_geo(df, ent, mun)
    else:
        print(f"  ERROR: cannot find CVE cols. Available: {list(df.columns)}")
        return pd.DataFrame()

    df = filter_states(df)

    rename = {}
    for c in df.columns:
        if re.search(r"INDICE.*REZAGO|IRS_2020", c): rename[c] = "CONEVAL_IRS"
        elif re.search(r"GRADO.*REZAGO", c):          rename[c] = "CONEVAL_GRADO"
        elif re.search(r"LUGAR.*NAC", c):              rename[c] = "CONEVAL_LUGAR_NAC"
    df = df.rename(columns=rename)

    keep = ["CVE_GEO"] + [c for c in ["CONEVAL_IRS","CONEVAL_GRADO","CONEVAL_LUGAR_NAC"] if c in df.columns]
    print(f"  CONEVAL: {len(df)} municipalities")
    return df[keep]


# ─────────────────────────────────────────────
# 3. INEGI Census ITER — key demographic variables
# ─────────────────────────────────────────────
ITER_MAP = {
    # ITER variable : output name
    "POBTOT":    "POB_TOTAL",
    "POBFEM":    "POB_FEM",
    "P3YM_HLI":  "PCT_HABLA_INDIG",    # speaks indigenous language (3+), raw count
    "PHOGJEF_F": "PCT_JEFA_HOGAR_F",   # female-headed households, raw count
    "TVIVHAB":   "VIV_HABITADAS",
    "GRAPROES":  "ESCOLARIDAD_PROM",
    "PCON_DISC": "PCT_DISCAPACIDAD",    # with disability, raw count
    "VPH_PISOTI":"PCT_PISO_TIERRA",     # earthen floor, count of dwellings
    "VPH_S_ELEC":"PCT_SIN_ELEC",        # no electricity, count
    "VPH_AGUAFV":"PCT_SIN_AGUA",        # no piped water, count
    "VPH_NODREN":"PCT_SIN_DRENAJE",     # no sewerage, count
    "VPH_INTER": "VPH_INTERNET",        # with internet, count
    "PROM_OCUP": "PROM_OCUP_CUARTO",    # avg occupants per room
    "P65YM_M":   "POB_65M_MASC",        # 65+ male
    "P65YM_F":   "POB_65M_FEM",         # 65+ female
    "TOTHOG":    "TOTAL_HOGARES",
}

def load_iter():
    frames = []
    for state in ["07", "12", "20"]:
        path = os.path.join(RAW, f"iter_{state}_cpv2020.zip")
        if not os.path.exists(path):
            print(f"  [skip] ITER {state} — file not found"); continue
        with zipfile.ZipFile(path) as z:
            csvs = [n for n in z.namelist() if n.upper().endswith(".CSV")]
            if not csvs:
                print(f"  WARNING: no CSV in ITER {state} zip"); continue
            # Use largest CSV (the main ITER file)
            csv_name = max(csvs, key=lambda n: z.getinfo(n).file_size)
            with z.open(csv_name) as f:
                raw = pd.read_csv(f, dtype=str, encoding="latin-1", low_memory=False)

        raw = norm_cols(raw)

        # Filter to municipality-total rows (LOCODE == 0 or NOM_LOC contains "Total")
        if "NOM_LOC" in raw.columns:
            mun = raw[raw["NOM_LOC"].str.upper().str.contains("TOTAL.*MUNI|^TOTAL$", na=False)].copy()
        elif "LOC" in raw.columns:
            mun = raw[raw["LOC"].astype(str).str.strip().isin(["0","0000"])].copy()
        elif "CLOC" in raw.columns:
            mun = raw[raw["CLOC"].astype(str).str.strip().isin(["0","0000"])].copy()
        else:
            print(f"  WARNING: cannot identify municipality rows in ITER {state}")
            mun = raw.head(1000)  # best effort

        # Build CVE_GEO
        ent = next((c for c in mun.columns if re.search(r"^ENT$|CVE_ENT", c)), None)
        mn  = next((c for c in mun.columns if re.search(r"^MUN$|CVE_MUN", c)), None)
        if ent and mn:
            mun["CVE_GEO"] = mun[ent].str.zfill(2) + mun[mn].str.zfill(3)
        else:
            mun["CVE_GEO"] = state + mun.get("MUN", mun.get("MUNICIPIO",pd.Series())).astype(str).str.zfill(3)

        # Select available variables
        available = {k: v for k, v in ITER_MAP.items() if k in mun.columns}
        cols = ["CVE_GEO"] + list(available.keys())
        sub = mun[[c for c in cols if c in mun.columns]].rename(columns=available).copy()

        # Convert counts to percentages where meaningful
        pop = pd.to_numeric(sub.get("POB_TOTAL", pd.Series(dtype=float)), errors="coerce")
        viv = pd.to_numeric(sub.get("VIV_HABITADAS", pd.Series(dtype=float)), errors="coerce")
        hog = pd.to_numeric(sub.get("TOTAL_HOGARES", pd.Series(dtype=float)), errors="coerce")

        for col, denom in [
            ("PCT_HABLA_INDIG", pop), ("PCT_DISCAPACIDAD", pop),
            ("PCT_JEFA_HOGAR_F", hog),
            ("PCT_PISO_TIERRA", viv), ("PCT_SIN_ELEC", viv),
            ("PCT_SIN_AGUA", viv), ("PCT_SIN_DRENAJE", viv),
            ("VPH_INTERNET", viv),
        ]:
            if col in sub.columns:
                raw_val = pd.to_numeric(sub[col], errors="coerce")
                # If values look like raw counts (> 1.5 max suggests counts not fractions)
                if raw_val.dropna().max() > 1.5 and denom is not None:
                    sub[col] = (raw_val / denom.replace(0, float("nan"))).round(4)

        # Derive elderly share
        if "POB_65M_MASC" in sub.columns and "POB_65M_FEM" in sub.columns:
            e65m = pd.to_numeric(sub["POB_65M_MASC"], errors="coerce")
            e65f = pd.to_numeric(sub["POB_65M_FEM"], errors="coerce")
            sub["PCT_65MAS"] = ((e65m + e65f) / pop.replace(0, float("nan"))).round(4)

        # Internet access: flip to "no internet" percentage
        if "VPH_INTERNET" in sub.columns:
            sub["PCT_SIN_INTERNET"] = (1 - pd.to_numeric(sub["VPH_INTERNET"], errors="coerce")).clip(0,1).round(4)

        frames.append(sub)
        print(f"  ITER {state}: {len(sub)} municipalities")

    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


# ─────────────────────────────────────────────
# 4. SESNSP Homicide rates
# ─────────────────────────────────────────────
def load_sesnsp():
    path = os.path.join(RAW, "sesnsp_incidencia.csv")
    if not os.path.exists(path):
        print("  [skip] SESNSP — file not found"); return pd.DataFrame()
    try:
        df = pd.read_csv(path, dtype=str, encoding="latin-1", low_memory=False)
        df = norm_cols(df)

        # Filter to homicidio doloso only
        tipo_col = next((c for c in df.columns if "TIPO" in c and "DELITO" in c), None)
        sub_col  = next((c for c in df.columns if "SUBTIPO" in c or "BIEN" in c), None)
        if tipo_col:
            df = df[df[tipo_col].str.upper().str.contains("HOMICIDIO", na=False)]

        # Sum monthly columns for 2022–2024
        year_cols = [c for c in df.columns if re.match(r"[A-Z]{3,4}_202[234]", c)]
        if not year_cols:
            # Try numeric month columns
            year_cols = [c for c in df.columns if re.match(r"202[234]", c)]
        if year_cols:
            df["HOMICIDIOS_22_24"] = df[year_cols].apply(pd.to_numeric, errors="coerce").sum(axis=1)
        else:
            print("  WARNING: cannot find year columns in SESNSP data")
            return pd.DataFrame()

        ent = next((c for c in df.columns if re.search(r"CVE.?ENT|CLAVE.?ENT", c) and "NOM" not in c), None)
        mun = next((c for c in df.columns if re.search(r"CVE.?MUN|CLAVE.?MUN", c) and "NOM" not in c), None)
        if ent and mun:
            df["CVE_GEO"] = df[ent].astype(str).str.zfill(2) + df[mun].astype(str).str.zfill(3)
        else:
            print("  ERROR: cannot identify CVE cols in SESNSP"); return pd.DataFrame()

        agg = df.groupby("CVE_GEO")["HOMICIDIOS_22_24"].sum().reset_index()
        agg = agg[agg["CVE_GEO"].str[:2].isin(TARGET.keys())]
        print(f"  SESNSP: {len(agg)} municipalities with homicide data")
        return agg
    except Exception as e:
        print(f"  SESNSP error: {e}"); return pd.DataFrame()


# ─────────────────────────────────────────────
# 5. CONAPO Migration Intensity
# ─────────────────────────────────────────────
def load_migracion():
    path = os.path.join(RAW, "IIM_2020.xlsx")
    if not os.path.exists(path):
        print("  [skip] CONAPO Migración — file not found"); return pd.DataFrame()
    df = pd.read_excel(path, dtype=str)
    df = norm_cols(df)

    ent = next((c for c in df.columns if re.search(r"CVE.?ENT", c) and "NOM" not in c), None)
    mun = next((c for c in df.columns if re.search(r"CVE.?MUN", c) and "NOM" not in c), None)
    geo = next((c for c in df.columns if re.search(r"CVE.?GEO", c)), None)
    if geo:
        df["CVE_GEO"] = df[geo].astype(str).str.zfill(5)
    elif ent and mun:
        df = pad_geo(df, ent, mun)
    else:
        print("  ERROR: cannot identify CVE cols in migration data"); return pd.DataFrame()

    df = filter_states(df)
    rename = {}
    for c in df.columns:
        if re.search(r"INDICE.*INTEN|IIM", c): rename[c] = "CONAPO_IIM"
        elif re.search(r"GRADO.*INTEN", c):    rename[c] = "CONAPO_IIM_GRADO"
    df = df.rename(columns=rename)

    keep = ["CVE_GEO"] + [c for c in ["CONAPO_IIM","CONAPO_IIM_GRADO"] if c in df.columns]
    print(f"  Migración: {len(df)} municipalities")
    return df[keep]


# ─────────────────────────────────────────────
# 6. IFT Connectivity
# ─────────────────────────────────────────────
def load_ift():
    path = os.path.join(RAW, "ift_cobertura_2023.csv")
    if not os.path.exists(path):
        print("  [skip] IFT — file not found"); return pd.DataFrame()
    try:
        df = pd.read_csv(path, dtype=str, encoding="latin-1", low_memory=False)
        df = norm_cols(df)
        print(f"  IFT cols: {list(df.columns)[:8]}")

        ent = next((c for c in df.columns if re.search(r"ENT|ESTADO", c) and "NOM" not in c), None)
        mun = next((c for c in df.columns if re.search(r"MUN|MUNICIPIO", c) and "NOM" not in c), None)
        geo = next((c for c in df.columns if "CVE_GEO" in c or "CLAVE_MUN" in c), None)
        if geo:
            df["CVE_GEO"] = df[geo].astype(str).str.zfill(5)
        elif ent and mun:
            df = pad_geo(df, ent, mun)
        else:
            print("  ERROR: cannot identify CVE cols in IFT data"); return pd.DataFrame()

        df = filter_states(df)
        # Find coverage percentage columns
        cov_cols = [c for c in df.columns if re.search(r"COBER|4G|LTE|MOVIL|CELULAR", c)]
        if not cov_cols:
            cov_cols = [c for c in df.columns if re.search(r"PCT|PORC|POP_COV", c)]
        if cov_cols:
            df = df[["CVE_GEO"] + cov_cols[:3]]
            for c in cov_cols[:3]:
                df = df.rename(columns={c: f"IFT_{c[:20]}"})
            print(f"  IFT: {len(df)} municipalities, coverage cols: {cov_cols[:3]}")
            return df
    except Exception as e:
        print(f"  IFT error: {e}")
    return pd.DataFrame()


# ─────────────────────────────────────────────
# JOIN ALL → MASTER TABLE
# ─────────────────────────────────────────────
def build_master():
    print("\n" + "═"*56)
    print("Building master municipality table")
    print("═"*56 + "\n")

    loaders = [
        ("CONAPO",    load_conapo),
        ("CONEVAL",   load_coneval),
        ("ITER",      load_iter),
        ("SESNSP",    load_sesnsp),
        ("Migración", load_migracion),
        ("IFT",       load_ift),
    ]

    frames = {}
    for name, fn in loaders:
        print(f"Loading {name}...")
        try:
            frames[name] = fn()
        except Exception as e:
            print(f"  ERROR in {name}: {e}")
            frames[name] = pd.DataFrame()

    # Start from CONAPO as the municipality backbone
    master = frames.get("CONAPO", pd.DataFrame())
    if master.empty:
        # Fall back to ITER as backbone
        master = frames.get("ITER", pd.DataFrame())
    if master.empty:
        print("ERROR: no backbone dataset loaded — check downloads")
        sys.exit(1)

    print(f"\nBackbone: {len(master)} municipalities")

    for name, df in frames.items():
        if name in ("CONAPO",) or df.empty or "CVE_GEO" not in df.columns:
            continue
        # Avoid duplicate columns
        new_cols = [c for c in df.columns if c not in master.columns or c == "CVE_GEO"]
        master = master.merge(df[new_cols], on="CVE_GEO", how="left")
        print(f"  + {name}: {len(df)} rows merged")

    # Add state name
    master["NOM_ENT"] = master["CVE_GEO"].str[:2].map(TARGET)

    # ── Normalise key numeric columns 0–1 ──────────────────────────
    print("\nNormalising numeric columns...")
    numeric_cols = [c for c in master.columns
                    if c not in ("CVE_GEO","NOM_MUN","NOM_ENT","NOM_ENT_CONAPO",
                                 "CONAPO_GRADO","CONEVAL_GRADO","CONAPO_IIM_GRADO")]
    for c in numeric_cols:
        master[c] = pd.to_numeric(master[c], errors="coerce")

    # CONAPO_IMM: higher = worse → normalise so 1.0 = worst
    if "CONAPO_IMM" in master.columns:
        mn, mx = master["CONAPO_IMM"].min(), master["CONAPO_IMM"].max()
        if mx > mn:
            master["CONAPO_IMM_NORM"] = ((master["CONAPO_IMM"] - mn) / (mx - mn)).round(4)

    # CONEVAL_IRS: higher = worse → normalise
    if "CONEVAL_IRS" in master.columns:
        mn, mx = master["CONEVAL_IRS"].min(), master["CONEVAL_IRS"].max()
        if mx > mn:
            master["CONEVAL_IRS_NORM"] = ((master["CONEVAL_IRS"] - mn) / (mx - mn)).round(4)

    # HOMICIDIOS: normalise per 100k using population
    if "HOMICIDIOS_22_24" in master.columns and "POB_TOTAL" in master.columns:
        # 3-year sum → rate per 100k per year
        master["HOMICIDIO_RATE_100K"] = (
            (master["HOMICIDIOS_22_24"] / master["POB_TOTAL"].replace(0, float("nan"))) * 100000 / 3
        ).round(2)
        mn, mx = master["HOMICIDIO_RATE_100K"].quantile(0.01), master["HOMICIDIO_RATE_100K"].quantile(0.99)
        master["HOMICIDIO_NORM"] = ((master["HOMICIDIO_RATE_100K"].clip(mn, mx) - mn) / (mx - mn)).round(4)

    # ── Derive SVI cluster approximations ─────────────────────────
    # These are simple aggregates — full cluster scoring in next step
    social_vars = [c for c in ["CONAPO_IMM_NORM","CONEVAL_IRS_NORM","PCT_HABLA_INDIG",
                                "PCT_DISCAPACIDAD","PCT_PISO_TIERRA","PCT_SIN_AGUA"] if c in master.columns]
    if social_vars:
        master["SVI_SOCIAL_COMPOSITE"] = master[social_vars].mean(axis=1).round(4)

    hazard_vars = [c for c in ["HAZARD_SISMICO","HAZARD_CICLONICO"] if c in master.columns]
    if hazard_vars:
        master["HAZARD_FISICO"] = master[hazard_vars].mean(axis=1).round(4)

    # Divergence flag: high SVI, low physical hazard (the underserved)
    if "SVI_SOCIAL_COMPOSITE" in master.columns and "HAZARD_FISICO" in master.columns:
        master["DIVERGE_FLAG"] = (
            (master["SVI_SOCIAL_COMPOSITE"] > 0.65) & (master["HAZARD_FISICO"] < 0.55)
        ).map({True: "HIGH_SVI_LOW_PHYS", False: ""})

    # ── Sort and save ──────────────────────────────────────────────
    master = master.sort_values("CVE_GEO").reset_index(drop=True)
    out_csv = os.path.join(PROC, "master_municipalities.csv")
    master.to_csv(out_csv, index=False)

    print(f"\n✓ Master table → {out_csv}")
    print(f"  {len(master)} municipalities × {len(master.columns)} columns")

    # Summary
    print(f"\nBreakdown by state:")
    print(master["NOM_ENT"].value_counts().to_string())

    if "SVI_SOCIAL_COMPOSITE" in master.columns:
        print(f"\nTop 10 highest SVI social score:")
        top = master.nlargest(10, "SVI_SOCIAL_COMPOSITE")[
            ["CVE_GEO", "NOM_MUN", "NOM_ENT", "SVI_SOCIAL_COMPOSITE",
             "HAZARD_FISICO" if "HAZARD_FISICO" in master.columns else "CONAPO_GRADO"]
        ]
        print(top.to_string(index=False))

    if "DIVERGE_FLAG" in master.columns:
        flagged = master[master["DIVERGE_FLAG"] == "HIGH_SVI_LOW_PHYS"]
        print(f"\n{len(flagged)} municipalities flagged: high SVI / low physical hazard")
        print("(These are the ones a hazard-only model would systematically miss)")

    # ── Optional GeoJSON ──────────────────────────────────────────
    try:
        import geopandas as gpd
        print("\nBuilding GeoJSON...")
        zip_path = os.path.join(RAW, "mg_municipios_2020.zip")
        if not os.path.exists(zip_path):
            print("  [skip] Shapefile not downloaded")
            raise ImportError("no shapefile")

        extract_dir = os.path.join(RAW, "mg_shp")
        with zipfile.ZipFile(zip_path) as z:
            z.extractall(extract_dir)

        shps = glob.glob(os.path.join(extract_dir, "**", "*muni*.shp"), recursive=True)
        if not shps:
            shps = glob.glob(os.path.join(extract_dir, "**", "*.shp"), recursive=True)
        if not shps:
            print("  No .shp found in archive")
            raise ImportError("no shp")

        gdf = gpd.read_file(shps[0])
        gdf = norm_cols(gdf)

        geo_col = next((c for c in gdf.columns if re.search(r"CVE.?GEO|CVEGEO", c)), None)
        ent_c   = next((c for c in gdf.columns if re.search(r"CVE.?ENT|^ENT$", c) and "NOM" not in c), None)
        mun_c   = next((c for c in gdf.columns if re.search(r"CVE.?MUN|^MUN$", c) and "NOM" not in c), None)
        if geo_col:
            gdf["CVE_GEO"] = gdf[geo_col].astype(str).str.zfill(5)
        elif ent_c and mun_c:
            gdf = pad_geo(gdf, ent_c, mun_c)

        gdf = gdf[gdf["CVE_GEO"].str[:2].isin(TARGET.keys())]

        # Merge attributes (drop geometry-incompatible cols)
        attr = master.drop(columns=["NOM_ENT","NOM_ENT_CONAPO"], errors="ignore")
        gdf = gdf.merge(attr, on="CVE_GEO", how="left")
        gdf = gdf.to_crs(epsg=4326)

        out_geo = os.path.join(PROC, "municipalities.geojson")
        gdf.to_file(out_geo, driver="GeoJSON")
        print(f"  ✓ GeoJSON → {out_geo}  ({len(gdf)} features)")

    except ImportError:
        print("  (geopandas not installed — run: pip install geopandas to get GeoJSON output)")
    except Exception as e:
        print(f"  GeoJSON error: {e}")

    return master


if __name__ == "__main__":
    build_master()
    print("\nAll done. Next: open data/processed/master_municipalities.csv to review.")
