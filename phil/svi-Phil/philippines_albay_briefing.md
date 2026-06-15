# Philippines / Albay SVI Tool — Project Briefing
*Paste this at the start of a new chat to resume work on this project.*

---

## What This Is

An extension of an existing Puerto Rico Social Vulnerability & Hazard Intelligence tool (a single-file `index.html` interactive map). The goal is to build a parallel tool for **Albay Province, Philippines** — using the same overall architecture but evolved to handle multi-hazard exposure, a formal tenure layer, and a reconstruction record layer that the PR tool didn't have.

The tool is being built as a demonstration piece, with a secondary goal of showing value to Daniel's former colleagues at IOM's Housing, Land and Property (HLP) team / Global Shelter Cluster to eventually unlock access to LandLedger data from their Albay deployment.

---

## Why Albay

Albay was chosen over Eastern Visayas (Haiyan) because:

1. **LandLedger was deployed here.** IOM's digital tenure documentation tool was used in Albay — a very low formal-tenure area. Even though the data isn't accessible yet, the tool is being built to show where that data would slot in, making the pitch to the IOM team concrete.
2. **Multi-hazard layering.** Albay has Mayon Volcano (one of the world's most active, with a 6km Permanent Danger Zone and 8km Extended Danger Zone), typhoon exposure (most typhoon-prone region in the Philippines), lahar risk, and flooding. The 2006 compound event — Typhoon Durian (Reming) triggering lahar flows from Mayon's slopes — killed ~1,500 people and is the anchor event.
3. **The tenure trap is on permanent display.** The PDZ has existed for decades. ~30,000–50,000 people live within or adjacent to it. They can't get formal tenure because land is classified as hazard land. Without tenure, they can't access housing programs, credit, or reconstruction assistance. Without economic alternatives, they continue farming the volcanic slopes (extremely fertile andisol soil). The cycle repeats with every eruption.
4. **APSEMO's zero casualty program** is nationally and internationally recognized — 19 consecutive years of zero disaster deaths through pre-emptive evacuation protocols. This makes Albay simultaneously the country's best institutional preparedness story AND a place where the underlying vulnerability cycle has never been broken.
5. **Mayon is actively erupting.** Significant unrest January 2026, ashfall events May 2026 (₱6M in crop losses). This is a live story, not historical.

**Geographic scope:** Albay Province — 3 cities (Legazpi, Ligao, Tabaco) + 15 municipalities. Unit of analysis: municipality level with barangay-level detail in the Mayon danger zone ring. Language: English (Philippines official language; all government data is in English).

---

## Analytical Framework

The tool is grounded in Daniel's thesis: *"Raised Under Bad Stars: Tracing the complexities of creating, transmitting, and preserving a culture of preparedness among disaster-vulnerable communities"* (UC Berkeley, 2022).

Key thesis concepts that shape the tool:
- **The four-stage lifecycle:** Formulation → Strengthening → Operationalizing → Degradation. The Cultural Record layer should explicitly map where communities sit in this cycle.
- **Top-down failure mode:** Government no-build zones and resettlement projects that ignore community norms consistently fail. The Tacloban (post-Haiyan) and Albay (post-Reming) cases are both documented in the thesis and in the literature.
- **The tool as anti-degradation infrastructure:** Documenting cultural memory, community organizations, and resilience knowledge before it degrades.

---

## Core Analytical Tension

Albay has **the best institutional disaster response in the Philippines** (APSEMO, zero casualties, 720 barangay risk maps since 1991, pre-emptive evacuation) coexisting with **a documented inability to break the underlying vulnerability cycle** (14 of 25 NHA post-Reming resettlement sites still at risk; families returning to danger zones after every eruption; Bulatlat 2026: "Eruption after eruption, Albay's disaster funding never breaks the cycle").

This tension — exceptional preparedness + structural failure in reconstruction — is the analytical core.

---

## The Tenure Trap (Key New Layer vs. PR Tool)

Standard SVI measures income, housing quality, education — but not whether someone has a legal right to their home. In Albay:

- Communities in the PDZ have no formal tenure because the land is classified as hazard land
- Without formal tenure → can't access housing programs, agricultural credit, reconstruction assistance
- Without economic alternatives → no reason to leave the fertile volcanic slopes
- Government resettlement sites are often 20+ km from livelihoods (same failure as post-Haiyan Tacloban)
- People return after every eruption. The cycle closes where it started.

**LandLedger connection:** IOM's HLP team deployed LandLedger in Albay to document informal land rights digitally. The tool will show where that data would integrate, even before access is granted.

**Post-Haiyan reconstruction failures (relevant context):**
- Fishing communities relocated to farming areas — livelihoods severed for displaced AND host farmers
- NGO/NHA single-family units built for nuclear families; Filipino homes are multigenerational by design → families added floors and extensions without engineering, making structures more dangerous
- Cinder block perceived as higher-status than bamboo despite bamboo being more structurally appropriate for typhoon/seismic contexts
- Contractors cheaped out on concrete mixes → structurally unsound from day one
- No engineering oversight at scale
- "Who built the homes and under what level of engineering management" is a key analytical question for the Reconstruction Record layer

---

## Data Sources Identified

### Physical Hazard
- **PHIVOLCS** — Mayon danger zone boundaries (6km PDZ, 8km EDZ), lahar channel maps, volcanic hazard zones, eruption history
- **MGB (Mines and Geosciences Bureau)** — Geohazard maps at barangay level (landslide + flood susceptibility); one of the most comprehensive sub-municipal hazard datasets in the region
- **PAGASA** — Historical typhoon tracks, rainfall data
- **JTWC / IBTrACS** — Western Pacific typhoon best-track database (1945–present)
- **PhilAWARE** — Multi-hazard aggregation platform, English, open access
- **NDRRMC** — Situation reports for major events with impact by province/municipality

### Social Vulnerability
- **PSA 2020 Census** — Barangay-level data: income, education, housing materials, water/sanitation access; shapefiles via PSA GIS portal
- **DSWD Listahanan / NHTS-PR** — National household poverty targeting system; municipality-level counts of poor households
- **DSWD 4Ps beneficiary counts** — Municipality-level; primary poverty proxy (4Ps = Pantawid Pamilyang Pilipino Program, ~4M beneficiary households nationally)
- **CBMS (Community-Based Monitoring System)** — Barangay-level poverty indicators where available
- **DOH health facility master list** — Geocoded; access to care layer
- **DepEd school data** — Enrollment, location

### Tenure Layer (Proxy Data — Placeholder for LandLedger)
- **PHIVOLCS PDZ/EDZ boundaries** — Who is inside the no-build zone
- **NHA resettlement site locations** — FOI portal has Typhoon Reming resettlement project location dataset specifically
- **SHFC Community Mortgage Program coverage** — Where tenure formalization has/hasn't happened
- **DHSUD danger zone classifications** — Department of Human Settlements and Urban Development
- **LRA titling density by municipality** — Inverse = where informal tenure concentrates

### Reconstruction Record (New Layer)
- **FOI Philippines — Typhoon Reming resettlement projects** — Direct dataset on site locations: foi.gov.ph
- **IOM post-Reming housing** — 907 permanent shelters + 5 community centers (Albay + Camarines Sur), USAID-funded, documented
- **IOM newer program** — "Typhoon and earthquake-proof homes" currently being built in Albay (2024–present); different design standards than 2007 round
- **PMC peer-reviewed study** — "Geophilosophical realness of risk: a case study in NHA resettlement sites in Albay" — 14 of 25 sites still at/increasing risk. PMC article ID: PMC7989691
- **Build Change Philippines** — Structural survey data on housing quality in disaster-affected areas; they specifically work on engineering quality in Philippine reconstruction
- **ESSC (Institute of Environmental Science for Social Change)** — Rapid review of post-disaster housing reconstruction approaches; covers Albay programs
- **Shelter Cluster Philippines / ReliefWeb** — Post-Haiyan housing compendium (applicable methodology)

### Social Resilience / Community Organizations
- **APSEMO (Albay Public Safety and Emergency Management Office)** — The anchor institution. Founded 1995. Galing Pook Award winner. UNDP partner. Pre-emptive evacuation protocol triggers at typhoon ≥120 km/h + direct hit projection. 720 barangay risk maps since 1991. 115 evacuation centers activated in 2023 Mayon unrest. Cost data: ₱25.71M ($435K) from Quick Response Fund for 2023 evacuation = ~₱1,267 ($21.50) per person.
- **DSWD KALAHI-CIDSS** — Community-driven development program; geographic coverage data by municipality
- **BDRRMCs (Barangay Disaster Risk Reduction and Management Committees)** — Required in all 42,000+ barangays; quality varies; barangay-level DRRM plans
- **Philippine Red Cross — Albay Chapter** — Disaster response coverage
- **NDRRMC member agencies** — Oxfam Philippines, World Vision, Save the Children presence in Bicol

### Historical Events (Anchor Stories)
- **Typhoon Reming (Durian), November 2006** — Lahar flows from Mayon triggered by typhoon rainfall; ~1,500 killed; anchor compound event
- **Mayon eruption 2018** — 90,000+ evacuated; PHIVOLCS alert Level 4
- **Mayon unrest January 2026** — 3,000+ displaced; ongoing
- **Mayon ashfall May 2026** — ₱6M agricultural losses; active

### Additional / Cross-Cutting
- **IDMC (Internal Displacement Monitoring Centre)** — Philippines displacement data; HDX
- **PhilSys (National ID)** — Being used for DSWD calamity assistance verification; documented problem: displaced people lose IDs, then lose access to assistance
- **BSP remittance data** — OFW remittance flows by region; critical resilience indicator
- **UNESCO tentative World Heritage listing** — Mayon Cultural Landscape; acknowledges centuries of agricultural use of slopes as inseparable from hazard exposure
- **Academic: "Moving for safety: evacuation response during 2014 Mayon eruption"** — Applied Volcanology journal; documents evacuation-return behavior of farmers inside PDZ

---

## Key Human Stories to Develop

1. **The farming family inside the PDZ** — Choosing to farm the slopes because the andisol soil yields multiple harvests per year; the volcanic soil is measurably more productive than alternatives; the economic pull quantified against the hazard push. Short-term cost: ashfall destroys crops (₱6M in May 2026). Long-term value: mineral enrichment makes slopes among the most productive agricultural land in the region.

2. **The lahar of 2006** — Typhoon Durian's rainfall on Mayon's slopes triggered lahar flows. ~1,500 deaths. Many were people who had returned to the PDZ after previous evacuations or who had no alternative due to the tenure trap. This is the compound event that shows what happens when both hazard systems (volcanic + typhoon) activate simultaneously.

3. **The resettlement that didn't hold** — NHA post-Reming sites built in "safe" locations. 14 of 25 remain at ongoing or increasing risk because families built secondary structures in gullies and alluvial fans — precisely the areas they were meant to move away from — because the resettlement sites had no economic logic for them. The Bulatlat 2026 investigation documents the ongoing funding cycle that patches without solving.

4. **The evacuation machine** — APSEMO's zero casualty achievement as institutional resilience: the 19-year record, the pre-emptive evacuation protocol, the school-as-shelter system, the per-person cost of each activation. Coexisting with the fact that after every evacuation, people return.

---

## Tool Architecture Decisions (Agreed)

**Evolving from PR, not replicating it.** Key changes:

1. **Multi-hazard toggle** — Three switchable hazard layers: Volcanic (PDZ + lahar channels), Typhoon (historical tracks + storm surge zones), Compound Flood/Lahar (MGB geohazard maps). PR was hurricane-centric; this needs to show all three clearly.

2. **Tenure layer** — New layer entirely. Shows: PDZ boundary vs. actual settlement concentration; NHA resettlement site locations with distance-to-livelihood calculations; SHFC coverage gaps; LandLedger placeholder clearly labeled.

3. **Reconstruction Record layer** — New layer. Maps past recovery projects by location, builder (NHA / IOM / NGO / community-driven), materials, engineering oversight presence, livelihood compatibility, and outcome (occupied / modified / abandoned / at-risk).

4. **Cultural Record layer** — Uses Daniel's thesis framework (Formulation → Strengthening → Operationalizing → Degradation) as explicit spine rather than ad-hoc organization.

5. **Language:** English throughout.

6. **Geographic unit:** Municipality level with barangay detail for the Mayon PDZ ring specifically.

---

## Daniel's Background Context

- Master of Development Practice, UC Berkeley 2022
- Thesis on history, memory, and culture of disaster preparedness across global contexts
- Worked on LandLedger with IOM's Housing, Land and Property team under the Shelter and Settlements sector and Global Shelter Cluster
- Currently at Nubank (São Paulo)
- Has Spanish language capacity (relevant for the Mexico tool being built in parallel)
- The Puerto Rico tool already exists as a complete `index.html` and is being put on GitHub Pages

---

## Mexico Tool (Parallel Project — Separate Chat)

A parallel tool is being planned for the **Guerrero/Oaxaca/Chiapas corridor** in Mexico, with a multi-hazard frame (Pacific hurricane + seismic + flood/landslide), anchored to Hurricane Otis 2023 and the September 2017 compound earthquake events, with 1985 Mexico City earthquake as the Cultural Record origin story. That tool is being built separately — this briefing is Philippines only.

---

## Key Sources

- [APSEMO Zero Casualty Strategy](https://advance.sagepub.com/articles/preprint/Zero_Casualty_The_Disaster_Risk_Reduction_and_Management_Strategy_of_Albay_Province_Philippines/8080748)
- [Geophilosophical realness of risk: NHA resettlement sites in Albay — PMC7989691](https://pmc.ncbi.nlm.nih.gov/articles/PMC7989691/)
- [FOI: Typhoon Reming resettlement project locations](https://www.foi.gov.ph/requests/typhoon-reming-resettlement-projects-location/)
- [Eruption after eruption, Albay's disaster funding never breaks the cycle — Bulatlat 2026](https://www.bulatlat.com/2026/01/25/eruption-after-eruption-albays-disaster-funding-never-breaks-the-cycle/)
- [IOM typhoon and earthquake-proof homes in Albay](https://philippines.iom.int/news/construction-typhoon-and-earthquake-proof-homes-begins-albay)
- [Moving for safety: Mayon evacuation behavior study](https://appliedvolc.biomedcentral.com/articles/10.1186/s13617-021-00109-4)
- [Post-Disaster Shelter Recovery Policy Framework — World Bank Philippines](https://documents1.worldbank.org/curated/en/579231642696271929/pdf/Post-Disaster-Shelter-Recovery-Policy-Framework-Building-a-Responsive-System-to-Support-Resilient-and-Equitable-Recovery-in-the-Philippines.pdf)
- [Oxfam Philippines: The Right Move — durable relocation after Haiyan](https://oxfam.org.ph/download/the-right-move-ensuring-durable-relocation-after-haiyan/)
- [Mayon ashfall devastates Albay agriculture — Manila Times May 2026](https://www.manilatimes.net/2026/05/11/regions/mayon-volcano-ashfall-devastates-albay-agriculture-crops-worth-p6m/2340204)
- [PhilAWARE multi-hazard platform](https://www.philaware.ph/)
- [IDMC Philippines displacement data — HDX](https://data.humdata.org/dataset/idmc-idp-data-for-philippines)
