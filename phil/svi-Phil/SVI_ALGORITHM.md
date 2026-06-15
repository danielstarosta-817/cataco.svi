# Albay SVI Tool — Algorithm & Weighting Methodology

*How the tool scores vulnerability, resilience, and composite risk for each unit.*
*Last updated: June 2026*

---

## Design Philosophy

Standard disaster risk models score physical hazard exposure and stop there. This tool is built around a specific argument: **physical exposure alone systematically undercounts the most vulnerable communities.** A community directly in Mayon's path but with strong tenure, good road access, and active APSEMO coverage may recover faster than a community in a moderate typhoon zone with 60% informal tenure, no documentation, and road isolation that cuts it off for days.

The composite score is designed to make that gap visible and measurable. The gap between a location's physical hazard score and its full SVI composite is as important as either score alone.

---

## Unit of Analysis

The tool operates at two resolutions:

**Municipality level** (18 cities/municipalities): Full scoring with hardcoded data from PSA, PHIVOLCS, and field research. All fields available.

**Barangay level** (~720 barangays): Boundary geometry fetched at runtime from GeoRisk API. Where BRGY_ENRICHED data exists (47-field array per barangay, pcode-keyed), barangay-specific scores override municipality-level estimates. Where BRGY_ENRICHED data is absent, the parent municipality's score is used as the barangay floor.

---

## Score Architecture: Three Tiers

### Tier 1 — Physical Hazard Score (`phys_score`, 0–1)

Measures exposure to physical hazard events, independent of who is there.

```
phys_score = pvol×w_vol + ptyph×w_typh + pfl×w_flood
```

Weights are set by the left-panel toggle state — users can adjust which hazard layers are active. Default weights:

| Component | Field | Default Weight | Source |
|-----------|-------|----------------|--------|
| Volcanic (Mayon) | `pvol` | 0.45 | PHIVOLCS distance from PDZ + summit |
| Typhoon / storm surge | `ptyph` | 0.35 | PAGASA track exposure + HazardHunterPH |
| Flooding | `pfl` | 0.20 | HazardHunterPH flood return periods |

The weights sum to 1.0. When a user deactivates a hazard layer (e.g., turns off flood), the remaining weights are renormalized so they continue summing to 1.0. This means the physical score reflects the user's active hazard query, not a fixed formula — the map responds to the question being asked.

**What physical score does NOT capture:** who is exposed. Two communities with identical physical scores may have radically different vulnerability if one is wealthy with good documentation and the other is informal settlers with no road out.

---

### Tier 2 — Social Vulnerability Index (`svi_score`, 0–1)

Measures the population's pre-existing conditions that determine how much harm a hazard event causes and how long recovery takes.

```
svi_score = f(svi_housing, svi_poverty, svi_elderly, svi_road, svi_cell, svi_doc)
```

Each dimension is scored 0–1 where 1 = maximum vulnerability:

| Dimension | Field | What It Measures | Data Source |
|-----------|-------|-----------------|-------------|
| Housing fragility | `svi_housing` | % households in light-material or salvaged construction | PSA 2020 CPH housing structure |
| Economic fragility | `svi_poverty` | Poverty incidence; household income buffer | PSA SAE 2021 |
| Elderly / care-dependent | `svi_elderly` | % population 65+ or dependent; evacuation-limiting | PSA 2020 CPH age structure |
| Road isolation | `svi_road` | Primary road flood risk; single-road dependency | DPWH + field observation |
| Communication gaps | `svi_cell` | Cell coverage reliability; early warning reach | NTC + field reports |
| Documentation barrier | `svi_doc` | % households unable to prove tenure for aid access | PSA informal tenure proxy + IOM field data |

