# Albay SVI Tool — Sources & References

*All sources consulted in building the Albay Social Vulnerability Index tool.*
*Compiled: June 2026*

---

## Primary Research & Academic Sources

**APSEMO Zero-Casualty Protocol**
Naz, R. et al., Bicol University. "Institutional Determinants of Zero-Casualty Outcomes in Mayon Volcano Evacuations." Peer-reviewed analysis of APSEMO's six-strategy model, including the 8km pre-emptive evacuation zone extension and its effect on mortality outcomes. Establishes APSEMO as the institutional variable explaining Albay's anomalous safety record relative to comparable Philippine provinces.
*Used for: resilience scores, institutional context, APSEMO Cultural Record entry, phase guidance.*

**NHA Resettlement Compound Risk Study**
PMC7989691 — "Compounding Hazard at NHA Resettlement Sites in Albay Province." Published in peer-reviewed journal, accessed via PubMed Central. Documents lahar channel routing errors, inadequate drainage at post-Reming relocation sites, and failure to account for typhoon flood exposure when siting resettlement communities. Oson (z=4.54) and Miisi (z=4.19) identified as highest-risk sites.
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7989691/
*Used for: NHA_SITES dataset, compound risk scores, Eduardo story profile.*

**Bulatlat 2026 Investigation**
"Families Displaced by Mayon Still Without Land Titles, 18 Years On." Investigative report documenting continuing land tenure insecurity among post-Reming resettlement households in Tabaco City, Daraga, and Guinobatan. Confirms NHA lot title transfer failure rate; documents DSWD aid exclusion mechanisms for informal tenure households.
https://bulatlat.com/2026/04/mayon-resettlement-land-tenure/
*Used for: svi_doc scores, tenure insecurity framing, Eduardo story, compounding conditions flags.*

**IOM Housing, Land and Property — Albay**
IOM Philippines HLP Program documentation: LandLedger pilot deployment scope, PDZ municipality coverage, institutional recognition gap (DSWD/NHA have not yet accepted LandLedger as formal proof of tenure). Covers Camalig, Daraga, Guinobatan, Santo Domingo, Malilipot.
https://philippines.iom.int/hlp-landledger
*Used for: LandLedger tool context, svi_doc field rationale, plan-mode guidance, Maricel story.*

**Mayon Evacuation Behavior Study**
Bicol University / PHIVOLCS collaborative research on household evacuation decision-making in PDZ communities. Key finding: generational hazard knowledge is a meaningful adaptive capacity asset; compliance with pre-emptive APSEMO orders is high in communities with multi-decade evacuation experience. Also documents "evacuation fatigue" as a behavioral risk after repeated events without property loss.
*Used for: resilience scoring, adaptive capacity dimension, preparedness phase guidance.*

**Manila Times — Ashfall Coverage, May 2026**
"Mayon Ashfall Disrupts Harvest Season in Guinobatan and Camalig." Real-time event coverage of 2026 ashfall event. Documents crop loss, road coating, school closures. Confirms repeat_ash pattern for municipalities documented in BRGY_ENRICHED data.
*Used for: repeat_ash flag in compounding conditions, ashfall hazard scoring validation.*

---

## Government Data Sources

**Philippine Statistics Authority (PSA)**
2020 Census of Population and Housing (CPH). Used for:
- Municipal and barangay population counts
- Housing tenure (% informal/rent-free without consent)
- Housing construction materials (% light/salvaged)
- Elderly population proportion by municipality
- Province total: 1,374,768 population, 720 barangays

2021 Small Area Estimation (SAE) — Municipal Poverty Incidence. Used for `svi_poverty` baseline per municipality.
https://psa.gov.ph/content/psa-releases-2021-city-and-municipal-level-poverty-estimates

2020 CPH Housing Characteristics Report.
https://psa.gov.ph/content/housing-characteristics-philippines-2020-census-population-and-housing

OpenStat Data Portal: https://openstat.psa.gov.ph/

**PHIVOLCS — Philippine Institute of Volcanology and Seismology**
Mayon Volcano Danger Zone Definitions (official). PDZ: 6km radius from summit (13.2567°N, 123.6853°E). EDZ: 8km. Alert Level protocol (0–5). PDZ barangay list: 29 confirmed barangays with land inside the 6km PDZ, from 2016 PSA boundary data.
https://www.phivolcs.dost.gov.ph/volcano-hazard-maps/
*Used for: in_pdz flag, PDZ_BARANGAYS set, volcanic hazard scoring, pvol field.*

**GeoRisk Philippines (PHIVOLCS / DOST)**
ArcGIS REST API providing PSA 2015-census-era barangay boundary polygons for all Philippine provinces. Province code for Albay: `0518`. Runtime fetch at tool load time.
Endpoint: https://portal.georisk.gov.ph/arcgis/rest/services/PSA/Barangay/MapServer/4/query
*Used for: all barangay boundary geometry in the map layer.*

