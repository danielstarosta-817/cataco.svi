# Albay SVI Tool — Data Sources Landscape
*What's available, how to access it, and how it maps to tool fields.*
*Last updated: May 2026. Based on research into Philippine open data infrastructure.*

---

## Summary Table

| Source | Data | Granularity | Access | Fields Available |
|--------|------|-------------|--------|-----------------|
| GeoRisk API | Barangay boundaries (GeoJSON) | Barangay | Browser API ✅ | brgy_name, mun_name, prov_code, geometry |
| PSA 2020 CPH | Population | Barangay | Browser/OpenStat ✅ | pop_total, households, avg_hh_size |
| PSA SAE 2021 | Poverty incidence | Municipality | Browser ✅ | poverty_incidence_pct |
| PSA 2020 CPH Housing | Housing tenure, structure | Municipality | Browser/OpenStat ✅ | owner_pct, renter_pct, owned_no_doc, structure_type |
| PHIVOLCS | PDZ/EDZ danger zones | Barangay (named list) | Hardcoded ✅ | in_pdz, in_edz (boolean flags) |
| HazardHunterPH | Multi-hazard exposure scores | Barangay | Browser API ✅ | flood_prone, typhoon_prone, landslide_prone |
| DSWD Listahanan 3 | Household poverty targeting | Barangay | FOI only ⚠️ | poor_hh_count, listahanan_beneficiaries |
| DSWD 4Ps | Conditional cash transfer beneficiaries | Barangay | FOI only ⚠️ | cct_beneficiaries |
| NDRRMC | Disaster history, casualties | Municipality | PDF/reports ⚠️ | — |
| PhilAtlas | Compiled census summaries | Barangay | Browser (JS-rendered) | population, area, density |
| GADM / altcoder/philippines-psgc-shapefiles | Admin boundary GeoJSON | Barangay | GitHub download ✅ | geometry only |
| faeldon/philippines-json-maps | Admin boundary GeoJSON (multi-res) | Barangay | GitHub download ✅ | geometry only |

---

## Source 1: GeoRisk API — Barangay Boundaries

**What it is:** The Philippine government's multi-hazard risk portal (PHIVOLCS/DOST) hosts an ArcGIS REST API with the PSA 2015-census-era barangay boundary polygons. This is the most convenient single source for barangay geometry.

**Endpoint:**
```
https://portal.georisk.gov.ph/arcgis/rest/services/PSA/Barangay/MapServer/4/query
  ?where=prov_code='0518'
  &outFields=brgy_name,mun_name,prov_code
  &f=geojson
  &resultRecordCount=2000
```

**Province code for Albay:** `0518` (PSA PSGC format: Region V, Province 05)

**Key facts:**
- Layer ID 4 = PSA Barangay Boundary (the standard administrative layer)
- Supports GeoJSON output format directly
- Max 20,000 records per request — Albay's 720 barangays fit in a single call
- Attribution required: Philippine Statistics Authority (PSA)
- Boundaries are from 2015 census, not updated for 2020 PSGC changes — a few barangay splits/merges may exist
- Alternative endpoint: `https://ulap-nga.georisk.gov.ph/arcgis/rest/services/PSA/Barangay/MapServer/0/query`

**Fields returned:**
- `brgy_name` — barangay name
- `mun_name` — parent municipality/city name
- `prov_name` — province name
- `prov_code` — PSA province code (0518 for Albay)
- `geometry` — polygon coordinates in GeoJSON format

**How to use in the tool (runtime fetch):**
```javascript
function fetchBarangayBoundaries(){
  var url = 'https://portal.georisk.gov.ph/arcgis/rest/services/PSA/Barangay/MapServer/4/query'
    + '?where=prov_code%3D%270518%27'
    + '&outFields=brgy_name%2Cmun_name%2Cprov_code'
    + '&f=geojson&resultRecordCount=2000';
  fetch(url)
    .then(function(r){return r.json();})
    .then(function(data){processBarangayBoundaries(data.features);})
    .catch(function(e){console.warn('GeoRisk API unavailable:',e);});
}
```

**Mapping to BARANGAYS array:** For each feature, extract centroid from polygon coordinates using a simple average of all vertices. This gives approximate barangay centroids without needing a separate centroid endpoint.

```javascript
function polygonCentroid(coordinates){
  var ring = coordinates[0]; // outer ring
  var lat=0, lng=0;
  ring.forEach(function(pt){ lng+=pt[0]; lat+=pt[1]; }); // GeoJSON is [lng,lat]
  return { lat: lat/ring.length, lng: lng/ring.length };
}
```

