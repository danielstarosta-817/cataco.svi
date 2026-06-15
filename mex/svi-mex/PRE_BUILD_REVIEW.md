# Pre-Build Review — Mexico SVI Tool
*Lessons from the PR and PH builds. Do not touch index.html until this is read.*

---

## SECTION 1: CRITICAL BUGS THAT WILL BREAK THE MAP

These all produce the same symptom: **base map tiles show, hexes never appear.** They're silent failures.

### Bug 1: Variable Declared After It's Used (THE BIG ONE)
Any data array or object referenced before it's declared causes a `TypeError` at that line. The script
crashes silently. Everything that was initialized before the crash (the base tile layer) renders normally,
making it look like a hex problem when it's actually a data ordering problem.

**Symptom**: Base map shows, hex grid never appears, no error in visible UI.  
**Diagnosis**: Run `node --check file.html` or extract the `<script>` block and run `node extracted.js`.  
**Fix**: Declare ALL data arrays before any code that references them. Never reference a `const` or `var`
in code that runs before its declaration line.

**In Mexico build**: Be careful with MUNICIPIOS data → resourceLayer → OVERLAYS ordering.
Always order: data arrays → Leaflet layers using that data → OVERLAYS object.

---

### Bug 2: Unescaped Apostrophes in Single-Quoted JS Strings
`'One of Mexico\'s most important...'` works. `'One of Mexico's most important...'` does NOT — the
apostrophe silently ends the string, causing a `SyntaxError: Unexpected identifier 's'` that crashes
the entire script block.

**Most likely locations**: Municipality `detail:` narrative fields, tooltip text, any string with
Spanish possessives or contractions.  
**Fix**: Always escape apostrophes in single-quoted strings. Prefer backtick template literals for
long narrative text.

---

### Bug 3: Missing `</div>` Causes Map to End Up Inside Left Panel
A single missing closing `</div>` (e.g. on `lpg-res`) caused the entire remainder of the HTML
(`#mapwrap`, `#rightpanel`) to be nested inside `#leftpanel`. CSS grid placement only applies to
direct children of `#app`, so the map ended up invisible/misplaced.

**Symptom**: Map disappears entirely or renders in the wrong place.  
**Diagnosis**: Count div opens vs. closes with:
```bash
python3 -c "
html = open('index.html').read()
print('Opens:', html.count('<div'))
print('Closes:', html.count('</div'))
"
```
Or trace absolute depth from `#app` opening to each child element.  
**Fix**: Verify div balance after every major HTML edit. The six direct children of `#app` must be:
`#topbar`, `#leftpanel`, `#mapwrap`, `#rightpanel` — in that order, all at depth 1.

---

### Bug 4: CDN Blocking (h3-js)
The h3-js library on jsdelivr/unpkg may be blocked on corporate networks or offline environments.
Hard reload does not help — it's not a cache issue.

**Symptom**: `typeof h3 === 'undefined'`, hexes never render.  
**Fix**: The inline h3 implementation is already documented in `SVI_MAP_ARCHITECTURE_GENERIC.md`.
Copy it verbatim into `<head>` as the first `<script>` block. Zero CDN dependency for hex grid.

---

## SECTION 2: HEX GRID ARCHITECTURE — GET THIS RIGHT BEFORE CSS

### Hex Orientation: Flat-Top Only
The inline h3 engine must use **flat-top** hexes (classic honeycomb). Two things must match:

`cellToBoundary` vertex angle:
```javascript
// WRONG (pointy-top):
var a = Math.PI / 3 * i;
// CORRECT (flat-top):
var a = Math.PI / 3 * i - Math.PI / 6;
```

`polygonToCells` step sizes:
```javascript
// CORRECT (matched to flat-top):
var rowStep = R * S3;        // S3 = sqrt(3)
var colStep = R * 1.5 / cosLat;
```

If orientation and step sizes don't match, hexes won't tile — you get gaps or overlap.

---

### cosLat Correction (Required at Non-Equatorial Latitudes)
Mexico corridor is ~15–19°N. Without cosLat correction, hexes are compressed east-west.

Apply to BOTH places:
1. `polygonToCells` column step: `var colStep = R * 1.5 / cosLat;`
2. `cellToBoundary` vertex longitude offset: `lng + R * Math.cos(a) / cosLat`

---

### Ocean Bleeding: Two Layers Required
Both are needed; neither alone is sufficient.

**Layer 1 — Polygon mask** (`ptInMexico`): Filters hex *centers*. Eliminates hexes entirely in
the ocean. A hex center can be on land while the hex body extends over water — the polygon
mask alone leaves visible color spikes in bays and inlets.

