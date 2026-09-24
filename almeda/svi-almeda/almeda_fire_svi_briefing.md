# Almeda Fire SVI Tool — Project Briefing
*Paste this at the start of a new chat to resume work on this project.*

---

## What This Is

A parallel extension of the Puerto Rico Social Vulnerability & Hazard Intelligence tool — a single-file `index.html` interactive map — for **Talent and Phoenix, Oregon**, in the Rogue Valley (Jackson County), anchored to the Almeda Fire of September 8, 2020. It is one of four US SVI tools in this project (alongside Western NC/Helene, Hurricane Ian, and Lahaina), and shares the same underlying US federal data infrastructure: FEMA NRI/OpenFEMA, CDC/ATSDR SVI, Census/ACS, USDA agricultural data.

Like Western NC and Ian, this build sits in an English-language, US-regulatory data context. But Almeda's analytical wrinkle is distinct from both: it is a **wildfire**, not a hurricane or flood, and its exclusion mechanism isn't purely documentation status (Western NC, Ian) or purely a market failure (Ian's insurance layer) — it's a **housing-tenure trap that is structurally domestic** rather than the ejido/informal-settlement tenure traps of Mexico, PR, and Albay. Manufactured-home residents in Talent and Phoenix owned their houses but not the ground under them, on lots inside privately owned mobile home parks — meaning the international tenure trap this project has documented abroad reappears, in a different legal form, inside the United States. Layered directly on top of that is the same documentation-status exclusion from FEMA aid seen in Western NC and Ian, plus a distinct new failure mode: a literal, documented emergency-alert system failure that left an entire town without evacuation warning.

---

## Why Talent & Phoenix

1. **The disproportionate impact on manufactured housing is the sharpest quantifiable thread in this build.** Of roughly 2,300–2,600 structures the Almeda Fire destroyed, an estimated 1,500–1,700 were manufactured homes spread across 18–19 mobile home parks strung along the Bear Creek corridor and Highway 99. At Talent Mobile Estates alone, nearly all 99 homes in the park were destroyed. Statewide, manufactured homes made up roughly 42% of all structures lost across Oregon's entire 2020 Labor Day fire event — this single fire corridor concentrated a hugely outsized share of that loss into two small towns.

2. **The Rogue Valley's Latino and immigrant farmworker community sat disproportionately inside that manufactured-housing footprint.** Talent's Hispanic/Latino population share (roughly 14–16.5% per Census data) is itself higher than Oregon's statewide average, and the Rogue Valley's pear-orchard, vineyard, and nursery-stock agricultural economy depends on a farmworker population concentrated in exactly the mobile home parks the fire tore through. Many of the families most affected were undocumented or had mixed-status households, placing them outside the same bank-account, insurance, and disaster-loan systems available to their neighbors.

3. **FEMA's aid-denial rate here mirrors, and for undocumented households exceeds, the pattern seen in Western NC and Ian.** FEMA denied roughly 57% of the ~27,000 individual-assistance applications filed after Oregon's 2020 wildfires (some tallies citing closer to 70% once fraud-suspect denials are included). For households with any undocumented member, the exclusion isn't a denial rate at all — it's categorical: FEMA's Individuals and Households Program and Disaster Unemployment Assistance require the applicant to be a US citizen, non-citizen national, or Qualified Alien, full stop. This is the same trap documented in Western NC and Ian, now appearing for the third time in this project's four-tool US shortlist.

4. **A documented emergency-alert failure is a distinct institutional-failure mode this project hasn't captured in this exact form.** Jackson County did not issue an emergency broadcast alert for the Almeda Fire; the town of Talent never received an evacuation alert of any kind through the county's opt-in Everbridge system. A subsequent county review cited miscommunication, understaffing, and insufficient training. This is a sharper, more literal failure than Western NC's post-disaster misinformation campaigns — this is the absence of the warning itself, for a community where many residents' primary language wasn't the one the system wasn't reaching them in anyway.

5. **The manufactured-housing tenure trap reappears here as a wholly domestic legal structure, not an informal one.** Unlike PR, Albay, or Mexico — where the trap is *informal* tenure (no title, no deed, no individual document) — the Rogue Valley's mobile home park residents held fully legal, formal ownership of their homes. What they didn't own was the land beneath them, leaving them exposed to park-owner decisions, lot-rent increases, and — after the fire — a rebuild process where the land they'd need to rebuild on wasn't theirs to control. This is a different *kind* of tenure exclusion than any prior tool in this project has modeled, even though the underlying mechanism (ownership fragmented from land) rhymes with all of them.

6. **The community's post-fire response produced a genuinely new resilience artifact for this project: resident ownership.** With CASA of Oregon's help, Talent Mobile Estates became the first resident-owned manufactured home community (ROC) in the Rogue Valley — 89 displaced households converting the park itself into a resident-governed cooperative. This is a concrete, scoreable adaptive-capacity outcome this project hasn't seen elsewhere: the tenure trap being closed, not just documented.

---

## The Anchor Event

### The Almeda Fire — September 8–15, 2020
- Started near Ashland, Oregon, on September 8, 2020, and driven by 40–45 mph wind gusts and severe drought conditions, ran roughly 15 miles north along the Bear Creek Greenway and Highway 99 corridor through Talent, Phoenix, and into south Medford
- Burned approximately 3,200 acres and destroyed 2,300–3,000+ structures (estimates vary by source and by inclusion of outbuildings/commercial property) in a matter of hours
- Roughly 1,500–1,700 of the destroyed structures were manufactured homes across 18–19 mobile home parks; Talent Mobile Estates lost nearly all 99 of its homes
- Approximately 180 commercial properties were also destroyed
- 3 confirmed deaths; approximately 8,500 people displaced
- Jackson County issued no emergency broadcast alert; the opt-in Everbridge system never reached Talent at all — one of the most-cited institutional failures of Oregon's entire 2020 Labor Day fire event
- Part of the broader September 2020 Labor Day fire event across Oregon, which together destroyed more manufactured homes (about 1,700, ~42% of all structures lost statewide) than any prior wildfire season in state history

### Five Years Later — 2025/2026 Status
- Talent has issued roughly 350 certificates of occupancy for rebuilt homes and businesses, with ~25 more permitted and about a dozen in early review — roughly 72% of lost homes rebuilt, permitted, or underway
- Phoenix has passed the halfway mark, with over half of destroyed homes rebuilt and reoccupied
- Talent's population has climbed back to roughly 6,411, close to its pre-fire ~6,600
- Vacant lots remain concentrated in downtown Talent and along the Highway 99 corridor — the same corridor where the manufactured home parks stood
- Bear Creek's streamside habitat, burned through by the fire, is undergoing a large-scale native-plant restoration effort
- Talent has been recognized nationally as a wildfire-resilience case study in the years since, even as the rebuild remains incomplete

---

## Core Analytical Tension

Talent and Phoenix sit inside an agricultural valley whose economy depends on a workforce structurally invisible to the disaster-recovery systems built around it. The fire that destroyed their homes moved through a landscape of tightly packed manufactured-home parks along a highway corridor — the exact housing type and location pattern that concentrates the Rogue Valley's lowest-income, most immigrant-heavy population into the highest-loss ground. The people who owned their homes outright, in the fullest legal sense the state recognizes, still had no claim on the land under them, no path to disaster aid if any household member lacked status, and — in Talent's case — no warning that the fire was coming at all.

The tool's job is to show that "manufactured housing" is not a neutral housing-type category the way a choropleth might imply — it is where a specific legal tenure structure (own the house, lease the land), a specific labor economy (Rogue Valley agriculture), a specific documentation-status exclusion (FEMA eligibility), and a specific institutional failure (the alert system) all stacked on the same parcels, along the same highway, in the same afternoon.

---

## The Manufactured Housing Tenure Trap (Key New Element vs. Prior Tools)

Every prior tool in this project has one dominant exclusion mechanism layered onto a physical hazard: informal land tenure (PR, Albay, Mexico), and — starting with Western NC and continuing through Ian — documentation status. Almeda needs **two** simultaneously-modeled tracks, plus a third institutional-failure layer, none of which fully replicate Western NC or Ian's architecture:

**Track 1 — Manufactured Housing Land Tenure (new to this project).** Unlike the informal/undocumented tenure traps abroad, mobile home park residents in Talent and Phoenix held fully formal title to their homes — the exclusion is structural, not documentary. Residents lease the lot from a private park owner, meaning rebuild eligibility, timeline, and even whether the park reopens at all depends on a landlord's decision the resident has no legal claim over. Proxy fields at tract/parcel level: mobile-home-park density, park ownership type (private landlord vs. resident-owned/ROC), lot-rent burden, and rebuild-permit status by park. CASA of Oregon's ROC conversions (Talent Mobile Estates and others since) provide a positive, scoreable counter-indicator: a park where residents converted to cooperative ownership scores differently on adaptive capacity than one still under private-landlord control.

**Track 2 — Documentation-Status Exclusion (reused from Western NC and Ian, not reinvented).** Same mechanism, same architecture: undocumented and mixed-status farmworker households structurally ineligible for FEMA's Individuals and Households Program and Disaster Unemployment Assistance. Reuse the Western NC/Ian pattern verbatim: USDA agricultural employment concentration plus Census foreign-born/limited-English proxies as the sensitivity-layer stand-in for documentation status, since no direct dataset exists at any public geographic resolution.

**Track 3 — Emergency Alert Failure (new to this project, distinct from Western NC's misinformation layer).** Western NC's institutional-failure mode was a wave of active misinformation competing with real aid messaging after the storm. Almeda's failure predates that: the warning itself never arrived. This should be modeled as a scored or flagged sensitivity sub-dimension — alert-system opt-in vs. opt-out coverage, language capability at time of event (English-only in 2020; Jackson County has since added Spanish-language capability and integrated with the state alert program), and documented gaps in specific zones (Talent's zero-alert status is the sharpest, most citable data point).

**Analytical question the tool should let a user ask:** Does a parcel's outcome track its physical wildfire exposure, or does it track which of these three systems — land tenure, documentation status, or alert coverage — it happened to fall into? The hex grid should make visible that the highest-consequence ground wasn't necessarily the highest fire-behavior-modeled ground — it was where fire risk met a manufactured-home park, an undocumented household, and a warning system that never fired.

---

## Data Sources

### Physical Hazard
- **FEMA National Risk Index (NRI)** — county and census-tract level wildfire-specific expected annual loss, hazard frequency, and community resilience scores; Jackson County ranks among the highest-risk counties nationally by wildfire expected annual loss rate. Downloadable via OpenFEMA / hazards.fema.gov/nri
- **Oregon Statewide Wildfire Hazard Map (ODF, mandated under SB 762, public since June 2022)** — parcel-level wildfire hazard classification (extreme/high/moderate/low/no-risk in the underlying methodology; public-facing map simplified to low/moderate/high); useful as an independent cross-check against FEMA NRI for the Rogue Valley
- **Jackson County GIS — Almeda Drive Fire Official perimeter and Wildfire Hazard Areas layers** — the actual fire footprint and county-level hazard zoning, directly overlayable on Talent/Phoenix parcels
- **NOAA/NWS historical wind and drought data** — the 40–45 mph wind-gust and drought conditions that drove the fire's speed, useful for framing fire-weather context

### Social Vulnerability
- **CDC/ATSDR Social Vulnerability Index (SVI)** — census-tract level, 16-variable/4-theme composite, covering Jackson County
- **US Census / ACS** — tract/block-group income, mobile-home housing-type share, Hispanic/Latino population share, foreign-born and limited-English share (the proxy layer for the undocumented/mixed-status farmworker population, same pattern as Western NC and Ian)
- **USDA NASS Census of Agriculture** — Jackson County baseline for pear, vineyard, and nursery-stock agricultural employment — the sensitivity-layer proxy for farmworker labor concentration in and around Talent/Phoenix

### Housing Tenure & Institutional Record
- **CASA of Oregon** — resident-owned manufactured home community (ROC) conversion records, including Talent Mobile Estates (89 households, first ROC in the Rogue Valley) and subsequent conversions; the direct data source for the Track 1 tenure-trap scoring and its positive counter-indicator
- **Jackson County mobile home park registry / Oregon manufactured dwelling park records** — park ownership type (private landlord vs. resident-owned), lot count, and rebuild-permit status by park
- **City of Talent and City of Phoenix rebuild-permit dashboards** — certificates of occupancy issued, active permits, and parcels still vacant, supporting the five-years-later recovery-progress framing
- **Jackson County Emergency Management after-action review** — the documented record of the Everbridge alert failure, understaffing, and miscommunication findings; the core source for the Track 3 alert-failure layer

### Aid & Institutional Record (FEMA)
- **OpenFEMA Individuals & Households Program — Valid Registrations** — the core dataset for mapping the ~27,000 applications and 57% (or higher, depending on methodology) denial rate across Jackson County
- **UNETE Center for Farm Worker and Immigrant Advocacy** — direct-assistance and Homeowner Assistance and Reconstruction Program (HARP) records; UNETE estimates having helped 700+ families through the full recovery process, a documentable record of the aid gap FEMA left and who filled it
- **Coalición Fortaleza** — BIPOC-led coalition formed directly out of the Almeda Fire response, focused on land, housing, and community-space solutions for displaced Latinx and Indigenous families; organizational record of the community-driven recovery track parallel to (not inside) the FEMA system

### Community Resilience / Cultural Record
- **Proud Ground / New Spirit Village** — community land trust development (~87 affordable homes, ~$28M project) built specifically for Almeda Fire survivors in Medford, a direct positive-resilience data point
- **Rogue Climate and Rogue Action Center** — community organizing and long-term recovery advocacy records
- **Ashland Climate Collaborative "Lessons Learned from the Almeda Fire"** — structured post-fire review, useful as a Cultural Record-layer source alongside the county's own after-action findings

---

## Key Human Stories to Develop

1. **The Talent Mobile Estates resident who now owns the park.** A household displaced when nearly all 99 homes in Talent Mobile Estates burned, now part of the Rogue Valley's first resident-owned manufactured home cooperative — the tenure trap not just documented but closed, through CASA of Oregon's ROC model. A concrete, positive counterweight to the exclusion stories in every other tool in this project.

2. **The farmworker family FEMA can't see, again.** A mixed-status household on one of the Bear Creek corridor's mobile home lots, working Rogue Valley pear orchards or vineyards, who lost everything in the fire but never appears in a FEMA registration count — the same trap as Western NC's Christmas-tree workers and Ian's Immokalee field labor, now in its third US appearance, filled instead by UNETE and Coalición Fortaleza.

3. **The Talent resident who got no warning at all.** A household in the path of the fire who received no Everbridge alert, no emergency broadcast — not a bureaucratic exclusion or a documentation-status gap, but a literal absence of warning in a town the county's own after-action review found under-resourced and under-trained to protect.

4. **The park that didn't come back.** Not every one of the 18–19 destroyed mobile home parks has rebuilt at the same pace; some sit as vacant lots along Highway 99 five years on, a landlord decision the residents who once lived there had no legal standing to contest — the sharpest illustration of Track 1's tenure trap.

5. **The five-years-later return.** A family that left the Rogue Valley after the fire — priced out, discouraged by the slow rebuild, or unable to find another lot — set against a family that stayed and is now moving back into a rebuilt or resident-owned home; Talent's population has recovered to near pre-fire levels, but not household-by-household, and not evenly across tenure types.

---

## Tool Architecture Decisions (Evolving from Western NC / Ian)

**Evolving from the US-context build pattern established by Western NC and Ian, not replicating either's specific narrative layer.** Key changes:

1. **Geographic unit: census tract or parcel, not county or city.** Given the extreme concentration of loss along the Bear Creek/Highway 99 corridor and the park-by-park variation in rebuild status, county- or even city-level resolution would repeat the Albay municipality-centroid trap documented in the generic architecture doc. The nearest-lookup array should be built from CDC/ATSDR SVI tracts for the Talent/Phoenix/south Medford corridor, ideally with individual mobile home park locations as point overlays given how much the analytical argument depends on park-level tenure status.

2. **Single dominant hazard (wildfire), no multi-hazard toggle needed.** Unlike Mexico's three-hazard toggle or Ian's surge/wind split, Almeda is a single-hazard tool — wildfire spread along a wind-driven, drought-primed corridor. Historical wildfire frequency for the Rogue Valley (rather than a second hazard type) can serve as the framing device, similar to how Western NC used 1916/2004/2024 flood recurrence.

3. **New "Manufactured Housing Tenure" layer — on the Sensitivity axis, distinct from Ian's Insurance Market Stress layer.** This is the genuinely new architectural element for this build: park-level (or tract-level, aggregated) fields for mobile-home-park density, ownership type (private landlord vs. ROC/resident-owned), and lot-rent burden. Unlike Ian's insurance layer (an economic/adaptive-capacity dimension), this is closer to the international tenure-trap dimension (PR/Albay/Mexico) reimagined for a formal-but-fragmented US ownership structure — it should sit on Sensitivity, with ROC conversion status as a positive Adaptive Capacity counter-indicator layered on top.

4. **Documentation-status exclusion layer — reused verbatim from Western NC and Ian.** Same USDA agricultural employment + Census foreign-born/limited-English proxy pattern, same absence of direct documentation-status data, same analytical framing. Port the existing implementation and re-point it at Jackson County/Rogue Valley agricultural fields (pear, vineyard, nursery stock in place of Christmas tree/poultry/dairy or Immokalee field labor).

5. **New "Alert System Failure" flag — a scored or binary sensitivity sub-layer distinct from Western NC's misinformation layer.** Western NC modeled active misinformation competing with real recovery messaging; Almeda's failure is the prior step — no warning reaching the household at all. Score at tract/park level using the documented Everbridge/emergency-broadcast gap (Talent's zero-alert status is the clearest concrete data point) rather than treating it as a narrative-only footnote.

6. **Language: English throughout**, with the same acknowledgment as Western NC and Ian that the excluded population is predominantly Latino/immigrant, and that Jackson County's post-fire addition of Spanish-language alert capability should be presented as a resolved (not ongoing) gap, distinct from the still-open documentation-status and tenure gaps.

7. **Resident-Owned Community (ROC) status as a first-class Adaptive Capacity field**, not a footnote — this project's first concrete example of a community actively closing a tenure trap rather than merely being exposed by one, and worth surfacing prominently in the "What is already working?" / Resilience panel group.

---

## Daniel's Background Context

- Master of Development Practice, UC Berkeley 2022
- Thesis: *"Raised Under Bad Stars: Tracing the complexities of creating, transmitting, and preserving a culture of preparedness among disaster-vulnerable communities"*
- Worked on LandLedger with IOM's Housing, Land and Property team / Global Shelter Cluster
- Currently at Nubank (São Paulo)
- The Puerto Rico tool exists as a complete `index.html` (on GitHub Pages) and is the codebase all US tools evolve from
- Western NC (`wnc/svi-wnc/western_nc_svi_briefing.md`) and Hurricane Ian (`ian/svi-ian/hurricane_ian_svi_briefing.md`) are the most-developed prior US tools and the direct architectural precedents for this one; Lahaina is a parallel, less-developed US build in the same project
- This document should be read alongside `phil/svi-Phil/SVI_MAP_ARCHITECTURE_GENERIC.md` (shared hex-grid/scoring architecture) before any map-building code is written

---

## Key Sources

- [Almeda Drive Fire — Wikipedia](https://en.wikipedia.org/wiki/Almeda_Drive_Fire)
- [FEMA denied most Oregonians' requests for wildfire disaster assistance — OPB](https://www.opb.org/article/2021/02/11/oregon-2020-wildfires-fema-disaster-aid-denied/)
- [FEMA aid limited for undocumented immigrants — Mail Tribune](https://www.mailtribune.com/news/top-stories/fema-aid-limited-for-undocumented-immigrants/)
- [Latinx immigrants severely impacted by the devastating Almeda fire — KXLH](https://www.kxlh.com/news/national/latinx-immigrants-severely-impacted-by-the-devastating-almeda-fire-in-southern-oregon)
- [After the Almeda Fires, Oregon Fights for Food Access for Immigrants — YES! Magazine](https://www.yesmagazine.org/climate/2024/12/18/almeda-fires-food-justice-immigrants)
- [Jackson County's emergency alert system left many without warnings during the Almeda Fire — OPB](https://www.opb.org/article/2020/09/21/wildfire-almeda-fire-southern-oregon-emergency-alerts/)
- [No evacuation Everbridge alert sent for Talent during Almeda fire — KOBI-TV](https://kobi5.com/news/no-evacuation-everbridge-alert-sent-for-talent-during-almeda-fire-137966/)
- [Emergency Broadcast Alerts Never Issued For Almeda Fire — Jefferson Public Radio](https://www.ijpr.org/wildfire/2020-09-16/emergency-broadcast-alerts-never-issued-for-almeda-fire)
- [Almeda Fire survivors to form first resident-owned manufactured home park in the Rogue Valley — KLCC](https://www.klcc.org/2022-09-08/almeda-fire-survivors-to-form-first-resident-owned-manufactured-home-park-in-the-rogue-valley)
- [Seeking solutions for slow post-fire rebuilding of manufactured home parks in Southern Oregon — OPB](https://www.opb.org/article/2021/10/21/seeking-solutions-for-slow-post-fire-rebuilding-of-manufactured-home-parks-in-southern-oregon/)
- [Introducing our newest member, Coalición Fortaleza — OJTA](https://www.ojta.org/blog/coalicion-fortaleza)
- [Partner Spotlight: Coalición Fortaleza — Oregon Food Bank](https://www.oregonfoodbank.org/posts/partner-spotlight-coalicion-fortaleza)
- [Wildfire relief for people of color aimed at building stronger community for long term — OPB](https://www.opb.org/article/2021/05/21/wildfire-relief-for-people-of-color-aimed-at-building-stronger-community-for-long-term/)
- [UNETE, OGC Mission Fund Recipient — Organically Grown Company](https://www.organicgrown.com/blog/unete-ogc-mission-fund-recipient)
- [New affordable housing for fire survivors coming to the Rogue Valley — KTVL](https://ktvl.com/news/local/new-affordable-housing-coming-rogue-valley-medford-phoenix-almeda-obenchain-fire-survivors-oregon-access-community-property-home-royaloaks-mobilemanor)
- [Almeda Fire recovery brings affordable housing to Medford, Gov. Kotek attends opening — KDRV](https://www.kdrv.com/news/housing-crisis/almeda-fire-recovery-brings-affordable-housing-to-medford-gov-kotek-attends-opening/article_668e2c34-503c-11ef-8454-c3be7a3ca257.html)
- ['I think we're getting there': Almeda Fire recovery efforts continue in Phoenix, Talent — The Bulletin](https://bendbulletin.com/2025/09/03/i-think-were-getting-there-almeda-fire-recovery-efforts-continue-in-phoenix-talent/)
- [What fire recovery looks like in Talent, Oregon — OPB](https://www.opb.org/article/2025/01/27/wildfire-recovery-oregon-almeda-talent/)
- [Almeda Fire, Five Years After: Talent community reemerges as a nationally recognized leader in wildfire resilience — Ashland News](https://ashland.news/almeda-fire-five-years-after-talent-community-reemerges-as-a-nationally-recognized-leader-in-wildfire-resilience/)
- [Five Years After the Almeda Fire, Some Families Still Waiting to Come Home — KOBI-TV](https://kobi5.com/news/five-years-after-the-almeda-fire-some-families-still-waiting-to-come-home-282848/)
- [The Almeda Fire burned through Bear Creek. Now native plants are taking hold — Jefferson Public Radio](https://www.ijpr.org/environment-energy-and-transportation/2025-09-07/bear-creek-recovery-post-almeda-fire)
- [2 Almeda Fire survivors share why they left Southern Oregon — and why 1 is coming back — OPB](https://www.opb.org/article/2025/08/26/almeda-fire-phoenix-talent-oregon-recovery/)
- [Talent Almeda Fire Opportunity Framework — Oregon APA](https://oregon.planning.org/community/capp/services-and-resources-for-wildfire-recovery/talent-almeda-fire-opportunity-framework/)
- [Wildfire Risk By Market: What FEMA Data Reveals — Cove](https://cove.inc/blog/wildfire-risk-by-market-fema-data-2026-part-1/)
- [FEMA National Risk Index data](https://www.fema.gov/about/openfema/data-sets/national-risk-index-data)
- [Oregon Statewide Wildfire Hazard Map](https://hazardmap.forestry.oregonstate.edu/)
- [CDC/ATSDR Social Vulnerability Index](https://www.atsdr.cdc.gov/place-health/php/svi/index.html)