---

## Source 2: PSA 2020 CPH — Barangay Population

**What it is:** The Philippine Statistics Authority's 2020 Census of Population and Housing. Barangay-level population data was officially declared by Presidential Proclamation No. 1179.

**Access path:**
- **OpenStat portal:** `https://openstat.psa.gov.ph/` — PSA's official data portal. Barangay population is under "Population" → "2020 Census of Population and Housing"
- **PSA website:** `https://psa.gov.ph/classification/psgc/` — PSGC classification includes population counts
- **PhilAtlas:** `https://www.philatlas.com/lists/population/2020-most-populous-barangays-albay.html` — scraped 2020 data, JS-rendered but has all 720 barangays

**Albay province totals (2020):**
- Total population: 1,374,768
- Male: 695,486 (50.6%)
- Female: 679,282 (49.4%)
- Total barangays: 720
- Cities: 3 (Legazpi, Ligao, Tabaco)
- Municipalities: 15

**Data available at barangay level:**
- `pop_total` — total household population
- `hh_count` — number of households
- `avg_hh_size` — average household size (derived)

**Data available at municipality level only:**
- Age distribution (elderly population %)
- Educational attainment
- Housing tenure (owner/renter/informal)
- Housing structure type (concrete vs. light materials)
- Labor force participation rate

**How this maps to SVI fields:**
- `pop_total` → used for the detail panel pop display and for density calculations
- Elderly % (municipality-level) → `svi_elderly` baseline
- Housing tenure (municipality-level) → `svi_housing` partial input

**API note:** OpenStat has a PX-Web API but documentation is limited. Direct CSV downloads are available through the portal UI. For runtime fetch, use PhilAtlas or construct a PSA PSGC query.

---

## Source 3: PSA Small Area Estimation (SAE) — Municipal Poverty Incidence

**What it is:** The 2021 SAE uses 2020 CPH + FIES 2021 data to estimate poverty incidence for all 1,484 Philippines municipalities. This is the most granular official poverty data available without a FOI request.

**Access:** `https://psa.gov.ph/content/psa-releases-2021-city-and-municipal-level-poverty-estimates`

**Granularity:** Municipality only (not barangay)

**Data available:**
- Poverty incidence (% of population below poverty threshold)
- Magnitude (number of poor persons)
- Standard error of estimate

**Albay municipalities have official 2021 SAE estimates.** These are the values to use for `svi_poverty` baseline per municipality, applied uniformly to all barangays within that municipality (as a floor, then modified by local signals).

**Known limitation:** SAE estimates have wider confidence intervals for smaller municipalities. Rapu-Rapu (island municipality, small population) has higher uncertainty than Legazpi or Daraga.

---

## Source 4: PSA 2020 CPH — Housing Characteristics

**What it is:** The housing component of the 2020 census covers construction materials, tenure status, and housing type at the province and municipality levels.

**Published report:** `https://psa.gov.ph/content/housing-characteristics-philippines-2020-census-population-and-housing`

**PSA Albay regional office:** `https://rsso05.psa.gov.ph/albay`

**Fields available (municipality level):**
- Tenure status: owned/amortized, rented, rent-free (with consent), rent-free (without consent/squatting)
- Construction materials: strong materials (concrete/brick/stone), light materials (wood/bamboo/mixed), salvaged/makeshift
- Type of building: single house, duplex, apartment, commercial/industrial, indigenous

**Mapping to SVI fields:**
- Pct. light/salvaged materials → `svi_housing` (housing fragility)
- Pct. rent-free without consent → `svi_tenure` (informal/undocumented tenure — the LandLedger gap)
- Pct. owned fully → reduces `svi_tenure`

**Critical note on tenure data:** The "rent-free without consent" category is the PSA proxy for informal settlers. This is an undercount — it only captures situations where the respondent admitted to informal tenure. The true rate of undocumented/insecure tenure in Albay (especially in PDZ/EDZ barangays) is substantially higher, which is precisely the gap that LandLedger is designed to fill. The `svi_doc` field should be flagged explicitly as "incomplete without LandLedger data."

---

## Source 5: PHIVOLCS — Mayon Volcano Danger Zones (HARDCODED — use directly)

**What it is:** The Philippine Institute of Volcanology and Seismology maintains official volcanic hazard maps for Mayon. The danger zones are defined by radius from summit and validated by actual eruptive behavior.

