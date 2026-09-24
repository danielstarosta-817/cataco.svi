# Western North Carolina SVI Tool — Project Briefing
*Paste this at the start of a new chat to resume work on this project.*

---

## What This Is

A parallel extension of the Puerto Rico Social Vulnerability & Hazard Intelligence tool — a single-file `index.html` interactive map. The goal is to build a new tool for **western North Carolina's Blue Ridge / French Broad River corridor** (Buncombe, Yancey, Mitchell, Madison, Rutherford, and surrounding counties) using the same base architecture as the PR tool, anchored to Hurricane Helene's catastrophic flooding of September 2024.

The PR tool already exists as a complete `index.html` and is the codebase to evolve from. Unlike the Philippines, Mexico, and Kenya extensions, this tool is built in **English** and sits in a US regulatory/data context — meaning federal open-data infrastructure (FEMA, USGS, Census/CDC) is far richer and more current than in prior builds, but the "informal tenure" analytical lens from PR/Albay/Mexico doesn't map directly. The new analytical wrinkle here is different: a region *branded as safe from the very hazard that just devastated it*, plus an immigrant labor population invisible to the same federal aid system serving everyone else in the same holler.

---

## Why Western North Carolina

1. **Hurricane Helene is the anchor event, but not a one-off.** Helene (September 2024) sent the French Broad and Swannanoa rivers to their highest recorded crests, topping the 1916 flood by over a foot and a half. But this is the third catastrophic flood in the region's recorded history — 1916 (two back-to-back hurricanes, ~80 dead) and 2004 (Ivan/Frances remnants, 11 dead) both hit the same rivers, the same towns, the same geography. This is a cyclical hazard with a 20th-century-plus paper trail, not a freak event.

2. **The "climate haven" inversion is the sharpest available hook in the whole US shortlist.** Asheville and the surrounding mountains had been informally and repeatedly branded a climate-safe relocation destination — mild summers, no coastal storm exposure, no sea-level risk, low wildfire/drought profile — driving real in-migration from the coasts. Helene didn't just flood the region; it flooded the *premise* people moved there on. This is a fundamentally different kind of "gap between assumed and actual vulnerability" than any prior tool: it's not that the region's risk was hidden from planners, it's that it was actively marketed as absent.

3. **An immigrant farmworker population sits invisible inside the same disaster zone.** Latino and immigrant workers on Christmas tree farms (Ashe, Avery, Alleghany, Watauga, Jackson counties), poultry operations, and dairy farms were hit as hard as anyone, but undocumented and visa-tied workers were largely invisible to FEMA aid — some fearing that seeking help could trigger immigration enforcement, some reportedly pressured to keep working despite impassable roads. This is the closest US analog to the PR "three households, one FEMA lot" problem and the Mexico ejido/tenure trap: a real, quantifiable population that the response system's paperwork simply doesn't see.

4. **Institutional failure took a form none of the other tools have captured yet: weaponized misinformation.** FEMA had to stand up a dedicated rumor-response page during the response — false claims that officials "manipulated the weather" to target specific political areas, that a $750 FEMA payment was a loan cap when further aid was available, that the government sought to seize land in Chimney Rock for lithium mining. This actively slowed real aid uptake and is a distinct failure mode from bureaucratic exclusion (PR, Albay, Mexico) — it's an information-environment failure layered on top of a physical one.

5. **Damage is wildly uneven county to county, in ways a state or even county-level view erases.** Yancey County had roughly double the per-capita death rate of any other county in the storm, with 300+ roads on one side of the county left with zero access. Mitchell County lost ~1,400 structures outright with 2,300 more severely damaged. Buncombe County (Asheville) got the vast majority of the media coverage. A tool that only differentiates at the county level would flatten exactly the variation that matters here — this needs tract-level (or finer) resolution, same lesson as the Albay barangay trap documented in the generic architecture doc.

---

## The Anchor Event

