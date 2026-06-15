# Albay SVI Tool — Session Notes
**Date:** June 2, 2026  
**File:** `index.html` (single-file interactive map)

---

## What We Worked On

### 1. UI Polish — Right Panel Header
- Fixed the `MUNICIPALITY · ALBAY PROVINCE` eyebrow text and subtitle (Pop / road risk / power restore) — both were using `#475569`, nearly invisible on the dark background. Changed to `#7a9cc0`.
- Fixed the (×) close button: was positioned with `margin-top:4px` making it awkward. Changed to `align-self:center` on the flex row.

---

### 2. Vulnerability Layer Fixes

**Compounding wasn't working.**  
When multiple vulnerability layer checkboxes were checked, the map wasn't changing because `updateBrgyColors()` was falling back to a single hardcoded `BE.soc` field for all multi-layer cases instead of computing across checked dims.

Fixed by building a proper `activeBeIdxs` array from all checked dims and averaging across them.

**Layer checkboxes didn't update the map when the right panel was open.**  
`toggleSocDim` was calling `updateBrgyColors()` before `openPanel()`, and `openPanel()` calls `selectBarangayBoundary()` which resets all barangay fills to transparent. Fixed by moving `updateBrgyColors()` to after `openPanel()`.

**"Access isolation" and "Physical connectivity" were identical.**  
Both mapped to `BE.isolation`. Fixed by mapping `svi_road → BE.road_iso` and `svi_cell → BE.isolation` — genuinely different fields.

---

### 3. Hazard Layers Redesign

Restructured the sidebar from two sections into three:

| Before | After |
|--------|-------|
| Hazard Layers (PDZ rings, lahar channels, etc.) | **Hazard Layers** (Volcanic exposure, Typhoon exposure, Lahar & flood risk) — drive choropleth |
| Vulnerability Layers | **Vulnerability Layers** — unchanged |
| *(nothing)* | **Map Overlays** (PDZ rings, lahar channels, typhoon tracks, storm surge zones, NHA sites) — visual decorations only, moved to bottom |

The old "Hazard Layers" were really just visual overlays. The new Hazard Layers are proper checkable dimensions that color the map.

Added hover tooltips on each layer checkbox showing top 3 most/least exposed municipalities for that dimension.

---

### 4. The Barangay Choropleth Experiment (and Why We Reverted)

**What we tried:**  
Instead of coloring hex grid cells, we attempted to color the barangay boundary polygons themselves — giving each polygon a fill based on its enrichment data.

**The problems we hit, in order:**
1. Most barangay polygons have no enrichment data (`poly._enr === null`) → most stayed transparent
2. Municipality-level fallback gave all barangays in a municipality the same flat color → blocky, no spatial variation
3. Tried sampling extreme vertices (northmost/southmost/eastmost/westmost) of each polygon to get spatial variation → helped somewhat but still lost within-municipality hotspots
4. Averaging formula diluted scores (pvol=0.9 + ptyph=0.45 = 0.675, looked less red than volcanic-only)
5. Compound OR formula (`1 - ∏(1-s)`) saturated everything to red
6. MAX formula (`max across all dims`) didn't compound — Rapu-Rapu with high isolation scored same after adding social layers
7. Fixed `sMin/sMax` stretch caused all-red map when scores clustered 0.55–0.90

**The verdict:**  
The hex grid was purpose-built for spatial scoring. It computes at arbitrary lat/lng points, so it captures within-barangay variation (island tips, lahar corridor edges, etc.). The barangay polygon approach could only use centroids or extreme vertices — always losing information.

**Final architecture:**
- **Hex grid** = choropleth (colors, layer scoring, all spatial computation)
- **Barangay polygons** = transparent white-border overlays only, used as click targets to open the right panel

---

### 5. Layer Scoring — Final Design

**Formula:** Additive physical + social (mirrors original `calcSoc` design)

```
raw_score = physNorm + socNorm × frac × 1.4
```

Where:
- `physNorm` = weighted average of active hazard dims (pvol weight 1.5, ptyph 1.2, pfl 1.0)
- `socNorm` = weighted average of active social dims (using SOC_LAYERS weights)
- `frac` = fraction of total social weight that's active (0→1)
- Raw scores **can exceed 1.0** — `normalize()` spreads the full range across viewport hexes

**Why this works:**  
Areas high on BOTH physical hazard AND social vulnerability accumulate higher raw scores than areas high on only one dimension. The normalization step then spreads this into a full green→red gradient. Rapu-Rapu with isolation=0.95 AND typhoon exposure AND social vulnerability compounds to a much higher raw score than a PDZ-adjacent municipality with only high pvol.

**Composite view:**  
"Composite risk index" is a **reset preset**, not an additive layer. Clicking it clears all individual checkboxes and reverts to the original `calcPhys × 0.5 + calcSoc × 0.5` blended view. Selecting any individual layer automatically deselects composite.

**Why composite looks different from checking everything:**  
Composite weights volcanic proximity heavily (pvol weight 1.5) so the PDZ core dominates. Checking all layers additively surfaces Rapu-Rapu's compound isolation+social score which gets diluted in the fixed-weight composite formula. Both are valid views of different questions.

---

