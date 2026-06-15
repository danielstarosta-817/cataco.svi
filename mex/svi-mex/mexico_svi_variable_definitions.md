# Mexico SVI — Variable Definitions and Scoring Rubric
*Nine clusters → one composite SVI score (choropleth) + nine sub-scores (detail panel)*
*All variable names in Spanish as they will appear in the tool.*

---

## How Scoring Works

Each variable is scored **0.0 – 1.0** where:
- **1.0** = highest vulnerability / lowest resilience on this dimension
- **0.0** = lowest vulnerability / highest resilience

Variables within a cluster are averaged to produce the cluster score. Cluster scores are combined using the weights in the briefing document to produce the composite SVI score. The composite is then displayed against the physical hazard score on the comparison toggle.

Where a variable has a **+/– adjustment**, it modifies the cluster score after averaging (e.g., cultural heritage at risk adds +0.1; documented tequio network subtracts –0.1).

**Data vintage:** INEGI 2020 Census and CONEVAL/CONAPO 2020 indices are the primary baselines. More recent event-level data (SESNSP homicide 2023, ACLED 2024, DESINVENTAR through 2023) overlaid where available.

---

## Cluster 1: Capital Social (Social)
*Weight in composite: 0.15*

**What this cluster captures:** Who has the fewest material and social resources to absorb a shock and mount their own recovery — independent of what the hazard does physically.

| Variable (Spanish) | Variable (English) | Data Source | Scoring Logic | 1.0 looks like | 0.0 looks like |
|---|---|---|---|---|---|
| Concentración de pobreza | Poverty concentration | CONEVAL Rezago Social 2020 / CONAPO Marginación 2020 | Normalized CONEVAL social lag index score | Cochoapa el Grande (Guerrero), Chalchihuitán (Chiapas) | Municipal centers with diversified income base |
| Proporción de adultos mayores | Elderly population share | INEGI Censo 2020, % 65+ | % population 65+, normalized against state range | >20% elderly, no home health infrastructure | <8% elderly |
| Prevalencia de discapacidad | Disability prevalence | INEGI Censo 2020 | % population with at least one disability | >15% | <5% |
| Hogares con jefatura femenina sola | Single female-headed households | INEGI Censo 2020 | % households headed by woman with no spouse/partner | >40% | <15% |
| Aislamiento lingüístico | Linguistic institutional exclusion | INEGI Censo 2020, % speaks indigenous language as primary; cross-referenced with SASMEX alert language (Spanish-only) | % speaking indigenous language as primary × (1 – official bilingual service coverage proxy) | Municipality >80% indigenous-language primary; zero bilingual government services | Spanish-dominant municipality with full institutional access |
| Densidad del hogar | Household crowding | INEGI Censo 2020, avg. occupants per room | Avg. occupants per room, normalized | >3 occupants/room | <1 occupant/room |
| Experiencia de desastre previo | Prior disaster experience | DESINVENTAR historical events + INEGI Encuesta Nacional de Seguridad Pública | Inverse: municipalities with documented prior disaster *and* organized community response score lower (resilience) | No recorded prior disasters; no preparedness culture | Multiple documented events; community-organized response on record |
| Conexión y apego al lugar | Connection and attachment to place | Proxy: % born in municipality (INEGI Censo 2020, inmigración) + ejido/comunal land tenure share | High attachment = lower vulnerability score (more likely to stay, rebuild, organize) — **this is a resilience variable** | Low attachment (high migration, transient population, no communal land) | High attachment, multigenerational community, communal governance |

*Cluster adjustment: If municipality has documented presence of indigenous autonomous governance (municipio de usos y costumbres, INEGI catalog), apply –0.05 to cluster score.*

---

## Cluster 2: Entorno Natural (Ecology / Hydrology)
*Weight in composite: 0.10*