**Why `svi_doc` is the most important field:** It is the bottleneck between evacuation success and recovery success. APSEMO can achieve zero casualty — getting people physically safe. But if 40–60% of evacuated households cannot prove residency to DSWD's satisfaction, they receive no shelter repair grant, no livelihood support, no NHA housing. The physical outcome (alive) is separated from the recovery outcome (recovered) by a documentation wall. `svi_doc` is the tool's way of making that wall measurable.

---

### Tier 3 — Composite SVI Score (0–1)

Combines physical hazard with social vulnerability dimensions into a single composite:

```
composite = min(1.0,
    phys_score
    + svi_doc    × 0.25
    + svi_poverty × 0.20
    + svi_housing × 0.18
    + svi_road   × 0.15
    + svi_elderly × 0.12
    + svi_cell   × 0.10
)
```

The composite is additive rather than multiplicative. Physical hazard is the base; social dimensions are added as increments. A community with zero physical exposure contributes only through its social dimensions (maximum social contribution ≈ 1.00). A community with high physical exposure has that as its floor, with social dimensions potentially pushing it above what hazard models alone would predict.

**The gap:**
```
gap = composite − phys_score
```
When `gap > 0.12`, the tool displays a high-priority alert: "Social vulnerability significantly exceeds physical hazard score. Physical risk maps alone will undercount this community's need."

When `gap > 0.06`, a moderate alert is shown.

**Composite weight rationale:**

- `svi_doc` (0.25, highest weight): Documentation barrier is the single most predictive variable for whether a household recovers after displacement. This is the LandLedger argument embedded in the algorithm.
- `svi_poverty` (0.20): Income determines whether households can absorb losses, self-recover, or enter debt cycles. Municipal SAE poverty incidence is the best available proxy.
- `svi_housing` (0.18): Construction material determines direct physical damage. Light-material construction collapses in typhoon winds and under ashfall load.
- `svi_road` (0.15): Road isolation determines whether evacuation and aid delivery are possible at all. Single-road municipalities are disproportionately cut off.
- `svi_elderly` (0.12): Elderly and dependent populations require more evacuation support, have lower self-recovery capacity, and have higher mortality in heat/cold stress at evacuation centers.
- `svi_cell` (0.10): Communication gaps affect early warning reach. Communities without reliable cell coverage may not receive PHIVOLCS/APSEMO alerts in time.

---

## Resilience Score (`res`, 0–1)

Resilience is scored separately from vulnerability and displayed as a distinct map mode. It is not subtracted from the composite — it is a parallel dimension showing the community's capacity to bounce back, which is analytically distinct from its exposure.

```
resilience = f(
    apsemo_drill_coverage,
    institutional_continuity,
    community_tenure_security,
    economic_diversity,
    post_event_recovery_rate
)
```

In practice, `res` is calibrated from:
- APSEMO drill frequency and PDZ coverage
- Historical post-event recovery time observations
- Economic base diversity (abacá monoculture vs. mixed livelihoods)
- Tenure security (titled households have more collateral, faster recovery access)
- Social capital proxies (barangay governance quality, community organizations)

Resilience interpretation:

| Score | Label | What It Means |
|-------|-------|---------------|
| 0.70–1.00 | Strong | Institutions active, economy diverse, tenure mostly formal |
| 0.50–0.69 | Emerging | Some capacity; gaps in documentation or economic diversity |
| 0.30–0.49 | Weak | High dependency on external aid; slow historical recovery |
| 0.00–0.29 | Critical | Isolated, undocumented, economically exposed |

---

## Barangay-Level Enrichment (BRGY_ENRICHED)

Where barangay-specific data exists, the 47-field enriched array overrides municipality-level estimates. Field index (`BE`):

