# Maui SVI Tool — Project Briefing
*Paste this at the start of a new chat to resume work on this project.*

---

## What This Is

A parallel extension of the Puerto Rico Social Vulnerability & Hazard Intelligence tool — a single-file `index.html` interactive map. The goal is to build a new tool covering **the island of Maui, Hawaii**, using the same base architecture as the PR tool, anchored to the wind-driven wildfires of August 8, 2023.

Unlike the original card concept (a Lahaina-only tool), this build is scoped to **all of Maui island**, with two communities highlighted as the analytical focal points: **Lahaina** (West Maui, the plantation-town fire that killed 102 people) and **Upcountry Maui / Kula–Olinda** (the ranching and small-farm community that burned the same night, on the opposite side of the island, with zero deaths). Both fires ignited within hours of each other, in the same windstorm, under the same emergency-management failures — but they hit two demographically and economically distinct Mauis. Building the tool at island scale, rather than Lahaina alone, is what makes that contrast visible instead of assumed.

This is a US-context build like Western NC: FEMA, CDC/ATSDR, and Census/ACS data infrastructure is rich and current. But Hawaii's small population sizes mean census tracts here are coarse relative to the mainland — Lahaina itself is roughly one to two tracts total, which limits how much sub-community differentiation tract-level SVI alone can support (see Data Sources and Tool Architecture Decisions below for the parcel/TMK-level workaround).

---

## Why Maui (All of It, Not Just Lahaina)

1. **One windstorm, one night, two fires, wildly different outcomes.** The Lahaina fire and the Upcountry/Kula–Olinda fires both ignited on August 8, 2023, driven by the same hurricane-remnant wind event. Lahaina: 102 dead, over 2,200 structures destroyed, a historic town center erased in an afternoon. Kula/Olinda: zero deaths, 19 homes destroyed across roughly 1,300 acres. Same night, same wind, same county emergency-management failures — completely different body count. A tool that only builds Lahaina treats the outcome gap as a given; a tool that builds both fires side by side has to explain it.

2. **The two communities sit on opposite ends of Maui's economic and land-use spectrum.** Lahaina is the old plantation and whaling capital, coastal, dense, tourism-saturated, historically home to a large Native Hawaiian, Filipino, and immigrant plantation-labor population. Upcountry/Kula is inland, elevated, agricultural and ranching country — Maui's paniolo (Hawaiian cowboy) heartland, lower density, larger lot sizes, a different demographic mix shaped by Portuguese immigrant ranching families rather than Asian and Pacific plantation labor. Building island-wide lets the tool show these as two different vulnerability profiles under one hazard system, not just two disaster sites.

3. **The plantation-water-diversion trap is a Maui-wide story, not a Lahaina-only one.** The dried streams, fallow cane and pineapple fields, and invasive fire-prone grasses that fueled the Lahaina fire are the direct legacy of over a century of sugar (HC&S, Pioneer Mill, Amfac/West Maui Land Company) and pineapple plantation agriculture across the island, not something specific to West Maui alone. Upcountry's own agricultural land-use shift — from diversified plantation-era farming to today's smaller ranches and flower/produce farms — sits on the same underlying water-rights and land-use history. An island-scale tool can show the same fuel-load mechanism playing out in two different microclimates and land-use contexts.

4. **Tourism dependence and the housing crisis are county-level, not town-level, forces.** Maui County drew roughly 2.4 million visitors a year against a resident population of about 165,000 before the fires — in peak season, close to one in three people on the island is a tourist. That imbalance, and the short-term-rental-driven housing shortage it created, pre-dates the fire and shaped both Lahaina's density and the vulnerability of displaced residents afterward across the whole island, not just within the burn scar.

5. **Native Hawaiian land dispossession is a centuries-long, island-wide mechanism that the fire exposed rather than created.** The Great Māhele (1848) and the 1850 Kuleana Act converted communal Hawaiian land tenure into fee-simple title, and Native Hawaiians ended up with well under 1% of the islands' land under that process. Post-fire land-grab attempts in and around Lahaina are the most visible recent instance of a dispossession mechanism — unclear or contested kuleana title, absentee/foreign ownership, speculative acquisition after crisis — that has operated across Maui for 175 years. This is the island's version of the tenure/documentation trap found in every prior tool in this project.