### Hurricane Helene — September 26–27, 2024
- Remnant moisture dumped up to 30 inches of rain across parts of the Blue Ridge; Asheville itself recorded 13+ inches
- **French Broad River at Marshall crested well above its 1916 record**; **Swannanoa River at Biltmore hit 26.1 ft — over 5 ft above its own 1916 mark**, arguably the worst flood on that river since NC statehood
- Damage far outran Asheville: Chimney Rock (Rutherford Co.) lost ~40 businesses and 20 homes; Marshall (Madison Co.), Bat Cave, Old Fort, and Black Mountain/Swannanoa saw comparable total-loss scenes
- **Yancey County: 11 deaths**, roughly double the per-capita rate of any other county; Mount Mitchell recorded the storm's highest wind gust
- **Mitchell County: ~1,400 structures destroyed, 2,300 severely damaged**; bridges and roads wiped out, some families still reporting effective isolation a full year later
- Statewide: 400+ roads closed, widespread multi-week loss of cell service, power, and drinking water
- FEMA built a dedicated rumor-response page mid-crisis to counter disaster misinformation actively slowing aid uptake

### Historical Precedent — 1916 and 2004
- **July 1916:** two back-to-back hurricanes dumped ~26 inches of rain on the region in days; French Broad crested at ~21 ft; ~80 dead — the flood every subsequent event in the region has been measured against
- **September 2004:** remnants of Hurricanes Ivan and Frances hit the same rivers; French Broad crested at ~14 ft; 11 dead
- Helene topped the 1916 record by more than 18 inches on the French Broad — the fourth major flood event on these same rivers in just over a century

---

## Core Analytical Tension

Western North Carolina sits at the intersection of two things that are supposed to be mutually exclusive: it was sold as a place to escape climate risk, and it is a place with a well-documented, escalating flood cycle stretching back over a century. The people most likely to have taken the "climate haven" narrative at face value — recent transplants without generational memory of 1916 or 2004 — are layered on top of a rural mountain population that has always lived with this risk but has comparatively little of the institutional infrastructure (flood insurance uptake, road redundancy, cell coverage) that would let it recover quickly. Underneath both groups, an immigrant agricultural workforce works the land is genuinely invisible to the recovery system meant to serve everyone else in the same county.

The tool's job is to show that "climate haven" and "generational flood-risk region" are not in tension — they are the same place, and the mismatch between the story a community told about itself and the story its geology has told for 100+ years is what determined how hard Helene actually hit.

---

## The Climate Haven Trap (Key New Element vs. Prior Tools)

Every prior tool (PR, Albay, Mexico, Kenya) is built around communities that were already known — by planners, by aid systems, by the communities themselves — to be high-risk. Western NC inverts that: the region's *dominant public narrative* was one of relative safety. That narrative:

- Was actively used in real estate marketing and local economic-development messaging aimed at climate migrants from the coasts
- Was explicitly disclaimed by NC's own state climatologist, who noted officials "never really agreed with" the label — meaning the gap between expert knowledge and public perception was known and unaddressed
- Directly shaped who moved in (people prioritizing climate safety) without shaping how prepared the built environment or emergency infrastructure actually was
- Continues to shape the recovery narrative — Asheville's City Council response (tightening floodplain zoning, January 2025) implicitly concedes the "haven" framing was wrong, without publicly reckoning with why it took hold in the first place

**Analytical question:** Does living somewhere *because* you believed it was low-risk make you more or less prepared when that belief turns out to be wrong — compared to a household that never had the luxury of choosing where to live based on risk at all?

A second, parallel trap operates underneath this one, closer to the Mexico ejido/PR tenure-lot problem: **documentation status, not land title, is the exclusion mechanism.** Undocumented and visa-tied farmworkers on Christmas tree, poultry, and dairy operations experienced the same flood as everyone else in their counties but are structurally invisible to FEMA individual assistance — the US analog to "one FEMA lot, three households" or "no formal ejido title, no FONDEN aid."

---

## Data Sources

### Physical Hazard
- **FEMA National Risk Index (NRI)** — county and census-tract level, hazard-specific (flood, hurricane, landslide) expected annual loss, hazard frequency, and community resilience scores; downloadable via OpenFEMA / hazards.fema.gov/nri
- **USGS Water Data for the Nation** — real-time and historical stream gauge data; French Broad at Marshall (gauge 03453500) and Swannanoa at Biltmore (gauge 03451000), both with 100+ years of record, directly supporting the 1916/2004/2024 crest comparison
- **NC Emergency Management FIMAN** (Flood Inundation Mapping and Alert Network) — real-time and modeled flood extent for structures and roads
- **NC Forest Service Hurricane Helene Damage Appraisal** — county-level timberland/agricultural land damage assessment
- **NOAA/NWS historical storm track and rainfall data** — 1916, 2004, and 2024 event comparisons

