# SVI Tool — Generic Map Architecture Reference
*How to build the hex-grid map layer for any new country extension. Paste into the new chat as context.*

Country-specific documents exist for:
- **Puerto Rico** — the original; source of all architecture
- **Philippines / Albay** — PR_MAP_ARCHITECTURE.md in svi-Phil/
- **Mexico / Guerrero–Oaxaca–Chiapas** — use this document

---

## ⚠️ CRITICAL LESSON — Read This Before You Touch Anything Else

### The Municipality Centroid Trap (Discovered During Philippines Build)

When first building the Albay tool, we used ~20 municipality centroids as the nearest-lookup targets for the hex grid. The tool looked reasonable — the hex grid showed color variation across the map, the Mayon volcano boost created a visible high-risk zone near the summit, coastal areas looked different from inland. It felt like it was working.

**It wasn't working analytically.** Here's why:

Every hex is colored by finding the nearest data point and using that point's score. With 20 municipality centroids, the "nearest data point" for any location is always the centroid of whatever municipality that location is inside. The result: every hex within Daraga municipality shows Daraga's score. Every hex within Oas shows Oas's score. The hex colors map exactly to the municipality Voronoi tessellation — which is the same as just showing a GeoJSON choropleth, just with blurrier edges.

**The geographic boosts (Mayon distance, coastal proximity, random jitter) are real**, and they do create *apparent* variation within municipality areas. A barangay near Mayon's foot gets a higher volcanic color than a barangay at the far edge of the same municipality. That's accurate physics. But the **social vulnerability score** they inherit — poverty, housing fragility, documentation, elderly % — is the municipality average applied identically to every hex in that municipality. There is no differentiation between a well-off barangay and an impoverished barangay within the same municipality, even if they sit side-by-side.

**Why this matters:** The entire analytical purpose of this tool is to show that *one barangay may be socially vulnerable while its next-door neighbor is well-off*. Municipality-level data cannot do that. The hex grid existed to give us sub-administrative resolution. If the nearest-lookup targets are municipality centroids, it gives us zero sub-administrative resolution.

**The symptom to recognize:** If clicking any point within a municipality always opens the same detail panel, and the panel shows the same score regardless of where within that municipality you click — you have fallen into this trap.

**The fix:**

Use **BARANGAYS** (not MUNICIPIOS) as the nearest-lookup array. With 720 barangay centroids instead of 20 municipality centroids, the Voronoi cells divide within each municipality. Clicking a barangay next to Mayon opens a different panel than clicking a barangay 15km away in the same municipality. That's what makes the tool analytically honest.

```javascript
// WRONG — municipality-level resolution masquerading as hex-grid resolution:
function hexScore(lat, lng){
  var m = nearestMuniCached(lat, lng); // <-- only 20 targets
  return calcScore(m);
}

// RIGHT — barangay-level resolution:
function hexScore(lat, lng){
  var b = nearestBarangayCached(lat, lng); // <-- 720 targets
  return calcScore(b);
}
```

**What you need per barangay (minimum viable):**
1. `lat`, `lng` — barangay centroid coordinates (derive from polygon centroid if you have boundary GeoJSON)
2. A score field, or sub-score fields — inherited from municipality baseline + barangay-specific modifiers (PDZ flag, Mayon distance, coastal proximity, HazardHunter scores)
3. `n` — barangay name for the popup

**When you don't have barangay-level sub-scores yet:**  
Compute barangay scores as: `municipality_baseline + geographic_modifiers`. The municipality baseline comes from whatever municipal data you have (poverty incidence SAE, housing census, etc.). The geographic modifiers are the same boosts you'd apply in hexScore anyway (Mayon distance, coastal proximity). This is analytically honest — you're saying "within this municipality, proximity to the volcano increases the score" — which is true.

**The conceptual trap in plain language:**  
Sub-municipality visual variation ≠ sub-municipality data resolution. They look identical on screen but represent fundamentally different things analytically. Always ask: "If I hover over two hexes in the same municipality, will I see different scores?" If the answer is "only because of geographic boosts applied to the same base score" — you are in municipality-resolution mode, not barangay-resolution mode.

---

## Overview: What the Map Layer Is

The SVI tool map renders a **dense color-scored hex grid** — every point of land gets a hex cell colored by the computed risk score for the nearest municipality/unit. The grid updates on every pan and zoom. Clicking any hex opens the detail panel for that municipality.

This is NOT the default Leaflet way of doing things (which would be GeoJSON choropleth). The hex grid approach is used because:
- It works without boundary GeoJSON data (which is hard to get for many countries)
- It provides sub-municipal visual variation without sub-municipal data
- It's visually richer and allows scores to blend across municipal lines
- It scales gracefully from national to neighborhood zoom levels

The boundary GeoJSON/Overpass layer is a **complement** to the hexes, not the primary data layer.

**Important:** As noted above — the hex grid only provides genuine sub-municipal resolution when the nearest-lookup targets are sub-municipal units (barangays, census tracts, etc.). If the nearest-lookup targets are municipal centroids, the hex grid is a prettier choropleth, not a higher-resolution analysis.

---

## The Five Things That Must Be Country-Specific

Everything else copies verbatim from the PR tool. Only these five need to change per geography:

### 1. `COUNTRY_POLY` — the land polygon
A clockwise ring of `[lat, lng]` pairs tracing the outer boundary of the region. Used to filter out hex cells that land in the ocean.

**Format:**
```javascript
var COUNTRY_POLY = [
  [lat1, lng1],
  [lat2, lng2],
  // ... as many points as needed for a good approximation ...
  [lat1, lng1], // close the ring
];
// Add additional polygons for islands:
var ISLAND_POLY_1 = [[lat, lng], ...];
```