### 6. Spatial Precision Boosts Added to `hexScore()`

| Area | Boost | Reason |
|------|-------|--------|
| Rapu-Rapu island (lng > 124.05) | +0.18 isolation, +0.10 typhoon | Island isolation is radically worse than municipality average suggests |
| Eastern island chain (lng > 123.82, lat 13.25–13.60) | +0.12 isolation, +0.08 typhoon | San Miguel and Batan islands undercounted |
| Oson NHA site, Tabaco (z-score 4.54) | +0.18 housing within 1.5km | Highest compound risk NHA site in province |
| Miisi NHA site, Daraga (z-score 4.19) | +0.16 housing within 1.5km | Second-highest compound NHA site |
| Cullat NHA site, Daraga (z-score 3.32) | +0.11 housing within 1.5km | Third-highest NHA site |
| Pinabobong, Tabaco (z-score 3.40) | +0.13 housing within 1.5km | Fourth-highest NHA site |

Boosts fade with distance (50% at 1.5–3.5km radius) so hotspots have crisp edges, not hard cutoffs.

---

### 7. Hex Tooltip — Risk Breakdown

Each hex now shows a proper risk breakdown on hover, computed at the hex's specific geographic point:
- Distance to Mayon calculated at hex centroid → precise volcanic proximity score
- Coastal surge boost from latitude → precise typhoon/storm exposure
- Risk factors only shown if above threshold (keeps tooltip clean)
- Note at bottom: "Click barangay boundary to open full profile"

This was important because a barangay's panel shows the barangay-average assessment, but a red hex within that barangay might be driven by a specific factor (e.g., inside a lahar channel corridor) that the barangay average doesn't surface.

---

### 8. Legazpi City Added to Key Communities

Added Rosa (39, Legazpi City) as a new community story — the IOM LandLedger pilot site. Key framing:
- Urban informal tenure (generational, not rural PDZ)
- Strong community networks = reason IOM chose it
- First successful DSWD registration using LandLedger document
- Scale: hundreds of households documented, national policy pathway still unclear

Also added Legazpi City to the "Key communities to explore" quick-nav list with an "IOM Pilot" badge, positioned first in the list.

---

### 9. Other Fixes

- **Initial map load orange patches:** `updateBrgyColors()` was called via `setTimeout` after barangay layer loaded. Removed — barangays now start transparent, colors only applied when layers are checked or a municipality is selected.
- **Hex layer initial confusion:** Users were confused by colors showing when nothing was checked. Hex layer now clears when `activeSoc` and `activeHaz` are both empty.
- **Composite pre-checked on load:** Now only "Composite view" is pre-checked on initial load (was previously composite + volcanic).
- **Sidebar visual consistency:** All three sections (Hazard Layers, Vulnerability Layers, Map Overlays) now use identical card styling — `rgba(8,12,24,.82)` with blur.
- **Composite label:** Visually distinct from individual layer checkboxes — italic, "ALL FACTORS" sublabel, subtle border and background.

---

## Key Architectural Decisions

| Decision | What We Chose | Why |
|----------|--------------|-----|
| Choropleth engine | Hex grid | Spatial precision at arbitrary points; captures island tips, lahar corridor edges, within-barangay variation |
| Barangay polygons | Click targets only, transparent fill | Can't match hex spatial precision; centroid/extreme-vertex scoring loses too much information |
| Multi-layer scoring | Additive (physical base + social on top) | Allows scores > 1.0, which `normalize()` spreads into wide visible variation. Pure MAX doesn't reward compound risk. Averaging dilutes it. |
| Composite | Reset preset, not an additive layer | Including composite in additive scoring double-counts all dimensions |
| Normalization | Dynamic `normalize()` across viewport hexes | Fixed floor/ceiling caused all-red saturation when score clusters were narrow |

---

## Files Modified
- `/svi-Phil/index.html` — all changes in one file

## Next Session Priorities

### Must-do
- **Failure Mode tab** — implement full content for the "Failure Modes" left panel tab (currently stubbed). Should cover the system failure scenarios: DSWD documentation wall, NHA resettlement compound risk, APSEMO coverage gaps, lahar corridor re-exposure.
- **Land Tenure tab** — implement full content for the "Land Tenure" left panel tab. Content exists in research but needs to be wired into the panel: tenure rate by municipality, IOM LandLedger status, DSWD eligibility gap, PDZ informal tenure concentration.
- **Verify NGO/Humanitarian tags in `_buildPhase`** — the edit adding `<span class="rp-ngo-tag">Humanitarian</span>` to specific phased guidance items failed due to string mismatch in an earlier session. CSS class is in place, tags need re-applying.
- **Review Legazpi City in Analyze panel** — given it's the IOM pilot focus, make sure the barangay-level scores and panel content are representative and coherent.

### Nice-to-have
- **Resilience nodes** — pull from accumulated research (APSEMO doctrine, IOM LandLedger, PMC/NHA studies, evacuation behavior thesis) and surface key resilience assets in the Resilience tab. Should be a relatively quick content pass since the research is already synthesized.
- **First-use onboarding** — a brief "how to read this map" moment for new users: what the color scale means, what the difference between composite and individual layers is, how to use the panel.
