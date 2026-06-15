# Mexico / Guerrero–Oaxaca–Chiapas SVI Tool — Project Briefing
*Paste this at the start of a new chat to resume work on this project.*

---

## What This Is

A companion tool to an existing Puerto Rico Social Vulnerability & Hazard Intelligence tool (`index.html` interactive map). The goal is to build a parallel tool for the **Guerrero–Oaxaca–Chiapas corridor in Mexico** — using the same overall architecture but evolved for a multi-hazard, multi-tenure context where violence/displacement is a co-equal vulnerability driver alongside physical hazards.

The tool is being built in Spanish throughout (the PR tool is bilingual EN/ES; this one is Spanish-only since that's the language of the communities and data). It is a demonstration piece and a companion to the Philippines/Albay tool.

**North star (Daniel's exact words):** *"This should be about showing the disparity between who organizations may look to give aid to vs who actually is most affected/most at risk, and championing the importance of nuance, localized understanding of risk profiles. Humanitarians should be able to see the tool and understand what risk actually looks like, not just what they think, and communities should be able to see it and say 'see, look at how we match up, we deserve more support!'"*

---

## Why This Corridor

The Guerrero–Oaxaca–Chiapas corridor was chosen because it is simultaneously:

1. **The most hazard-exposed region in Mexico.** Three independent hazard systems converge here: Pacific hurricane exposure (Otis 2023, the strongest Pacific landfalling hurricane ever recorded), a live subduction gap capable of Mw >8 (Guerrero Gap, ~115 years without major rupture, 5-meter slip deficit), and endemic flooding/landslide risk in highly deforested highland terrain.

2. **The most socially marginalized region in Mexico.** All three states rank in the top 3 nationally on both CONEVAL's Social Lag Index and CONAPO's Marginalization Index (2020). Guerrero: #1 "very high" marginalization; Chiapas: #2; Oaxaca: #3. Municipal-level data reveals pockets of extreme deprivation in municipalities like Cochoapa el Grande (Guerrero), Chalchihuitán (Chiapas), and San José Tenango (Oaxaca).

3. **The clearest case in Mexico for the aid-distribution vs. actual-need gap.** Post-Otis reconstruction focused on Acapulco's tourist zones and hotel strip. Thirty-six rural communal-land communities (Cacahuatepec) lost 10,000 hectares of corn crops and received zero official aid for months. The indigenous and Afro-descendant communities most affected by Otis are still demanding reconstruction of 26,000 housing units as of July 2025. Meanwhile AMLO declared Acapulco fully recovered by March 2024.

4. **The ejido/comunidad tenure trap is on permanent display.** Post-Otis housing assistance required property deeds. Ejidatarios have PROCEDE certificates as a fallback; comuneros (indigenous communal land holders) have only community assembly membership — no individual document that satisfies federal reconstruction requirements. The CECOP documented this exclusion pattern directly. It parallels the Philippines PDZ tenure trap almost exactly.

5. **Violence/forced displacement is a co-equal vulnerability driver.** Chiapas had 61.8% of all forced internal displacements in Mexico in 2024 (29,000 total nationally, 79% organized crime-driven). Guerrero ranks among the most violent states. Displaced persons lose ID documents, address registrations, and census enrollment — exactly the documentation FEMA/Bienestar require for aid. Violence and disaster are not separate systems here.

6. **Remittances are a primary resilience infrastructure.** Chiapas and Guerrero are the two most remittance-dependent states in Mexico: 14.6% and 14.0% of GDP respectively. This is the Mexican equivalent of OFW remittance flows as disaster resilience in the Philippines — a critical informal safety net that standard SVI frameworks don't capture.

7. **Hurricane Otis is the live anchor event.** October 25, 2023: Cat 5, 165 mph, strongest Pacific landfall ever recorded. Rapidly intensified from Cat 1 to Cat 5 in 12 hours — missed entirely by forecast models. 7 in 10 Acapulco residents live in poverty; over 98% of homes damaged. Reconstruction remains unequal and incomplete as of May 2026.

**Geographic scope:** 3 states — Guerrero, Oaxaca, Chiapas — approximately 80 municipalities in Phase 1 at consistent depth, with higher-resolution drill-down into coastal Guerrero/Acapulco zone in Phase 2. Unit of analysis: municipality level. Language: Spanish throughout.

---

## Analytical Framework

The tool is grounded in Daniel's thesis: *"Raised Under Bad Stars: Tracing the complexities of creating, transmitting, and preserving a culture of preparedness among disaster-vulnerable communities"* (UC Berkeley, published 2023 in IJDRM).

Key thesis concepts that shape the tool:
- **The four-stage lifecycle:** Formulation → Strengthening → Operationalizing → Degradation. The Cultural Record layer should explicitly map where communities sit in this cycle.
- **Top-down failure mode:** Government reconstruction projects that ignore community livelihoods, land rights, and social structure consistently fail. Post-Otis Acapulco and post-Haiyan Tacloban are structural parallels.
- **The tool as anti-degradation infrastructure:** Documenting cultural memory, community organizations, and resilience knowledge before it degrades.

The SEABEA framework (Social, Ecology, Built Environment, Agricultural, Engagement, Action) provides the backbone, adapted for Mexico with two additions: **Tenure/Displacement** and **Violence/Security** as explicit dimensions rather than sub-variables buried elsewhere.

---

## Core Analytical Tension

Mexico has **SASMEX — one of the world's oldest and most sophisticated seismic early warning systems** (since 1991, 96+ sensors, 60–80 second lead time for Mexico City) coexisting with **communities in Guerrero and Oaxaca where SASMEX alerts broadcast in Spanish, reaching residents who speak Nahuatl, Mixtec, Zapotec, or Tzeltal as their primary language**, and where the elimination of FONDEN in 2021 removed the primary institutional disaster finance mechanism before Otis ever made landfall.

The parallel with the Philippines is exact: exceptional institutional preparedness infrastructure coexisting with structural failure in reconstruction equity — with the additional dimension that violence/organized crime creates a third vulnerability layer that is absent in Albay.

---

## The Tenure Trap (Key New Layer vs. PR Tool)

Standard SVI measures income, housing quality, education — but not whether someone has a legal right to their home. In the Guerrero–Oaxaca–Chiapas corridor:

- **Ejido land** (~50% of rural Mexico): Ejidatarios hold PROCEDE certificates as individual documentation. These can serve as proof of habitation for some aid programs, but ejido land cannot be sold or mortgaged on the open market, limiting access to reconstruction credit.
- **Comunidad indígena / bienes comunales** (indigenous communal lands, prevalent in Oaxaca and Chiapas): Comuneros hold only community assembly membership — no individual document. This is the most absolute exclusion from formal reconstruction assistance. Post-Otis, housing aid required property deeds; communal land residents in Cacahuatepec simply didn't qualify.
- **Urban informal settlements** (colonias populares, periferia of Acapulco): Urban informal tenure — squatter occupation without title — creates the same exclusion in the city that ejido/comunal tenure creates in the countryside. Ciudad Renacimiento was explicitly excluded from Acapulco's federal reconstruction plan.

**FONDEN elimination (2021) connection:** FONDEN was replaced by Bienestar cash transfers and residual CONAVI housing programs. Bienestar requires census registration (Padrón del Bienestar). Displaced persons — whether by hurricane or by organized crime violence — lose address registration. The documentation requirement to receive aid eliminates the most vulnerable first.

**The CECOP case:** The Council of Ejidos and Communities Opposed to the La Parota Dam documented that 36 communal-land communities in Cacahuatepec received zero official post-Otis aid for months. Civil society (Oxfam México, Tlachinollan, Cooperación Comunitaria, Isla Urbana, Cinco Panes) filled the gap with 300+ tons of corn and 8,000+ food packages. This is the Albay CECOP parallel.

---

## The Violence/Displacement Layer (New vs. PR Tool)

This layer has no equivalent in the Philippines tool and only a marginal role in the Puerto Rico tool. In Mexico it is a primary vulnerability driver:

- **Forced internal displacement 2024:** ~29,000 people displaced by organized crime violence. Chiapas: 61.8% of national total. Sinaloa: 15.5%. Guerrero: 4.8%. Oaxaca also in the list.
- **Compounding mechanism:** Displaced persons lose ID documents, address records, Padrón de Bienestar enrollment. Without these, they cannot access disaster aid. Violence-induced displacement thus pre-destroys the documentation infrastructure that disaster response depends on.
- **Territorial control by organized crime** as a barrier to aid delivery: In several Guerrero and Chiapas municipalities, organized crime controls territorial access. NGOs and government programs cannot enter without cartel permission. This is a "last mile" access gap that standard logistics/vulnerability frameworks don't model.
- **Data source:** SESNSP (homicide rates by municipality), ACLED (conflict events and locations), IBERO Human Rights Program (forced displacement reports).

---

## The "Three Acapulcos" Frame

The most powerful narrative organizing device for the tool comes from journalism that describes Acapulco as three separate cities:

1. **The tourist Acapulco** — the hotel strip on Costera Miguel Alemán, which received the overwhelming share of post-Otis reconstruction attention and federal resources. Hotels largely restored, tourism economy recovering.

2. **The peripheral Acapulco** — the colonia populares climbing the hillsides above the tourist zone. Families in tin-roofed homes. Post-Otis: these areas received limited census-taking, irregular aid delivery, and are not in the federal reconstruction plan.

3. **The rural Acapulco** — communal lands like Cacahuatepec. Received zero official aid. 10,000 hectares of crops destroyed. Civil society response only.

This "three cities" framing maps directly onto the tool's core mechanic: the physical hazard model treats all of Acapulco as roughly equivalently exposed to a Cat 5 storm; the SVI-inclusive model makes the disparity visible.

As of **May 2026 (TODAY)**, Acapulco residents are still holding events demanding cleanup and reconstruction completion, two and a half years after Otis.

---

## The 1985 Earthquake as Cultural Record Origin Story

The Cultural Record layer needs an origin story — the formative moment that created Mexico's current disaster preparedness culture. That origin is September 19, 1985.

- The government's failure to respond to the Mexico City earthquake (10,000–40,000 deaths) triggered the largest grassroots civic mobilization in Mexican history.
- The Coordinadora Única de Damnificados (CUD) and neighborhood assemblies (Asamblea de Barrios) forced a popular, community-driven reconstruction.
- **SASMEX was born from this failure** — the 1985 earthquake demonstrated that warning time existed between subduction zone rupture and shaking in Mexico City, leading to the creation of the seismic alert system in 1991.
- The September 19 National Civil Simulation (nationwide earthquake drill) is an annual commemoration. When the 2017 earthquake struck Mexico City on September 19 (32nd anniversary), it was initially mistaken for a drill by many residents — a complex and documented degradation of the cultural safety reflex.
- **Formulation stage** (1985–1995): Social earthquake → civic organizations → SASMEX creation.
- **Strengthening stage** (1995–2017): Annual drills, SASMEX expansion, FONDEN development.
- **Operationalizing stage** (2017): September 19 earthquake tests the system; SASMEX performed well for Mexico City but the alert did not reach rural Oaxaca and Chiapas in indigenous languages.
- **Degradation stage** (2021–present): FONDEN eliminated; Bienestar substitution; coverage gaps for indigenous communities remain unaddressed; post-Otis failure exposes structural limits.

---

## Tequio and Gozona: The Resilience Infrastructure That Doesn't Appear in Datasets

- **Tequio** (Zapotec): Communal labor obligation — the mechanism by which community infrastructure is built and maintained collectively without government involvement. After Otis, Zapotec communities in Oaxaca mobilized tequio for immediate home repair and food distribution before any institutional aid arrived.
- **Gozona** (Mixtec): Reciprocal labor exchange — a neighbor works your land today; you work theirs tomorrow. Creates a network of mutual obligation that functions as informal insurance.
- These are not "informal coping mechanisms" — they are institutional systems with centuries of organizational history that standard SVI frameworks do not measure and standard reconstruction programs actively bypass.
- **They appear in the tool** as positive resilience indicators in the Engagement cluster — communities with strong tequio/gozona networks will score higher on adaptive capacity even when they score lower on formal institutional access.

---

## SASMEX Coverage Gaps as SVI Variable

- SASMEX has 96 sensors across Jalisco, Colima, Michoacán, Guerrero, Oaxaca, and Puebla. Guerrero has 18 coastal + 15 interior sensors. Oaxaca has coverage. **Chiapas has partial coverage** — the planned 28-sensor expansion would add western two-thirds of Chiapas, but it's not complete.
- Alerts broadcast in Spanish only. Indigenous-language communities in highland Guerrero, Sierra Sur/Norte Oaxaca, and highland Chiapas receive the alert sound but not the verbal content.
- Alert speakers are installed in urban centers — many rural and highland communities have no speaker infrastructure. The alert exists technically; it does not reach effectively.
- **This is the SEABEA Action cluster variable**: "Communication infrastructure redundancy" — a municipality where SASMEX physically reaches but the content is in a language 60% of residents don't speak as primary language scores differently from one with full functional coverage.

---

## Data Sources

### Tier 1 — Foundation (Priority Pull)

- **INEGI Marco Geoestadístico 2020** — Municipal boundary shapefiles for Guerrero, Oaxaca, Chiapas. Direct download at [https://www.inegi.org.mx/programas/mg/](https://www.inegi.org.mx/programas/mg/). Also Diego Valle's clean 2020 Census shapefiles: [https://blog.diegovalle.net/2022/11/inegi-mexico-2020-census-shapefiles.html](https://blog.diegovalle.net/2022/11/inegi-mexico-2020-census-shapefiles.html)
- **CONEVAL Índice de Rezago Social 2020** — Municipal-level social lag index. Education, health, housing, household assets. Chiapas, Oaxaca, Guerrero are top 3 nationally. Direct download at [https://www.coneval.org.mx/Medicion/IRS/Paginas/Indice_Rezago_Social_2020.aspx](https://www.coneval.org.mx/Medicion/IRS/Paginas/Indice_Rezago_Social_2020.aspx)
- **CONAPO Índice de Marginación Municipal 2020** — Direct `.xls` download: [https://conapo.segob.gob.mx/work/models/CONAPO/Datos_Abiertos/Municipio/IMM_2020.xls](https://conapo.segob.gob.mx/work/models/CONAPO/Datos_Abiertos/Municipio/IMM_2020.xls). Guerrero: #1 very high; Chiapas: #2; Oaxaca: #3.
- **INEGI Censo de Población y Vivienda 2020** — Municipal tables: population, indigenous language speakers (%), housing materials, household assets, disability, single-parent households. Download via [https://www.inegi.org.mx/programas/ccpv/2020/](https://www.inegi.org.mx/programas/ccpv/2020/)

### Tier 2 — Hazard

- **CENAPRED Atlas Nacional de Riesgos** — Multi-hazard indices at municipal level (seismic, cyclone, flood, landslide, volcanic). Portal: [http://www.atlasnacionalderiesgos.gob.mx/](http://www.atlasnacionalderiesgos.gob.mx/). Datos Abiertos: [https://datos.gob.mx/busca/dataset/centro-nacional-de-prevencion-de-desastres](https://datos.gob.mx/busca/dataset/centro-nacional-de-prevencion-de-desastres)
- **NHC HURDAT2** — Western Pacific + Eastern Pacific best-track database. Hurricane Otis (EP18 2023) track and intensity. [https://www.nhc.noaa.gov/data/tcr/EP182023_Otis.pdf](https://www.nhc.noaa.gov/data/tcr/EP182023_Otis.pdf) for the official report; HURDAT2 CSV at nhc.noaa.gov/data/#hurdat
- **SSN (Servicio Sismológico Nacional)** — Seismic catalog for Mexico, epicenter data for Guerrero Gap events. [http://www.ssn.unam.mx/](http://www.ssn.unam.mx/)
- **Guerrero Gap research** — PMC article on slow slip events: [https://pmc.ncbi.nlm.nih.gov/articles/PMC8239025/](https://pmc.ncbi.nlm.nih.gov/articles/PMC8239025/). 2024 tsunami deposit paper: [https://www.nature.com/articles/s43247-024-01364-0](https://www.nature.com/articles/s43247-024-01364-0). Key stats: 5m slip deficit; Mw >8 potential; ~115 years since last major rupture; slow slip events Mw >7.5 every ~4 years.
- **SASMEX sensor coverage** — [http://www.cires.org.mx/sasmex_n.php](http://www.cires.org.mx/sasmex_n.php). Guerrero: 18 coastal + 15 interior sensors. Chiapas: partial coverage only.

### Tier 3 — Tenure, Resilience, Violence

- **RAN (Registro Agrario Nacional)** — Ejido and comunidad indígena boundaries. Access via PHIDA portal. Note: full geometry access is pending a future upgrade; V1 will use municipal-level ejido/comunal coverage as an attribute, not polygon boundary layer.
- **PROCEDE coverage by municipality** — Where ejido land certification has/hasn't happened. Inverse = where informal tenure concentrates.
- **SESNSP homicide rates** — State and municipal homicide statistics. [https://www.gob.mx/sesnsp/](https://www.gob.mx/sesnsp/)
- **ACLED Mexico** — Conflict event locations (armed clashes, organized crime violence, displacement events). [https://acleddata.com/](https://acleddata.com/)
- **DESINVENTAR Mexico** — Historical disaster events database, media-sourced. [https://www.desinventar.net/DesInventar/profiletab.jsp?countrycode=mex](https://www.desinventar.net/DesInventar/profiletab.jsp?countrycode=mex)
- **SIAP (Servicio de Información Agroalimentaria y Pesquera)** — Agricultural production by municipality; crop damage after disasters. Measures livelihood-agriculture dependence.
- **IFT connectivity data** — Internet and mobile coverage maps by municipality. Language-corrected access to SASMEX alerts.
- **CONAPO migration intensity index** — Municipalities with high out-migration = remittance-dependent resilience. High outmigration also = population of older adults, women-headed households, children left behind.
- **Remittance GDP share by state** — Chiapas: 14.6% of GDP; Guerrero: 14.0% (2024 data from Banxico via UnoTV/La Jornada).
- **IBERO/PDH forced displacement reports** — Annual displacement data by state and cause. 2024 report: [https://ibero.mx/prensa/crimen-organizado-dispara-desplazamiento-interno-en-mexico-casi-29-mil-personas-en-2024-pdh-ibero](https://ibero.mx/prensa/crimen-organizado-dispara-desplazamiento-interno-en-mexico-casi-29-mil-personas-en-2024-pdh-ibero)

### Tier 4 — Validation / Cross-Cut

- **GRDI (Global Gridded Relative Deprivation Index v1)** — 1km resolution raster; can be zonal-averaged to municipality boundaries as independent validation of CONEVAL/CONAPO scores. From NASA SEDAC: [https://sedac.ciesin.columbia.edu/data/set/povmap-grdi-v1](https://sedac.ciesin.columbia.edu/data/set/povmap-grdi-v1)
- **World Bank Climate Change Knowledge Portal** — Country/subnational climate exposure data. [https://climateknowledgeportal.worldbank.org/country/mexico](https://climateknowledgeportal.worldbank.org/country/mexico)
- **HeiGIT Risk Assessment Dataset** — Heidelberg Institute for Geoinformation Technology; multi-hazard risk at sub-national level. From Lakshman Srikanth's Notion hub.

---

## Nine SVI Cluster Architecture

**Architecture decision:** Single composite SVI score on the choropleth map (enabling the physical vs. SVI-inclusive comparison toggle, same as PR tool), with all nine clusters shown as sub-dimensions in the municipality detail panel. Composite uses weighted mean with Mexico-specific weights upweighting Tenure and Violence clusters.

### The Nine Clusters (Spanish labels for the tool)

1. **Social / Capital Social** — Poverty concentration (CONEVAL rezago), elderly population share, disability prevalence, single-parent household rate, household density, child-to-adult ratio, past disaster experience, community connection/attachment. *Weight: upweighted vs. standard SEABEA due to extreme baseline marginalization.*

2. **Ecology / Entorno Natural** — Coastal flood exposure, floodplain position, slope instability / landslide susceptibility (MGB equivalent = CENAPRED geohazard), deforestation rate (mangrove/forest loss accelerates flood risk), proximity to volcanic/seismic hazard zones.

3. **Built Environment / Entorno Construido** — Housing materials (adobe, wood, lámina vs. concrete), road network redundancy, bridge condition, healthcare facility distance, school distance, critical infrastructure elevation above flood line.

4. **Agricultural/Livelihoods / Medios de Vida Agrícolas** — Agricultural dependence (SIAP crop value share of municipal income), crop type vulnerability to specific hazards (corn susceptible to ashfall; coffee to landslide), FONDEN/Bienestar disaster payment history, crop insurance access.

5. **Engagement / Participación Comunitaria** — Civic organization density (tequio/gozona documented presence, ejido assembly activity, religious organization networks), prior disaster aid uptake and denial patterns, trust in institutions (Bienestar enrollment rates as proxy), electoral turnout, indigenous governance structures (usos y costumbres municipalities).

6. **Action / Capacidad Adaptativa** — SASMEX signal reach (sensor coverage) AND functional reach (Spanish-only alert in indigenous-majority municipality = reduced score), mobile connectivity (IFT), healthcare access during disruption, disaster plan existence at municipal level, prior evacuation compliance.

7. **Tenure / Tenencia de la Tierra** *(New vs. PR tool)* — Ejido vs. comunidad indígena vs. urban informal settlement classification; PROCEDE coverage rate (inverse = informal tenure concentration); post-disaster housing aid eligibility (proxy: how many households hold individual documentation); LRA equivalent = RAN titling density.

8. **Violence/Displacement / Violencia y Desplazamiento** *(New vs. PR tool)* — SESNSP homicide rate; ACLED organized crime event density; IBERO/PDH forced displacement events; cartel territorial control presence (ACLED). Captures the way violence pre-destroys the documentation and social infrastructure that disaster response requires.

9. **Cultural Record / Memoria Cultural** — Community organizations with documented disaster history; cultural practices that encode hazard knowledge (analogous to Simeulue smong, Japan namazu-e); where the community sits in the Formulation → Strengthening → Operationalizing → Degradation cycle; presence/absence of 1985 earthquake memory organizations; indigenous governance continuity post-disaster.

### Composite Weight Rationale

| Cluster | Proposed Weight | Rationale |
|---|---|---|
| Social / Capital Social | 0.15 | Extreme baseline scores; high analytical signal |
| Ecology / Entorno Natural | 0.10 | Feeds into physical hazard layer; SVI layer captures sensitivity |
| Built Environment / Construido | 0.15 | High variance across municipalities; reconstruction target |
| Agricultural / Medios de Vida | 0.10 | Critical for rural majority; crop loss is first-wave impact |
| Engagement / Participación | 0.10 | Tequio/gozona upweight; institutional trust data quality varies |
| Action / Capacidad Adaptativa | 0.10 | SASMEX + connectivity data available; good signal |
| Tenure / Tenencia | 0.15 | Core new dimension; most invisible to standard frameworks |
| Violence/Displacement | 0.10 | Measurable but partially correlated with Social cluster |
| Cultural Record | 0.05 | Qualitative; important framing but weaker quantitative proxy |
| **TOTAL** | **1.00** | |

---

## Story Layer Architecture

The Mexico tool has a richer documented story base than either the PR or Philippines tools, enabling a more sophisticated story design. Two registers are used, both clearly labeled in the UI.

### The 1985 → 2017 → 2023 Structural Failure Arc

The same government failure mode plays out across three events, forty years, and two geographies. This is the core Cultural Record argument — not three separate disasters, but one mechanism cycling without resolution.

| Stage | 1985 CDMX | 2023 Otis / Guerrero |
|---|---|---|
| Initial failure | Government non-response; civic mobilization fills gap | Aid bypasses communal and rural lands entirely |
| Civic response | CUD, damnificados movement, neighborhood assemblies | CECOP, Oxfam México, Tlachinollan, civil society coalition |
| Promise made | Permanent housing for all displaced | "Recovered by March 2024" (AMLO) |
| Promise broken | Reuters 2017: hundreds of damnificados still homeless 32 years later | La Jornada May 2026: residents still demanding cleanup and reconstruction |
| Corruption layer | Post-1985 building codes not enforced; buildings with filed violations collapse in 2017 (The Guardian) | Census irregularities; Bienestar assistance resold; irregular titling |
| Official narrative | "Great response" to 2017 earthquake | AMLO: homes "now better than before" |
| Memory capture | Monument commissioned (60M pesos); victims demand investigation instead (Al Día) | — (too recent for memorialization) |

The 2017 earthquake struck on **September 19** — the exact anniversary of 1985, the date of the annual national simulation drill. Some residents didn't respond immediately because they assumed it was the drill. The cultural safety reflex — the direct product of the 1985 Formulation stage — had degraded into noise. Social media became the real information system, with documented fact/fiction chaos (PS Mag).

### Hilos Documentados (Documented Threads)

Four story threads that run as continuous narratives across events, accessible from a "Historias" toggle layer. Each is geo-referenced to the tool's map where possible.

**Hilo 1: El ciclo que no se rompe**
*The cycle that doesn't break.*
The structural failure mode across 1985 → 2017 → 2023. Documented via Reuters (damnificados still homeless in 2017), La Jornada May 2026 (Otis victims still demanding reconstruction), CECOP statements. Not the same people — the same mechanism. This is the anchor thread for the entire tool.
*Sources: Reuters 2017 (idUSKCN1BX2HJ); La Jornada 2026-05-13; CECOP/La Jornada 2024-05-01*

**Hilo 2: El edificio que no debería haber caído**
*The building that should not have fallen.*
Post-1985 Mexico enacted new building codes. In 2017, buildings with formally filed construction violation complaints still collapsed — because enforcement was the gap between the code and reality. The Guardian documented this directly. The Acapulco parallel: CONAVI/Bienestar-funded post-Otis housing already documented as substandard by NGOs.
*Sources: The Guardian 2017-10-13; Al Día News 2018 (memorial controversy); Build Change / Shelter Cluster post-Otis documentation*

**Hilo 3: El simulacro que fue real**
*The drill that was real.*
September 19, 2017. SASMEX fires. The annual earthquake commemoration drill happens every September 19 — the 1985 anniversary. Residents conditioned to the drill date didn't immediately respond to the real event. Social media flooded with fact and fiction simultaneously (PS Mag). This is the Formulation → Degradation cycle in a single morning.
*Sources: PS Mag social media article; LA Times 2018 one-year anniversary; thesis Chapter IV "Quick to Forget"*

**Hilo 4: Los que nunca llegaron**
*Those who never arrived.*
Cacahuatepec, October–November 2023. CECOP's Marco Antonio Suástegui: "it is all backwards — first the rich." 36 communities. 10,000 hectares of corn. Zero official aid. Civil society (Oxfam, Tlachinollan, Isla Urbana, Cooperación Comunitaria) delivers 300+ tons of corn and 8,000 food packages before any federal program reaches them. This is the geo-anchored story for coastal Guerrero.
*Sources: La Jornada 2024-05-01; El Sur Acapulco; Animal Político Río Papagayo*

### Retratos Compuestos (Composite Portraits)

For municipalities without a documented specific case, the detail panel generates a composite portrait drawn transparently from that municipality's SVI cluster scores. Clearly labeled: *"Este retrato es compuesto — construido a partir de los datos de este municipio y de patrones documentados en comunidades similares."* Everything in the portrait is grounded in real patterns; no detail is invented. The portrait adapts based on which clusters score highest: a municipality in the top quintile on Tenure + Violence + Social generates a different portrait than one dominated by Ecology + Agricultural risk.

---

## Key Human Stories to Develop

1. **The Cacahuatepec corn farmer** — 36 communities, 10,000 hectares destroyed, zero official aid. CECOP's Marco Antonio Suástegui documented: "It is incredible now that governments that call themselves leftist have said that first the poor — it is all backwards, first the rich." Civil society filled the gap. Six months after Otis, rural Acapulco faces a food crisis because crops weren't replanted in time. This is the anchor exclusion story.

2. **The three Acapulcos** — Tourist zone vs. colonia popular vs. rural communal land. Physical hazard model: all three exposed equally. SVI-inclusive: dramatically different outcomes. Ciudad Renacimiento not in the reconstruction plan. As of May 2026, residents still claiming abandonment. The gap between AMLO's "recovered by March 2024" and ground reality.

3. **The Guerrero Gap** — The earthquake that hasn't happened yet. 5-meter slip deficit. Mw >8 potential. Slow slip events every 4 years (invisible seismicity that may or may not be releasing pressure or loading the next rupture). If it ruptures while the Guerrero coast is still in Otis recovery mode, the compound effect would be catastrophic. This is the compound hazard story — the same analytical move as Typhoon Durian triggering lahars from Mayon.

4. **SASMEX in a Zapotec village** — The alert sounds. The siren goes off. The recorded message plays in Spanish. In a village where 80% of residents speak Zapotec as their primary language. 60 seconds of warning, in a language they didn't grow up speaking, for a hazard that hasn't struck in living memory. This is the "Action/Adaptive Capacity" story — a technically sophisticated early warning system that doesn't reach the most at-risk communities effectively.

5. **The tequio that arrived before the government** — In Oaxacan communities after Otis (and the 2017 Chiapas earthquake), tequio and mutual aid networks mobilized before any institutional response. Cooperación Comunitaria, Tlachinollan, Isla Urbana operating in communities the government didn't census. This is the Engagement cluster story — dense informal networks as positive resilience infrastructure that organizations miss because it's not on any official list.

6. **The 1985 origin and the 2017 echo** — SASMEX was born from 1985. The September 19 drill was born from 1985. In 2017, the earthquake struck on September 19. Some residents heard the earthquake and thought it was the annual drill. The cultural safety reflex — the formulation stage product — had begun to degrade into noise. This is the Formulation → Degradation cycle made concrete.

---

## Tool Architecture Decisions (Agreed)

**Evolving from PR, not replicating it.** Key changes:

1. **Multi-hazard toggle** — Three switchable hazard layers: Seismic/Guerrero Gap (subduction zone + historical epicenters), Hurricane/Cyclone (HURDAT2 tracks + Otis track specifically), Compound Flood/Landslide (CENAPRED geohazard maps). PR was hurricane-centric; this needs all three.

2. **Tenure layer** — New layer entirely. Shows: ejido vs. comunidad indígena vs. urban informal classification; PROCEDE coverage gaps; Bienestar census registration rates (inverse exclusion proxy); RAN boundary placeholder clearly labeled as "future upgrade."

3. **Violence/Displacement layer** — New layer entirely (absent from both PR and Philippines tools). Maps SESNSP homicide rates, ACLED conflict event density, and IBERO forced displacement counts by municipality. Framed as: "vulnerability pre-loading" — how violence destroys the documentation and social infrastructure disaster response depends on.

4. **Cultural Record layer** — Uses Daniel's thesis framework (Formulation → Strengthening → Operationalizing → Degradation) as spine. 1985 earthquake as origin anchor; 2017 as inflection point; 2023 Otis as current state.

5. **Language:** Spanish throughout the tool. Planning documents in English.

6. **Geographic unit:** Municipality level, Phase 1 (~80 municipalities across the three states). Phase 2: higher-resolution barangay-equivalent (AGEB/localidad) for coastal Guerrero/Acapulco.

7. **Comparison toggle** (inherited from PR tool): Physical hazard score vs. SVI-inclusive score, same choropleth, same scale. This is the core mechanic that shows the disparity. The "Tres Acapulcos" story becomes visible through this toggle.

8. **Output folder:** `/Users/danielstarosta/Desktop/claude projects/svi-mex/`

---

## Parallel Projects

- **Puerto Rico SVI Tool** — Complete `index.html`. Architecture reference. Dark theme CSS variables: `--bg:#080C18`, `--surface:#0F1628`, `--cyan:#00D4FF`, `--green:#00E096`, `--yellow:#FFD93D`, `--orange:#FF6B35`, `--red:#FF2D55`. Grid: `#app{display:grid;grid-template-rows:38px 1fr;grid-template-columns:52px 0px 1fr}`.
- **Philippines/Albay SVI Tool** — In planning. See `svi-PR/philippines_albay_briefing.md`. Multi-hazard (volcanic + typhoon + lahar), tenure layer (PDZ), reconstruction record layer.

---

## About the Notion Hub

Lakshman Srikanth (Deltares senior advisor) maintains a living disaster risk intelligence archive at the shared Notion link. Items of particular relevance to this project:

- **Global Gridded Relative Deprivation Index** — 1km raster, can validate CONEVAL/CONAPO scores
- **HeiGIT risk assessment dataset** — Heidelberg Institute; sub-national multi-hazard risk
- **"Disaster authoritarianism: how autocratic regimes deal with earthquakes"** — directly relevant to Mexico's 1985–2017–2023 institutional trajectory
- **"Early warning systems: Bridging tech and tradition to protect communities"** — directly relevant to SASMEX/indigenous language gap
- **"A Lesson in Vulnerability: How Nevado del Ruiz Changed Risk Disaster Management"** — volcano + community warning parallel to Guerrero Gap scenario
- **PDNA (Post Disaster Needs Assessment) repository** — sector-specific survey questionnaires; useful for Reconstruction Record layer methodology

---

## Key Sources

- [NHC Tropical Cyclone Report — Hurricane Otis](https://www.nhc.noaa.gov/data/tcr/EP182023_Otis.pdf)
- [La Jornada — Sin ayuda oficial, 36 comunidades rurales de Acapulco afectadas por Otis](https://www.jornada.com.mx/noticia/2024/05/01/estados/sin-ayuda-oficial-36-comunidades-rurales-de-acapulco-afectadas-por-2018otis2019-8515)
- [La Jornada — Exigen comunidades indígenas y afros reconstrucción de 26 mil viviendas](https://www.jornada.com.mx/noticia/2025/07/15/estados/exigen-comunidades-indigenas-y-afros-de-guerrero-reconstruccion-de-26-mil-viviendas)
- [La Jornada — Acapulco: Afectados por Otis reclaman abandono, a tres años aún falta limpieza y obras](https://www.jornada.com.mx/noticia/2026/05/13/estados/acapulco-afectados-por-otis-reclaman-abandono-de-autoridades-falta-limpieza-y-obras) *(May 2026 — live story)*
- [Animal Político — Reconstrucción de Acapulco tras huracanes: todo al turismo y excluye a los más pobres](https://www.animalpolitico.com/estados/reconstruccion-acapulco-huracanes-turismo-pobres)
- [El Universal — "Hay tres Acapulcos; el de la miseria está aquí"](https://www.eluniversal.com.mx/estados/hay-tres-acapulcos-el-de-la-miseria-esta-aqui/)
- [IBERO — Crimen Organizado Dispara Desplazamiento Interno: 29,000 personas en 2024](https://ibero.mx/prensa/crimen-organizado-dispara-desplazamiento-interno-en-mexico-casi-29-mil-personas-en-2024-pdh-ibero)
- [UnoTV — Chiapas y Guerrero, los estados más dependientes de remesas 2024](https://www.unotv.com/nacional/chiapas-y-guerrero-los-estados-mas-dependientes-de-las-remesas-de-los-migrantes-durante-2024/)
- [Nature Communications — Shallow slow earthquakes to decipher future catastrophic earthquakes in the Guerrero seismic gap](https://www.nature.com/articles/s41467-021-24210-9)
- [Nature / Communications Earth & Environment — Tsunami deposits highlight high-magnitude earthquake potential in the Guerrero seismic gap (2024)](https://www.nature.com/articles/s43247-024-01364-0)
- [PMC — Social and seismic structural vulnerability in Zihuatanejo, Guerrero (2024)](https://link.springer.com/article/10.1007/s11069-023-06385-0)
- [CEPAL — Socioeconomic vulnerability to natural disasters in Mexico: rural areas](https://repositorio.cepal.org/server/api/core/bitstreams/c0c127ff-e5ee-461a-8209-91ac4143c698/content)
- [Scielo — Resiliencia de municipios costeros del Pacífico mexicano ante desastres socionaturales](https://www.scielo.org.mx/scielo.php?script=sci_arttext&pid=S1405-84212021000100205)
- [P2P Foundation — Tequio](https://wiki.p2pfoundation.net/Tequio)
- [Global Voices — 1985 earthquake and the awakening of Mexican civil society](https://globalvoices.org/2015/10/15/a-devastating-earthquake-in-1985-gave-rise-to-an-awakening-in-mexican-society/)
- [Dartmouth — 1985: The Earth Shook, the Government Failed, Mexicans Took Action](https://course-exhibits.library.dartmouth.edu/s/modernmexico/page/reyes)
- [CONAPO Marginalization Index 2020 — Direct XLS download](https://conapo.segob.gob.mx/work/models/CONAPO/Datos_Abiertos/Municipio/IMM_2020.xls)
- [NASA SEDAC — GRDI Global Gridded Relative Deprivation Index v1](https://sedac.ciesin.columbia.edu/data/set/povmap-grdi-v1)
- [DesInventar Mexico historical disasters database](https://www.desinventar.net/DesInventar/profiletab.jsp?countrycode=mex)
- [SASMEX — CIRES official site](http://www.cires.org.mx/sasmex_n.php)
- [It's Going Down — Hurricane Otis, Mutual Aid, and the Multiple Disasters in Guerrero](https://itsgoingdown.org/hurricane-otis-mutual-aid-and-the-multiple-disasters-in-guerrero/)
- [Reuters — Thirty-two years after quake, angry Mexicans still wait for homes (2017)](https://www.reuters.com/article/business/environment/thirty-two-years-after-quake-angry-mexicans-still-wait-for-homes-idUSKCN1BX2HJ/) *(Hilo 1 primary source)*
- [The Guardian — Complaints, earthquake scandal: Mexico City buildings that shouldn't have fallen (2017)](https://www.theguardian.com/cities/2017/oct/13/complaints-earthquake-scandal-mexico-city-dead-construction-collapse) *(Hilo 2 primary source)*
- [Al Día News — Memorial for Mexico City earthquake victims sparks controversy (2018)](https://aldianews.com/en/culture/heritage-and-history/limits-remembrance) *(Hilo 2: monument vs. investigation)*
- [PS Mag — How Mexico City residents used social media to debunk fact from fiction (2017)](https://psmag.com/social-justice/how-mexico-city-residents-used-social-media-to-debunk-fact-from-fiction/) *(Hilo 3: September 19 drill/real confusion)*
- [LA Times — Mexico earthquake: One year anniversary (2018)](https://www.latimes.com/world/mexico-americas/la-fg-mexico-earthquake-20180912-story.html) *(Hilo 3 context)*
- [LA Times — 30th anniversary of 1985 earthquake (2015)](https://www.latimes.com/world/mexico-americas/la-fg-mexico-quake-anniversary-20151005-story.html) *(Cultural memory arc)*
- [Disaster risk intelligence hub — Lakshman Srikanth / Deltares (Notion)](https://rain-cost-4dc.notion.site/1f032c74a0e68064a877fc01ac4ec0ed)

---

*Project briefing by Daniel Starosta. Methodology draws on Daniel's UC Berkeley thesis (2022/2023), the ATSDR Social Vulnerability Index, the SEABEA framework, and the INFORM Risk Framework (EC Joint Research Centre).*