**Accuracy needed:** Good enough that hex cell *centers* over water are excluded. Does not need to match the exact shoreline — the SVG coast clip handles visual edge clipping. A 20–30 point polygon is usually sufficient for a province-level tool; 50–80 points for a full country.

**Coordinate source:** Use Google Maps "measure distance" tool to trace the outline, or extract from any country GeoJSON (just grab the outer ring coords and simplify).

**Bounding box check (required):** Always add a fast bbox pre-filter before the polygon test:
```javascript
function ptIn[COUNTRY](lat, lng){
  if(lat < SOUTH_BOUND || lat > NORTH_BOUND || lng < WEST_BOUND || lng > EAST_BOUND) return false;
  return ptInPoly(lat, lng, COUNTRY_POLY)
      || ptInPoly(lat, lng, ISLAND_POLY_1)
      // ... add more polygons as needed
}
```

**Ocean hex bleeding — diagnosis:** When hexes appear over the ocean, the cause is almost always #1: the polygon is not accurate enough. Straight lines between polygon vertices bridge bays and inlets, including hex centers that are over water. Fix by adding more polygon vertices around major bays, especially large irregular coastline features. Do NOT attempt to fix ocean bleeding through score adjustments or transparency — fix the polygon.

### 2. `map.setView([lat, lng], zoom)` — starting view
Center the map on the region. Typical starting zoom: 9–11 for a province, 7–8 for a whole country.

```javascript
// Philippines / Albay:
map.setView([13.18, 123.73], 10);

// Puerto Rico:
map.setView([18.22, -66.50], 9);

// Mexico / Guerrero–Oaxaca–Chiapas (example):
map.setView([17.00, -96.50], 7);
```

### 3. `MUNICIPIOS` / `BARANGAYS` — the data array

**⚠️ See the Critical Lesson section above before choosing what to put here.**

The nearest-lookup array. Each object represents one data point whose Voronoi cell is a colored hex region. The visual and analytical resolution of the tool equals the density of this array.

- **For municipality-level analysis:** Use MUNICIPIOS (~15–25 objects for a typical province). Appropriate when you have no sub-municipal data and the tool is not claiming sub-municipal differentiation.
- **For barangay-level analysis:** Use BARANGAYS (~700+ objects for a typical Philippine province). Required when the analytical argument depends on within-municipality variation.

**Required fields (all tools):**
```javascript
{
  n: "Unit Name",       // string — must match boundary layer name for tooltip matching
  lat: 0.0,            // float — centroid latitude
  lng: 0.0,            // float — centroid longitude
  phys: 0.0,           // float 0–1 — overall physical hazard composite
  svi: 0.0,            // float 0–1 — overall SVI composite
  res: 0.0,            // float 0–1 — resilience score
  // physical sub-scores (adapt names to local hazard types):
  p[hazard1]: 0.0,     // e.g. pvol, ptyph, pfl, phurricane, pseismic, pflood
  p[hazard2]: 0.0,
  // social vulnerability sub-scores:
  svi_[dim1]: 0.0,     // e.g. svi_poverty, svi_housing, svi_tenure, svi_elderly
  svi_[dim2]: 0.0,
  // display fields:
  rtag: "Short tag",   // string — shown in resilience panel
  rnote: "...",        // string — resilience note
  detail: "...",       // string — full narrative HTML for detail panel
}
```

**Building BARANGAYS from GeoJSON boundaries + municipal data:**
```javascript
// 1. Fetch GeoRisk or GADM barangay polygons
// 2. Compute centroid per polygon
// 3. Assign municipality baseline scores (from municipal-level data)
// 4. Apply barangay-specific modifiers (PDZ flag, Mayon distance, flood zone)

var BARANGAYS = geoJsonFeatures.map(function(f){
  var centroid = polygonCentroid(f.geometry.coordinates);
  var muni = MUNICIPIOS.find(function(m){ return m.n === f.properties.mun_name; });
  var baseline = muni || FIELD_DEFAULTS;
  var distMayon = haversineDeg(centroid.lat, centroid.lng, 13.2567, 123.6853);
  var volcBoost = distMayon < 8 ? Math.max(0, (8-distMayon)/8) * 0.15 : 0;
  return Object.assign({}, baseline, {
    n: f.properties.brgy_name,
    lat: centroid.lat,
    lng: centroid.lng,
    pvol: clamp(baseline.pvol + volcBoost),
    in_pdz: PDZ_BARANGAYS.has(f.properties.brgy_name),
    in_edz: distMayon < 8,
    dist_mayon_km: distMayon,
    muni_n: f.properties.mun_name,
  });
});
```

### 4. `calcPhys(m)` — physical hazard formula
Weighted sum of the physical sub-scores for the relevant hazard types. Weights reflect relative lethality and prevalence for this geography.

```javascript
function calcPhys(m){
  if(!activePhys.size) return 0;
  var s=0, w=0;
  // Add one line per hazard type:
  if(activePhys.has('hurricane')){w+=1.3; s+=m.phurricane*1.3;}
  if(activePhys.has('seismic'))  {w+=1.2; s+=m.pseismic*1.2;}
  if(activePhys.has('flood'))    {w+=1.0; s+=m.pfl*1.0;}
  if(activePhys.has('landslide')){w+=0.8; s+=m.pslide*0.8;}
  return w>0 ? s/w : 0;
}
```

**Calibration guidance:**
- Weights should roughly reflect "how much does this hazard affect who survives"
- For Puerto Rico: flood=1.2, surge=1.1, wind=1.0, landslide=1.0
- For Philippines/Albay: volcanic=1.5, typhoon=1.2, flood=1.0 (volcano is dominant hazard)
- For Mexico/Guerrero: hurricane=1.3, seismic=1.2, flood=1.0 (two roughly equal primary hazards)

### 5. `SOC_LAYERS` — social vulnerability dimensions
The social vulnerability toggle dimensions. Each maps to a field in MUNICIPIOS/BARANGAYS and has a weight used in the additive formula.