| Index | Field | Description |
|-------|-------|-------------|
| 0 | `mayon_km` | Distance from Mayon summit (km) |
| 1 | `lahar_km` | Distance to nearest active lahar channel (km) |
| 2 | `lahar_gully` | Nearest named gully (1=Mi-isi, 2=Bonga, 3=Basud, 4=Masarawag, 5=Buyuan) |
| 3 | `pdz` | Boolean: inside PHIVOLCS 6km PDZ |
| 4 | `edz` | Boolean: inside 8km EDZ |
| 5 | `ashfall` | Boolean: documented ashfall exposure |
| 6 | `ashfall_mm` | Peak ashfall loading (mm equivalent) |
| 7 | `nha_dest` | Boolean: NHA destination site (resettlement) |
| 8 | `nha_compound` | Boolean: NHA site with documented compound hazard |
| 9 | `nha_origin` | Boolean: community of origin for resettled households |
| 10 | `reming` | Boolean: displaced/damaged in Typhoon Reming 2006 |
| 11 | `fishing` | Boolean: fishing-dependent livelihood |
| 12 | `mining` | Boolean: affected by mining operations (Rapu-Rapu context) |
| 13 | `road_iso` | Boolean: documented road isolation |
| 14 | `abaca` | Boolean: abacá cultivation present |
| 15 | `shield` | Boolean: geomorphically sheltered from primary PDC flow |
| 16 | `pvol` | Volcanic hazard score (0–1) |
| 17 | `plahar` | Lahar hazard score (0–1) |
| 18 | `ash_score` | Ashfall hazard score (0–1) |
| 19 | `storm` | Storm surge / typhoon hazard score (0–1) |
| 20 | `tenure` | Tenure insecurity score (0–1) |
| 21 | `livelihood` | Livelihood fragility score (0–1) |
| 22 | `isolation` | Isolation score (0–1) |
| 23 | `elderly` | Elderly/dependent population proportion (0–1) |
| 24 | `agri` | Agricultural dependence score (0–1) |
| 25 | `phys` | Physical hazard composite (0–1) — barangay level |
| 26 | `soc` | Social vulnerability composite (0–1) — barangay level |
| 27 | `res` | Resilience score (0–1) — barangay level |
| 28 | `composite` | Full SVI composite (0–1) — barangay level |
| 29 | `island` | Boolean: island barangay (maritime access only) |
| 30 | `quarry` | Boolean: active quarry nearby (lahar channel risk) |
| 31 | `stacked` | Boolean: multiple high-severity risk factors co-occurring |
| 32 | `lada` | Boolean: LADA (Local Adaptation) program active |
| 33 | `kristine` | Boolean: affected by Typhoon Kristine 2024 |
| 34 | `proactive` | Boolean: proactive household relocation recorded |
| 35 | `ash2018` | Boolean: affected by 2018 Mayon ashfall event |
| 36 | `repeat_ash` | Boolean: multiple ashfall events recorded |
| 37 | `evac2023` | Boolean: evacuated during 2023 Mayon eruption |
| 38 | `bantay` | Boolean: within Bantay Mayon monitoring network |
| 39 | `mangrove` | Boolean: mangrove buffer present (coastal resilience asset) |
| 40 | `weaving` | Boolean: abacá weaving livelihood (economic diversity asset) |
| 41 | `transformed` | Boolean: post-relocation community with rebuilt livelihoods |
| 42 | `apn_rain` | Boolean: APN rain-triggered hazard documented |
| 43 | `sci_vuln` | Boolean: identified in scientific vulnerability assessment |
| 44 | `iom_hous` | Boolean: IOM housing program active |
| 45 | `irrigated` | Boolean: irrigated agriculture (partial income stability) |
| 46 | `housing` | Housing quality score (0–1) |

---

## Fingerprint Display Logic

The vulnerability fingerprint in the "Analyze this place" panel splits into two subsections:

**Physical Hazards** (uses barangay BE fields when available, municipality scores as fallback):
1. Mayon volcanic risk → `pvol`
2. Lahar exposure → `plahar`
3. Ashfall loading → `ash_score`
4. Storm surge / cyclone → `storm`