**Layer 2 — SVG clip path** (`refreshCoastClip`): Visually trims the canvas to the coastline
polygon. Handles hex overhang perfectly. BUT: clip coordinates are screen pixels — must
recalculate on every pan and zoom.

**Critical**: `map.on('moveend zoomend', refreshCoastClip)` MUST be wired up or the clip
drifts immediately on first pan.

**Mexico polygon accuracy needed**: The corridor covers roughly 14–18°N, 88–100°W. Need
separate polygons for Guerrero coast, Chiapas coast, and Oaxaca coast (the Pacific shoreline
is complex). Do NOT bridge the Tehuantepec Isthmus with a straight line — that's a narrow
neck and a straight line will mask legitimate land.

---

### Municipality Centroid Trap
If `nearestMuniCached()` only has 80 municipal centroids as targets, the hex grid is a
prettier choropleth — every hex within a municipality gets that municipality's score.
Sub-municipal visual variation comes ONLY from geographic boosts (hurricane track distance,
coast proximity, random jitter), not from actual sub-municipal data.

**For Phase 1 Mexico this is acceptable** — we have municipal-level data only. But:
1. Be honest about it: the tool shows municipal vulnerability, not sub-municipal
2. Apply geographic boosts for concentrated hazard sources (major fault lines, known flood zones)
3. The random jitter (phash-based ±0.04) is still important to prevent solid-color municipality blocks

---

### Canvas Renderer (Always)
SVG hits a performance wall at ~500 hexes. Use `L.canvas({padding:0.3})` unconditionally.
Canvas means no CSS hover — handle `mouseover`/`mouseout` on each Leaflet polygon object.

---

## SECTION 3: UX BUGS TO PREVENT

### Bug 5: Tooltip Stacking on Fast Mouse Movement
When the mouse moves quickly between hexes, Leaflet sticky tooltips stack instead of replacing.

**Fix**: In every `mouseover` handler on the hex layer, close all other layers first:
```javascript
poly.on('mouseover', function(e){
  hexLayer.eachLayer(function(l){ if(l !== poly){ try{ l.closeTooltip(); }catch(err){} } });
  // ... rest of handler
});
poly.on('mouseout', function(){
  try{ poly.closeTooltip(); }catch(err){}
  map.closePopup();
});
```

---

### Bug 6: Boundary Colors Out of Sync After Mode Change
When switching tabs, boundary polygon layer keeps the fill color from the previous mode.

**Fix**: Call `updateBoundaryColors()` inside `setMode()` every time mode changes:
```javascript
function setMode(mode){
  curMode = mode;
  scheduleRegen(0);
  updateBoundaryColors(); // always sync boundary colors
}
```

---

### Bug 7: Resilience Tab Click/Hover Behavior
On the Resilience tab, clicking hexes or boundary polygons should NOT open the municipality
detail panel (Resilience tab responds to hub pin clicks only).

**Fix**: Early return in click/mouseover handlers:
```javascript
poly.on('click', function(){
  if(curMode === 'res') return;
  openPanel(m);
});
poly.on('mouseover', function(){
  if(curMode === 'res'){ try{ poly.closeTooltip(); }catch(e){} return; }
  // ...
});
```

---

### Bug 8: Cell/Overlay Dead Zones Block Hex Click-Through
Any overlay polygon layer (surge, flood zones, etc.) on top of the hex layer will intercept
mouse events, making it impossible to click hexes underneath.

**Fix**: Set `interactive: false` on ALL overlay polygon layers:
```javascript
var surgeLayer = L.geoJSON(surgeData, { interactive: false, ... });
```

---

### Bug 9: Right Panel Width Inconsistency Between Modes
Different modes had different right panel widths even in the unclicked (teaser) state.

**Fix**: ALL modes start at the same narrow teaser width (180px). Only expand when a hex is
clicked (`has-detail` class added to `#app`). Each mode can have its own expanded width:
```css
#app { grid-template-columns: 270px 180px 1fr; }
#app.has-detail { grid-template-columns: 270px 340px 1fr; }
#app.cas-mode { grid-template-columns: 270px 180px 1fr; }  /* same teaser */
#app.cas-mode.has-detail { grid-template-columns: 270px 380px 1fr; } /* wider for cascade chain */
```

---

### Bug 10: Stale Mode Badge on Tab Switch
The shift badge / hex-score pill doesn't reset when switching to modes where scoring doesn't apply.

**Fix**: In `setMode()`, explicitly reset the badge for non-scoring modes before any hexes render:
```javascript
function setMode(mode){
  if(mode === 'str' || mode === 'cas' || mode === 'exp'){
    var badge = document.getElementById('shift-badge');
    if(badge) badge.textContent = '—';
  }
  // ...
}
```

---