```javascript
var SOC_LAYERS=[
  {id:'poverty',  key:'svi_poverty',  w:.20},
  {id:'housing',  key:'svi_housing',  w:.18},
  {id:'tenure',   key:'svi_tenure',   w:.20}, // weight higher if tenure is a key analytical focus
  {id:'elderly',  key:'svi_elderly',  w:.12},
  {id:'access',   key:'svi_access',   w:.15},
  {id:'cell',     key:'svi_cell',     w:.10},
  // add/remove dimensions to match the analytical frame
];
var SOC_MAX_W=SOC_LAYERS.reduce(function(a,l){return a+l.w;},0);
```

**Note on id vs. key:** The `id` must match the `data-dim` attribute on the checkbox in the HTML. The `key` must match the field name in MUNICIPIOS/BARANGAYS. They can differ — use the shorter id in HTML for readability. The Philippines Albay build currently uses `id:'svi_housing'` and `key:'svi_housing'` (identical) because the HTML was built that way. Either convention works; just be consistent.

---

## Everything Below Copies Verbatim (No Country-Specific Changes)

### H3 Hex Engine
Copy the entire inline `h3.js` block from PR tool lines 19–81. It is geography-independent — it generates hex grids anywhere on Earth using degree-based radius values.

### Color Scales
```javascript
var RISK_STOPS=[[0,[0,224,150]],[.22,[74,222,128]],[.42,[255,217,61]],[.64,[255,107,53]],[.82,[255,45,85]],[1,[180,0,50]]];
var RES_STOPS= [[0,[18,38,28]],[.25,[22,85,55]],[.50,[34,160,95]],[.75,[52,211,130]],[1,[0,240,130]]];

function interpColor(t,stops){
  var s=Math.max(0,Math.min(1,t));
  for(var i=0;i<stops.length-1;i++){
    var a=stops[i][0],ca=stops[i][1],b=stops[i+1][0],cb=stops[i+1][1];
    if(s<=b){var f=(s-a)/(b-a);return 'rgb('+Math.round(ca[0]+f*(cb[0]-ca[0]))+','+Math.round(ca[1]+f*(cb[1]-ca[1]))+','+Math.round(ca[2]+f*(cb[2]-ca[2]))+')'}
  }
  return 'rgb('+stops[stops.length-1][1].join(',')+')';
}
function riskColor(t){return interpColor(t,RISK_STOPS);}
function resColor(t){return interpColor(t,RES_STOPS);}
function normalize(arr){var mn=Math.min.apply(null,arr),mx=Math.max.apply(null,arr),r=mx-mn||.01;return arr.map(function(v){return(v-mn)/r;});}
```

### Score Pipeline (Additive Formula — Copy, Then Customize Weights)
```javascript
function calcSoc(m){
  var physS=calcPhys(m);
  if(!activeSoc.size) return physS;
  var sw=0,ss=0;
  activeSoc.forEach(function(id){
    var L=SOC_LAYERS.find(function(l){return l.id===id;});
    if(!L) return;
    sw+=L.w; ss+=m[L.key]*L.w;
  });
  var socNorm=ss/sw;
  var frac=Math.min(1,sw/SOC_MAX_W);
  return physS+socNorm*frac*1.2; // additive: social adds to physical
}

function calcScore(m){
  if(curMode==='res')  return m.res;
  if(curMode==='phys') return calcPhys(m);
  return calcSoc(m);
}
```

### Muni/Barangay Cache
```javascript
// Works identically whether the array is MUNICIPIOS or BARANGAYS
// Just rename to nearestBarangayCached and point at BARANGAYS array

function nearestMuni(lat,lng){
  var best=null,bd=Infinity;
  var cosL=Math.cos(lat*Math.PI/180);
  BARANGAYS.forEach(function(m){  // <-- BARANGAYS not MUNICIPIOS for barangay builds
    var d=(m.lat-lat)*(m.lat-lat)+((m.lng-lng)*cosL)*((m.lng-lng)*cosL);
    if(d<bd){bd=d;best=m;}
  });
  return best;
}
var _muniCache={};
function nearestMuniCached(lat,lng){
  var key=(lat*50|0)+','+(lng*50|0);
  if(_muniCache[key]) return _muniCache[key];
  var m=nearestMuni(lat,lng);
  _muniCache[key]=m;
  return m;
}
function phash(lat,lng){var s=Math.sin(lat*127.1+lng*311.7)*43758.5453;return s-Math.floor(s);}
```

**Performance note:** With 720 barangay centroids instead of 20 municipality centroids, the linear search `nearestMuni()` runs 36x more comparisons per hex. At res 7–8 this is fine. At res 9–10 (zoom 12+) with hundreds of hex cells, it can slow down. Consider a grid-bucket spatial index for the cache if performance degrades at high zoom levels.