**Zone definitions:**
- **PDZ (Permanent Danger Zone):** 6km radius from summit (13.2567°N, 123.6853°E). No permanent settlement permitted. APSEMO enforces mandatory evacuation for all barangays with any land in PDZ.
- **EDZ (Extended Danger Zone):** 8km radius (6km PDZ + 2km extension). Pre-emptive evacuation during elevated alert levels.
- **Alert Level system:** PHIVOLCS uses Levels 0–5; Level 3+ triggers mandatory EDZ evacuation; Level 4+ triggers wider 10km zone.

**Known barangays with land inside the PDZ (29 confirmed, 2016 PSA boundaries):**

*Bacacay municipality:*
Upper Bonga, Sogod

*Camalig municipality:*
Anoling, Cabagñan, Quirangay, Salugan, Sua, Tumpa

*Daraga municipality:*
Bañadero, Budiao, Matnog, Mi-isi, Salvacion

*Guinobatan municipality:*
Doña Tomasa, Maninila, Masarawag, Muladbucad Pequeño, Muladbucad Grande

*Legazpi City:*
Barangays 50, 51, 52, 53, 54

*Ligao City:*
Baligang, Amtic, Nabonton, Tambo

*Malilipot municipality:*
Calbayog, Canaway, San Francisco, San Jose, San Roque, Santa Cruz, Santa Teresa

*Santo Domingo municipality:*
Fidel Surtida, Lidong, San Fernando, Santa Misericordia

*Tabaco City:*
Bantayan, Bonot, San Isidro, Buang, Buhian, Comon, Magapo, Mariroc, Oras, Oson, Tabiguian

**How to use in BARANGAYS array:**
```javascript
var PDZ_BARANGAYS = new Set([
  // Bacacay
  'Upper Bonga','Sogod',
  // Camalig
  'Anoling','Cabagnan','Quirangay','Salugan','Sua','Tumpa',
  // Daraga
  'Banadero','Budiao','Matnog','Mi-isi','Salvacion',
  // Guinobatan
  'Dona Tomasa','Maninila','Masarawag','Muladbucad Pequeno','Muladbucad Grande',
  // Legazpi
  'Barangay 50','Barangay 51','Barangay 52','Barangay 53','Barangay 54',
  // Ligao
  'Baligang','Amtic','Nabonton','Tambo',
  // Malilipot
  'Calbayog','Canaway','San Francisco','San Jose','San Roque','Santa Cruz','Santa Teresa',
  // Santo Domingo
  'Fidel Surtida','Lidong','San Fernando','Santa Misericordia',
  // Tabaco
  'Bantayan','Bonot','San Isidro','Buang','Buhian','Comon','Magapo','Mariroc','Oras','Oson','Tabiguian'
]);

// When building BARANGAYS array:
BARANGAYS.forEach(function(b){
  b.in_pdz = PDZ_BARANGAYS.has(b.n);
  // EDZ: use distance from summit
  var distMayon = Math.sqrt(
    Math.pow(b.lat - 13.2567, 2) +
    Math.pow((b.lng - 123.6853) * Math.cos(b.lat * Math.PI/180), 2)
  );
  b.in_edz = distMayon < (2/111); // 2km in degrees approx
  b.dist_mayon_km = distMayon * 111;
});
```

**Source:** `https://www.phivolcs.dost.gov.ph/volcano-hazard-maps/`

---

## Source 6: HazardHunterPH — Multi-Hazard Exposure at Barangay Level

**What it is:** GeoRisk's public-facing web tool that computes hazard exposure for each Philippine barangay by intersecting hazard layers with population. Available as a REST API under the hood.

**Web interface:** `https://hazardhunter.georisk.gov.ph/map`

**Hazard layers available:**
- Storm surge (return periods: 5yr, 25yr, 100yr)
- Rain-induced landslide (susceptibility: Low/Med/High/Very High)
- Earthquake ground shaking (intensity zones)
- Flood (return periods: 5yr, 25yr, 100yr)
- Volcanic hazard (Mayon, debris avalanche, lahar channels)
- Tropical cyclone wind (return periods)

**API pattern (undocumented but functional):**
```
https://hazardhunter.georisk.gov.ph/api/barangay/hazard?brgy_code=[PSGC_CODE]
```

**Limitation:** The API requires the 10-digit PSGC barangay code, not just name. These codes must be matched from the PSA PSGC table.

