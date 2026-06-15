# Albay SVI Tool — Session Notes
**Date:** June 3, 2026  
**File:** `index.html` (single-file interactive map)

---

## What We Worked On

### 1. Failure Modes Tab — Full Build

The biggest build of the session. Went from a stubbed left-panel accordion to a full visual simulation experience.

**Architecture decisions:**
- Left panel: compact intro text only — controls moved to right panel
- Right panel (600px wide): controls + all analytical content
- Two floating map cards replace the legend when in failure mode
- Map centers on Mayon via `flyTo` on tab entry

**Right panel layout (top to bottom):**
1. Alert level selector (2/3/4/5 tiles, active one highlighted in level color)
2. "What breaks next?" cascade toggle grid (5 system icons, clickable)
3. Historical parallel (closest real Albay event for selected level)
4. Cascade flow diagram (🌋→🚗→⚡→🏥→💧→📄, active nodes lit in system color)
5. Compound failure warning (appears when 2+ cascades active, with specific cross-system sentences)
6. Evacuation zone table (municipality, population, informal tenure %)
7. Cascade detail cards (per active cascade, left-bordered in system color)
8. NGO/Responder action cards (operational guidance per cascade, addressed to specific audiences)

**Floating map cards:**
- `#fail-summary` (bottom-right): alert level badge, 3 stat tiles (LGUs out, people affected, informal tenure), "Who gets left behind" count
- `#fail-timeline` (top-right, where legend was): escalation timeline T+0 through T+36h, dots light up in cascade color when toggle is active

**"Who gets left behind" calculation:**
People simultaneously: in evacuation zone + informal tenure + (if road cascade active) isolated from nearest aid center. Displayed as the headline number on the summary card.

**Historical parallels by level:**
- Level 2: January 2023 — advisory only, no evacuation
- Level 3: June 2023 — 12,000 displaced, ~4,200 informal households screened out of aid
- Level 4: January 2018 — 90,000 displaced, 56-day event, lahar channels active
- Level 5: November 2006 Reming/Durian — 1,266 dead, tenure documentation gap affected recovery for 10+ years

**Cascade content (5 systems × 4 alert levels = 20 content blocks):**
Each system (road, power, health, water, tenure) has specific status labels and bullet points for each alert level (2–5), grounded in actual Albay infrastructure data.

**NGO action cards:** Per active cascade, addressed to specific responder audiences:
- Road → NGOs with shelter/NFI pre-positioning
- Power → Emergency logistics / OCHA / DRRMO
- Health → DOH Region V / health cluster leads
- Water → WASH cluster
- Tenure → IOM HLP / DSWD field officers / NGO shelter leads

---

### 2. Map Overlays for Failure Mode

Replaced scattered dot markers with geographic polygon highlights and proper lahar corridors.

**Per cascade:**
- **Alert level** — affected municipality boundaries glow in alert color (dashed outline)
- **Road cascade** — lahar flow corridors as thick dashed lines with soft glow: Miisi Gully, Buyuan River, Bonga Gully, Padang River. Affected municipalities highlighted in blue.
- **Power cascade** — municipalities losing grid power highlighted in yellow, scaled by alert level
- **Health cascade** — evacuation zone municipalities highlighted green; single clean Bicol Medical Center marker
- **Water cascade** — municipalities losing water access highlighted cyan
- **Tenure cascade** — barangay-level polygons highlighted purple, intensity scaled by informal tenure rate

Municipality and barangay polygon styles are reset to default when overlays are cleared.

---

### 3. Layer System Overhaul

Major rework of how vulnerability/hazard layers score and display.

**Scoring formula (final):**
```
raw_score = physNorm + socNorm × frac × 1.4
```
- Physical: weighted average of active hazard dims (pvol=1.5, ptyph=1.2, pfl=1.0)
- Social: weighted average of active social dims, added ON TOP of physical
- Raw scores can exceed 1.0 — `normalize()` spreads the range
- Areas high on BOTH physical AND social accumulate higher raw scores

**Composite view:** Reset preset — clears all individual layers, shows pre-blended `calcPhys × 0.5 + calcSoc × 0.5`. Labeled distinctly (italic, "ALL FACTORS" sublabel, subtle border) and auto-deselects when any individual layer is clicked.