### hexScore() — Adapt the Geographic Boosts, Rest is Verbatim
```javascript
function hexScore(lat,lng){
  var m=nearestMuniCached(lat,lng);  // returns nearest BARANGAY if array was swapped
  if(curMode==='res') return m&&m.res!=null?m.res:0.30;
  var rnd=(phash(lat,lng)-.5);
  var cosLat=Math.cos(lat*Math.PI/180);
  var cl=function(v){return Math.min(1,Math.max(0,v));};

  // ── COUNTRY-SPECIFIC GEOGRAPHIC BOOSTS ──────────────────────────
  // Add a boost here for any hazard that should appear concentrated
  // at specific lat/lng coordinates (e.g. volcano summit, fault line,
  // coast surge zone) rather than being uniform within a municipality.
  //
  // Pattern:
  //   var distFromFeature = Math.sqrt(Math.pow(lat-FEAT_LAT,2)+Math.pow((lng-FEAT_LNG)*cosLat,2));
  //   var boost = (distFromFeature < RADIUS) ? Math.max(0,(RADIUS-distFromFeature)/RADIUS)*INTENSITY : 0;
  //
  // Example (Mayon Volcano):
  //   var distFromMayon = Math.sqrt(Math.pow(lat-13.2567,2)+Math.pow((lng-123.6853)*cosLat,2));
  //   var volcBoost = distFromMayon<0.08 ? Math.max(0,(0.08-distFromMayon)/0.08)*0.12 : 0;
  //
  // Note: When using BARANGAYS array, the barangay centroids already encode
  // PDZ/EDZ flags and Mayon-distance-based pvol scores. The boost in hexScore()
  // adds finer-grained within-barangay variation on top of the barangay score.
  // ────────────────────────────────────────────────────────────────

  var hm=Object.assign({},m,{
    // Jitter all scored fields by ±rnd*0.04 to break up Voronoi banding
    phys:  cl(m.phys  + rnd*.04),
    svi:   cl(m.svi   + rnd*.04),
    // Add jitter for every p[hazard] and svi_[dim] field:
    // p[hazard1]: cl(m.p[hazard1] + boost + rnd*.04),
    // svi_[dim1]: cl(m.svi_[dim1] + rnd*.04),
  });
  if(curMode==='phys') return calcPhys(hm);
  return calcSoc(hm);
}
```

### generateHexes() — Copy Verbatim, Change ptInPR → ptIn[COUNTRY]
```javascript
var canvasRenderer = L.canvas({padding:0.3});
var hexLayer = L.layerGroup().addTo(map);
var _lastZoom = -1, _regenTimer = null, _muniPolyMap = {};

function getH3Res(zoom){
  if(zoom>=14) return 10;
  if(zoom>=12) return 9;
  if(zoom>=10) return 8;
  return 7;
}
function scheduleRegen(delay){
  if(_regenTimer) clearTimeout(_regenTimer);
  _regenTimer=setTimeout(generateHexes,delay||180);
}

function generateHexes(){
  if(!map||typeof map.getBounds!=='function') return;
  if(curMode==='cult'||curMode==='str'){
    hexLayer.clearLayers();
    if(canvasRenderer&&canvasRenderer._canvas) canvasRenderer._canvas.style.clipPath='';
    return;
  }
  var bounds=map.getBounds(), zoom=map.getZoom(), res=getH3Res(zoom), pad=0.04;
  var n=bounds.getNorth()+pad, s=bounds.getSouth()-pad, e=bounds.getEast()+pad, w=bounds.getWest()-pad;
  var cells;
  try{cells=h3.polygonToCells([[n,w],[n,e],[s,e],[s,w],[n,w]],res);}catch(err){return;}
  var landCells=[];
  cells.forEach(function(cell){
    var c=h3.cellToLatLng(cell);
    if(!ptIn[COUNTRY](c[0],c[1])) return; // <-- CHANGE THIS FUNCTION NAME
    landCells.push(cell);
  });
  if(!landCells.length) return;
  var scores=landCells.map(function(cell){var c=h3.cellToLatLng(cell);return hexScore(c[0],c[1]);});
  var norm=curMode==='res'?scores.map(function(v){return Math.max(0,Math.min(1,v||0));}):normalize(scores);
  var cf=curMode==='res'?resColor:riskColor;
  var sw=zoom>=13?0.25:zoom>=11?0.4:0.6;
  hexLayer.clearLayers();
  _muniPolyMap={};
  landCells.forEach(function(cell,i){
    var boundary=h3.cellToBoundary(cell);
    var c=h3.cellToLatLng(cell);
    var m=nearestMuniCached(c[0],c[1]);
    var poly=L.polygon(boundary,{renderer:canvasRenderer,weight:sw,color:'rgba(255,255,255,0.14)',fillColor:cf(norm[i]),fillOpacity:0.50});
    if(!_muniPolyMap[m.n]) _muniPolyMap[m.n]=[];
    _muniPolyMap[m.n].push(poly);
    poly.on('click',function(){if(curMode!=='res'&&typeof openPanel==='function') openPanel(m);});
    poly.on('mouseover',function(e){
      poly.setStyle({weight:2,color:'rgba(255,255,255,0.75)'});
      L.popup({closeButton:false,offset:[0,-2]}).setLatLng(e.latlng)
        .setContent('<strong>'+m.n+'</strong><br><span style="color:#8896AA;font-size:11px">Click for full analysis</span>').openOn(map);
    });
    poly.on('mouseout',function(){
      poly.setStyle({weight:sw,color:'rgba(255,255,255,0.14)'});
      map.closePopup();
    });
    hexLayer.addLayer(poly);
  });
  refreshCoastClip();
}

map.on('moveend zoomend',function(){scheduleRegen(200);});
map.on('zoom',function(){var nr=getH3Res(map.getZoom()),or=getH3Res(_lastZoom);if(nr!==or)scheduleRegen(60);});
```

### SVG Coast Clip — Copy Verbatim, Update Polygon IDs
```javascript
// In initCoastClip(), update the id list to match your polygon names:
['main','island1','island2'].forEach(function(id){ ... });

// In refreshCoastClip(), update references:
mpEl.setAttribute('points', polyPts(COUNTRY_POLY));
i1El.setAttribute('points', polyPts(ISLAND_POLY_1));
```

---

## Known Bugs to Apply to Every New Build

These bugs were found and fixed in the PR tool. Apply the same fixes proactively to every new country tool.

### Bug 1: Tooltip Stacking
Cause: Leaflet sticky tooltips don't close cleanly when mouse moves quickly between features.
Fix: In every `mouseover` handler on the hex layer and boundary layer, close all other tooltips first:
```javascript
poly.on('mouseover', function(e){
  hexLayer.eachLayer(function(l){if(l!==poly){try{l.closeTooltip();}catch(err){}}}); // close others
  // ... rest of handler
});
poly.on('mouseout', function(){
  try{poly.closeTooltip();}catch(err){} // always close self
  map.closePopup();
  // ... rest of handler
});
```