**What this cluster captures:** The physical-ecological conditions that amplify or buffer hazard impacts — not the hazard itself (that's the separate physical score), but how the landscape transmits it.

| Variable (Spanish) | Variable (English) | Data Source | Scoring Logic | 1.0 looks like | 0.0 looks like |
|---|---|---|---|---|---|
| Exposición costera e inundación | Coastal and flood exposure | CENAPRED Atlas Nacional de Riesgos — índice de peligro por ciclones + inundación | Normalized CENAPRED flood/cyclone hazard index | Coastal Guerrero below 10m elevation; river delta municipalities | Inland highland municipalities above 1,500m |
| Susceptibilidad a deslizamientos | Landslide susceptibility | CENAPRED Atlas — índice de peligro por deslizamiento | Normalized score | Steep deforested slopes, high rainfall, unconsolidated soils (Sierra Sur Oaxaca, highland Chiapas) | Low-slope, consolidated geology |
| Pérdida de cobertura vegetal | Vegetation/forest cover loss | Hansen Global Forest Change (available via GEE) or CONAFOR SEMARNAT deforestation maps | % forest loss 2000–2020, normalized | >40% forest loss in 20 years | Stable or increasing cover |
| Degradación de manglar o barrera natural | Mangrove / natural buffer degradation | CONABIO mangrove coverage maps | % mangrove loss if coastal municipality; 0 for inland | Coastal municipality with >50% mangrove loss | Intact mangrove coverage |
| Zona de cuenca alta con alta escorrentía | Upstream watershed / runoff risk | CENAPRED or CONAGUA watershed classification | High upstream catchment population above = higher lahar/flood amplification risk | Dense upstream settlement on steep watershed | Low upstream settlement, natural absorption capacity |

---

## Cluster 3: Entorno Construido (Built Environment)
*Weight in composite: 0.15*

**What this cluster captures:** The physical infrastructure that collapses first and takes longest to rebuild. Also: whether the reconstruction record shows patterns of cutting corners.

| Variable (Spanish) | Variable (English) | Data Source | Scoring Logic | 1.0 looks like | 0.0 looks like |
|---|---|---|---|---|---|
| Calidad de materiales de vivienda | Housing material quality | INEGI Censo 2020 — % viviendas con piso de tierra, paredes de material no duradero, techo de lámina/palma | Weighted index: floor material (20%) + wall material (40%) + roof material (40%) | >60% non-durable materials; earthen floors predominant | <10% non-durable; reinforced concrete construction |
| Acceso a agua y saneamiento | Water and sanitation access | INEGI Censo 2020 — % sin agua entubada, % sin drenaje | Average of % without piped water + % without drainage | >50% lacking both | Full infrastructure coverage |
| Red vial y redundancia | Road network redundancy | INEGI Red Nacional de Caminos; count of road types (federal/state/rural) per municipality; bridge conditions | Municipal accessibility index: single-road-access municipalities score highest | Single unpaved access road; no alternate routes; bridges not rated | Multiple paved routes; no single points of failure |
| Distancia a centro de salud | Healthcare facility distance | Secretaría de Salud CLUES database — nearest IMSS/ISSSTE/SSA facility by road distance | Average road-distance to nearest tier-2 health facility, normalized | >2 hrs road travel to nearest hospital | <30 min to hospital |
| Distancia a escuela primaria | Primary school distance | SEP / DepEd equivalent — school location database | Average road distance, normalized | >1 hr travel to nearest primary school | School within community |
| Infraestructura energética | Energy infrastructure fragility | CFE outage history + INEGI % viviendas sin electricidad | % without electricity + inverse of CFE grid reliability score for zone | >20% no electricity; frequent outages | Full coverage; resilient grid |
| Antecedentes de construcción irregular | Record of irregular construction | DESINVENTAR collapse records + CECOP / NGO post-event documentation | Binary/graded: documented cases of building collapse attributed to substandard construction = higher score | Post-Otis structures with documented defects; pre-2017 buildings with filed complaints | No documented irregular construction |

---

## Cluster 4: Medios de Vida Agrícolas (Agricultural / Livelihoods)
*Weight in composite: 0.10*

**What this cluster captures:** When the disaster destroys both home and livelihood simultaneously, the recovery calculus changes entirely. Communities whose economic base is corn milpa, coffee, or coastal fishing face a fundamentally different timeline than those with diversified income.

| Variable (Spanish) | Variable (English) | Data Source | Scoring Logic | 1.0 looks like | 0.0 looks like |
|---|---|---|---|---|---|
| Dependencia agrícola | Agricultural income dependence | SIAP / INEGI Censo Económico — % employed in primary sector | % municipal workforce in agriculture/fishing/forestry | >70% agricultural dependency | <20%; diversified economy |
| Vulnerabilidad del cultivo principal | Principal crop hazard vulnerability | SIAP crop maps × CENAPRED hazard overlap | Crop type × primary hazard alignment: corn + cyclone/flood = high; coffee + landslide = high; diversified = low | Monoculture corn in cyclone corridor (Cacahuatepec) | Diversified or non-weather-dependent crops |
| Pérdidas agrícolas documentadas | Documented agricultural losses | SIAP / SAGARPA disaster loss reports + DESINVENTAR | Total documented crop losses as % of municipal agricultural value, most recent 10 years | Repeated total-loss events (Cacahuatepec post-Otis: 10,000 ha corn) | No documented significant losses |
| Acceso a seguro agrícola | Agricultural insurance access | AGROASEMEX / FONDEN replacement programs — municipal enrollment data | % of agricultural households with crop insurance coverage | <5% insured | >60% insured |
| Diversificación de ingresos | Income diversification | INEGI ENIGH / Censo: % households with non-agricultural income source | % with at least one non-agricultural income stream | Single-income agricultural household | Multiple income streams |
| Dependencia de remesas | Remittance dependence | Banxico / CONAPO remittance intensity by municipality | **Dual-scored:** High remittance = resilience asset (positive buffer) AND risk factor (absent working-age population, female-headed households, elderly care burden) — shown as two sub-indicators | >25% household income from remittances | <5% remittance income |

*Note on remittances: Guerrero (14% of state GDP) and Chiapas (14.6%) are the most remittance-dependent states nationally. High remittance score is flagged in the detail panel with both its resilience value (cash buffer, financial linkage) and its vulnerability dimension (absent working-age adults, eldercare burden).*

---

## Cluster 5: Participación Comunitaria (Engagement)
*Weight in composite: 0.10*

**What this cluster captures:** The density and quality of community organization — the infrastructure that activates when formal systems fail. Tequio, gozona, ejido assemblies, religious networks, mutual aid history. This is the cluster that most directly reverses the standard aid-distribution assumption.

| Variable (Spanish) | Variable (English) | Data Source | Scoring Logic | 1.0 looks like | 0.0 looks like |
|---|---|---|---|---|---|
| Redes de ayuda mutua documentadas | Documented mutual aid networks | NGO/academic documentation of tequio, gozona, comités de vecinos; CECOP presence; Red Cross chapter coverage | Qualitative to graded: documented active network = lower vulnerability | No documented networks; aid-dependent | Active tequio/gozona documented in post-disaster record; CECOP or equivalent present |
| Gobernanza indígena autónoma | Indigenous autonomous governance | INEGI catalog of municipios con sistemas normativos indígenas (usos y costumbres) | Binary: usos y costumbres municipality = strong governance asset (resilience) | No autonomous governance; fully dependent on state/federal programs | Active indigenous governance with documented disaster-response role |
| Historial de ayuda post-desastre | Prior aid uptake and denial patterns | FONDEN disbursement records (FOI) + Bienestar enrollment data + CECOP / NGO documentation | % of disaster-eligible households that successfully accessed formal aid after previous events; inverse = institutional exclusion rate | <20% successful aid access in prior events | >80% successful access; familiar with application processes |
| Confianza institucional | Institutional trust | Proxy: voter turnout (INE), Bienestar enrollment rate relative to estimated eligible population, local DRRM plan existence | Low trust = low enrollment relative to eligibility; low turnout; no local plan | <40% Bienestar enrollment of estimated eligible; low turnout | High enrollment; strong local DRRM plan; high civic participation |
| Densidad organizacional | Organizational density | INEGI Directorio Estadístico Nacional de Unidades Económicas (DENUE) — civil society, religious, cooperative organizations per 1,000 residents | Organizations/1,000 residents, normalized | <1 org/1,000 residents | >10 orgs/1,000 residents |
| Participación de mujeres | Women's participation | Proxy: % female-headed ejido parcels (RAN) + % women in municipal government (INE) + documented women's organizations | Low female civic participation = higher vulnerability (women disproportionately carry disaster burden and disproportionately excluded from aid) | <5% female ejido parcel holders; no women in municipal government | >30% female civic leadership; documented women's disaster networks |

---

## Cluster 6: Capacidad Adaptativa (Action)
*Weight in composite: 0.10*

**What this cluster captures:** Whether households and communities can *act* on information and warnings when they receive them. Distinguishes communities that receive the SASMEX alert from those that can functionally respond to it.

| Variable (Spanish) | Variable (English) | Data Source | Scoring Logic | 1.0 looks like | 0.0 looks like |
|---|---|---|---|---|---|
| Cobertura física de SASMEX | SASMEX physical sensor coverage | CIRES SASMEX sensor map | Binary/graded: in coverage zone = 0; partial/no coverage = 1 | Chiapas eastern zone; no sensor within 150km | Guerrero coast; full sensor density |
| Efectividad funcional de alerta | Functional alert effectiveness | INEGI Censo 2020 % indigenous-language primary × Spanish-only SASMEX audio content | % population for whom alert audio is not in primary language | >80% indigenous-language primary, no translated alert | Spanish-dominant municipality with full alert comprehension |
| Cobertura de telefonía móvil | Mobile phone coverage | IFT connectivity maps | % of municipal territory with 4G coverage | <20% coverage | >90% coverage |
| Acceso a internet | Internet access | INEGI Censo 2020 — % viviendas con internet | % without internet, normalized | >90% without internet | <10% without internet |
| Plan municipal de DRRM | Municipal DRRM plan existence | CENAPRED / SEGOB municipal plan registry | Binary: no plan = 1; plan exists but >5 years old = 0.5; current plan = 0 | No plan; no civil protection officer | Current plan; dedicated PC officer; regular drills |
| Simulacros documentados | Documented evacuation drills | CENAPRED Simulacro Nacional participation records + media | Inverse of participation rate in national drills | No documented participation in national drills | Regular participation; community-initiated drills |
| Seguro de vivienda | Housing insurance coverage | Proxy: CONAVI / INFONAVIT mortgage penetration + private insurance | % households with any property insurance | <2% insured | >50% insured |

*Note: The "drill confusion" documented on September 19, 2017 is the behavioral prediction story for this cluster — municipalities that score high on this cluster (low adaptive capacity) face exactly this failure mode when the drill and the real event overlap.*

---

## Cluster 7: Tenencia de la Tierra (Tenure)
*Weight in composite: 0.15*
*New vs. PR tool. This cluster has no equivalent in standard SVI frameworks.*

**What this cluster captures:** Whether residents have legal documentation sufficient to access post-disaster housing programs, reconstruction credit, and agricultural support. The absence of this documentation is not about poverty — it is about land classification and legal regime.

| Variable (Spanish) | Variable (English) | Data Source | Scoring Logic | 1.0 looks like | 0.0 looks like |
|---|---|---|---|---|---|
| Régimen ejidal o comunal | Ejido / comunal land regime | RAN (Registro Agrario Nacional) — % municipal territory in ejido or comunidad indígena | % territory under collective tenure | >90% communal/ejidal; zero individual titles | >80% private titled land |
| Cobertura de PROCEDE | PROCEDE certificate coverage | RAN PROCEDE dataset — % ejido parcels with individual certificate issued | % ejidatarios with PROCEDE certificate (fallback documentation) | <20% PROCEDE coverage; comunidad indígena (no individual certs possible) | >80% PROCEDE coverage |
| Tenencia urbana informal | Urban informal tenure | INEGI ITER — % viviendas en asentamientos irregulares (proxy: % on ejido land in urban areas); CONARETT / SEDATU data | % urban households without individual property title | >50% informal urban tenure (colonias populares) | Full formal titling |
| Elegibilidad para programas de reconstrucción | Reconstruction program eligibility | Bienestar Padrón / CONAVI housing program participation + proxy: % population with CURP + RFC | % of estimated disaster-affected households that hold qualifying documentation for CONAVI / Bienestar housing aid | <30% eligible based on documentation | >90% eligible |
| Acceso a crédito hipotecario | Mortgage / reconstruction credit access | INFONAVIT / SHF municipal coverage | % employed population with INFONAVIT affiliation (formal employment = access) | <10% INFONAVIT affiliation; informal economy dominant | >60% affiliation |
| Historial de desalojo post-desastre | Post-disaster eviction / displacement record | CECOP / HIC-AL / CDHM documentation + DESINVENTAR | Documented cases of post-disaster land dispossession or failure to return resettled communities | Documented cases (CECOP Cacahuatepec; post-Otis RU evictions) | No documented cases |

*Note: Comunidad indígena (bienes comunales) members score maximum on this cluster by design — they hold no individual document that satisfies federal reconstruction requirements. This is the most structurally excluded tenure category in the corridor.*

---

## Cluster 8: Violencia y Desplazamiento (Violence / Displacement)
*Weight in composite: 0.10*
*New vs. both PR and Philippines tools. Absent from standard SVI frameworks.*

**What this cluster captures:** How organized crime violence and forced displacement pre-destroy the documentation, social trust, and institutional access infrastructure that disaster response depends on. Violence and disaster are not separate systems in this corridor.

| Variable (Spanish) | Variable (English) | Data Source | Scoring Logic | 1.0 looks like | 0.0 looks like |
|---|---|---|---|---|---|
| Tasa de homicidios | Homicide rate | SESNSP homicide statistics by municipality, 2022–2024 average | Homicide rate per 100,000, normalized against national range | >80/100,000 (Guerrero hotspots) | <5/100,000 |
| Densidad de eventos de crimen organizado | Organized crime event density | ACLED Mexico — armed group events, territorial control markers, 2022–2024 | Events per 100 km², normalized | Persistent cartel territorial conflict; documented NGO/government access restrictions | No ACLED events recorded |
| Desplazamiento forzado documentado | Documented forced displacement | IBERO/PDH annual displacement reports + CNDH + local media | Displacement events documented, normalized by population | Documented mass displacement events (Chiapas: 61.8% of national total 2024) | No documented displacement events |
| Pérdida de documentación por violencia | Documentation loss from violence | Indirect proxy: % population registered in Padrón de Bienestar vs. estimated eligible × displacement event presence | Gap between estimated eligible and registered population in displacement-affected municipalities | High gap between eligible and registered; documented ID loss events | Full registration; no displacement-driven doc loss |
| Restricciones de acceso humanitario | Humanitarian access restrictions | ACLED territorial control + OCHA/NGO access reports | Documented cartel territorial restrictions on NGO/government access | Active access restrictions; no-go zones for aid | Full humanitarian access |
| Coherencia del tejido social | Social fabric coherence | Proxy: INEGI social cohesion indicators + homicide trend (improving/worsening) | Worsening homicide trend = degrading social fabric | Accelerating homicide trend + active displacement + restricted access | Stable or improving security; no displacement |

*Note: The compounding mechanism — violence destroys census registration, which destroys disaster aid eligibility — should be called out explicitly in the detail panel when this cluster scores high alongside the Tenure cluster.*

---

## Cluster 9: Memoria Cultural (Cultural Record)
*Weight in composite: 0.05*
*Qualitative by nature; weakest quantitative proxy availability. Weighted lowest accordingly.*

**What this cluster captures:** Where a community sits in the Formulation → Strengthening → Operationalizing → Degradation cycle. The presence of cultural practices, community organizations, and historical memory that encode hazard knowledge and preparedness behavior. This is the thesis framework made measurable.

| Variable (Spanish) | Variable (English) | Data Source | Scoring Logic | 1.0 looks like | 0.0 looks like |
|---|---|---|---|---|---|
| Prácticas culturales de preparación documentadas | Documented cultural preparedness practices | Academic literature + NGO reports + journalism: documented presence of tequio/gozona in disaster response; oral history of prior events; community-maintained risk knowledge | Qualitative graded: no documentation = 1; documented but inactive = 0.5; active practice = 0 | No documented cultural preparedness practices; no community disaster memory | Active tequio/gozona in disaster response; oral history maintained; community risk maps |
| Fase del ciclo de preparación | Preparedness cycle stage | Assessed from: DRRM plan age, drill history, prior event response record, civil society presence | Formulation=0.2, Strengthening=0.4, Operationalizing=0.6, Degradation=0.9 (degradation = highest vulnerability) | Degradation stage: former preparedness culture now inactive or ceremonial; drill became ritual without meaning | Operationalizing stage: active, embedded practices |
| Continuidad de gobernanza post-desastre | Post-disaster governance continuity | Proxy: % of municipal government continuity after major events; indigenous governance continuity | Collapse or capture of local governance after events = high score | Local governance collapsed or captured by organized crime post-event | Continuous community governance through and after events |
| Patrimonio cultural en riesgo | Cultural heritage at risk | UNESCO / INAH registered heritage sites + CENAPRED hazard overlap | Count of INAH-registered sites in high-hazard zone | Multiple registered sites in PDZ equivalent or flood zone | No registered heritage sites at risk |
| Medios de comunicación comunitarios | Community media presence | Proxy: AMARC community radio registry + indigenous-language media | Presence of community-controlled communication channel | No community radio; no indigenous media | Active community radio; indigenous-language broadcast |

*Cluster note: Cultural heritage at risk applies a +0.05 adjustment to the cluster score when INAH-registered sites overlap with CENAPRED high-hazard zones.*

---

## Physical Hazard Score (Separate Layer — Not Part of SVI Composite)

The physical hazard score is computed independently and displayed alongside the SVI composite in the comparison toggle. It uses three sub-scores:

| Sub-score | Data Source | Weight |
|---|---|---|
| Peligro sísmico | CENAPRED índice de peligro sísmico municipal + SSN Guerrero Gap proximity | 0.40 |
| Peligro ciclónico | CENAPRED índice ciclónico + HURDAT2 historical track density within 100km | 0.35 |
| Peligro por inundación/deslizamiento | CENAPRED índice de inundación + índice de deslizamiento | 0.25 |

The comparison toggle flips between Physical Hazard Score and SVI-Inclusive Score on the choropleth. Municipalities that score high on SVI-Inclusive but low on Physical Hazard are the tool's most important finding — they are the communities most likely to be underserved by aid that follows hazard maps.

---

## Cross-Cluster Interaction Flags

These combinations trigger an explicit warning/callout in the municipality detail panel:

| Flag | Trigger | Panel Message |
|---|---|---|
| **Trampa de tenencia** | Tenure cluster >0.7 AND Social cluster >0.7 | *"Esta comunidad combina exclusión documental con alta marginación social — el perfil más excluido de programas de reconstrucción."* |
| **Violencia + desastre** | Violence cluster >0.6 AND DESINVENTAR events present | *"La violencia organizada preexistente destruye la infraestructura documental y de confianza institucional que la respuesta al desastre requiere."* |
| **Alerta sin alcance** | Action cluster >0.7 (SASMEX functional coverage <0.3) AND Seismic hazard >0.7 | *"Esta comunidad está en zona de alto peligro sísmico pero la alerta SASMEX no llega en idioma comprensible para la mayoría de residentes."* |
| **Resiliencia invisible** | Engagement cluster <0.3 (strong networks) AND Social cluster >0.7 (high poverty) | *"Alta marginación económica coexiste con redes comunitarias sólidas — el activo más importante es el más invisible para los programas de ayuda formal."* |
| **Ciclo sin ruptura** | Tenure >0.7 AND DESINVENTAR >2 events AND Violence >0.5 | *"Perfil de vulnerabilidad estructural persistente: múltiples eventos pasados sin reconstrucción exitosa documentada."* |

---

## Scoring Rubric Quality Notes

**Variables with strong quantitative proxies (high confidence):**
Poverty/marginalization (CONEVAL/CONAPO), housing materials (INEGI), homicide rates (SESNSP), agricultural dependence (SIAP), connectivity (IFT), healthcare distance (CLUES database).

**Variables with moderate proxies (medium confidence):**
Tenure exclusion (RAN coverage rates as proxy for documentation gaps), remittance dependence (state-level data downscaled to municipality), SASMEX functional coverage (derived from census language data × sensor map).

**Variables with weak proxies (low confidence — qualitative grading required):**
Cultural preparedness practices, mutual aid network documentation, humanitarian access restrictions, post-disaster governance continuity. These are flagged in the detail panel as "Estimado — datos cualitativos" to be transparent about data quality.

**Variables where community input would upgrade confidence:**
All Engagement and Cultural Record variables would improve substantially with community-level participatory data. The tool is explicitly designed to be a placeholder pending that data, not a substitute for it.
