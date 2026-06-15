#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# Mexico SVI Tool — Data Download Script
# Run from Terminal on your Mac:
#   cd ~/Desktop/claude\ projects/svi-mex/data
#   chmod +x fetch_all_data.sh
#   ./fetch_all_data.sh
#
# Downloads all Tier 1–3 data into data/raw/
# Then runs the Python processing script to join everything.
# ─────────────────────────────────────────────────────────────────────────────

set -e
RAW="$(dirname "$0")/raw"
mkdir -p "$RAW"

OK=0; FAIL=0
dl() {
  local desc="$1"; local url="$2"; local dest="$RAW/$3"
  if [ -f "$dest" ]; then echo "  [skip] $desc"; return; fi
  echo "  Downloading $desc..."
  if curl -fsSL --retry 3 -o "$dest" "$url"; then
    echo "  ✓ $desc → raw/$3"
    OK=$((OK+1))
  else
    echo "  ✗ FAILED: $desc"
    echo "    URL: $url"
    FAIL=$((FAIL+1))
    rm -f "$dest"
  fi
}

echo "════════════════════════════════════════════════"
echo " Mexico SVI — Data Fetch"
echo "════════════════════════════════════════════════"

# ── TIER 1A: CONAPO Marginalization Index 2020 ───────────────────────────────
echo ""
echo "[1] CONAPO Índice de Marginación Municipal 2020"
dl "CONAPO IMM 2020 (XLS)" \
   "https://conapo.segob.gob.mx/work/models/CONAPO/Datos_Abiertos/Municipio/IMM_2020.xls" \
   "IMM_2020.xls"

# ── TIER 1B: CONEVAL Social Lag Index 2020 ───────────────────────────────────
echo ""
echo "[2] CONEVAL Índice de Rezago Social 2020"
# Primary URL
dl "CONEVAL IRS 2020 (XLSX)" \
   "https://www.coneval.org.mx/Medicion/IRS/Documents/IRS_2020_municipios.xlsx" \
   "IRS_2020_municipios.xlsx"
# If that fails, try the alternate path
if [ ! -f "$RAW/IRS_2020_municipios.xlsx" ]; then
  dl "CONEVAL IRS 2020 alternate" \
     "https://www.coneval.org.mx/Medicion/IRS/Documents/rezago_social_2020_municipio.xlsx" \
     "IRS_2020_municipios.xlsx"
fi

# ── TIER 1C: INEGI Census 2020 ITER (per-state ZIPs) ─────────────────────────
echo ""
echo "[3] INEGI Censo 2020 ITER — Chiapas, Guerrero, Oaxaca"
dl "ITER Chiapas (07)" \
   "https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/iter/iter_07_cpv2020_csv.zip" \
   "iter_07_cpv2020.zip"
dl "ITER Guerrero (12)" \
   "https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/iter/iter_12_cpv2020_csv.zip" \
   "iter_12_cpv2020.zip"
dl "ITER Oaxaca (20)" \
   "https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/iter/iter_20_cpv2020_csv.zip" \
   "iter_20_cpv2020.zip"

# ── TIER 1D: INEGI Marco Geoestadístico 2020 Shapefiles ──────────────────────
echo ""
echo "[4] INEGI Marco Geoestadístico 2020 — Municipal boundaries"
# National municipalities shapefile
dl "INEGI municipios shapefile (national)" \
   "https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/geografia/marcogeo/889463807469_mg.zip" \
   "mg_municipios_2020.zip"

# ── TIER 2A: CENAPRED Hazard Indices ─────────────────────────────────────────
echo ""
echo "[5] CENAPRED — Atlas Nacional de Riesgos indices"
dl "CENAPRED peligros municipales (CSV)" \
   "https://datos.gob.mx/busca/api/3/action/datastore_search?resource_id=04e5a21c-90d2-4e2f-a813-7a4dc9c33a32&limit=5000" \
   "cenapred_peligros_raw.json"

# ── TIER 2B: HURDAT2 Eastern Pacific track data ───────────────────────────────
echo ""
echo "[6] HURDAT2 — Eastern Pacific hurricane tracks"
dl "HURDAT2 Eastern Pacific (1949–2023)" \
   "https://www.nhc.noaa.gov/data/hurdat/hurdat2-nepac-1949-2023-042624.txt" \
   "hurdat2_epac.txt"

# ── TIER 3A: SESNSP Homicide data ────────────────────────────────────────────
echo ""
echo "[7] SESNSP — Incidencia Delictiva Municipal"
# SESNSP publishes through a form; the direct CSV is at:
dl "SESNSP homicidios dolosos 2015–2024 (CSV)" \
   "https://drive.google.com/uc?export=download&id=1GwXxlv4AGSY6zxZQQLOFBXzRrv0llNO5" \
   "sesnsp_incidencia.csv"

# ── TIER 3B: CONAPO Intensidad Migratoria ─────────────────────────────────────
echo ""
echo "[8] CONAPO — Índice de Intensidad Migratoria 2020"
dl "CONAPO Migración 2020 (XLS)" \
   "https://conapo.segob.gob.mx/work/models/CONAPO/Datos_Abiertos/Intensidad_Migratoria/IIM_2020.xlsx" \
   "IIM_2020.xlsx"

# ── TIER 3C: IFT Connectivity coverage ───────────────────────────────────────
echo ""
echo "[9] IFT — Cobertura de conectividad por municipio"
dl "IFT cobertura móvil (CSV)" \
   "https://datos.ift.org.mx/datos-abiertos/Infraestructura_INFTEL/Cobertura_2023.csv" \
   "ift_cobertura_2023.csv"

# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo "════════════════════════════════════════════════"
echo " Download summary: $OK succeeded, $FAIL failed"
echo "════════════════════════════════════════════════"

if [ "$FAIL" -gt 0 ]; then
  echo ""
  echo "⚠  Some downloads failed. For manual fallbacks:"
  echo "   CONAPO:   https://www.gob.mx/conapo/documentos/indices-de-marginacion-2020-284372"
  echo "   CONEVAL:  https://www.coneval.org.mx/Medicion/IRS/Paginas/Indice_Rezago_Social_2020.aspx"
  echo "   INEGI:    https://www.inegi.org.mx/programas/ccpv/2020/#Datos_abiertos"
  echo "   CENAPRED: http://www.atlasnacionalderiesgos.gob.mx/ → Descarga"
  echo "   SESNSP:   https://www.gob.mx/sesnsp/acciones-y-programas/datos-abiertos-de-incidencia-delictiva"
  echo "   HURDAT2:  https://www.nhc.noaa.gov/data/hurdat/"
  echo ""
  echo "Place any manually downloaded files in: $RAW"
fi

echo ""
echo "Running Python processing script..."
python3 "$(dirname "$0")/process_raw_data.py"