### Bug 2: Resilience Tab Tract/Boundary Interactions
Cause: Clicking any polygon on the Resilience tab opens the municipality detail panel, but Resilience tab should only respond to hub pin clicks.
Fix: Early return in click and mouseover handlers:
```javascript
poly.on('click',function(){
  if(curMode==='res') return; // <-- add this
  openPanel(m);
});
poly.on('mouseover',function(){
  if(curMode==='res'){try{poly.closeTooltip();}catch(e){} return;} // <-- add this
  // ...
});
poly.on('mouseout',function(){
  if(curMode==='res') return; // <-- add this
  // ...
});
```
Also clear any selected state when switching TO the Resilience tab:
```javascript
if(mode==='res'){
  _closeStuckTooltips();
  // clear any selected boundary
}
```

### Bug 3: Duplicate Composite Portrait Disclaimer (Human Stories tab)
Cause: One disclaimer is hardcoded in static HTML, another is injected dynamically by the story list renderer.
Fix: Remove the dynamically injected one. In the story list render function, find and delete:
```javascript
h += '<div class="str-composite-note">...</div>'; // DELETE THIS LINE
```
Keep the static HTML version that appears above the "Choose a household" header.

### Bug 4: Boundary Layer Colors Out of Sync After Mode Change
Cause: The boundary choropleth polygon layer keeps the fill color from the previous mode after the user switches tabs.
Fix: Call `updateBoundaryColors()` inside `setMode()`:
```javascript
function setMode(mode){
  curMode = mode;
  // ... existing logic ...
  scheduleRegen(0);         // regen hexes for new mode
  updateBoundaryColors();   // sync boundary colors
}
function updateBoundaryColors(){
  _muniPolys.forEach(function(obj){
    var col = curMode==='res' ? resColor(obj.m.res||.5) : riskColor(calcScore(obj.m));
    try{obj.poly.setStyle({fillColor:col});}catch(e){}
  });
}
```

---

## Checklist for a New Country Build

Copy this checklist into the new chat and check off each item:

- [ ] **FIRST:** Decide — is this a municipality-resolution or barangay-resolution tool? (See Critical Lesson above)
- [ ] Nearest-lookup array is BARANGAYS (not MUNICIPIOS) if barangay-level differentiation is the analytical purpose
- [ ] `COUNTRY_POLY` defined with correct `[lat, lng]` coordinates (not `[lng, lat]`)
- [ ] Island polygons defined if needed
- [ ] `ptIn[COUNTRY]()` function with correct bbox bounds
- [ ] `map.setView()` centered on the region at appropriate zoom
- [ ] All `MUNICIPIOS`/`BARANGAYS` objects have every required field; no `undefined` numeric values
- [ ] `calcPhys()` uses the correct hazard fields and weights for this geography
- [ ] `SOC_LAYERS` dimensions match the analytical frame and `svi_*` fields in MUNICIPIOS/BARANGAYS
- [ ] `hexScore()` geographic boosts added for concentrated hazard sources (volcano summits, fault lines, known flood zones)
- [ ] H3 inline script added to `<head>`
- [ ] `initCoastClip()` + `refreshCoastClip()` added, polygon IDs updated
- [ ] `generateHexes()` using `ptIn[COUNTRY]()` not `ptInPR()`
- [ ] `setMode()` calls `scheduleRegen(0)` and `updateBoundaryColors()`
- [ ] All three tooltip/interaction bugs applied (Bug 1, 2, 4)
- [ ] Composite portrait disclaimer: only one instance in HTML (Bug 3)
- [ ] Console test: `ptIn[COUNTRY](CENTER_LAT, CENTER_LNG)` returns `true`
- [ ] Console test: hexes visible at default zoom, all over land
- [ ] **Resolution test:** Hover two hexes in the same municipality → verify different scores if using BARANGAYS
- [ ] Click test: clicking a hex opens the correct municipality/barangay detail panel

---

## Boundary Layer: Overpass vs. Static GeoJSON

**Overpass API** (what Philippines tool uses): Works well for countries/regions with good OSM coverage. Admin level query pattern:
```javascript
// For a province's municipalities (admin_level 6):
var query='[out:json][timeout:60];rel["name"="[Province]"]["admin_level"="4"];map_to_area->.a;rel(area.a)["admin_level"="6"]["boundary"="administrative"];out geom;';

// For barangays (admin_level 10 in Philippines):
var query='[out:json][timeout:90];rel["name"="Albay"]["admin_level"="4"];map_to_area->.a;rel(area.a)["admin_level"="10"]["boundary"="administrative"];out geom;';

// For Mexico municipalities (admin_level 6 in Mexico):
var query='[out:json][timeout:90];rel["name"="Guerrero"]["admin_level"="4"];map_to_area->.a;rel(area.a)["admin_level"="6"];out geom;';
```
Always add a timeout fallback — if Overpass fails, the hex grid still works.

**Note on OSM barangay coverage in Philippines:** admin_level=10 coverage is incomplete. Use the GeoRisk API (`portal.georisk.gov.ph/arcgis/rest/services/PSA/Barangay/MapServer/4`) as primary source for Philippines barangay boundaries — it has full national coverage from the PSA 2015 census.

**Static GeoJSON**: More reliable, faster, but requires sourcing the file. For Mexico: INEGI provides free municipal boundary shapefiles (convert to GeoJSON with QGIS or mapshaper.org). For Philippines: PSA provides shapefiles. For any country: GADM (gadm.org) has admin boundaries for every country as free GeoJSON downloads.

**Recommendation:** Start with Overpass for speed. If Overpass proves unreliable for that region, download and inline the GADM GeoJSON.

---

## Language Notes