**Spatial precision boosts in `hexScore()`:**
| Area | Boost |
|------|-------|
| Rapu-Rapu island (lng > 124.05) | +0.18 isolation, +0.10 typhoon |
| Eastern island chain | +0.12 isolation, +0.08 typhoon |
| Oson NHA site (z=4.54) | +0.18 housing within 1.5km |
| Miisi NHA site (z=4.19) | +0.16 housing within 1.5km |
| Cullat/Pinabobong NHA sites | +0.11/0.13 housing |

**Hex tooltips:** Per-hex risk breakdown on hover — computes volcanic proximity, coastal surge, and social factors at the specific hex centroid and shows only factors above threshold.

**Layer checkboxes → map:** `toggleHazDim` and `toggleSocDim` both call `scheduleRegen(0)` so the hex grid updates immediately when layers are toggled.

---

### 4. Sidebar Structure

Restructured the layer control panel into three sections:

| Section | Contents | Initial state |
|---------|----------|---------------|
| **Hazard Layers** | Composite view, Volcanic exposure, Typhoon exposure, Lahar & flood risk | Composite pre-checked |
| **Vulnerability Layers** | Tenure, Social, Elderly, Access isolation, Physical connectivity, Livelihood disruption | All unchecked |
| **Map Overlays** | PDZ/EDZ rings, Lahar channels, Typhoon tracks, Storm surge zones, NHA sites | PDZ rings pre-checked |

Layer hover tooltips show top 3 most/least exposed municipalities per dimension.

---

### 5. Tab Panel Reset

When switching tabs, the right panel now resets cleanly:
- **Entering fail mode**: closes any open municipality panel, resets `_selectedMuni`, widens panel to 600px, hides legend, centers map on Mayon, shows failure mode default
- **Leaving fail mode**: restores 380px panel width, shows legend, hides floating fail cards, clears map overlays, closes right panel
- **Switching between non-fail tabs**: closes right panel (user must click a municipality to reopen)

---

### 6. Legazpi City — IOM Pilot

- Added "Rosa, 39" story to the human stories section — IOM LandLedger pilot framing, urban informal tenure, first successful DSWD registration using LandLedger document
- Added Legazpi City to "Key communities to explore" quick-nav with "IOM Pilot" badge, positioned first in list

---

## Key Design Decisions

| Decision | What We Chose | Why |
|----------|--------------|-----|
| Failure mode controls location | Right panel (not left) | Left panel too cramped; right panel has room for visual layout |
| Floating cards on map | Scenario summary + timeline | Separates "what is happening" (map) from "what to do" (panel) |
| Cascade system | Option A — always contextualised within alert level | More coherent for volcanic risk tool; interesting story is always compound failure during eruption |
| Map overlays | Municipality polygon highlights + lahar corridor lines | Point markers were noisy and didn't show geography; polygon highlights show affected areas clearly |
| Hex grid as choropleth | Kept hex grid, barangays as click targets | Hex grid has spatial precision; barangay centroid scoring lost too much within-municipality variation |
| Scoring formula | Additive physical + social (can exceed 1.0) | Rewards areas high on multiple dimensions; normalization then spreads the range |

---

## Files Modified
- `/svi-Phil/index.html` — all changes in one file
- `/svi-Phil/SESSION_NOTES_2026-06-02.md` — previous session notes
- `/svi-Phil/SESSION_NOTES_2026-06-03.md` — this file

---

## Next Session Priorities

### Must-do
- **Verify NGO/Humanitarian tags in `_buildPhase`** — edit adding `<span class="rp-ngo-tag">Humanitarian</span>` to specific phased guidance items failed in an earlier session. CSS class is in place, tags need re-applying.
- **Review Legazpi City in Analyze panel** — given it's the IOM pilot focus, confirm barangay-level scores and panel content are representative.
- **Land Tenure tab** — already has solid content skeleton; needs: richer data specificity (actual LandLedger enrollment numbers, DSWD acceptance rates), and better visual representation beyond text lists.

### Nice-to-have
- **Resilience nodes** — pull from accumulated research (APSEMO doctrine, IOM LandLedger, PMC/NHA studies, evacuation behavior thesis) and populate the Resilience tab anchor institutions section. Quick content pass.
- **First-use onboarding** — "how to read this map" moment for new users: color scale, composite vs individual layers, how to use the panel.
- **Failure mode polish** — the `0k` showing in stats before an alert level is selected looks odd; could show `—` instead. Also consider whether the cascade toggles should be disabled-looking (greyed) until an alert level is selected.