6. **County-level, or even Lahaina-only, resolution would flatten exactly the variation that matters.** Just as Albay's municipality centroids erased barangay-level difference, and Western NC's county view erased Yancey-vs-Buncombe variation, a Maui tool that stops at "Lahaina" would erase both the Upcountry contrast and the tract-by-tract variation across the rest of the island (Wailuku, Kahului, Hana, South Maui). This needs island-wide tract-level resolution, with Lahaina and Upcountry called out as the two narrative anchors.

---

## The Anchor Events

### The Lahaina Fire — August 8, 2023
- Ignition traced to **6:34 a.m.**, when sparks from a broken, re-energized Hawaiian Electric power line ignited dry, unmaintained vegetation off Lahainaluna Road. Firefighters declared the fire extinguished by late morning after dousing and bulldozing it.
- The smoldering remnant reignited in a gully around midafternoon as hurricane-driven winds (from Hurricane Dora passing well south of the islands) intensified; the fire then grew explosively through the afternoon and evening.
- **102 confirmed deaths** — the deadliest wildfire in the US in over a century (since 1918).
- **Over 2,200 structures destroyed**, more than 86% of them residential; roughly 2,746 housing units lost in total.
- **Warning sirens did not sound.** Hawaii's outdoor siren network — the largest in the world, built primarily for tsunami warning — was not activated for the fire; then-MEMA administrator Herman Andaya said the decision was deliberate, out of concern residents would head toward the coast as they're trained to for tsunamis. Separately, **2 of the 3 sirens serving the Lahaina area had pre-existing mechanical failures** and would not have sounded even had activation been ordered. Maui Emergency Management instead relied on wireless emergency alerts and social media, both of which were undercut by widespread power and cellular outages (and a non-functional satellite-phone backup).
- ~$5.5 billion in estimated damage; roughly 12,000 people displaced.
- The Maui Fire Department / ATF joint investigation (report released October 2024) and the state's separate Fire Safety Research Institute (FSRI) phased investigation both attribute the fire's origin to the reignited power-line ignition, not a single unbroken blaze.

### The Upcountry / Kula–Olinda Fires — Same Night
- Ignited within hours of Lahaina, in the Kula/Olinda area on the slopes of Haleakalā, roughly 25 miles from Lahaina as the crow flies but a world apart in land use and density.
- **Zero deaths.** 19 homes destroyed (3 in Olinda, 16 in Kula) across a combined burn area of roughly 1,300 acres (Olinda ~1,081 acres, Kula ~202 acres).
- Same wind event, same county emergency-response system, same night — but larger lot sizes, lower population density, and different terrain and evacuation geography produced a dramatically different casualty outcome.
- Far less national media attention than Lahaina, despite being part of the same disaster declaration (DR-4724-HI) and the same emergency-management failure.

### Historical Precedent — A Century of Water Diversion, Not a Freak Event
- Pre-contact and 19th-century Lahaina sat amid fishponds and wetlands fed by free-flowing mountain streams. Beginning with sugar plantations in the late 1800s (Pioneer Mill, later Amfac/West Maui Land Company) and continuing through 20th-century agriculture and real estate development, an estimated 90%+ of the surface water historically reaching West Maui's streams was diverted for irrigation — first for cane, later for other uses.
- When the plantation economy collapsed under global competition in the late 20th century, the irrigated fields were abandoned rather than restored — leaving vast tracts of dry, formerly-irrigated land that were rapidly colonized by highly flammable invasive grasses (guinea grass, buffelgrass and similar species) in place of the native and agricultural vegetation the water had supported.
- Local fire officials had flagged the fire risk of these fallow, grass-choked former plantation lands for years before 2023; a preliminary Insurance Institute for Business & Home Safety analysis identified the invasive-grass buildup around Lahaina as a direct driver of the fire's "catastrophic spread."
- This is the same underlying land-use and water-rights history across Maui's former plantation lands, not a Lahaina-specific anomaly — which is part of the case for building the tool at island scale.

---

## Core Analytical Tension

Maui is an island where the same infrastructure and economic system that makes it a globally desirable place to visit — diverted water feeding resorts and golf courses, a housing stock increasingly built for short-term rental income rather than residents, an emergency siren network built for tsunamis rather than fire — is also what made two communities, on opposite sides of the island, catastrophically vulnerable to a wind-driven fire on the same night. The Lahaina/Upcountry contrast shows that "vulnerability" is not one number: a plantation town with dense historic housing and a large working-class and Native Hawaiian population burned with catastrophic loss of life; an agricultural community with more land per household and different evacuation geography burned the same night without losing anyone. Layered underneath both is a 175-year-old land-tenure system — the Great Māhele and Kuleana Act — that already determined, well before 2023, who had secure title to the land their family lived on and who didn't; the post-fire wave of land-grab offers to fire survivors is that same mechanism operating in real time rather than a new one.