- **Puerto Rico:** English (with Spanish toponyms)
- **Philippines / Albay:** English (official language; all data in English)
- **Mexico:** Spanish throughout — UI labels, legend, story text, mode names, all tooltips

For a Spanish build, all user-visible strings need Spanish equivalents. The MUNICIPIOS `n` field should use the local-language name (e.g. "Acapulco de Juárez" not "Acapulco"). The left-panel nav labels, mode descriptions, and badge text all need Spanish strings.

---

## Left Panel Architecture

The left panel is a collapsible sidebar that houses all mode controls, narrative context, and the SVI layer builder. It is the primary "explain what you're looking at" surface of the tool.

### Structure Overview

```
#leftpanel
  #lp-toggle-wrap          ← collapse/expand chevron button
  #lp-nav                  ← vertical tab navigation
    .lp-nav-btn[data-grp]  ← one button per major section
  .lp-group[id="lpg-*"]   ← content panel for each tab (only active one shows)
    .lp-group-intro        ← short label + framing paragraph
    .lp-accord             ← collapsible accordion block(s)
      .lp-accord-hdr       ← accordion header (clickable)
      .lp-accord-body      ← accordion content (show/hide)
```

### Nav Buttons

Each nav button has:
- `data-grp="[name]"` attribute — the group it activates
- `onclick="setModeGroup('[name]')"` — fires `setModeGroup()`
- `.lp-nav-icon` span — emoji icon
- `.lp-nav-text` span — contains two children:
  - `.lp-nav-label` — bold label (e.g., "Vulnerability")
  - `.lp-nav-q` — gray sub-question (e.g., "Who is most at risk, and why?")

The panel collapses to icon-only width when `.lp-pinned` class is absent. When collapsed, `.lp-nav-text` is hidden via CSS.

**Standard nav sections (copy for each new build):**
```html
<button class="lp-nav-btn active" data-grp="hazard" onclick="setModeGroup('hazard')">
  <span class="lp-nav-icon">🌊</span>
  <span class="lp-nav-text">
    <span class="lp-nav-label">Hazard</span>
    <span class="lp-nav-q">What physical risks exist?</span>
  </span>
</button>
<button class="lp-nav-btn" data-grp="vuln" onclick="setModeGroup('vuln')">
  <span class="lp-nav-icon">👥</span>
  <span class="lp-nav-text">
    <span class="lp-nav-label">Vulnerability</span>
    <span class="lp-nav-q">Who is most at risk, and why?</span>
  </span>
</button>
<button class="lp-nav-btn" data-grp="fail" onclick="setModeGroup('fail')">
  <span class="lp-nav-icon">⚡</span>
  <span class="lp-nav-text">
    <span class="lp-nav-label">Failure Modes</span>
    <span class="lp-nav-q">What breaks when [HAZARD] hits?</span>
  </span>
</button>
<button class="lp-nav-btn" data-grp="res" onclick="setModeGroup('res')">
  <span class="lp-nav-icon">🌿</span>
  <span class="lp-nav-text">
    <span class="lp-nav-label">Resilience</span>
    <span class="lp-nav-q">What is already working?</span>
  </span>
</button>
<!-- Divider line separates analytical modes from narrative modes -->
<div style="height:1px;background:rgba(255,255,255,.07);margin:4px 10px"></div>
<button class="lp-nav-btn" data-grp="str" onclick="setModeGroup('str')">
  <span class="lp-nav-icon">🧑</span>
  <span class="lp-nav-text">
    <span class="lp-nav-label">Human Stories</span>
    <span class="lp-nav-q">What did it feel like to live it?</span>
  </span>
</button>
```

### Group Panels (`.lp-group`)

Each group panel is a `<div id="lpg-[name]" class="lp-group">`. Only the active group is visible. `setModeGroup()` handles show/hide.

Each group typically begins with a `.lp-group-intro` block:
```html
<div class="lp-group-intro">
  <div class="lp-gi-label">THE DEEPER PICTURE</div>
  <p>Narrative framing paragraph explaining what this section reveals and why the user should care.</p>
</div>
```

Below the intro, one or more `.lp-accord` accordion blocks hold mode-specific controls:
```html
<div class="lp-accord" data-mode="soc">
  <div class="lp-accord-hdr" onclick="toggleAccord(this)">
    <span class="lp-accord-question">How does social vulnerability change the picture?</span>
    <span class="lp-accord-chev">▼</span>
  </div>
  <div class="lp-accord-body">
    <!-- SVI layer toggles, legend, description -->
  </div>
</div>
```

### SVI Layer Builder (inside Vulnerability group)

The Social Vulnerability Builder is a checkbox list inside the vulnerability group. Each SVI dimension gets a checkbox:

```html
<div class="svi-builder-section">
  <div class="svi-builder-header">Social Vulnerability Builder</div>
  <div class="svi-builder-note">Toggle social vulnerability dimensions one at a time. Watch [KEY_COMMUNITY] jump when [KEY_VARIABLE] is added.</div>
  <div id="soc-layer-list">
    <!-- Dynamically generated from SOC_LAYERS array, or hard-coded: -->
    <label class="soc-layer-item">
      <input type="checkbox" class="soc-cb" data-id="housing" onchange="toggleSocLayer('housing',this.checked)">
      <div class="soc-layer-body">
        <div class="soc-layer-name">Housing fragility</div>
        <div class="soc-layer-desc">Light-frame / non-engineered construction, informal materials</div>
      </div>
    </label>
    <!-- repeat for each SOC_LAYERS entry -->
  </div>
</div>
```

`toggleSocLayer(id, on)` adds/removes the layer from `activeSoc` Set and calls `scheduleRegen()`.

### Human Stories Tab — Cultural Record Note