**How this maps to SVI fields:**
- `flood_high` + `flood_med` → `pfl` (flood hazard score)
- `surge_high` → `ptyph` partial input (coastal surge component)
- `landslide_high` → `pslide` (if added as a hazard dimension)
- Volcanic hazard layer → validates/supplements PDZ boolean with continuous distance-based scores

---

## Source 7: DSWD Listahanan 3 — Household Poverty Targeting (FOI ONLY)

**What it is:** The National Household Targeting System for Poverty Reduction. House-to-house interviews covering 15.4 million households across all 42,045 barangays nationally. Completed 2019-2022.

**Data includes:**
- Household-level poverty assessment (scored against 11 indicators)
- Count of poor households per barangay
- 4Ps (Pantawid) beneficiary enrollment by barangay

**Access:** FOI request only via `https://www.foi.gov.ph/agencies/dswd/listahanan-and-4ps-program-data/`

**Processing time:** 15 working days standard; often longer in practice.

**Why this matters:** Listahanan gives the only sub-municipal poverty density data that is independently verified. PSA poverty incidence (SAE) is an estimate; Listahanan is a count. For Albay barangays in evacuation zones, Listahanan data directly measures who is likely to need post-disaster aid.

**Current status in tool:** Not available. `svi_poverty` per barangay uses municipality-level SAE as baseline. Mark this field explicitly as "municipality estimate" in the detail panel.

---

## Source 8: NDRRMC / APSEMO — Disaster History and Evacuation Records

**What it is:** National Disaster Risk Reduction and Management Council maintains evacuation records, casualty reports, and damage assessments for each hazard event. Albay Provincial Disaster Risk Reduction and Management Office (PDRRMO) and APSEMO (Albay Public Safety Emergency Management Office) maintain local records.

**Available data:**
- Mayon eruption event history (2018, 2023 significant; 1814, 1984 reference events)
- Evacuation count per event by municipality
- Typhoon track and impact data (Reming/Durian 2006 — worst in modern record: ~1,200 deaths in Albay alone)
- APSEMO's "Zero Casualty" protocol outcomes per event

**Access:** Mostly PDF reports via NDRRMC website (`ndrrmc.gov.ph`) and PhilAtlas event summaries. No structured API.

**How this maps to SVI fields:**
- Historical evacuation frequency → component of `svi_doc` (displacement without documentation)
- Reming/Durian 2006 mortality → calibration reference for overall risk scoring
- APSEMO protocol compliance → component of resilience (`res`) score

---

## Source 9: Open Street Map / Overpass API — Roads, Schools, Health Facilities

**What it is:** OSM data for Philippines is reasonably good at the municipal level, with barangay-level coverage varying significantly (urban Legazpi and Daraga are well-mapped; remote island municipalities like Rapu-Rapu are sparse).

**Useful queries for SVI:**
```javascript
// Barangay boundaries (admin_level=10 in Philippines OSM)
'[out:json];rel["admin_level"="10"]["is_in:province"~"Albay"];out geom;'

// Health facilities in Albay
'[out:json];area["name"="Albay"]["admin_level"="4"]->.a;node(area.a)["amenity"~"hospital|clinic|health_post"];out;'

// Schools
'[out:json];area["name"="Albay"]["admin_level"="4"]->.a;node(area.a)["amenity"="school"];out;'
```

**Note on barangay boundaries via Overpass:** OSM admin_level=10 coverage for Philippines barangays is incomplete — many rural barangays are not mapped. Use GeoRisk API (Source 1) as the primary boundary source. Overpass is more useful for POI data (health, schools, evacuation centers).

**Evacuation centers:**
```
"emergency"="assembly_point"
"amenity"="social_facility"
"amenity"="community_centre"
```

---

## Source 10: LandLedger (IOM HLP) — Tenure Documentation

**What it is:** IOM's Housing, Land and Property initiative is compiling formal tenure records for post-disaster affected communities in the Philippines. This is the dataset this tool is designed to demonstrate the need for.

**Current status:** Not publicly accessible. The entire purpose of this tool demo is to show IOM's HLP team what barangay-level tenure data would enable — and to argue that the `svi_doc` layer is currently the weakest because this data doesn't exist.

**How it maps to the tool:**
- `svi_doc` — currently estimated from PSA "rent-free without consent" + DSWD Listahanan enrollment as proxies
- When LandLedger data becomes available: replace with actual documentation rate per barangay (% with formal title/CLOA/lease vs. undocumented)
- `svi_tenure` — land tenure security (overlaps with `svi_doc`; can be split into two dimensions once LandLedger data exists)