### Social Vulnerability
- **CDC/ATSDR Social Vulnerability Index (SVI)** — census-tract level, 16-variable/4-theme composite; usable across all affected WNC counties
- **US Census / ACS** — tract and block-group level income, age (65+ share), housing tenure, mobile-home share, limited-English and foreign-born share (proxy layer for the immigrant farmworker population given data gaps elsewhere)
- **USDA NASS Census of Agriculture** — county-level baseline for Christmas tree, poultry, and dairy operations in Ashe, Avery, Watauga, Yancey, and neighboring counties — the sensitivity-layer proxy for immigrant agricultural labor exposure

### Aid & Institutional Record
- **OpenFEMA Individual/Public Assistance & Housing Assistance datasets** — county/zip level (some household-level), specific to Hurricane Helene's official disaster declaration (DR-4827-NC)
- **NC OneMap / NC Emergency Management GIS damage assessment layer** — 64,000+ point-level damage assessments collected across the ten hardest-hit counties
- **NC Office of State Budget and Management Damage and Needs Assessment** — official state-level DNA report, county granularity
- **FEMA Hurricane Rumor Response page** — documented record of specific misinformation claims circulated during the response, useful as a structured "institutional failure" content source

### Community Resilience / Cultural Record
- **NC Collaboratory / UNC Asheville rapid-grant research portfolio** — 21 active university research projects (Appalachian State, Davidson, UNC-Chapel Hill, Western Carolina, UNC Asheville) covering flood modeling, infrastructure resilience, recovery barriers, and warning-message effectiveness; a live, still-growing dataset source
- **Farmworker Association of Florida / equivalent NC-based farmworker advocacy orgs** (to be identified — likely NC Justice Center, NC FIELD, or similar) — organizational response filling the FEMA gap for undocumented agricultural workers
- **Local flood-memory record** — 1916 and 2004 flood markers, oral history, and local news archives as the Appalachian equivalent of PR's musical/cultural disaster record

---

## Key Human Stories to Develop

1. **The transplant and the multigenerational mountain family, same street, same flood.** A household that moved to Asheville in the last five years specifically citing climate safety, living next to a family that has weathered 1916-adjacent flood folklore for generations — same water, completely different relationship to the risk that just proved both of them wrong or right in different ways.

2. **The Christmas tree farmworker FEMA can't see.** A worker on one of the Ashe/Avery/Watauga county tree farms who lost housing and income in the same flood that made national news, but who never appears in a FEMA registration count because applying risked exposing undocumented status — the same storm, a completely separate and invisible recovery track.

3. **The Yancey County isolation story.** With 300+ roads on one side of the county impassable and the highest per-capita death toll of the disaster, a household or community that was cut off from any outside response for days — not due to bureaucratic exclusion, but due to genuine physical isolation in mountain terrain, a different kind of "invisible to the response system" than the tenure/documentation traps in prior tools.

4. **The misinformation casualty.** Someone who delayed applying for real, available FEMA aid because they believed one of the specific false claims FEMA had to build a rumor-response page to counter — a documented case where the institutional failure was informational, not just bureaucratic.

5. **The 1916/2004/2024 repeat.** A family or property with a multi-generational flood history on the same parcel — three "worst flood in a century" events across four generations — used to visually and narratively demonstrate that this is a cyclical hazard the "climate haven" narrative had to actively ignore, not one nobody could have known about.

---

## Tool Architecture Decisions (Evolving from PR)

**Evolving from PR, not replicating it.** Key changes from the Puerto Rico base:

1. **Geographic unit: census tract, not county.** Given the damage variation documented above (Yancey vs. Buncombe vs. Mitchell, and likely sharp variation within Buncombe County itself between downtown Asheville and outlying communities), county-level resolution would repeat the Albay municipality-centroid trap documented in the generic architecture doc. Nearest-lookup array should be built from CDC/ATSDR SVI census tracts across the affected multi-county region, not county centroids.

2. **Single dominant hazard, not multi-hazard toggle.** Unlike Mexico's three-system toggle (hurricane/seismic/flood) or Albay's volcanic/typhoon compound, western NC's tool is built around one hazard system — riverine/flash flooding from tropical storm remnants — with historical recurrence (1916/2004/2024) as the framing device rather than a second hazard type. Landslide risk (a real secondary hazard in steep terrain) can be a secondary sub-score within the flood-dominant model rather than a separate toggle.