The Human Stories tab in the Puerto Rico tool includes a **Cultural Record** section with a music/song component (`cr-songs`, `cr-song-lyric` CSS classes) that maps songs and cultural artifacts documenting community experiences of Maria. **This section is specific to Puerto Rico** and reflects Daniel's research on cultural narrative as preparedness data (see the thesis framework). Do not replicate the music component in other country extensions. Instead, the Human Stories tab in new builds should contain:
- Community portraits (existing narrative `detail` field from MUNICIPIOS)
- Oral history excerpts specific to that geography
- Any cultural/institutional record layer appropriate to that context (e.g., for Philippines: displacement records, IOM LandLedger entries, APSEMO evacuation history)

---

## Right Panel (Detail Panel) Architecture

The right panel opens when a user clicks any hex on the map. It shows municipality/barangay-level detail: scores, SVI fingerprint, contextual alerts, and action recommendations.

### Structure Overview

```
#rightpanel
  .rp-ph#rp-teaser           ← placeholder shown before any hex is clicked
  .rp-hd                     ← header: municipality name + meta stats
    #rp-name                 ← large municipality name text
    #rp-meta                 ← pop · road risk · power restore time
  .rp-tabs                   ← sticky tab row (PROFILE / TENURE / WHAT TO DO)
    .rp-tab[data-tab]        ← one per sub-section
  .rp-tab-content[data-tab]  ← content for each tab (only active visible)
    .rp-sec                  ← individual section block within a tab
      h4                     ← section heading
      [content]              ← bars, cards, text, lists
```

### Opening the Panel

The panel is opened by calling `openPanel(m)` where `m` is a MUNICIPIOS or BARANGAYS object. This function:
1. Sets `#rp-name` text to `m.n`
2. Sets `#rp-meta` text to `Pop ${m.pop.toLocaleString()} · Road: ${m.road} · ~${m.pwr} days power restore`
3. Populates the **Hazard Model** score bars (one colored bar per hazard sub-score)
4. Populates the **SVI Fingerprint** bars (one bar per active SVI dimension)
5. Populates contextual alert cards (danger zone warnings, tenure alerts, aid eligibility flags)
6. Populates resettlement site cards if `m.nha_sites` exists
7. Activates the first tab

```javascript
function openPanel(m){
  document.getElementById('rp-name').textContent = m.n;
  document.getElementById('rp-meta').textContent =
    'Pop ' + (m.pop||0).toLocaleString() +
    ' · Road: ' + (m.road||'unknown') +
    ' · ~' + (m.pwr||'?') + ' days power restore';
  buildHazardBars(m);
  buildSviBars(m);
  buildAlertCards(m);
  // show panel
  document.getElementById('rightpanel').classList.add('open');
}
```

### Hazard Model Bars

Each hazard sub-score is rendered as a colored bar:
```html
<div class="rp-sec">
  <h4>Hazard Model</h4>
  <!-- generated for each hazard field: pvol, ptyph, pfl, etc. -->
  <div class="rp-score-row">
    <span class="rp-score-lbl">Volcanic</span>
    <div class="rp-bar-wrap">
      <div class="rp-bar" style="width:[score*100]%;background:[hazardColor]"></div>
    </div>
    <span class="rp-score-val">[score*100|0]</span>
  </div>
  <!-- ... -->
  <div class="rp-score-row rp-composite">
    <span class="rp-score-lbl"><strong>Composite Physical</strong></span>
    <div class="rp-bar-wrap">
      <div class="rp-bar" style="width:[phys*100]%;background:var(--cyan)"></div>
    </div>
    <span class="rp-score-val">[phys*100|0]</span>
  </div>
</div>
```

### SVI Fingerprint Bars

Same bar pattern, one per SVI sub-dimension:
```html
<div class="rp-sec">
  <h4>Social Vulnerability Fingerprint</h4>
  <!-- for each svi_* field in MUNICIPIOS/BARANGAYS -->
  <div class="rp-score-row">
    <span class="rp-score-lbl">Housing fragility</span>
    <div class="rp-bar-wrap">
      <div class="rp-bar" style="width:[m.svi_housing*100]%;background:#FF6B35"></div>
    </div>
    <span class="rp-score-val">[m.svi_housing*100|0]</span>
  </div>
  <!-- ... more svi_* fields ... -->
</div>
```

### Alert Cards

Context-specific alert cards appear conditionally based on MUNICIPIOS/BARANGAYS flags:
```html
<!-- Rendered when m.in_pdz === true (Philippines danger zone) -->
<div class="rp-alert-card rp-alert-danger">
  <div class="rp-alert-icon">⚠️</div>
  <div class="rp-alert-body">
    <div class="rp-alert-title">Inside Mayon Danger Zone</div>
    <div class="rp-alert-text">Within APSEMO 8km pre-emptive evacuation zone. Informal tenure common. DSWD aid eligibility often blocked.</div>
  </div>
</div>
```

Add a boolean flag to MUNICIPIOS/BARANGAYS for each alert condition. Generate cards dynamically in `openPanel()`. Keep alert cards visually distinct (colored border, icon) so they stand out from score sections.

### Tabs: PROFILE / TENURE / WHAT TO DO

The tabs divide the detail panel into three logical sections:
- **Profile**: Hazard bars + SVI fingerprint + contextual alerts
- **Tenure**: Land tenure status, CLOA/NHA site cards, documentation barrier explanation (Philippines-specific: informal tenure as SVI dimension)
- **What to Do**: Organization-specific action recommendations, pre-populated needs manifest, intervention priorities

Tab switching:
```javascript
function setRpTab(tabName){
  document.querySelectorAll('.rp-tab').forEach(function(t){
    t.classList.toggle('active', t.dataset.tab===tabName);
  });
  document.querySelectorAll('.rp-tab-content').forEach(function(c){
    c.style.display = c.dataset.tab===tabName?'':'none';
  });
}
```

---

## ⚠️ KNOWN BUGS & INTERACTION ISSUES — Albay Build (May 2026)