### Bug 11: Social Vulnerability Toggles Visible Outside SVI Mode
The SVI layer checkboxes affect hex colors only in `soc` mode. If they're visible in other modes
they appear to do nothing — confusing.

**Fix**: Hide the SVI layer builder section in non-soc modes:
```javascript
var socSection = document.getElementById('soc-layer-builder');
if(socSection) socSection.style.display = (mode === 'soc' || mode === 'sim') ? '' : 'none';
```

---

### Bug 12: Human Stories — Don't Pre-Load First Story
On initial entry to the Human Stories tab, start with a "pick a household" state, not with the
first story pre-loaded. Pre-loading looks overwhelming and skips the choice that establishes agency.

**Fix**: In `activateStoryMode()`, set `curStory = null` and render only the picker, not the
timeline, on initial entry.

---

## SECTION 4: UX PATTERNS TO REPLICATE

### Selected Hex Highlight
When a hex is clicked, draw a bright cyan border on ALL hexes belonging to that municipality
so the user can see the full footprint of their selection.

```javascript
// In openPanel(m):
// Clear previous selection
hexLayer.eachLayer(function(l){ l.setStyle({weight:sw, color:'rgba(255,255,255,0.14)'}); });
// Highlight all hexes for this municipality
if(_muniPolyMap[m.n]){
  _muniPolyMap[m.n].forEach(function(poly){
    poly.setStyle({weight:2.5, color:'rgba(0,212,255,0.9)'});
  });
}
```

Must also re-apply after `generateHexes()` — store the selected municipality name and re-highlight
after any regen.

---

### SVI Explanation Cards (Layer Toggle Feedback)
When a social vulnerability checkbox is checked, a plain-language "here's what this actually means"
card slides in at the top of the left panel. Not a tooltip — a persistent card that updates as
different layers are toggled.

Pattern: maintain a `lastCheckedLayer` variable; card HTML slides in above the checkbox list;
disappears when no boxes are checked; updates when a new box is checked while others are active.

---

### Right Panel Teaser State
Before any hex is clicked, the right panel shows a narrow (180px) teaser:
```html
<div class="rp-ph" id="rp-teaser">
  <div class="big">🗺</div>
  Haz clic en cualquier área del mapa para ver su perfil de vulnerabilidad completo.
</div>
```

The `has-detail` CSS class is added to `#app` when `openPanel()` fires, expanding the panel.
Remove `has-detail` when switching modes (unless the mode always shows an expanded panel).

---

### Mode Tooltips
Add `title` attributes to nav buttons with narrative/inviting text (not technical descriptions).
Tone should be community-accessible, not practitioner jargon:
- Not: "Toggle social vulnerability layers"
- Yes: "Los factores que ya estaban presentes antes de que llegara el desastre"

---

### Landing/Intro Page
A full-screen overlay before the tool loads that:
1. Frames the central argument (physical hazard alone is incomplete)
2. Shows a mini-map with the relevant geography/hazard (e.g., Hurricane Otis track + the corridor)
3. Names the key tension: who aid systems see vs. who is actually most affected
4. Single "Comenzar →" button to enter the tool

This is the most important screen for non-practitioners — it establishes what they're about
to see and why it matters before they interact with anything.

---

### Overlay Modals (Not Side Drawers)
Field kit / methodology notes / data sources → centered modal overlay (not right-side drawer):
```css
#modal {
  position:fixed; top:50%; left:50%;
  transform: translate(-50%, -48%) scale(0.96);
  opacity: 0; pointer-events: none;
  transition: transform .3s, opacity .3s;
}
#modal.open {
  transform: translate(-50%, -50%) scale(1);
  opacity: 1; pointer-events: auto;
}
```

---

## SECTION 5: MEXICO-SPECIFIC ADAPTATIONS

### Language
Everything user-facing is in Spanish. Including:
- Mode nav labels
- SVI layer names and descriptions
- Tooltip text on hover
- Right panel headers
- Explanation cards
- Landing page text

Municipality names use the official NOM_MUN form (e.g., "Acapulco de Juárez", "Chilpancingo de los Bravo").

---

### Boundary Polygon
Need a `ptInMexico(lat, lng)` function with a polygon covering the three-state corridor.
The Overpass query for Mexico municipalities is:
```javascript
var query = '[out:json][timeout:90];rel["name"="Guerrero"]["admin_level"="4"];map_to_area->.g;rel["name"="Oaxaca"]["admin_level"="4"];map_to_area->.o;rel["name"="Chiapas"]["admin_level"="4"];map_to_area->.c;(rel(area.g)["admin_level"="6"];rel(area.o)["admin_level"="6"];rel(area.c)["admin_level"="6"];);out geom;';
```

Note: the three states are not contiguous (Oaxaca separates Guerrero and Chiapas). The polygon
will need to be a compound union or three separate `ptInPoly` calls.