**Social Dimensions** (uses barangay BE fields when available, municipality SVI fields as fallback):
1. Livelihood fragility → `livelihood` (or `svi_poverty`)
2. Tenure insecurity → `tenure` (or `svi_doc`)
3. Housing quality → `housing` (or `svi_housing`)
4. Agricultural dependence → `agri`
5. Isolation → `isolation` (or `svi_road`)
6. Elderly / care-dependent → `elderly` (or `svi_elderly`)

---

## Compounding Conditions Logic

The following flags trigger compounding conditions alerts in the right panel. Each flag is independently checked from BE data (barangay) or muni fields:

| Flag | Trigger | Severity |
|------|---------|----------|
| Inside PDZ | `enr[BE.pdz] === 1` | DANGER |
| Stacked vulnerability | `enr[BE.stacked] === 1` | DANGER |
| Compound NHA site | `enr[BE.nha_compound] === 1` | WARNING |
| Reming displacement | `enr[BE.reming] === 1` | WARNING |
| Kristine (2024) affected | `enr[BE.kristine] === 1` | WARNING |
| Repeat ashfall | `enr[BE.repeat_ash] === 1` | WARNING |
| Island barangay | `enr[BE.island] === 1` | INFO |
| Active quarry | `enr[BE.quarry] === 1` | INFO |
| Proactive relocation | `enr[BE.proactive] === 1` | GREEN (asset) |
| Mangrove buffer | `enr[BE.mangrove] === 1` | GREEN (asset) |

---

## Three Dimensions of Vulnerability (Plan Mode)

The plan panel organizes the same data into a framework for responders:

**Sensitivity** — how much this population will be harmed by a given hazard event. Driven primarily by `soc` score and livelihood/tenure fragility.

**Exposure** — the degree to which this community is in harm's way. Driven by `phys` score and boolean hazard flags (PDZ, lahar gully, storm surge).

**Adaptive Capacity** — the ability to anticipate, cope with, and recover from shocks. Driven by `res` score plus qualitative flags: `proactive`, `bantay`, `weaving`, `transformed`, `iom_hous`.

Each dimension is rated HIGH / MID / LOW using the same 0.65 / 0.35 thresholds used throughout the tool. A HIGH sensitivity + HIGH exposure + LOW adaptive capacity combination is the "who is most screwed when response teams leave" signal the tool is designed to surface.

---

## Color Scale Reference

All scores (0–1) map to a continuous color ramp:

| Score | Color | Label |
|-------|-------|-------|
| 0.00–0.25 | `#00E096` (green) | Low |
| 0.25–0.50 | `#FFD93D` (yellow) | Moderate |
| 0.50–0.75 | `#FF6B35` (orange) | Elevated |
| 0.75–1.00 | `#B40032` (deep red) | Critical |

Resilience uses an inverted ramp: high resilience → green, low resilience → red.

Tenure uses a separate purple ramp (low informal → green; high informal → purple) to distinguish tenure from hazard visually.

---

## Known Limitations

**Municipality-floor problem:** Where barangay-level data is absent, all barangays in a municipality receive the same score — masking within-municipality variation that can be dramatic (a PDZ barangay and a lowland barangay may both show the same score if only the municipality average is used).

**`svi_doc` is the weakest field:** Until LandLedger data is formally integrated, tenure documentation scores are estimated. This is the primary data gap this tool is designed to argue for filling.

**Static composite weights:** The additive weights in the composite formula are research-informed but not empirically validated against post-disaster outcome data in Albay specifically. Future calibration should compare composite scores against observed DSWD aid exclusion rates and recovery timelines per barangay.

**Resilience is the hardest to operationalize:** The `res` field is more judgment-based than other fields. It captures an important dimension — whether a community can survive response teams leaving — but it would benefit from ground-truth validation via longitudinal recovery studies.

---

*For data sources, see SVI_REFERENCES.md*
*For raw score data, see albay_svi_scores.csv*
*For tool architecture, see SVI_MAP_ARCHITECTURE_GENERIC.md*
