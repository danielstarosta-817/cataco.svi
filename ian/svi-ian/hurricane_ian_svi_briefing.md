# Hurricane Ian SVI Tool — Project Briefing
*Paste this at the start of a new chat to resume work on this project.*

---

## What This Is

A parallel extension of the Puerto Rico Social Vulnerability & Hazard Intelligence tool — a single-file `index.html` interactive map — for **Lee County and Immokalee (Collier County), Florida**, anchored to Hurricane Ian's landfall on September 28, 2022. It is the third of the four US SVI tools (after Western NC/Helene, alongside Almeda and Lahaina) and shares the same underlying US federal data infrastructure as the others: FEMA NRI/OpenFEMA, CDC/ATSDR SVI, Census/ACS, USDA agricultural data.

Like Western NC, this build sits in an English-language, US-regulatory data context, so federal open data is rich and current. Unlike Western NC — which is built around one narrative wrinkle (the climate-haven reversal, with the undocumented-farmworker exclusion as a secondary layer underneath it) — Ian's tool has to hold **two simultaneous, nearly non-overlapping disasters produced by the same storm**: a slow-motion insurance-market collapse battering the retiree/transplant coast, and a documentation-status exclusion trap battering inland farmworkers, with almost no population experiencing both.

---

## Why Lee County & Immokalee

1. **The insurance collapse is the sharpest, most quantifiable thread in the entire four-tool US shortlist.** Ian caused an estimated $50–65B in insured losses. Six Florida-domiciled insurers were declared insolvent in 2022, and roughly 15 more stopped writing new business or exited the state outright. Lee County alone generated 272,299 insurance claims — more than a third of every claim filed statewide from the storm (Florida Office of Insurance Regulation data). Citizens Property Insurance Corporation, the state's statutory "insurer of last resort," swelled toward 1.1M+ policies despite being designed as a backstop, not a primary market. In Fort Myers Beach, premiums nearly doubled — roughly $9,000 to $14,000/year — between 2019 and 2024. This is not a one-time payout event; it's an ongoing structural market failure still reshaping who can afford to live on this coast, years after the storm.