3. **"Climate Haven" narrative layer** — new, replacing PR's SVI composite framing and Mexico's ejido/tenure lens as the region's distinctive analytical hook:
   - A binary or scored "in-migration recency" proxy (Census ACS "moved from different state in past 5 years" at tract level) as a stand-in for climate-migrant concentration
   - Overlay against flood exposure and historical flood-zone boundaries to visualize the mismatch between where people moved *for* safety and where the actual hazard sits
   - Undocumented/immigrant farmworker exposure layer (USDA agricultural employment + Census foreign-born/limited-English proxies) as the FEMA-aid-blind-spot equivalent of the ejido/tenure trap

4. **Language:** English throughout — no Spanish-language requirement equivalent to the Mexico build, though the farmworker narrative content should acknowledge the Latino/immigrant composition of that population directly.

5. **Misinformation/institutional-failure layer** — new content type not present in prior tools: a structured record of specific false claims documented via FEMA's rumor-response page, presented as a distinct failure mode alongside (not instead of) bureaucratic exclusion.

6. **Multi-event historical framing** — the tool should visually anchor 1916, 2004, and 2024 on the same river-gauge charts (USGS data supports this directly) to make the "this was never actually unprecedented" argument central to the climate-haven critique.

---

## Daniel's Background Context

- Master of Development Practice, UC Berkeley 2022
- Thesis: *"Raised Under Bad Stars: Tracing the complexities of creating, transmitting, and preserving a culture of preparedness among disaster-vulnerable communities"*
- Worked on LandLedger with IOM's Housing, Land and Property team / Global Shelter Cluster
- Currently at Nubank (São Paulo)
- The Puerto Rico tool exists as a complete `index.html` (on GitHub Pages) and is the codebase being evolved
- The Philippines/Albay, Mexico, and Kenya tools are parallel/prior projects — western NC work happens in a fresh chat with this document as context

---

## Key Sources

- [From 'climate haven' to disaster zone — Northeastern University](https://news.northeastern.edu/2024/10/01/hurricane-helene-asheville-north-carolina/)
- [Hurricane Helene impact challenges climate haven idea — The Hill](https://thehill.com/policy/energy-environment/4912092-hurricane-helene-north-carolina-asheville-climate-change-haven/)
- [Asheville was called a climate haven. Helene shows nowhere is safe — AccuWeather](https://www.accuweather.com/en/climate/asheville-was-called-a-climate-haven-helene-shows-nowhere-is-safe/1698994)
- [People moved to Asheville to escape extreme weather. They forgot its tragic history — CNN](https://www.cnn.com/2024/10/02/climate/asheville-flooding-history-helene/index.html)
- [Immigrants in western NC face a long recovery after Hurricane Helene — Prism Reports](https://prismreports.org/2024/10/24/immigrants-in-western-nc-hurricane-helene/)
- [Latino farmworkers isolated after Helene — NPR](https://www.npr.org/2024/10/05/g-s1-26557/hurricane-helene-latino-farm-workers-tennessee-isolated)
- [FEMA Hurricane Rumor Response](https://www.fema.gov/disaster/recover/rumor/hurricane-rumor-response)
- [FEMA denies North Carolina's request for Helene aid — Rolling Stone](https://www.rollingstone.com/politics/politics-news/fema-denies-north-carolina-request-hurricane-helene-aid-1235347521/)
- [North Carolina Tropical Storm Helene disaster declaration (DR-4827)](https://www.fema.gov/disaster/4827)
- [NC Christmas tree industry recovery — NC State Cooperative Extension](https://cnr.ncsu.edu/news/2024/11/nc-christmas-tree-industry-hurricane-helene-recovery/)
- [FEMA National Risk Index data](https://www.fema.gov/about/openfema/data-sets/national-risk-index-data)
- [CDC/ATSDR Social Vulnerability Index](https://www.atsdr.cdc.gov/place-health/php/svi/index.html)
- [USGS Water Data for the Nation](https://waterdata.usgs.gov/nwis)
- [NC Collaboratory Hurricane Helene research portfolio](https://collaboratory.unc.edu/)