The tool's job is to show that Maui's disaster risk cannot be read off a single "Lahaina burned" story — it has to hold the plantation-water-diversion fuel-load mechanism, the tourism-economy housing squeeze, the kuleana/land-title exclusion, and the sharply different casualty outcomes of two same-night fires in the same frame.

---

## The Kuleana Trap (Key New Element vs. Prior Tools)

Every prior tool in this project has its own version of a "who gets excluded from formal recognition and aid" mechanism: PR's one-FEMA-lot/three-households problem, Albay's PDZ/informal-tenure trap, Mexico's ejido system, Western NC's undocumented-immigrant-farmworker exclusion. Maui's version is older and more structurally embedded than any of those: it runs through **land title itself**, not occupancy or immigration status.

- The **Great Māhele (1848)** converted Hawaii's communal land system to Western fee-simple title. The subsequent **1850 Kuleana Act** allowed Native Hawaiian commoners to claim title to land they actively cultivated or lived on at the time — but required an affirmative claim process that many never completed, and even those who did collectively ended up with under 1% of the islands' total land area.
- 175 years later, many Native Hawaiian families hold **kuleana land rights** that are only partially documented, contested by later owners of the surrounding "ahupuaʻa" (larger land division), or split across generations of heirs without a clear title — a documentation gap structurally analogous to PR's undocumented tenure lots, but rooted in an 1850s claims process rather than a modern informal-settlement pattern.
- **The fire made this trap visible in real time.** Within days of the fire, Lahaina families reported receiving unsolicited offers from investors and developers to buy their land — land sales in and around Lahaina jumped roughly twelvefold in the first four months of 2024 versus the same period in 2023. Families with clear, documented, unified title were positioned to make an informed choice; families with contested, fractional, or undocumented kuleana claims were far more exposed to pressure, confusion about their rights, or the practical need to sell.
- Community response has organized around collective solutions — most notably proposals for a **Lahaina Community Land Trust** — that echo the "collective/formal recognition" fixes proposed in the PR and Mexico tools' tenure sections.

**Analytical question:** When a title system created 175 years ago already determined which families in a burned town had unambiguous legal standing to say no to a buyout offer, is a survivor who "chooses" to sell actually exercising a choice — or is the disaster just the moment the old exclusion becomes visible?

---

## Data Sources

### Physical Hazard
- **FEMA National Risk Index (NRI)** — county and census-tract level; includes a dedicated Wildfire hazard layer (annualized frequency and expected annual loss) alongside hurricane, drought, and other relevant hazards for Maui County; downloadable via OpenFEMA / hazards.fema.gov/nri
- **Maui Wildfires Mitigation Assessment Team (MAT) Reports** — FEMA's post-disaster technical reports (Recovery Advisory series and full Compendium Report, P-2425) documenting structure-level failure modes, defensible-space findings, and rebuilding code recommendations
- **Maui Fire Department / ATF joint investigation report (Oct. 2024)** and the **Hawaii Attorney General's Fire Safety Research Institute (FSRI) phased investigation** — authoritative record of ignition point, timeline, and cause (reignited power line)
- **NOAA/NWS Hurricane Dora wind-event data** — the offshore hurricane whose outer wind field drove both fires
- **Invasive grassland / fuel-load mapping** — Hawaii Wildfire Management Organization and University of Hawaii fire-risk assessments of former plantation lands, useful as a proxy layer for fuel load across the island's dry leeward zones (West Maui, Upcountry, South Maui)