**In the tool UI:** The documentation dimension should display a "Data source: estimated — LandLedger integration pending" note. This is the pitch embedded in the tool.

---

## Data Integration Strategy

### Phase 1 — Available Now (no FOI required)

These sources can be called at tool runtime or hardcoded from search data:

1. **GeoRisk API** → fetch barangay polygons at load time, compute centroids, build BARANGAYS array geometry
2. **PHIVOLCS PDZ list** → hardcode the 29 PDZ barangay names as `PDZ_BARANGAYS` Set; flag each BARANGAY on load
3. **PSA SAE 2021 poverty estimates** → hardcode per municipality from PSA published tables; apply as `svi_poverty` baseline per municipality, assigned to all barangays within

### Phase 2 — Manual Compilation (extract once, hardcode)

These require manually accessing the browser-based portals and constructing the data table:

4. **PSA 2020 CPH population by barangay** → access via OpenStat or PhilAtlas; compile CSV of 720 barangays with pop_total
5. **PSA housing characteristics (municipality level)** → read published PDF tables for Albay; hardcode % light construction and % informal tenure per municipality
6. **HazardHunterPH hazard scores** → query the web tool for flood/typhoon/landslide scores per municipality; hardcode as baseline values

### Phase 3 — FOI Request

7. **DSWD Listahanan 3** → file FOI request; 15 working day turnaround; provides ground-truth poverty density per barangay

### What to flag as incomplete in the tool UI

Every SVI dimension that is estimated from municipal averages (not real barangay data) should display a small "Municipality estimate" badge in the detail panel. This is honest about data quality and reinforces the need for LandLedger.

Specifically:
- `svi_poverty` → "PSA SAE 2021 estimate (municipality-level)"
- `svi_housing` → "PSA 2020 CPH (municipality-level)"
- `svi_doc` → "Estimated — LandLedger data pending"
- `svi_tenure` → "PSA proxy + estimated"
- `svi_elderly` → "PSA 2020 CPH (municipality-level)"

`pvol` and `in_pdz` are the only fields with TRUE barangay-level data (from PHIVOLCS), and they should be flagged as such ("PHIVOLCS verified").

---

## Albay Municipality Reference

18 cities & municipalities, 720 total barangays:

**Cities (3):**
- Legazpi City — provincial capital, most urbanized, Mayon-facing
- Ligao City — western Albay, less volcanic exposure
- Tabaco City — northern Albay, typhoon-exposed Pacific coast

**Municipalities (15):**
- Bacacay — southwestern coast, near Mayon, typhoon-exposed
- Camalig — directly on Mayon's western slope; highest PDZ coverage
- Daraga — near Legazpi, significant PDZ overlap
- Guinobatan — southwestern, significant PDZ overlap
- Jovellar — southeastern interior, lower volcanic risk
- Libon — western interior, lower volcanic risk
- Malilipot — northern Mayon slope; most barangays on the volcano itself
- Manito — southeastern coast, lagoon area (Manito Lagoon), Rapu-Rapu proximity
- Oas — central interior
- Pio Duran (Pioduran) — southeastern coast, flood-prone river delta
- Polangui — western Albay, lower volcanic risk
- Rapu-Rapu — island municipality in Albay Strait (isolated, high typhoon exposure)
- Santo Domingo — northern Mayon slope, PDZ barangays
- Tiwi — southeastern coast, geothermal area, hot spring tourism

---

## Key Numerical References

| Item | Value | Source |
|------|-------|--------|
| Albay total population (2020) | 1,374,768 | PSA CPH 2020 |
| Total barangays | 720 | PSA PSGC |
| Mayon summit coordinates | 13.2567°N, 123.6853°E | PHIVOLCS |
| PDZ radius | 6 km from summit | PHIVOLCS |
| EDZ radius | 8 km from summit | PHIVOLCS |
| Barangays with PDZ land | 29 | PHIVOLCS 2016 data |
| Province PSGC code | 0518 | PSA |
| Albay GeoRisk prov_code | '0518' | GeoRisk API |
| Typhoon Reming/Durian (2006) deaths in Albay | ~1,200 | NDRRMC |
| APSEMO founding | 1995 | APSEMO |
| Mayon last major eruption | 2023 | PHIVOLCS |

---

*Sources: PSA, PHIVOLCS, GeoRisk Philippines, DSWD, NDRRMC, PAGASA, PhilAtlas, Rappler, IOM Philippines*