**HazardHunterPH (GeoRisk)**
Multi-hazard exposure scoring per barangay. Storm surge return periods (5yr, 25yr, 100yr), flood, rain-induced landslide, tropical cyclone wind, volcanic hazard layers.
https://hazardhunter.georisk.gov.ph/map
*Used for: hazard component scores (ptyph, pfl, storm), lahar and ashfall risk flags.*

**NDRRMC — National Disaster Risk Reduction and Management Council**
Historical disaster event records: Typhoon Reming/Durian (2006) — ~1,200 Albay deaths, the worst single-event mortality in the province's modern record. Mayon eruption event log (2018, 2023 major events). Evacuation counts by municipality per event.
https://ndrrmc.gov.ph/
*Used for: disaster history calibration, reming flag, event timeline in story profiles.*

**DSWD — Department of Social Welfare and Development**
Emergency Shelter Assistance (ESA) eligibility rules and documentation requirements. Listahanan 3 (National Household Targeting System for Poverty Reduction) — FOI-only, not yet obtained for Albay at barangay level.
https://www.dswd.gov.ph/
*Used for: aid eligibility documentation in plan guidance, needs manifest.*

**NHA — National Housing Authority**
Resettlement site inventory for Albay. Sites documented: Oson, Pinabobong, Salvacion, San Vicente (Tabaco City); Cullat, Miisi (Daraga); other post-Reming sites. Z-score compound risk ratings from PMC study.
https://www.nha.gov.ph/
*Used for: NHA_SITES array, compound site risk flags, Eduardo story.*

**APSEMO — Albay Public Safety and Emergency Management Office**
Founded by SP Resolution No. 155-94 (June 16, 1994). Six-strategy zero-casualty doctrine. Pre-emptive evacuation at 8km (vs. PHIVOLCS standard 7km). Evacuation center network. Annual drill protocols.
*Used for: resilience scoring, institutional context, phase guidance, APSEMO Cultural Record.*

**PAGASA — Philippine Atmospheric, Geophysical and Astronomical Services Administration**
Storm surge assessment areas (SSA) for Albay coast; typhoon track historical database; weather advisory protocol integration with APSEMO.
*Used for: ptyph component, storm surge scores for coastal municipalities.*

---

## Academic and Policy Framework Sources

**Bicol University DRRM Research Program**
Multiple peer-reviewed outputs on Albay DRRM governance, APSEMO institutional analysis, and community-level disaster risk perception. Key variable identified: institutional continuity (same staff over years) as predictor of effective risk communication.
*Used for: resilience dimension, adaptive capacity framing, three-stage institutional model.*

**NAPC (National Anti-Poverty Commission)**
Voluntary relocation program data for PDZ communities. Convergence with NHA for site selection and title transfer.
*Used for: proactive_relocation flag, adaptive capacity, recovery phase guidance.*

**UN Sasakawa Award Documentation**
Albay READY program — Province of Albay received UN Sasakawa Award for Disaster Risk Reduction for integrating volcanic and climate risk into provincial development planning and school curricula. Documentation of what earned the award.
*Used for: adaptation phase guidance, institutional framing of APSEMO model.*

**IOM CCCM / DTM Philippines**
Displacement tracking and shelter monitoring post-Kristine (2024), post-Mayon 2023 eruption. Field reports on barangay-level displacement counts and recovery status.
*Used for: kristine flag, evac2023 flag in BRGY_ENRICHED.*

---

## Data Quality Notes

These sources are estimated or imputed rather than directly observed:

| Field | Status | Best Available Source |
|-------|--------|-----------------------|
| `svi_poverty` | Municipality estimate | PSA SAE 2021 |
| `svi_housing` | Municipality estimate | PSA 2020 CPH housing |
| `svi_doc` | **Estimated** | PSA informal tenure proxy + field reports. LandLedger integration pending. |
| `svi_elderly` | Municipality estimate | PSA 2020 CPH age structure |
| `svi_cell` | Estimated | NTC coverage reports + field reports |
| `in_pdz` | Verified (PHIVOLCS) | PHIVOLCS 2016 PDZ boundary |
| `pvol` | PHIVOLCS-calibrated | Distance from summit + PDZ status |
| `res` | Composite estimate | APSEMO drill coverage + governance indicators |

The `svi_doc` field is the weakest in the dataset. Until LandLedger data is formally integrated, this is estimated from PSA "rent-free without consent" housing tenure data plus field-based adjustments for PDZ barangays. This is the core argument for the LandLedger pilot: the tool demonstrates what becomes possible when that data exists.

---

*For tool architecture documentation, see SVI_MAP_ARCHITECTURE_GENERIC.md*
*For raw source landscape and API endpoints, see ALBAY_DATA_SOURCES.md*
*For score computation methodology, see SVI_ALGORITHM.md*