### Social Vulnerability
- **CDC/ATSDR Social Vulnerability Index (SVI)** — census-tract level, 16-variable/4-theme composite, available for all of Maui County; **caveat: Lahaina's small population means the town itself is covered by only one or two tracts**, so tract-level SVI alone will under-resolve within-Lahaina variation (see Tool Architecture Decisions)
- **US Census / ACS** — tract and block-group level income, age (65+ share), housing tenure, Native Hawaiian/Pacific Islander population share, limited-English and foreign-born share (relevant to Lahaina's historic Filipino plantation-descendant population)
- **Hawaii Open Data / Hawaii Statewide GIS Program — Maui County Parcels (TMK)** — parcel-level shapefile/GeoJSON/CSV data (opendata.hawaii.gov), the parcel/TMK-level workaround this project's notes flagged as necessary given how coarse tract data will be for a town the size of Lahaina; parcel-level ownership records are also the substrate for tracking land-grab/absentee-ownership patterns
- **USDA NASS Census of Agriculture** — county-level baseline for Upcountry's ranching and diversified-agriculture operations, the closest available proxy for the Kula/Olinda agricultural labor and land-use profile

### Aid & Institutional Record
- **OpenFEMA Individual/Public Assistance & Housing Assistance datasets** — specific to Hawaii Wildfires disaster declaration **DR-4724-HI**
- **UHERO (University of Hawaii Economic Research Organization) Maui Recovery Dashboard** — housing, jobs, and displacement tracking, updated on a rolling basis since the fire; a live, still-growing dataset source similar in role to the NC Collaboratory portfolio in the WNC tool
- **Maui County Office of Recovery** rebuilding-permit and structure-completion tracking (as of August 2026: ~577 homes completed, ~400 under construction, ~82% of lost housing units on a path toward rebuilding)
- **Hawaii Governor's Office / Maui County land-grab response record** — public statements and any subsequent legislative or county action addressing predatory post-fire land acquisition

### Community Resilience / Cultural Record
- **Kuleana Land Workshops / Native Hawaiian legal aid organizations** (e.g., the Kapu family's ongoing advocacy work; Native Hawaiian Legal Corporation) — organizational response to the kuleana-title exclusion trap
- **Lahaina Community Land Trust proposal** — community-organized collective-ownership response, directly analogous to prior tools' "formal recognition" interventions
- **Kula Community Association / Upcountry ranching heritage record** — Upcountry's paniolo (Hawaiian cowboy) and Portuguese-immigrant ranching history, the community-identity equivalent of PR's musical record or WNC's flood-memory record
- **Hawaiian oral history / moʻolelo of Lahaina** as the historic capital of the Hawaiian Kingdom — the town's pre-plantation and pre-fire cultural significance, essential context for why the fire is experienced as loss of national historical memory, not just property loss

---

## Key Human Stories to Develop

1. **The kuleana family fighting for a title 175 years unresolved.** A Lahaina family (the Kapu family's public case is a documented real-world example) whose ancestors were awarded land in the 1848 Great Māhele, now navigating a decades-long legal battle to have that title formally recognized — with the 2023 fire adding urgency and outside pressure to a dispute that predates the disaster by generations.

2. **The land-grab offer that arrived while the fire was still burning.** A Lahaina household that received an unsolicited purchase inquiry from an out-of-state investor within days (in some documented cases, hours) of losing their home — juxtaposed against a household with clear title and enough documentation to refuse and rebuild instead.

3. **The Upcountry rancher who lost the barn but not the house.** A Kula or Olinda family whose larger lot size and rural road access meant defensible space and an evacuation option Lahaina households structurally lacked — used to make the Lahaina/Upcountry outcome gap concrete at the household level rather than only at the statistical level.

4. **The tourism-industry worker priced out by the same crisis that employs them.** A hotel or service-industry worker who lived in a since-destroyed unit that was, until 2023, one of a shrinking pool of long-term rentals competing against short-term vacation rentals for the same housing stock — displaced twice over, first by pre-fire market pressure and then by the fire itself.

5. **The multi-generational Lahaina family who never got a siren.** A household in town on the afternoon of August 8 with functioning phones but no cell service and no siren, reconstructing (from the FSRI/ATF timeline) how little warning they actually had between the afternoon reignition and the fire reaching their street — the same "institutional silence" story as WNC's misinformation narrative, but caused by non-activation rather than false information.

---

## Tool Architecture Decisions (Evolving from PR / Western NC)

**Island-wide scope with two highlighted anchor communities**, not a single-town tool. Key changes from the Puerto Rico base and the Western NC approach:

1. **Geographic unit: census tract, island-wide, with a parcel/TMK-level supplemental layer for Lahaina and Kula/Olinda specifically.** Tract-level CDC/ATSDR SVI data covers all of Maui County adequately at the island scale, but Lahaina's small population (roughly 12,700 pre-fire) means the town proper is only one or two tracts — not enough resolution to show meaningful within-Lahaina variation the way Western NC's multi-tract Buncombe County view could. The fix: use tract-level data as the base nearest-lookup array island-wide, but layer in **Maui County parcel/TMK data** (from Hawaii Open Data) specifically within the Lahaina and Kula/Olinda burn perimeters to give the two anchor communities real sub-tract resolution — parcel-level ownership/absentee-owner flags, structure-loss status, and kuleana-claim flags where documented. This mirrors the generic architecture doc's barangay-resolution lesson: **if the analytical claim is "these two neighborhoods differ, and even within Lahaina some blocks differ from others," tract-level alone cannot support that claim — parcels can.**

2. **Dual-anchor narrative framing, not single dominant hazard.** Unlike Western NC's single-hazard flood framing, this tool's hazard system (wildfire, wind-driven) is the same across the island, but the narrative is explicitly dual-anchored: Lahaina and Upcountry/Kula-Olinda as two case studies of the same hazard producing different outcomes. The UI should let a user toggle or jump between the two anchor regions directly (a "focus" affordance similar to the generic doc's `focusMuni()` pattern), in addition to panning the full island.

3. **Kuleana/Land-Tenure narrative layer** — new, this tool's version of PR's tenure lens / Mexico's ejido lens / WNC's documentation-status lens:
   - A parcel-level flag for **contested/fractional/undocumented kuleana claims** where identifiable from public record or reporting (start with documented cases like the Kapu family; expand cautiously and only from sourced public reporting, given the sensitivity of individual land-title status)
   - A parcel-level or tract-level **absentee-ownership / post-fire sale proxy** (out-of-state buyer share, land-sale frequency pre- vs. post-fire) as the closest available quantifiable proxy for land-grab exposure
   - Presented alongside, not instead of, the standard SVI composite — this is an additive vulnerability dimension specific to Hawaii's land-tenure history

4. **Tourism-economy / housing-market layer** — new content type: a socioeconomic dimension (short-term-rental density, visitor-to-resident ratio by district, long-term rental vacancy rate) that explains both pre-fire housing precarity and post-fire displacement dynamics. This is analytically distinct from — but should sit near — the SVI housing-tenure dimension.

5. **Language:** English throughout, with Hawaiian-language place names and terms (ahupuaʻa, kuleana, moʻolelo, paniolo) used and briefly glossed in context, similar to how the PR tool uses Spanish toponyms without requiring translation.

6. **Same-night dual-fire framing on the historical/timeline record** — the tool should present the Lahaina and Kula/Olinda ignition-and-spread timelines side by side (both traceable to the same morning wind event and the same non-activation of the siren network), making the outcome-divergence argument central rather than incidental.

7. **Flags:** Given the existing homepage card treatment (`flags: ['us', 'hawaii', 'kanaka-maoli']`), carry the Kanaka Maoli flag alongside US and Hawaii state flags into the tool itself, not just the homepage card — this is a meaningful signal given the land-dispossession narrative core to the tool.

---

## Daniel's Background Context

- Master of Development Practice, UC Berkeley 2022
- Thesis: *"Raised Under Bad Stars: Tracing the complexities of creating, transmitting, and preserving a culture of preparedness among disaster-vulnerable communities"*
- Worked on LandLedger with IOM's Housing, Land and Property team / Global Shelter Cluster — directly relevant background given this tool's land-tenure/kuleana core analytical frame
- Currently at Nubank (São Paulo)
- The Puerto Rico tool exists as a complete `index.html` (on GitHub Pages) and is the codebase being evolved
- The Philippines/Albay, Mexico, Kenya, and Western NC tools are parallel/prior projects — Maui work happens with this document as context, and can draw directly on Western NC's dual-community, tract-level-resolution approach and the generic architecture doc's barangay-resolution lesson

---

## Key Sources

- [2023 Hawaii wildfires — Wikipedia](https://en.wikipedia.org/wiki/2023_Hawaii_wildfires)
- [Maui wildfire updates: Death toll rises, structures impacted — Maui Now](https://mauinow.com/2023/08/08/haleakala-highway-closure-due-to-brush-fire-evacuation-of-kula-200-off-auli%CA%BBi-dr/)
- [The Kula Upcountry Fire is burning 25 miles from Lahaina — NPR](https://www.npr.org/sections/pictureshow/2023/08/18/1194381656/kula-upcountry-fire-lahaina-maui-wildfires-death-toll-hawaii)
- [First part of Hawaii's report on deadly Lahaina wildfire highlights communications failures — WIBW/AP](https://www.wibw.com/2024/04/18/first-park-hawaiis-report-deadly-lahaina-wildfire-highlights-communications-failures-including-lack-emergency-alerts/)
- [Maui fires death toll rises, marking deadliest natural disaster in Hawaii history — CBS News](https://www.cbsnews.com/news/hawaii-wildfires-maui-lahaina-death-toll-warning-sirens/)
- [Investigation finds sparks from broken power line caused deadly Lahaina Fire — AccuWeather](https://www.accuweather.com/en/weather-news/investigation-finds-sparks-from-broken-power-line-caused-deadly-lahaina-fire/1699152)
- [Everybody Knew the Invasive Grass of Maui Posed a Deadly Fire Threat, but Few Acted](https://www.pitchstonewaters.com/everybody-knew-the-invasive-grass-of-maui-posed-a-deadly-fire-threat-but-few-acted/)
- [Plantation Capitalism's Legacy Produced the Maui Wildfires — LPE Project](https://lpeproject.org/blog/plantation-capitalisms-legacy-produced-the-maui-wildfires/)
- [The Maui Fire Was Fueled by Centuries of Extractive Farming — Civil Eats](https://civileats.com/2023/08/23/how-two-centuries-of-extractive-agriculture-helped-set-the-stage-for-the-maui-fires/)
- [How Maui's Wildfire Sparked a Disaster Capitalist Power Grab for Hawaiʻi's Public Water — Earthjustice](https://earthjustice.org/experts/elena-bryant/how-mauis-wildfire-sparked-a-disaster-capitalist-power-grab-for-hawaiis-public-water)
- [Lahaina land grab rumors reveal an erosion of trust — Hawaiʻi Public Radio](https://www.hawaiipublicradio.org/local-news/2023-11-17/lahaina-land-grab-rumors-reveal-an-erosion-of-trust)
- ['Vulture capitalists': Maui's indigenous community fights land grabs after wildfires — Middle East Eye](https://www.middleeasteye.net/news/vulture-capitalists-maui-indigenous-community-fights-land-grabs-wildifres)
- [Vacant Land Sales Around Lahaina Have Jumped Since The Wildfires — Honolulu Civil Beat](https://www.civilbeat.org/2024/05/vacant-land-sales-around-lahaina-have-jumped-since-the-wildfires/)
- ['Ea' highlights Lahaina family's legal battle to protect ancestral kuleana lands — Maui News](https://www.mauinews.com/news/local-news/2026/04/ea-highlights-lahaina-familys-legal-battle-to-protect-ancestral-kuleana-lands/)
- [Kuleana rights — Wikipedia](https://en.wikipedia.org/wiki/Kuleana_rights)
- [In Pieces: A Family's Kuleana Land in Hawaiʻi — Places Journal](https://placesjournal.org/article/in-pieces-kuleana-lands-hawaii/)
- [A Year After Maui Fire, Housing Shortage Persists — Weather.com](https://weather.com/news/news/2024-08-07-maui-lahaina-wildfire-housing-shortage-vacation-rentals)
- [Hawaiʻi's homeless rate soars to worst in nation after Lahaina wildfire — Maui Now/UHERO](https://mauinow.com/2025/05/14/hawaiis-homeless-rate-soars-to-worst-in-nation-after-lahaina-wildfire-uhero-reports/)
- [Maui Wildfires 3 Years Later: Lahaina Recovery Continues — Honolulu Civil Beat](https://www.civilbeat.org/2026/08/maui-wildfires-3-years-later-anniversary-lahaina-recovery-continues/)
- [County releases recovery update ahead of 2023 Maui Wildfires anniversary — Maui Now](https://mauinow.com/2026/08/07/county-releases-recovery-update-ahead-of-2023-maui-wildfires-anniversary/)
- [FEMA National Risk Index data](https://www.fema.gov/about/openfema/data-sets/national-risk-index-data)
- [Maui Wildfires Mitigation Assessment Team Compendium Report P-2425 — FEMA](https://www.fema.gov/sites/default/files/documents/fema_rsl_p2425_maui-mat-compendium_06052025.pdf)
- [Hawaii Wildfires disaster declaration (DR-4724-HI) — FEMA](https://www.fema.gov/disaster/4724)
- [CDC/ATSDR Social Vulnerability Index](https://www.atsdr.cdc.gov/place-health/php/svi/index.html)
- [Parcels - Maui County — Hawaii Open Data](https://opendata.hawaii.gov/dataset/parcels-maui-county)
- [The Inter-regional Economic Impact of the Reduction in Tourism Following the Maui Wildfires — UHERO](https://uhero.hawaii.edu/the-inter-regional-economic-impact-of-the-reduction-in-tourism-following-the-maui-wildfires/)
- [Kula Community Association — About Upcountry](https://www.kulamaui.org/about-upcountry)