---

### Physical Hazard Weights
Per documented architecture (from SVI_MAP_ARCHITECTURE_GENERIC.md):
```javascript
function calcPhys(m){
  var s=0,w=0;
  if(activePhys.has('hurricane'))  {w+=1.3; s+=m.phurricane*1.3;}
  if(activePhys.has('seismic'))    {w+=1.2; s+=m.pseismic*1.2;}
  if(activePhys.has('flood'))      {w+=1.0; s+=m.pfl*1.0;}
  if(activePhys.has('landslide'))  {w+=0.8; s+=m.pslide*0.8;}
  return w>0 ? s/w : 0;
}
```

---

### Starting View
```javascript
map.setView([17.00, -96.50], 7); // approximate corridor center
```

At zoom 7, all three states should be visible. The corridor spans roughly 14–18°N, 88–100°W.

---

### No Music/Cultural Record Section
The Cultural Record / music component of the PR tool is specific to Daniel's thesis research
on Puerto Rican musical culture. Do NOT replicate for Mexico. The Human Stories tab should
use composite personas drawn from the Guerrero/Oaxaca/Chiapas field research context.

---

### Mexico-Specific "Documentation Barrier" Equivalent
For PR the documentation barrier was FEMA proof-of-ownership requirements. For Mexico:
- Ejido communal land + informal parceling within ejidos (no individual CORETT titles)
- Comunidades agrarias with disputed internal boundaries (RAN records incomplete)
- Oral tenure traditions in Mixtec/Zapotec/Tzeltal communities
- This maps to the `svi_tenure` field and should have dedicated explanation card content

---

### Violence Layer (Mexico-Specific SVI Dimension)
No equivalent in PR or PH builds. The NARCO_PRESSURE composite and ACLED fatalities
are Mexico-specific social vulnerability dimensions. In the SVI layer builder, these need
their own carefully worded explanation cards — the framing should be about community
exposure and aid/service delivery barriers, not sensationalism.

---

## SECTION 6: BUILD CHECKLIST

Work through this in order before shipping:

**Architecture:**
- [ ] Inline h3 script in `<head>` (first script, before Leaflet)
- [ ] All data arrays declared before any code that uses them
- [ ] Flat-top hex orientation: correct `cellToBoundary` and `polygonToCells` step sizes
- [ ] cosLat correction applied in both polygonToCells (colStep) and cellToBoundary (vertex lngs)
- [ ] `ptInMexico()` with bbox pre-filter
- [ ] `initCoastClip()` + `refreshCoastClip()` wired to `map.on('moveend zoomend')`
- [ ] `setMode()` calls `scheduleRegen(0)` and `updateBoundaryColors()`
- [ ] `generateHexes()` returns early in str/cult modes (clear hexes)
- [ ] Canvas renderer (`L.canvas`) for hex layer

**UX Bugs (from Bug list):**
- [ ] Tooltip stacking fix applied to hex + boundary layer mouseover
- [ ] Boundary colors synced in `setMode()`
- [ ] Resilience tab: click/hover early-return in hex handlers
- [ ] Overlay layers: `interactive: false` on all non-hex polygon layers
- [ ] Right panel: all modes start at 180px teaser width
- [ ] Mode badge reset in `setMode()` for non-scoring modes
- [ ] SVI toggles hidden outside soc mode
- [ ] Human Stories: no pre-loaded story on entry

**UX Patterns:**
- [ ] Selected hex cyan border highlight + re-apply after regen
- [ ] Explanation cards wired to SVI layer checkboxes
- [ ] Right panel teaser state with Spanish placeholder text
- [ ] `title` attributes on nav buttons (Spanish, community-accessible)
- [ ] Landing/intro page with Otis track animation

**Data/Scoring:**
- [ ] All MUNICIPIOS objects have every required field; no undefined numeric values
- [ ] Field defaults applied (`FIELD_DEFAULTS` pattern)
- [ ] Additive score formula (social adds to physical; tune the 1.2 multiplier against data distribution)
- [ ] Local normalization in all modes except resilience (which uses absolute 0-1)
- [ ] Bayesian smoothing applied to crime rates before incorporating in SVI (small population problem)

**Structure:**
- [ ] Verify div balance (opens == closes) before first test
- [ ] `node --check` equivalent syntax check before first test
- [ ] Console test: `ptInMexico(17.0, -99.5)` (Guerrero centroid) returns `true`
- [ ] Console test: hexes visible at zoom 7, all over land
- [ ] Click test: clicking hex opens municipality detail in Spanish

---

*Last updated: pre-build, May 2026. Reference the PR tool at `svi-PR/index.html` and PH tool at `svi-Phil/index.html` for working code patterns.*