The following bugs were observed during the Albay demo build and should be fixed before the next country extension. Each has a documented root cause and fix strategy.

---

### Bug 1: Blue Municipality Rectangle Appears Instead of Barangay Highlight

**Symptom:** Clicking a barangay polygon causes a blue rectangle to appear on the map (roughly the municipality extent) rather than the selected barangay being highlighted in orange.

**What should happen (PR tool standard):**
- Selected barangay → orange border (`rgba(255,107,53,0.92)`, weight 2.2)
- Parent municipality → blue border (`rgba(100,160,255,0.85)`, weight 2.5)
- No fill on either
- Barangay orange border is always visually on top of municipality blue border

**Root cause — `bringToFront` ordering:**
In `selectBarangayBoundary()`, the municipality polygon's `.bringToFront()` was called last, putting the blue outline on top of the barangay orange outline. The barangay highlight was there, just visually buried.

Fix: call `selItem.poly.bringToFront()` *after* `muniItem.poly.bringToFront()` so the barangay always sits on top.

**Root cause — name normalization for PSA mun_name variants:**
PSA adm4 data uses different name formats than MUNICIPIOS:
- PSA: `"City of Ligao"` → MUNICIPIOS: `"Ligao City"`
- PSA: `"City of Tabaco"` → MUNICIPIOS: `"Tabaco"`
- PSA: `"Daraga (Locsin)"` → MUNICIPIOS: `"Daraga"`
- PSA: `"Legazpi City (Capital)"` → MUNICIPIOS: `"Legazpi City"`
- PSA: `"Santo Domingo (Libog)"` → MUNICIPIOS: `"Santo Domingo"`

The `_muniForBarangay()` fuzzy match uses first-word matching, which works for most cases but needs the expanded match condition in `selectBarangayBoundary`:
```javascript
return iName===parentName
  || iName.replace(/city/g,'').trim()===parentName.replace(/city/g,'').trim()
  || iName.split(' ')[0]===parentName.split(' ')[0]
  || parentName.indexOf(iName.split(' ')[0])!==-1;
```

**Status:** Fixed in current build (May 2026).

---

### Bug 2: Map Auto-Zooms and Pans on Every Barangay Click

**Symptom:** Clicking any barangay or municipality on the map causes the map to zoom in abruptly and re-center. This is disorienting during demos and makes it impossible to compare nearby locations while keeping them both in view.

**What should happen (PR tool standard):** The map does not move at all when a barangay is clicked. The detail panel opens to the right. The user controls map position entirely with scroll/drag.

**Root cause — `drawSelectionHighlight()` called `fitBounds` and `setView`:**
```javascript
// BAD — was in the code:
var b = _selectionHighlight.getBounds();
if(b.isValid()) map.fitBounds(b, {maxZoom:12, padding:[50,50], animate:true});

// BAD fallback:
map.setView([m.lat, m.lng], 12, {animate:true});
```

Both lines were removed. `drawSelectionHighlight()` now draws the polygon overlay without touching the viewport.

**Rule for all future builds:** Never call `map.fitBounds()`, `map.setView()`, or `map.panTo()` from `openPanel()`, `drawSelectionHighlight()`, or `selectBarangayBoundary()`. The only functions that should move the map are explicit user-facing actions like `focusMuni()` (a deliberate "jump to municipality" feature, not triggered by normal click flow).

**Status:** Fixed in current build (May 2026).

---

### Bug 3: Right Panel Opened on Far Right of Screen Instead of Adjacent to Left Panel

**Symptom:** The detail panel (right panel) opened at the right edge of the viewport, with the full map between it and the left navigation panel — a wide, disconnected layout.

**What should happen (PR tool standard):** The detail panel opens immediately to the right of the left navigation panel. The map takes the remaining space. Layout from left to right: `[nav 52px] | [left panel 270px] | [detail panel 380px] | [map 1fr]`.

**Root cause — grid column order:**
The original CSS grid was `52px [lp] [map] [rp]`. The fix moves `[rp]` to column 3 and `[map]` to column 4, and reorders the DOM so `#rightpanel` appears before `#map-wrap`.

**CSS fix:**
```css
/* Default */     grid-template-columns: 52px 0px 0px 1fr;
/* LP open */     grid-template-columns: 52px var(--lp-w) 0px 1fr;
/* RP open */     grid-template-columns: 52px 0px var(--rp-w) 1fr;
/* Both open */   grid-template-columns: 52px var(--lp-w) var(--rp-w) 1fr;

#rightpanel { grid-column: 3; border-right: 1px solid var(--border); }
#map-wrap   { grid-column: 4; }
```

**DOM fix:** `#rightpanel` div must appear before `#map-wrap` div in HTML source.

**Status:** Fixed in current build (May 2026).

---

### Bug 4: GeoJSON Coordinate Nesting — Polygon vs MultiPolygon

*(Already documented above in the PSA/NAMRIA section — repeating here for bug log completeness.)*

**Symptom:** No barangay boundary polygons appeared on map. Municipality boundaries showed for some LGUs but not all.

**Root cause:** Python extraction script used `[simplified]` instead of `simplified` for Polygon geometry coordinates, adding one extra nesting level (`coordinates = [[ring]]` instead of `coordinates = [ring]`). This caused `_polygonCentroid()` to receive rings instead of points, returning NaN centroids, so all barangay entries were silently dropped from `built[]`.

**Correct nesting:**
- Polygon: `coordinates[0][0]` = `[lng, lat]` (float pair)
- MultiPolygon: `coordinates[0][0][0]` = `[lng, lat]` (float pair)

**Fix:** Regenerate GeoJSON with correct nesting. Always verify with: `coordinates[0][0] = [123.xxx, 13.xxx]` for Polygon (should be a two-element float array).

**Status:** Fixed in current build (May 2026) — corrected files re-embedded in HTML.