2. **A documentation-status exclusion trap, identical in mechanism to Western NC and Almeda, recurs here inland in Immokalee.** Of Florida's roughly 700,000 farmworkers, an estimated half are undocumented and structurally ineligible for FEMA Individual Assistance. Immokalee's farmworkers absorbed the same wind and flooding as coastal Lee County — many living in mobile homes and trailers with less structural resilience than site-built housing — with almost none of the same path into the federal recovery system that homeowners 30 miles away were using (however imperfectly). This is the third independent appearance of the same trap across the four US tools (Almeda's manufactured-home farmworkers, Helene's Christmas-tree/poultry/dairy workers, now Immokalee's field labor) — worth building once, well, and reusing rather than re-deriving.

3. **"Twenty minutes apart, the same storm produced two entirely different disasters" is a genuinely distinct analytical shape, not just a regional variant of Western NC's climate-haven story.** Western NC's tension is one population (recent transplants) misreading one hazard (flood risk) that a mountain community always knew about. Ian's tension is two *different* populations experiencing two *different failure systems* — one economic and multi-year (insurance), one legal-status and immediate (FEMA eligibility) — triggered by the identical physical event, sorted almost entirely by asset ownership and legal status rather than by storm intensity. A retiree in a Fort Myers Beach condo and a farmworker in an Immokalee trailer park could have experienced comparable wind and water; what diverged completely was which recovery system they had a door into.

4. **Elderly, power-dependent residents add a third, quieter failure mode specific to Lee County's demographic profile.** Of Florida's 149 Ian deaths, 72 occurred in Lee County alone, and nearly all were among residents over 50 — many tied to assisted-living residents whose electric medical devices lost power. (Death-toll figures vary somewhat by source and by direct/indirect classification methodology; the Florida Medical Examiners Commission's own running tallies have differed from later consolidated counts. The range across credible sources is roughly 50–72 Lee County deaths — still the highest of any Florida county from this storm, and still overwhelmingly among older residents.) This is an adaptive-capacity story about infrastructure dependency, distinct from both the insurance-affordability story and the documentation-exclusion story.

5. **Damage is wildly uneven at a hyper-local scale that only tract- or parcel-level resolution can show.** Poinsettia Mobile Home Park in Fort Myers — 300+ homes, mostly retirees — was devastated, while Lazy J Mobile Home & RV Park sat roughly 200 yards away across Ortiz Avenue with only minor damage. This is not a barrier-island-vs-mainland story; it's two parks on the same street with opposite outcomes. A county- or even zip-level tool would average this exact contrast away — the same lesson documented in the Albay municipality-centroid trap and applied in the Western NC tract-level build.

---

## The Anchor Event

### Hurricane Ian — September 28, 2022
- Made landfall near Cayo Costa, Lee County, as a Category 4 storm with ~150 mph sustained winds — one of the strongest hurricanes ever to hit the Florida coast
- Storm surge of 10–15 feet along the immediate coast; Fort Myers, Cape Coral, and Naples were hit hardest by surge
- Lee County: 5,000+ homes destroyed outright, nearly 30,000 more damaged
- San Carlos Island (Fort Myers Beach) — Florida's largest shrimping fleet at the time — had most of its ~40 boats pushed ashore into mangroves, parking lots, and buildings; a $8.45M state-contracted marine recovery operation was required just to re-float the fleet
- Statewide: 149 confirmed deaths, Lee County alone accounting for the largest share (72 per the county's own tally; other credible tallies run somewhat lower — see note above), nearly all among residents over 50
- $50–65B in insured losses statewide; among the costliest single storms in US history

### The Two Tracks That Followed
- **Coastal Lee County:** an insurance-market collapse that outlasted the storm itself by years — six insurer insolvencies, Citizens Property Insurance ballooning past 1.1M policies, premiums nearly doubling in the hardest-hit zip codes, and a slow, still-ongoing rebuilding fight in Fort Myers Beach over FEMA's 50%-substantial-damage rule and base flood elevation compliance (FEMA flagged the town in December 2024 for failing 3 of 5 National Flood Insurance Program Community Rating System criteria, threatening loss of the town's 25% flood-insurance discount)
- **Inland Immokalee (Collier County):** the same wind and flooding hit a population of largely undocumented farmworkers with almost no path into FEMA Individual Assistance; the Redlands Christian Migrant Association and Farmworker Association of Florida stepped into the resulting aid gap, while already-scarce Immokalee rents rose further in the storm's aftermath

---

## Core Analytical Tension

Hurricane Ian did not produce one disaster that hit some people harder than others. It produced two structurally separate disasters, roughly 30 miles apart, that shared a storm track and nothing else. Coastal Lee County's crisis was economic and slow: a market-level insurance collapse that primarily threatens the ability of legally-resident, asset-owning, often older homeowners to keep affording the place they already lived — a population with every formal right to every recovery program that exists, watching the market itself fail around them anyway. Immokalee's crisis was immediate and exclusionary: farmworkers absorbing the identical hazard with structurally weaker housing and almost no formal right to the recovery system serving the county next door.

The tool's job is to hold both of these as real, quantifiable, and simultaneous — not to rank which population "had it worse," but to show that the same physical event sorted its survivors into two nearly non-communicating systems of consequence, split along documentation status and asset ownership rather than along wind speed or surge height.

---

## The Two-Track Trap (Key New Element vs. Prior Tools)

Every prior tool in this project has one dominant exclusion mechanism: informal land tenure (PR, Albay, Mexico), and — starting with Western NC — documentation status. Ian's tool needs **two** simultaneously-modeled failure mechanisms that barely overlap in geography or population:

**Track 1 — Insurance Market Stress (new to this project).** No prior US SVI tool has modeled an institutional/economic system failure as its own scored dimension. This sits on the **Adaptive Capacity** axis, not the Sensitivity axis: insurance access and affordability is exactly "what people can draw on to cope and recover," and Ian is the first tool where that capacity itself collapsed at a market level, independent of any individual household's preparedness. Proxy fields at tract/zip level: % of policies with Citizens Property Insurance (where available), post-Ian premium change, insurer-of-record solvency status, structure type and year built (older/non-code-compliant construction faces steeper 50%-rule exposure), flood zone designation.

**Track 2 — Documentation-Status Exclusion (reused from Western NC, not reinvented).** Same mechanism, same architecture: undocumented/visa-tied farmworkers structurally invisible to FEMA Individual Assistance. Reuse Western NC's exact pattern — USDA agricultural employment concentration + Census foreign-born/limited-English proxies as the sensitivity-layer stand-in, since direct documentation-status data doesn't exist at any public geographic resolution.

**Analytical question the tool should let a user ask:** Does a tract's *outcome* track its *hazard exposure*, or does it track which of these two systems (insurance market, immigration status) it happens to fall into? The hex grid should make it visible that some of the highest-consequence tracts are not the highest-wind or highest-surge tracts — they're the ones where hazard exposure met one of these two systemic gaps.

---

## Data Sources

### Physical Hazard
- **FEMA National Risk Index (NRI)** — county and tract level, hurricane and storm-surge-specific expected annual loss, hazard frequency, community resilience scores
- **NOAA SLOSH / National Storm Surge Risk Maps v4** — basin-level surge inundation modeling, the primary Exposure-layer source for the surge-dominant hazard model
- **NOAA/NWS Hurricane Ian best-track and wind-swath data** — landfall intensity, wind field, historical storm comparison
- **Lee County & Collier County GIS / Property Appraiser parcel data** — flood zone, structure type, mobile-home designation, year built (feeds both the surge-exposure model and the insurance/50%-rule sensitivity model)

### Social Vulnerability
- **CDC/ATSDR Social Vulnerability Index (SVI)** — census-tract level, 16-variable/4-theme composite, covers both Lee and Collier counties
- **US Census / ACS** — tract/block-group income, age (65+ share — directly relevant to the elderly/power-dependency mortality pattern), housing tenure, mobile-home share, foreign-born and limited-English share (proxy for the Immokalee farmworker population)
- **USDA NASS Census of Agriculture** — county-level baseline for Collier County farm labor, the sensitivity-layer proxy for undocumented agricultural employment exposure

### Insurance & Institutional Record
- **Florida Office of Insurance Regulation (OIR)** — insurer solvency/exit filings, Citizens Property Insurance policy-count and claims data, county-level claims counts (Lee County: 272,299 claims from Ian)
- **FEMA NFIP Community Rating System documentation** — Fort Myers Beach's December 2024 compliance flag (3 of 5 criteria failed) as a structured record of the permitting/rebuild fight
- **Town of Fort Myers Beach 50% Rule / Building Services records** — substantial-damage determinations, a direct, documentable trigger for who could rebuild as-was versus who was forced into full elevation compliance

### Aid & Institutional Record (FEMA)
- **OpenFEMA Individuals & Households Program — Valid Registrations v2** — county/zip, per-application rows (~900K total Ian registrations), the core dataset for mapping aid-uptake and denial across Lee vs. Collier counties
- **FEMA Housing Assistance Program Data — Owners v2** — zip/county repair/replacement assistance amounts
- **Redlands Christian Migrant Association (RCMA)** and **Farmworker Association of Florida** — organizational response filling the FEMA gap for Immokalee's undocumented farmworkers; qualitative/programmatic data, county-level, not tract-granular

### Community Resilience / Cultural Record
- **San Carlos Island shrimping industry record** (news archive, Lee County economic development data) — a working-waterfront community whose recovery is a direct, trackable indicator distinct from residential rebuild rates
- **University of Florida / RCMA farmworker relief partnership records** — documented aid-gap response specific to Immokalee

---

## Key Human Stories to Develop

1. **The Fort Myers Beach retiree staring down the 50% rule.** A homeowner whose insurer went insolvent, whose premium nearly doubled on whatever policy replaced it, and who now faces a choice between full elevation-compliant rebuild (often unaffordable) or losing the property — legally entitled to every recovery program that exists, undone by the market itself.

2. **The San Carlos Island shrimper.** A multigenerational fishing family whose boats were thrown into the mangroves; three years on, only one property's docks remain from a waterfront that once housed Florida's largest shrimp fleet — a slow institutional unwinding (Trico Shrimp Company's shutdown) layered on top of the physical damage.

3. **The Immokalee farmworker FEMA can't see.** A field worker who lost housing and income in the same storm making national news 30 miles away, never appearing in a FEMA registration count because applying risked exposing undocumented status — RCMA or the Farmworker Association filling a gap the federal system was never built to fill.

4. **Poinsettia vs. Lazy J, 200 yards apart.** Two mobile home parks across Ortiz Avenue from each other in Fort Myers — one devastated, one barely touched — used to visually demonstrate that hazard exposure varies at a scale finer than any zip code or even census tract, the concrete argument for why the hex grid's resolution matters.

5. **The assisted-living resident who depended on power.** One of the 72 Lee County deaths, tied to an electric medical device losing power in a county-wide outage — a story about adaptive capacity as infrastructure dependency, not documentation status or insurance affordability.

---

## Tool Architecture Decisions (Evolving from Western NC / PR)

**Evolving from Western NC's US-context build, not replicating Western NC's specific narrative layer.** Key changes:

1. **Geographic unit: census tract, spanning two counties (Lee and Collier), not county centroid.** The nearest-lookup array needs tracts covering both counties' distinct sub-geographies: Lee County's barrier islands (Sanibel, Captiva, Fort Myers Beach/Estero Island, Pine Island), Lee County's mainland (Cape Coral, Fort Myers, North Fort Myers, Iona, Bonita Springs), and Collier County's Immokalee area plus surrounding Golden Gate Estates. Same rationale as Western NC and the Albay barangay lesson: county-level resolution would flatten the Poinsettia/Lazy J contrast and the coastal/inland divergence that is the entire analytical point.

2. **Single dominant hazard (storm surge), wind as secondary sub-score.** Unlike Western NC's riverine-flood-with-historical-recurrence framing, Ian's dominant hazard is coastal storm surge (NOAA SLOSH), with hurricane wind as a secondary weighted sub-score. Inland riverine/rainfall flooding is a minor tertiary factor for this two-county footprint (unlike the Peace River backwater flooding that hit Charlotte/DeSoto counties just outside it).

3. **New "Insurance Market Stress" layer — on the Adaptive Capacity axis, not Sensitivity.** This is the genuinely new architectural element for this build (see Two-Track Trap section above): tract/zip-level proxies for insurance-market collapse (premium change, Citizens policy share where available, structure age/code-compliance exposure to the 50% rule) scored as a resilience/adaptive-capacity dimension, not as a demographic vulnerability dimension. No prior tool in this project has modeled an economic-institution failure this way.

4. **Documentation-status exclusion layer — reused verbatim from Western NC's architecture.** Same USDA agricultural employment + Census foreign-born/limited-English proxy pattern, same absence of direct documentation-status data, same analytical framing. Do not re-derive this from scratch; port the Western NC implementation and re-point it at Collier County/Immokalee fields.

5. **Language: English throughout**, with the same acknowledgment as Western NC that the excluded farmworker population is predominantly Latino/immigrant and that the narrative content should say so directly.

6. **Dual-population framing without erasing either.** Because the two tracks (insurance stress, documentation exclusion) are concentrated in almost entirely different tracts, the "Failure Modes" panel group should present them as two distinct, simultaneously-scoreable accordion entries rather than a single toggle — a user should be able to see coastal tracts light up on the insurance layer and Immokalee tracts light up on the documentation layer on the same map, without one obscuring the other.

7. **Elderly/power-dependency as a Sensitivity sub-layer**, distinct from both tracks above: 65+ population share combined with a power-outage-duration proxy (from utility restoration data if obtainable, county-level as a fallback), grounding the assisted-living/medical-device mortality story in a scored field rather than leaving it purely anecdotal.

---

## Daniel's Background Context

- Master of Development Practice, UC Berkeley 2022
- Thesis: *"Raised Under Bad Stars: Tracing the complexities of creating, transmitting, and preserving a culture of preparedness among disaster-vulnerable communities"*
- Worked on LandLedger with IOM's Housing, Land and Property team / Global Shelter Cluster
- Currently at Nubank (São Paulo)
- The Puerto Rico tool exists as a complete `index.html` (on GitHub Pages) and is the codebase all US tools evolve from
- Western NC (`wnc/svi-wnc/western_nc_svi_briefing.md`) is the most-developed prior US tool and the direct architectural precedent for this one; Almeda and Lahaina are parallel, less-developed US builds in the same project
- This document should be read alongside `phil/svi-Phil/SVI_MAP_ARCHITECTURE_GENERIC.md` (shared hex-grid/scoring architecture) before any map-building code is written

---

## Key Sources

- [Hurricane risk in Florida is escalating. Home insurance is harder to get. — NBC News](https://www.nbcnews.com/business/real-estate/hurricane-risk-florida-escalating-flood-insurance-harder-get-rcna216843)
- [Florida homeowners battle for insurance after Hurricane Ian — Context/Thomson Reuters Foundation](https://www.context.news/climate-risks/florida-homeowners-battle-for-insurance-after-ians-devastation)
- [The 'hurricane tax': How Ian is pushing Florida's home insurance market toward collapse — Grist](https://grist.org/economics/hurricane-ian-florida-home-insurance-citizens/)
- [Florida's home insurer of last resort is in serious trouble — CNN Business](https://www.cnn.com/2024/10/11/business/citizens-insurance-hurricane-milton)
- [An island unto itself: Lee County's post-Hurricane Ian destruction — University of Florida Warrington College](https://warrington.ufl.edu/news/an-island-unto-itself/)
- [Florida's migrant workers can be extremely vulnerable to natural disasters — WFSU News](https://news.wfsu.org/state-news/2024-08-09/floridas-migrant-workers-can-be-extremely-vulnerable-to-natural-disasters)
- [Hurricane Ian damages undocumented migrant communities in Florida — Yahoo News](https://news.yahoo.com/hurricane-ian-damages-undocumented-migrant-213133272.html)
- [EGH helps provide hurricane relief to farmworker families — University of Florida PHHP](https://phhp.ufl.edu/2022/10/21/egh-helps-provide-hurricane-relief-to-farmworker-families/)
- [After Hurricane Ian, Fort Myers Beach shrimping industry shrinks but hopes for rebirth — Yahoo/AP](https://www.yahoo.com/news/hurricane-ian-fort-myers-beach-090330474.html)
- [Three years after Ian: Fort Myers Beach businesses and residents rebuilding, recovering — Fort Myers Beach Talk](https://www.fortmyersbeachtalk.com/news/community-news/2025/09/three-years-after-ian-fort-myers-beach-businesses-and-residents-rebuilding-recovering/)
- [Lee Co. may rebuild Ian-damaged site once home to Florida's largest shrimping fleet — Fox 4 Now](https://www.fox4now.com/news/local-news/lee-county/lee-co-may-rebuild-ian-damaged-site-once-home-to-floridas-largest-shrimping-fleet)
- [FEMA drops hammer on Fort Myers Beach after improper rebuilding in flood area — Insurance Journal](https://www.insurancejournal.com/news/southeast/2024/12/03/803322.htm)
- [FEMA's 50% Rule — Town of Fort Myers Beach, FL, official site](https://www.fortmyersbeachfl.gov/1254/FEMAs-50-Rule)
- [Hurricane Ian wrecked a mobile home park, but spared another across the street — NBC News](https://www.nbcnews.com/news/us-news/hurricane-ian-wrecked-mobile-home-park-spared-another-street-rcna50177)
- [Ian's death toll: At least 23 fatalities in six counties, mostly older residents — Florida Phoenix](https://floridaphoenix.com/2022/10/01/ians-death-toll-at-least-23-fatalities-in-six-counties-mostly-older-residents/)
- [How they died: Medical examiners release causes of death for Ian victims — WINK News](https://www.winknews.com/news/charlotte/how-they-died-medical-examiners-release-causes-of-death-for-ian-victims/article_f1357baa-a2c3-5bbd-9a4b-9531a716e608.html)
- [FEMA National Risk Index data](https://www.fema.gov/about/openfema/data-sets/national-risk-index-data)
- [FEMA Individual Assistance Housing Registrants — Large Disasters v1](https://www.fema.gov/openfema-data-page/individual-assistance-housing-registrants-large-disasters-v1)
- [CDC/ATSDR Social Vulnerability Index](https://www.atsdr.cdc.gov/place-health/php/svi/index.html)
- [NOAA SLOSH model / storm surge hazard data](https://www.fema.gov/emergency-managers/risk-management/hurricane-wind-water-surge)
