# PR Tool Map Architecture — Reference Document for Philippines Extension
*How the Puerto Rico tool's map actually works, what the Philippines tool is missing, and exactly how to fix it.*

---

## The Core Problem

The PR tool renders a **dense, color-scored hex grid** that fills the entire island — every point of land gets a color based on the nearest municipality's computed score. The Philippines tool renders **circle markers** (dots at the municipality centroid). That's the entire visual difference. The hex grid is also what makes clicking anywhere on the map work — you click a hex, it finds the nearest municipality, and opens the detail panel. Dots require precise clicks.

The Philippines tool has everything else right — MUNICIPIOS data structure, scoring functions, story data, landing screen. The map layer itself is the gap.

---

## What Needs to Be Added (Gap Analysis)

| Component | PR Tool | Philippines Tool | Status |
|---|---|---|---|
| H3 hex engine (inline JS) | ✅ Lines 19–81 | ❌ Missing entirely | Must add |
| Canvas renderer | ✅ `L.canvas()` | ❌ Missing | Must add |
| `hexLayer` + `generateHexes()` | ✅ ~200 lines | ❌ Missing | Must add |
| `ptInAlbay()` polygon mask | ✅ `ptInPR()` equivalent | ❌ Missing | Must add (Albay coords) |
| Albay coastline polygon | ✅ `PR_POLY` | ❌ Missing | Must add (Albay coords) |
| SVG coast clip | ✅ `initCoastClip()` | ❌ Missing | Must add |
| `nearestMuniCached()` | ✅ Full with grid cache | ❌ Missing | Must add |
| `hexScore()` with noise | ✅ Spatial micro-variation | ❌ Missing | Must add (adapted fields) |
| Multi-stop color interpolation | ✅ `interpColor()` | ❌ Basic if/else | Should upgrade |
| SOC_LAYERS additive formula | ✅ Weighted additive | Partial | Adapt |
| `scheduleRegen()` debounce | ✅ Zoom-aware | ❌ Missing | Must add |
| Boundary choropleth | ✅ esri-leaflet fetch | Partial (Overpass) | Overpass is fine, needs color sync |

---

## Part 1: The H3 Hex Engine (Copy Verbatim)

The PR tool does not use the real h3-js library (CDN dependency risk). It ships an inline implementation that mimics exactly the three functions used: `polygonToCells`, `cellToLatLng`, `cellToBoundary`.

**Copy this entire block into the Philippines `<head>`, after the Leaflet script tag:**

```html
<!-- h3-js inlined - no CDN dependency. Mimics polygonToCells, cellToLatLng, cellToBoundary -->
<script>
(function(){
'use strict';
// Circumradius in degrees latitude for each resolution level
// Calibrated to match H3 visual hex sizes at each zoom
var RES_R={7:0.013,8:0.005,9:0.0018,10:0.0007};
var S3=1.73205080757; // Math.sqrt(3)

function polygonToCells(polygon,res){
  var ring=(polygon.length>0&&Array.isArray(polygon[0])&&Array.isArray(polygon[0][0]))?polygon[0]:polygon;
  var lats=ring.map(function(p){return p[0];});
  var lngs=ring.map(function(p){return p[1];});
  var minLat=Math.min.apply(null,lats);
  var maxLat=Math.max.apply(null,lats);
  var minLng=Math.min.apply(null,lngs);
  var maxLng=Math.max.apply(null,lngs);
  var R=RES_R[res]||RES_R[7];
  var midLat=(minLat+maxLat)/2;
  var cosLat=Math.cos(midLat*Math.PI/180)||0.001;
  var rowStep=R*1.5;
  var colStep=R*S3/cosLat;
  var cells=[];
  var row=0;
  var lat=minLat-R*2;
  while(lat<=maxLat+R*2){
    var lngOff=(row%2===1)?(colStep/2):0;
    var lng=minLng-colStep+lngOff;
    while(lng<=maxLng+colStep){
      cells.push([lat,lng,res]);
      lng+=colStep;
    }
    lat+=rowStep;
    row++;
  }
  return cells;
}

function cellToLatLng(cell){return[cell[0],cell[1]];}

function cellToBoundary(cell){
  var lat=cell[0],lng=cell[1],res=cell[2];
  var R=RES_R[res]||RES_R[7];
  var cosLat=Math.cos(lat*Math.PI/180)||0.001;
  var verts=[];
  for(var i=0;i<6;i++){
    var a=i*Math.PI/3;
    verts.push([lat+R*Math.sin(a),lng+R*Math.cos(a)/cosLat]);
  }
  return verts;
}

window.h3={polygonToCells:polygonToCells,cellToLatLng:cellToLatLng,cellToBoundary:cellToBoundary};
})();
</script>
```

**Why RES_R values matter:** These control how large hexes appear at each zoom level. `7:0.013` = ~1.2km hex diameter at low zoom; `10:0.0007` = ~65m at high zoom. These same values work for the Philippines — they're based on degrees, not geography.

---

## Part 2: Albay Coastline Polygon (Replace ptInPR)

The PR tool uses `ptInPR()` to test whether a hex cell center is over land before rendering it. Without this, you get hexes covering the ocean. You need `ptInAlbay()` with an Albay Province polygon.

**Add this block after MUNICIPIOS definition:**

```javascript
// ================================================================
// ALBAY PROVINCE POLYGON MASKING
// ================================================================
// Approximate Albay Province coastline + inland boundary
// Refined polygon — replace with MGB/PSA shapefile coords when available
var ALBAY_POLY = [
  // North coast (San Miguel Bay / Lagonoy Gulf area going clockwise)
  [13.540, 123.740], // Tiwi north coast
  [13.520, 123.800], // NE tip, Lagonoy Gulf
  [13.480, 123.860], // Manito northeast
  [13.420, 123.930], // Manito east coast
  [13.360, 124.010], // East coast
  [13.280, 124.060], // Bacacay east / Rapu-Rapu channel (exclude island)
  [13.200, 124.000], // SE coast toward Legazpi
  [13.140, 123.820], // Legazpi Bay south
  [13.080, 123.760], // Legazpi south coast
  [13.020, 123.700], // Jovellar south
  [12.960, 123.640], // South border (Sorsogon boundary)
  [12.940, 123.560], // Southwest border
  [12.980, 123.480], // West border (Camarines Sur boundary)
  [13.040, 123.440], // Polangui / Oas area
  [13.130, 123.440], // Ligao City area
  [13.220, 123.450], // Interior NW
  [13.320, 123.490], // Libon / Camarines Sur border
  [13.380, 123.540], // Interior north
  [13.450, 123.600], // Polangui north
  [13.500, 123.660], // Tabaco City NW
  [13.540, 123.700], // Tabaco City north coast
  [13.540, 123.740], // close polygon
];

// Rapu-Rapu Island polygon (separate — it's an island municipality)
var RAPURAPU_POLY = [
  [13.240, 124.060],
  [13.200, 124.080],
  [13.160, 124.150],
  [13.130, 124.180],
  [13.150, 124.220],
  [13.200, 124.200],
  [13.250, 124.150],
  [13.260, 124.100],
  [13.240, 124.060],
];

// Manito Island patch (connects Manito municipality)
var MANITO_POLY = [
  [13.280, 124.000],
  [13.260, 124.080],
  [13.300, 124.100],
  [13.320, 124.060],
  [13.300, 124.010],
  [13.280, 124.000],
];

function ptInPoly(lat,lng,poly){
  var inside=false;
  for(var i=0,j=poly.length-1;i<poly.length;j=i++){
    var xi=poly[i][1],yi=poly[i][0],xj=poly[j][1],yj=poly[j][0];
    if(((yi>lat)!==(yj>lat))&&(lng<(xj-xi)*(lat-yi)/(yj-yi)+xi)) inside=!inside;
  }
  return inside;
}

function ptInAlbay(lat,lng){
  // Quick bbox pre-filter
  if(lat<12.90||lat>13.57||lng<123.40||lng>124.25) return false;
  return ptInPoly(lat,lng,ALBAY_POLY)||ptInPoly(lat,lng,RAPURAPU_POLY)||ptInPoly(lat,lng,MANITO_POLY);
}
```

**This polygon is the primary cause of ocean hex bleed.** The 20-point version above produces visible hexes over Lagonoy Gulf and the bay south of Legazpi because large inlets are bridged by straight lines. Use the refined 30-point version below instead, and replace with PSA/NAMRIA coords for production:

```javascript
// REFINED ALBAY_POLY — 30 points, significantly reduces ocean bleed
// For production: replace with PSA/NAMRIA official provincial boundary
// Source: mapshaper.org → simplify GADM Level-2 shapefile to ~0.001° tolerance
var ALBAY_POLY = [
  [13.545, 123.530], // NW — Camarines Sur border near Libon
  [13.540, 123.600], // N interior
  [13.535, 123.680], // Tabaco north coast
  [13.520, 123.740], // Tabaco City coast
  [13.500, 123.790], // Tiwi northwest coast
  [13.480, 123.860], // Tiwi hot springs coast
  [13.460, 123.940], // Tiwi NE coast
  [13.440, 124.010], // Tiwi east tip — Lagonoy Gulf
  [13.400, 124.040], // Manito-Bacacay coast heading south
  [13.360, 124.060], // Bacacay east
  [13.320, 124.060], // Bacacay south / Rapu-Rapu channel
  [13.280, 124.040], // Guinobatan east coast
  [13.240, 123.980], // Legazpi bay north
  [13.200, 123.960], // Legazpi bay NE — approaching Legazpi City
  [13.150, 123.870], // Legazpi City waterfront
  [13.100, 123.800], // South Legazpi / Daraga coast
  [13.060, 123.760], // Malilipot south
  [13.020, 123.720], // Camalig south
  [12.970, 123.680], // Jovellar coast toward Sorsogon
  [12.950, 123.640], // SW tip — Sorsogon border
  [12.940, 123.580], // South Oas area
  [12.960, 123.510], // West — Oas / Camarines Sur border
  [13.000, 123.465], // Polangui west
  [13.060, 123.450], // Libon west
  [13.130, 123.445], // Oas / Ligao west border
  [13.200, 123.450], // Ligao City west
  [13.280, 123.460], // Guinobatan west
  [13.360, 123.480], // Camalig / Camarines Sur border
  [13.420, 123.500], // Libon NW
  [13.480, 123.510], // Camarines Sur border north
  [13.545, 123.530], // close ring — back to NW corner
];
```

**Getting more accurate coords for production:**
1. Download Albay Province from [GADM](https://gadm.org/download_country.html) → Philippines → Level 2
2. Open the GeoJSON at [mapshaper.org](https://mapshaper.org)
3. Filter to just the Albay feature: `filter 'NAME_2 == "Albay"'`
4. Simplify: Edit → Simplify → `0.1%` (keeps ~100 vertices, removes noise)
5. Export as GeoJSON, extract the `coordinates[0]` outer ring
6. Swap each `[lng, lat]` to `[lat, lng]` (GADM GeoJSON uses GeoJSON order which is `[lng, lat]`)

**Note:** The polygon only needs to be accurate enough that hex *centers* over water are excluded. The SVG coast clip (Part 8) handles visual jaggedness at the edges. A 60–100 point polygon from GADM/simplified shapefile eliminates virtually all ocean bleed.

---

## Part 3: Color Scales (Upgrade from if/else to Interpolation)

The Philippines tool uses hard step `riskColor()` (4 if/else bands). The PR tool uses smooth linear interpolation between color stops. Smooth is much better visually.

**Replace the existing `riskColor()` and `resColor()` functions:**

```javascript
// ================================================================
// COLOR SCALES — smooth multi-stop interpolation
// ================================================================
var RISK_STOPS=[[0,[0,224,150]],[.22,[74,222,128]],[.42,[255,217,61]],[.64,[255,107,53]],[.82,[255,45,85]],[1,[180,0,50]]];
// Green = high resilience; dark = low resilience
var RES_STOPS=[[0,[18,38,28]],[.25,[22,85,55]],[.50,[34,160,95]],[.75,[52,211,130]],[1,[0,240,130]]];

function interpColor(t,stops){
  var s=Math.max(0,Math.min(1,t));
  for(var i=0;i<stops.length-1;i++){
    var a=stops[i][0],ca=stops[i][1],b=stops[i+1][0],cb=stops[i+1][1];
    if(s<=b){
      var f=(s-a)/(b-a);
      return 'rgb('+Math.round(ca[0]+f*(cb[0]-ca[0]))+','+Math.round(ca[1]+f*(cb[1]-ca[1]))+','+Math.round(ca[2]+f*(cb[2]-ca[2]))+')';
    }
  }
  return 'rgb('+stops[stops.length-1][1].join(',')+')';
}

function riskColor(t){return interpColor(t,RISK_STOPS);}
function resColor(t){return interpColor(t,RES_STOPS);}
function normalize(arr){
  var mn=Math.min.apply(null,arr),mx=Math.max.apply(null,arr),r=mx-mn||.01;
  return arr.map(function(v){return(v-mn)/r;});
}
```

**The normalize() function is critical:** In all modes except Resilience, scores are *locally normalized* — the visible viewport's min/max become 0–1. This spreads contrast across whatever you're looking at. In Resilience mode, raw scores are used (absolute 0–1 so the legend thresholds mean something consistent).

---

## Part 4: Score Calculation (Adapted for Philippines Fields)

The PR score pipeline has three layers: physical, social (additive on top of physical), and resilience. The Philippines version should follow the same additive pattern.

```javascript
// ================================================================
// SCORE CALCULATION
// ================================================================
// activePhys: Set of active hazard toggles
// activeSoc: Set of active social vulnerability toggles
var activePhys = new Set(['vol','typh','flood']);
var activeSoc  = new Set();

// Albay-specific physical hazard sub-scores (pvol, ptyph, pfl = fields in MUNICIPIOS)
// Weights are calibrated: volcanic is primary hazard for Mayon flank communities
function calcPhys(m){
  if(!activePhys.size) return 0;
  var s=0,w=0;
  if(activePhys.has('vol'))   {w+=1.5; s+=m.pvol*1.5;}
  if(activePhys.has('typh'))  {w+=1.2; s+=m.ptyph*1.2;}
  if(activePhys.has('flood')) {w+=1.0; s+=m.pfl*1.0;}
  if(activePhys.has('tenure')){w+=0.8; s+=m.ptenure*0.8;} // tenure as compound vulnerability
  return w>0?s/w:0;
}

// SOC_LAYERS: social vulnerability dimensions — each maps to a field in MUNICIPIOS
// id = toggle checkbox id, key = MUNICIPIOS field name, w = weight in additive formula
var SOC_LAYERS=[
  {id:'housing', key:'svi_housing', w:.18},
  {id:'poverty', key:'svi_poverty', w:.20},
  {id:'elderly', key:'svi_elderly', w:.12},
  {id:'road',    key:'svi_road',    w:.15},
  {id:'cell',    key:'svi_cell',    w:.10},
  {id:'doc',     key:'svi_doc',     w:.25}, // tenure documentation — highest weight for Albay
];
var SOC_MAX_W=SOC_LAYERS.reduce(function(a,l){return a+l.w;},0);

// ADDITIVE formula: social vulnerability adds to physical score
// This causes Rapu-Rapu and Santo Domingo to jump dramatically when doc/tenure toggles are on
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
  // No ceiling — scores float above 1.0; local normalize() spreads full spectrum
  return physS+socNorm*frac*1.2;
}

function calcScore(m){
  if(curMode==='res')  return m.res;
  if(curMode==='phys') return calcPhys(m);
  return calcSoc(m);
}
```

**The additive formula is the key insight:** When a user turns on the documentation barrier toggle, Rapu-Rapu and Santo Domingo should visibly jump in color because their `svi_doc` values are the highest in the province. The formula `physS + socNorm * frac * 1.2` ensures this. Starting from physical and adding social means the mountain of data tells the right story: Rapu-Rapu's isolation + informal tenure + physical exposure compound visibly.

---

## Part 5: Nearest Municipality Cache

The hex engine calls a muni-lookup function for every hex cell — potentially thousands per render. Without caching this is too slow. The PR tool uses a grid-snapped key to cache results.

```javascript
// ================================================================
// MUNI LOOKUP CACHE
// ================================================================
function nearestMuni(lat,lng){
  var best=null,bd=Infinity;
  var cosL=Math.cos(lat*Math.PI/180);
  MUNICIPIOS.forEach(function(m){
    var d=(m.lat-lat)*(m.lat-lat)+((m.lng-lng)*cosL)*((m.lng-lng)*cosL);
    if(d<bd){bd=d;best=m;}
  });
  return best;
}

var _muniCache={};
function nearestMuniCached(lat,lng){
  // Snap to ~2km grid for cache key (multiply by 50 = cells of 0.02°)
  var key=(lat*50|0)+','+(lng*50|0);
  if(_muniCache[key]) return _muniCache[key];
  var m=nearestMuni(lat,lng);
  _muniCache[key]=m;
  return m;
}

// Deterministic noise hash for per-hex micro-variation (prevents banding)
function phash(lat,lng){
  var s=Math.sin(lat*127.1+lng*311.7)*43758.5453;
  return s-Math.floor(s);
}
```

---

## Part 6: The hexScore() Function (Albay Adaptation)

Every hex cell gets a score from `hexScore()`. This function adds small per-hex random variation (using `phash`) so adjacent hexes within the same municipality don't all appear identical — it breaks up the Voronoi-tile look and makes the map feel continuous rather than blocky.

```javascript
function hexScore(lat,lng){
  var m=nearestMuniCached(lat,lng);
  // Resilience mode: raw scores, no jitter (so legend bands are meaningful)
  if(curMode==='res') return m&&m.res!=null?m.res:0.30;
  var rnd=(phash(lat,lng)-.5); // -0.5 to +0.5

  // Geographic adjustments for Albay
  // Mayon summit coords: [13.2567, 123.6853]
  var distFromMayon=Math.sqrt(Math.pow(lat-13.2567,2)+Math.pow((lng-123.6853)*Math.cos(lat*Math.PI/180),2));
  var volcBoost=(distFromMayon<0.08)?Math.max(0,(0.08-distFromMayon)/0.08)*0.12:0; // hot spot near Mayon
  var coastBoost=Math.max(0,(0.06-Math.min(Math.abs(lat-13.3),Math.abs(lat-13.1)))*2)*0.06; // coast surge

  var cl=function(v){return Math.min(1,Math.max(0,v));};
  var hm=Object.assign({},m,{
    pvol:  cl(m.pvol  + volcBoost + rnd*.04),
    ptyph: cl(m.ptyph + coastBoost + rnd*.04),
    pfl:   cl(m.pfl   + rnd*.03),
    ptenure: cl(m.ptenure + rnd*.02),
    svi_housing: cl(m.svi_housing + rnd*.04),
    svi_poverty: cl(m.svi_poverty + rnd*.04),
    svi_elderly: cl(m.svi_elderly + rnd*.03),
    svi_road:    cl(m.svi_road    + rnd*.04),
    svi_cell:    cl(m.svi_cell    + rnd*.04),
    svi_doc:     cl(m.svi_doc     + rnd*.03),
  });
  if(curMode==='phys') return calcPhys(hm);
  return calcSoc(hm);
}
```

**The `volcBoost` pattern:** Hexes very close to Mayon's summit (within ~9km) get an additional boost to volcanic hazard score regardless of which municipality they're nearest to. This prevents the visual discontinuity that would otherwise appear at municipal boundary lines — the danger zone looks continuous rather than chopped.

---

## Part 7: The Hex Generation Engine

This is the core rendering loop. It runs on every pan/zoom event (debounced) and redraws all hexes.

```javascript
// ================================================================
// HEX ENGINE
// ================================================================
var canvasRenderer = L.canvas({padding:0.3});
var hexLayer = L.layerGroup().addTo(map);
var _lastZoom = -1, _regenTimer = null;

function getH3Res(zoom){
  if(zoom>=14) return 10;
  if(zoom>=12) return 9;
  if(zoom>=10) return 8;
  return 7;
}

function scheduleRegen(delay){
  if(_regenTimer) clearTimeout(_regenTimer);
  _regenTimer = setTimeout(generateHexes, delay||180);
}

var _muniPolyMap = {}; // maps muni name → [polygon, polygon, ...] for click handling

function generateHexes(){
  if(!map||typeof map.getBounds!=='function') return;

  // Culture/Stories tabs: no hex overlay needed
  if(curMode==='cult'||curMode==='str'){
    hexLayer.clearLayers();
    if(canvasRenderer&&canvasRenderer._canvas) canvasRenderer._canvas.style.clipPath='';
    return;
  }

  var bounds = map.getBounds();
  var zoom   = map.getZoom();
  var res    = getH3Res(zoom);
  var pad    = 0.04;
  var n=bounds.getNorth()+pad, s=bounds.getSouth()-pad;
  var e=bounds.getEast()+pad,  w=bounds.getWest()-pad;

  var viewPoly = [[n,w],[n,e],[s,e],[s,w],[n,w]];
  var cells;
  try{ cells = h3.polygonToCells(viewPoly, res); }
  catch(err){ return; }

  // Filter to land cells only
  var landCells = [];
  cells.forEach(function(cell){
    var c = h3.cellToLatLng(cell);
    if(!ptInAlbay(c[0],c[1])) return;
    landCells.push(cell);
  });
  if(!landCells.length) return;

  // Compute scores for all land cells
  var scores = landCells.map(function(cell){
    var c = h3.cellToLatLng(cell);
    return hexScore(c[0], c[1]);
  });

  // Normalize EXCEPT in resilience mode (res mode uses absolute scale)
  var norm = curMode==='res'
    ? scores.map(function(v){return Math.max(0,Math.min(1,v||0));})
    : normalize(scores);
  var cf   = curMode==='res' ? resColor : riskColor;
  var sw   = zoom>=13 ? 0.25 : zoom>=11 ? 0.4 : 0.6; // stroke weight scales with zoom

  hexLayer.clearLayers();
  _muniPolyMap = {};

  landCells.forEach(function(cell,i){
    var boundary = h3.cellToBoundary(cell); // [[lat,lng],...] Leaflet-ready
    var c        = h3.cellToLatLng(cell);
    var m        = nearestMuniCached(c[0], c[1]);
    var poly     = L.polygon(boundary,{
      renderer:    canvasRenderer,
      weight:      sw,
      color:       'rgba(255,255,255,0.14)',
      fillColor:   cf(norm[i]),
      fillOpacity: 0.50,
    });

    if(!_muniPolyMap[m.n]) _muniPolyMap[m.n] = [];
    _muniPolyMap[m.n].push(poly);

    poly.on('click', function(){
      if(typeof openPanel==='function') openPanel(m);
    });
    poly.on('mouseover', function(e){
      poly.setStyle({weight:2, color:'rgba(255,255,255,0.75)'});
      L.popup({closeButton:false, offset:[0,-2]})
        .setLatLng(e.latlng)
        .setContent('<strong>'+m.n+'</strong><br><span style="color:#8896AA;font-size:11px">Click for full analysis</span>')
        .openOn(map);
    });
    poly.on('mouseout', function(){
      poly.setStyle({weight:sw, color:'rgba(255,255,255,0.14)'});
      map.closePopup();
    });

    hexLayer.addLayer(poly);
  });

  refreshCoastClip();
}

map.on('moveend zoomend', function(){ scheduleRegen(200); });
map.on('zoom', function(){
  var nr=getH3Res(map.getZoom()), or=getH3Res(_lastZoom);
  if(nr!==or) scheduleRegen(60);
});
```

**Why `scheduleRegen` instead of direct call:** Debouncing prevents re-rendering on every frame during a pan gesture. The 180ms delay means rendering only fires when the map has settled.

---

## Part 8: SVG Coast Clip

Without this, hexes near the coastline have jagged half-hexes sticking out over the water. The SVG clip path masks the canvas renderer to the coastline polygon shape, so hexes are cleanly clipped to land.

```javascript
// ================================================================
// COAST CLIP — SVG clipPath applied to hex canvas
// ================================================================
function initCoastClip(){
  var mapDiv = document.getElementById('map');
  if(!mapDiv || document.getElementById('coast-clip-svg')) return;
  var ns  = 'http://www.w3.org/2000/svg';
  var svg = document.createElementNS(ns, 'svg');
  svg.id  = 'coast-clip-svg';
  svg.setAttribute('style','position:absolute;top:0;left:0;width:0;height:0;overflow:hidden;pointer-events:none;z-index:-1');
  var defs = document.createElementNS(ns,'defs');
  var cp   = document.createElementNS(ns,'clipPath');
  cp.id    = 'coast-clip';
  cp.setAttribute('clipPathUnits','userSpaceOnUse');
  // One polygon element per land polygon (mainland + islands)
  ['main','rapurapu','manito'].forEach(function(id){
    var p = document.createElementNS(ns,'polygon');
    p.id  = 'coast-cp-'+id;
    cp.appendChild(p);
  });
  defs.appendChild(cp);
  svg.appendChild(defs);
  mapDiv.appendChild(svg);
}

function refreshCoastClip(){
  var canvas = canvasRenderer && canvasRenderer._canvas;
  if(!canvas) return;
  var mpEl = document.getElementById('coast-cp-main');
  var rrEl = document.getElementById('coast-cp-rapurapu');
  var mnEl = document.getElementById('coast-cp-manito');
  if(!mpEl||!rrEl||!mnEl) return;

  var mapDiv = document.getElementById('map');
  var cr = canvas.getBoundingClientRect();
  var mr = mapDiv.getBoundingClientRect();
  var ox = cr.left - mr.left;
  var oy = cr.top  - mr.top;

  function polyPts(ring){
    return ring.map(function(ll){
      var p = map.latLngToContainerPoint(L.latLng(ll[0],ll[1]));
      return (p.x-ox)+','+(p.y-oy);
    }).join(' ');
  }

  mpEl.setAttribute('points', polyPts(ALBAY_POLY));
  rrEl.setAttribute('points', polyPts(RAPURAPU_POLY));
  mnEl.setAttribute('points', polyPts(MANITO_POLY));
  canvas.style.clipPath = 'url(#coast-clip)';
}

// Call on init (after map is ready) and on every move/zoom
map.whenReady(function(){ initCoastClip(); });
map.on('moveend zoomend', refreshCoastClip);
```

---

## Part 9: setMode() Hook — Must Trigger Hex Regeneration

Every time the tab changes, `setMode()` must trigger `generateHexes()` so the hex colors update to reflect the new scoring mode. Without this, switching from Physical to Vulnerability doesn't change any colors.

**In the `setMode()` function, add this near the end:**

```javascript
function setMode(mode){
  curMode = mode;
  // ... existing tab switching logic ...

  // Regenerate hexes immediately for new mode
  if(mode==='cult'||mode==='str'){
    // These tabs don't use the hex grid — clear it
    hexLayer.clearLayers();
    if(canvasRenderer&&canvasRenderer._canvas) canvasRenderer._canvas.style.clipPath='';
  } else {
    // Re-score and re-color all hexes for new mode
    scheduleRegen(0);
  }

  // Sync boundary polygon colors with new hex colors
  updateBoundaryColors();
}
```

**And `updateBoundaryColors()` needs to use `calcScore()` not `getColor()`:**

```javascript
function updateBoundaryColors(){
  if(!_muniPolys) return;
  _muniPolys.forEach(function(obj){
    var col = curMode==='res' ? resColor(obj.m.res||.5) : riskColor(calcScore(obj.m));
    try{obj.poly.setStyle({fillColor:col, color:'rgba(255,255,255,0.18)'});}catch(e){}
  });
}
```

---

## Part 10: Removing Circle Markers

Once the hex grid is in place, the `buildMarkers()` / `muniMarkers` system is redundant and conflicts with the hex layer. Remove:

- The `buildMarkers()` function
- The `buildMarkers()` call
- The `muniMarkers = []` array and all `map.removeLayer(mk)` calls on it

The hex click handler (`poly.on('click', function(){ openPanel(m); })`) takes over all municipality click handling. You can keep the boundary polygon layer (Overpass) as a choropleth overlay — it's a good complement to the hexes.

---

## Part 11: Keeping the Overpass Boundary Layer (But Fixing It)

The Philippines tool fetches municipality boundaries from Overpass API and renders them as colored polygons. This is good — it provides visible municipality outlines. But there are two problems:

**Problem 1:** Overpass can be slow or fail — always add a fallback:
```javascript
function fetchAlbayBoundaries(){
  var query='[out:json][timeout:60];rel["name"="Albay"]["admin_level"="4"];map_to_area->.a;rel(area.a)["admin_level"="6"]["boundary"="administrative"];out geom;';
  var done=false;
  var timer=setTimeout(function(){
    if(!done){done=true; console.warn('Overpass timeout — map still functional via hex grid');}
  },15000);
  fetch('https://overpass-api.de/api/interpreter',{method:'POST',body:'data='+encodeURIComponent(query)})
    .then(function(r){return r.json();})
    .then(function(data){clearTimeout(timer);done=true;processOverpassData(data);})
    .catch(function(e){clearTimeout(timer);console.warn('Overpass error:',e);});
}
```

**Problem 2:** Boundary colors must use the same `calcScore()` / color functions as the hexes. Currently `processOverpassData` calls `getColor(m)` which uses the old if/else `riskColor`. After upgrading to `interpColor`, make sure the boundary layer calls the same function so colors match.

---

## Part 12: Initialization Order

The correct initialization sequence:

```javascript
// 1. Map init (already done)
var map = L.map('map',...).setView([13.18,123.73],10);

// 2. Tile layers (already done)
darkBase.addTo(map);

// 3. After map is ready, start hex rendering
map.whenReady(function(){
  initCoastClip();           // set up SVG clip element
  generateHexes();           // first render
  fetchAlbayBoundaries();    // async boundary fetch (non-blocking)
});

// 4. Score mode changes trigger re-render
// (handled in setMode() → scheduleRegen(0))
```

---

## Part 13: Bugs Fixed on the PR Tool (Apply Same Fixes to Philippines)

### Bug 1: Tooltip Stacking (Fixed in PR — Must Apply to Philippines Too)
**Problem:** When mousing quickly over multiple municipalities, tooltips stack instead of replacing each other.
**Fix:** In the hex `mouseover` handler, explicitly close all other open tooltips before showing the new one:

```javascript
poly.on('mouseover', function(e){
  // Close any stuck tooltips on other hex polys
  if(hexLayer){hexLayer.eachLayer(function(l){if(l!==poly){try{l.closeTooltip();}catch(err){}}}); }
  poly.setStyle({weight:2, color:'rgba(255,255,255,0.75)'});
  // ... open popup ...
});
poly.on('mouseout', function(){
  try{poly.closeTooltip();}catch(err){}
  poly.setStyle({weight:sw, color:'rgba(255,255,255,0.14)'});
  map.closePopup();
});
```

For the Philippines tool, apply this same pattern to the boundary polygon layer's `mouseover`/`mouseout` too.

### Bug 2: Tract/Boundary Interactions on Resilience Tab
**Problem:** On the Resilience tab, clicking individual tracts or boundary polygons opens the detail panel, but the tab is supposed to only be about resilience hubs (pins).
**Fix:** Early-return in the click handler if `curMode==='res'`:

```javascript
poly.on('click', function(){
  if(curMode==='res') return; // Resilience tab: pins only
  if(typeof openPanel==='function') openPanel(m);
});
poly.on('mouseover', function(){
  if(curMode==='res'){try{poly.closeTooltip();}catch(e){} return;}
  // ... rest of mouseover logic
});
```

### Bug 3: Duplicate Composite Portrait Disclaimer
**Problem:** The Human Stories panel shows two "COMPOSITE PORTRAITS" callout boxes — one hardcoded in static HTML, one injected dynamically by JavaScript when the list renders.
**Fix:** Remove the dynamically injected one (keep the static one). In the `renderStoryList()` or equivalent function, find and remove:
```javascript
h+='<div class="str-composite-note">...</div>';
```

### Bug 4: Boundary Colors Out of Sync After Mode Change
**Problem:** Switching tabs doesn't update the boundary polygon fill colors — they stay the color of the previous mode.
**Fix:** Call `updateBoundaryColors()` inside `setMode()` every time the mode changes (described in Part 9 above).

---

## Part 14: Complete Philippines Tool Data Fields Reference

The MUNICIPIOS objects in the Philippines tool use these fields. Make sure every field is present on every municipality object, or the scoring functions will return NaN:

| Field | Type | Range | Description |
|---|---|---|---|
| `n` | string | — | Municipality name (must match Overpass OSM name) |
| `lat`,`lng` | float | Albay coords | Municipality centroid |
| `pop` | int | — | Population |
| `phys` | float | 0–1 | Overall physical hazard composite (pre-computed) |
| `svi` | float | 0–1 | Overall SVI composite (pre-computed) |
| `pwr` | int | days | Post-storm power restoration time proxy |
| `road` | string | low/medium/high | Road access difficulty |
| `pvol` | float | 0–1 | Volcanic hazard sub-score |
| `ptyph` | float | 0–1 | Typhoon hazard sub-score |
| `pfl` | float | 0–1 | Flood hazard sub-score |
| `ptenure` | float | 0–1 | Informal tenure prevalence (higher = more informal) |
| `svi_housing` | float | 0–1 | Housing fragility SVI sub-score |
| `svi_poverty` | float | 0–1 | Poverty SVI sub-score |
| `svi_elderly` | float | 0–1 | Elderly/care burden SVI sub-score |
| `svi_road` | float | 0–1 | Road isolation SVI sub-score |
| `svi_cell` | float | 0–1 | Cell/communications SVI sub-score |
| `svi_doc` | float | 0–1 | Documentation barrier (0=fully titled, 1=fully informal) |
| `res` | float | 0–1 | Community resilience score |
| `rtag` | string | — | Short resilience tag for display |
| `rnote` | string | — | Resilience note for panel |
| `in_pdz` | bool | — | Whether municipality has barangays in APSEMO PDZ |
| `detail` | string | — | Full narrative text for detail panel |

**If any numeric field is missing on a municipality object, add a default:**
```javascript
// Safe defaults for any missing field
var FIELD_DEFAULTS = {pvol:.3,ptyph:.3,pfl:.3,ptenure:.3,svi_housing:.4,svi_poverty:.4,svi_elderly:.3,svi_road:.3,svi_cell:.3,svi_doc:.3,res:.5};
MUNICIPIOS.forEach(function(m){
  Object.keys(FIELD_DEFAULTS).forEach(function(k){
    if(m[k]===undefined||m[k]===null) m[k]=FIELD_DEFAULTS[k];
  });
});
```

---

## Part 15: Testing the Hex Grid

When hex generation is working, you should see:
1. At zoom 10 (the default starting zoom), ~300–500 hexes filling Albay Province
2. Hexes colored from green (low risk) to red/crimson (high risk)
3. Mayon's immediate flank hexes should be the darkest red/crimson
4. Rapu-Rapu Island should appear as a separate small cluster of hexes
5. No hexes over the ocean/water bodies
6. Clicking any hex opens the municipality detail panel

**Debugging:** If hexes are not appearing, add this to `generateHexes()` after the `landCells` filter:
```javascript
console.log('Hex debug — cells:', cells.length, 'landCells:', landCells.length, 'ptInAlbay test:', ptInAlbay(13.18, 123.73));
```
- `cells.length` should be several hundred
- `landCells.length` should be ~60–70% of cells
- `ptInAlbay(13.18, 123.73)` (Legazpi City centroid) should return `true`

If `landCells.length === 0`, the ALBAY_POLY polygon is wrong — check coordinate order (must be lat,lng not lng,lat) and ensure the polygon closes (first and last point match).

---

## Quick Implementation Order

1. Add H3 inline script to `<head>` (Part 1)
2. Add ALBAY_POLY + ptInAlbay() after MUNICIPIOS (Part 2)
3. Replace riskColor/resColor/add normalize() (Part 3)
4. Update calcPhys/calcSoc/SOC_LAYERS (Part 4)
5. Add nearestMuniCached + phash (Part 5)
6. Add hexScore() (Part 6)
7. Add canvasRenderer + hexLayer + generateHexes() (Part 7)
8. Add initCoastClip + refreshCoastClip + map event listeners (Part 8)
9. Update setMode() to call scheduleRegen() (Part 9)
10. Remove buildMarkers() and muniMarkers (Part 10)
11. Apply the three bug fixes to boundary/hover handlers (Part 13)
12. Wire up left panel nav buttons and group show/hide (Part 16)
13. Wire up right panel openPanel() and tab switching (Part 17)

---

## Part 16: Left Panel Architecture

The left panel is a collapsible sidebar on the left edge of the screen. It contains all mode navigation, narrative framing, and the SVI layer builder.

### Collapsed vs. Expanded

The panel expands/collapses by toggling the `.lp-pinned` class on `#leftpanel`. When collapsed, only icons are visible; `.lp-nav-text` content is hidden by CSS (`#leftpanel:not(.lp-pinned) .lp-nav-text{display:none}`).

```javascript
function toggleLpPanel(){
  var lp = document.getElementById('leftpanel');
  lp.classList.toggle('lp-pinned');
  // Update chevron direction
  var btn = document.getElementById('lp-toggle');
  btn.textContent = lp.classList.contains('lp-pinned') ? '‹' : '›';
}
```

### Nav Buttons → Mode Groups

Each `.lp-nav-btn` carries `data-grp="[name]"` and calls `setModeGroup('[name]')`. That function:
1. Sets the active state on the clicked button
2. Shows the corresponding `#lpg-[name]` group panel, hides all others
3. Calls `setMode()` or `setModeGroup()` to update the map

```javascript
function setModeGroup(grp){
  // Update nav button active state
  document.querySelectorAll('.lp-nav-btn').forEach(function(b){
    b.classList.toggle('active', b.dataset.grp === grp);
  });
  // Show/hide group panels
  document.querySelectorAll('.lp-group').forEach(function(g){
    g.style.display = (g.id === 'lpg-' + grp) ? '' : 'none';
  });
  // Map mode update
  var modeMap = {hazard:'phys', vuln:'soc', fail:'cas', res:'res', str:'str'};
  if(modeMap[grp]) setMode(modeMap[grp]);
}
```

### Group Panel Structure

Each group panel (`#lpg-hazard`, `#lpg-vuln`, etc.) contains:
1. A `.lp-group-intro` block with a short label and a framing paragraph that explains what the tab shows and why it matters
2. One or more `.lp-accord` accordion blocks — each is a collapsible section with a question header and content body

**The intro paragraph is important for usability.** It tells users what they're about to see before they interact. Example for Philippines Vulnerability:
```html
<div class="lp-group-intro">
  <div class="lp-gi-label">THE DEEPER PICTURE</div>
  <p>Physical exposure only tells part of the story. <strong>The communities that will struggle for years after an eruption are not always the ones closest to Mayon.</strong> They are the ones where poverty, informal tenure, and aid-system invisibility compound the physical damage. Toggle SVI dimensions below to watch the map respond.</p>
</div>
```

### SVI Layer Builder (inside Vulnerability group)

The SVI Builder section should have:
- A header label: "Social Vulnerability Builder"
- A one-sentence note naming the key community that jumps when documentation barriers or tenure is added: "Toggle dimensions one at a time. Watch Rapu-Rapu and Santo Domingo jump when documentation barriers are added."
- A checkbox list where each item maps to a `SOC_LAYERS` entry

```html
<div class="svi-builder-section">
  <div class="svi-builder-header">Social Vulnerability Builder</div>
  <div class="svi-builder-note">Toggle dimensions one at a time. Watch Rapu-Rapu and Santo Domingo jump when documentation barriers are added. <strong>The aid system cannot reach what it cannot see.</strong></div>
  <div id="soc-layer-list">
    <!-- Generated dynamically or hard-coded: -->
    <label class="soc-layer-item">
      <input type="checkbox" class="soc-cb" data-id="housing"
             onchange="toggleSocLayer('housing',this.checked)">
      <div class="soc-layer-body">
        <div class="soc-layer-name">Housing fragility</div>
        <div class="soc-layer-desc">Light-frame / non-engineered construction, informal materials</div>
      </div>
    </label>
    <label class="soc-layer-item">
      <input type="checkbox" class="soc-cb" data-id="poverty"
             onchange="toggleSocLayer('poverty',this.checked)">
      <div class="soc-layer-body">
        <div class="soc-layer-name">Poverty depth</div>
        <div class="soc-layer-desc">Subsistence agriculture, no savings, limited livelihood options</div>
      </div>
    </label>
    <label class="soc-layer-item">
      <input type="checkbox" class="soc-cb" data-id="elderly"
             onchange="toggleSocLayer('elderly',this.checked)">
      <div class="soc-layer-body">
        <div class="soc-layer-name">Elderly / care burden</div>
        <div class="soc-layer-desc">High elderly share, limited mobility, care dependency</div>
      </div>
    </label>
    <label class="soc-layer-item">
      <input type="checkbox" class="soc-cb" data-id="road"
             onchange="toggleSocLayer('road',this.checked)">
      <div class="soc-layer-body">
        <div class="soc-layer-name">Road isolation</div>
        <div class="soc-layer-desc">Single-route access, bridge risk, lahar channel crossings</div>
      </div>
    </label>
    <label class="soc-layer-item">
      <input type="checkbox" class="soc-cb" data-id="cell"
             onchange="toggleSocLayer('cell',this.checked)">
      <div class="soc-layer-body">
        <div class="soc-layer-name">Communication gap</div>
        <div class="soc-layer-desc">Limited cell coverage, low early warning access</div>
      </div>
    </label>
    <label class="soc-layer-item">
      <input type="checkbox" class="soc-cb" data-id="doc"
             onchange="toggleSocLayer('doc',this.checked)">
      <div class="soc-layer-body">
        <div class="soc-layer-name">Documentation barrier</div>
        <div class="soc-layer-desc">Informal tenure, no CLOA/land title — aid eligibility blocked</div>
      </div>
    </label>
  </div>
</div>
```

### Human Stories Tab — Cultural Record Note

The Human Stories tab in the **Puerto Rico** tool includes a Cultural Record section with a music component (`cr-songs`, `cr-song-lyric` CSS classes) that documents songs and cultural artifacts about Hurricane Maria. **This component is Puerto Rico-specific** and should not be replicated in the Philippines build.

For the Philippines Human Stories tab, the appropriate content is:
- **Community portraits** — drawn from the `detail` field in each MUNICIPIOS object
- **IOM LandLedger entries** — displacement and relocation records tied to specific municipalities
- **APSEMO evacuation history** — barangay-level historical evacuation narratives
- **Zero Casualty Doctrine** context — the institutional story of why pre-emptive evacuation was adopted

Do not add a music section. Do not import the `cr-song` CSS classes. The Cultural Record framework is from Daniel's academic research on Puerto Rican community narrative and is not generalized.

---

## Part 17: Right Panel (Detail Panel) Architecture

The right panel opens when a user clicks any hex. It shows municipality-level detail.

### Opening the Panel

Call `openPanel(m)` where `m` is a MUNICIPIOS object. This populates the panel header and all sub-sections, then makes the panel visible.

```javascript
function openPanel(m){
  if(!m) return;
  // Header
  document.getElementById('rp-name').textContent = m.n;
  document.getElementById('rp-meta').textContent =
    'Pop ' + (m.pop||0).toLocaleString() +
    ' · Road: ' + (m.road||'unknown') +
    ' · ~' + (m.pwr||'?') + ' days power restore';
  // Sections
  buildHazardBars(m);    // Hazard Model score bars
  buildSviBars(m);       // SVI Fingerprint bars
  buildAlertCards(m);    // Conditional alert cards (danger zone, tenure, etc.)
  buildNhaSites(m);      // Resettlement site cards if m.nha_sites exists
  // Show panel and reset to first tab
  document.getElementById('rightpanel').classList.add('open');
  setRpTab('profile');
}

function closePanel(){
  document.getElementById('rightpanel').classList.remove('open');
}
```

### Panel HTML Skeleton

```html
<div id="rightpanel">
  <!-- Placeholder shown before any hex is clicked -->
  <div class="rp-ph" id="rp-teaser">
    <div class="big">🗺</div>
    Click any area on the map to see its full vulnerability profile.
  </div>

  <!-- Populated content (hidden until openPanel() fires) -->
  <div id="rp-content" style="display:none">
    <!-- Header -->
    <div class="rp-hd">
      <button class="rp-close" onclick="closePanel()">×</button>
      <div id="rp-name"><!-- municipality name --></div>
      <div id="rp-meta"><!-- pop · road · power --></div>
    </div>

    <!-- Tab row -->
    <div class="rp-tabs">
      <button class="rp-tab active" data-tab="profile" onclick="setRpTab('profile')">PROFILE</button>
      <button class="rp-tab" data-tab="tenure" onclick="setRpTab('tenure')">TENURE</button>
      <button class="rp-tab" data-tab="use" onclick="setRpTab('use')">WHAT TO DO</button>
    </div>

    <!-- PROFILE tab -->
    <div class="rp-tab-content active" data-tab="profile">
      <div class="rp-sec">
        <h4>Hazard Model</h4>
        <div id="rp-hazard-bars"><!-- built by buildHazardBars() --></div>
      </div>
      <div class="rp-sec">
        <h4>Social Vulnerability Fingerprint</h4>
        <div id="rp-svi-bars"><!-- built by buildSviBars() --></div>
      </div>
      <div id="rp-alert-cards"><!-- built by buildAlertCards() --></div>
    </div>

    <!-- TENURE tab -->
    <div class="rp-tab-content" data-tab="tenure">
      <div class="rp-sec">
        <h4>Land Tenure Status</h4>
        <div id="rp-tenure-content"><!-- built by openPanel() --></div>
      </div>
      <div class="rp-sec">
        <h4>NHA Resettlement Sites</h4>
        <div id="rp-nha-sites"><!-- built by buildNhaSites() --></div>
      </div>
    </div>

    <!-- WHAT TO DO tab -->
    <div class="rp-tab-content" data-tab="use">
      <div class="rp-sec">
        <h4>Priority Actions</h4>
        <div id="rp-actions"><!-- built by openPanel() using m.detail --></div>
      </div>
    </div>
  </div>
</div>
```

### Hazard Model Bars — buildHazardBars(m)

```javascript
var HAZARD_FIELDS = [
  {key:'pvol',  label:'Volcanic',         color:'#FF6B35'},
  {key:'ptyph', label:'Typhoon',          color:'#A78BFA'},
  {key:'pfl',   label:'Flood/Lahar',      color:'#60A5FA'},
  {key:'phys',  label:'Composite Physical', color:'var(--cyan)', bold:true},
];

function buildHazardBars(m){
  var el = document.getElementById('rp-hazard-bars');
  el.innerHTML = HAZARD_FIELDS.map(function(f){
    var v = Math.round((m[f.key]||0)*100);
    return '<div class="rp-score-row' + (f.bold?' rp-composite':'') + '">' +
      '<span class="rp-score-lbl">' + (f.bold?'<strong>':'') + f.label + (f.bold?'</strong>':'') + '</span>' +
      '<div class="rp-bar-wrap"><div class="rp-bar" style="width:'+v+'%;background:'+f.color+'"></div></div>' +
      '<span class="rp-score-val">'+v+'</span>' +
    '</div>';
  }).join('');
}
```

### SVI Fingerprint Bars — buildSviBars(m)

```javascript
var SVI_FIELDS = [
  {key:'svi_housing', label:'Housing fragility'},
  {key:'svi_poverty', label:'Poverty depth'},
  {key:'svi_elderly', label:'Elderly population'},
  {key:'svi_road',    label:'Road Isolation'},
  {key:'svi_cell',    label:'Comm. gap'},
  {key:'svi_doc',     label:'Documentation barrier'},
];

function buildSviBars(m){
  var el = document.getElementById('rp-svi-bars');
  el.innerHTML = SVI_FIELDS.map(function(f){
    var v = Math.round((m[f.key]||0)*100);
    return '<div class="rp-score-row">' +
      '<span class="rp-score-lbl">' + f.label + '</span>' +
      '<div class="rp-bar-wrap"><div class="rp-bar" style="width:'+v+'%;background:#FF6B35"></div></div>' +
      '<span class="rp-score-val">'+v+'</span>' +
    '</div>';
  }).join('');
}
```

### Alert Cards — buildAlertCards(m)

Alert cards appear conditionally based on MUNICIPIOS flags:

```javascript
function buildAlertCards(m){
  var cards = [];
  if(m.in_pdz){
    cards.push({
      cls: 'rp-alert-danger',
      icon: '⚠️',
      title: 'Inside Mayon Danger Zone',
      text: 'Within APSEMO 8km pre-emptive evacuation zone. Informal tenure common. DSWD aid eligibility often blocked.'
    });
  }
  if((m.ptenure||0) > 0.6){
    cards.push({
      cls: 'rp-alert-warn',
      icon: '📄',
      title: 'High Informal Tenure',
      text: 'Majority of households lack formal land title. Post-disaster aid programs that require ownership documentation will underserve this community.'
    });
  }
  var el = document.getElementById('rp-alert-cards');
  el.innerHTML = cards.map(function(c){
    return '<div class="rp-alert-card ' + c.cls + '">' +
      '<div class="rp-alert-icon">' + c.icon + '</div>' +
      '<div class="rp-alert-body">' +
        '<div class="rp-alert-title">' + c.title + '</div>' +
        '<div class="rp-alert-text">' + c.text + '</div>' +
      '</div>' +
    '</div>';
  }).join('');
}
```

### Tab Switching

```javascript
function setRpTab(tabName){
  document.querySelectorAll('.rp-tab').forEach(function(t){
    t.classList.toggle('active', t.dataset.tab === tabName);
  });
  document.querySelectorAll('.rp-tab-content').forEach(function(c){
    c.classList.toggle('active', c.dataset.tab === tabName);
  });
}
```

### Key CSS Variables for Panels

```css
:root {
  --surface: #0B1828;        /* panel background */
  --surface2: #0d1f33;       /* slightly lighter — tab row, section headers */
  --border: rgba(255,255,255,.08);
  --text: #E2E8F4;
  --text-dim: #8896AA;
  --text-faint: #4A5568;
  --cyan: #00D4FF;
  --orange: #FF8C42;
}

/* Right panel positioning */
#rightpanel {
  position: fixed;
  right: 0; top: 0; bottom: 0;
  width: 320px;
  background: var(--surface);
  border-left: 1px solid var(--border);
  overflow-y: auto;
  transform: translateX(100%);
  transition: transform 0.2s ease;
  z-index: 1000;
}
#rightpanel.open { transform: translateX(0); }

/* Left panel positioning */
#leftpanel {
  position: fixed;
  left: 0; top: 0; bottom: 0;
  width: 48px;          /* collapsed width — icon only */
  background: var(--surface);
  border-right: 1px solid var(--border);
  overflow: hidden;
  transition: width 0.2s ease;
  z-index: 1000;
}
#leftpanel.lp-pinned { width: 300px; }
```
12. Test with browser console open; check hex debug output (Part 15)

---

## Part 18: Hard-Won Design Decisions — The Full Story

This section documents every major design decision made during the development of the PR tool. Many of these decisions were reached after extensive iteration, debugging, and conceptual back-and-forth. They are recorded here so that future builds — Philippines, Mexico, and beyond — start with the hard-won knowledge rather than repeating the journey.

---

### Decision 1: Why Hexagons — and Not Choropleth or Points

**The temptation:** Start with what census data gives you — municipio or census tract polygons — and color them by SVI score. This is how most vulnerability maps look. Fast to build and easy to interpret.

**The problem with choropleth at municipal level:** Puerto Rico's 78 municipios vary enormously in size. Averaging across a whole municipio blends a high-poverty coastal barrio and an inland middle-class neighborhood into one color. The visual result is a map of political boundaries, not vulnerability distribution.

**The problem with choropleth at census tract level:** PR has ~900 census tracts. Rendering 900 polygons works, but it creates visual noise where small urban tracts are nearly invisible. More importantly, it anchors the visual on administrative geometry unrelated to hazard logic.

**Why hexagons win:**
- Equal-area: every cell represents the same ground coverage, so visual weight equals geographic weight
- Resolution-independent: hexes regenerate at any zoom level; no fixed administrative unit
- Hazard-appropriate: floods and storm surge don't follow census tract boundaries; a uniform grid matches the physics better than administrative polygons
- Visually legible at scale: at island scale, the hex grid creates a readable thermal map

**The comparison that made this clear:** When the PR tool was first rendered with municipal polygons and then rerendered with hexes at ~2km resolution, the hex version immediately showed the north coast strip as higher vulnerability than the interior highlands — a pattern the municipal choropleth completely masked by averaging coastal and interior areas together.

---

### Decision 2: Hex Resolution / Size — From Municipal to Fine Grid

**Initial approach:** One hex per municipio. Hexagonal choropleth — same averaging problem, different shape.

**Intermediate approach:** Fixed ~5km hexes. Better, but still loses neighborhood-level variation.

**The zoom-responsive approach:** Right hex size depends on what the user is doing. At island-wide view (zoom 8–9), 3–5km hexes provide the right overview. At municipio level (zoom 11–12), 500m–1km shows neighborhood variation. At barrio level (zoom 13+), 100–250m resolves individual settlement patterns.

**PR implementation:**
```javascript
function hexRadius(zoom) {
  if (zoom <= 9)  return 3500;
  if (zoom <= 11) return 1200;
  if (zoom <= 12) return 600;
  return 250;
}
```
Values tuned empirically — zooming in should always reveal more structure.

**Why not sub-100m:** At 50m resolution, PR alone requires 280,000+ hexes. Pre-generating them crashes the browser. 100–250m at maximum zoom is the practical floor for single-page apps.

---

### Decision 3: The H3 Library — CDN vs. Inline Engine

**Original approach:** Load Uber's h3-js from CDN for `polygonToCells`, `cellToBoundary`, `cellToLatLng`.

**Why we switched to inline:** The tool must work offline (disaster response contexts, CSP-restricted environments). h3-js is ~300KB for three functions. The inline engine implements exactly the three functions needed using standard trigonometry.

**What the inline engine gives up:** True H3 cell IDs and index-based neighbor/parent/child traversal. Cells in the inline implementation are identified by center `[lat, lng]` pairs. For rendering and click interaction, this is sufficient. If H3 indexing is needed in a future version, the three functions can be swapped back to CDN h3-js.

---

### Decision 4: The Tessellation Bug — cosLat Correction

**The bug:** E-W hex compression at non-equatorial latitudes. At Puerto Rico (18°N), hexes appeared slightly squashed east-west.

**Root cause:**
```javascript
var lngStep = R * 1.5;  // WRONG — ignores longitude compression
```

At latitude φ, one degree of longitude spans `cos(φ)` as many meters as one degree of latitude. The correction:
```javascript
var cosLat = Math.cos(centerLat * Math.PI / 180);
var lngStep = R * 1.5 / cosLat;  // CORRECT
```

At 18°N, cosLat ≈ 0.951 — the uncorrected spacing was ~5% too narrow. Apply cosLat correction to ALL longitude-direction step calculations: both `polygonToCells` column step and `cellToBoundary` vertex longitude offsets.

---

### Decision 5: Canvas vs. SVG Renderer

**SVG hit the wall:** At 3,000 hexes in the viewport, SVG DOM has 3,000+ `<path>` elements. Pan events trigger O(n) DOM recalculations. The map lags 500ms+ on pan at fine zoom.

**Canvas solution:** `L.canvas({padding: 0.3})` renders all shapes onto one HTML5 canvas element. DOM has one element regardless of hex count. Performance is flat across hex count until canvas size limit.

**Hit testing manually:** Canvas doesn't support CSS hover. On `mousemove`, compute the nearest hex center within one hex radius and update tooltip manually — ~20 lines, negligible performance cost.

**Winner:** Canvas, unconditionally, for >500 simultaneous hexes.

```javascript
var renderer = L.canvas({ padding: 0.3 });
```

---

### Decision 6: SVI Scoring Formula — The "Everyone Looks Screwed" Problem

**First formula (blend):**
```javascript
score = physScore * (1 - frac) + socScore * frac;
```
Blend is subtractive. Social vulnerability can't exceed the physical ceiling. The toggle had almost no visual effect — colors shifted by one shade.

**Second formula (additive):**
```javascript
score = Math.min(1, physScore + socNorm * frac * 0.55);
```
Social vulnerability ADDS to the physical score. A community with moderate physical exposure and high social vulnerability now hits the red end of the scale. The toggle produces visible, dramatic shifts.

**The "everyone looks screwed" calibration:** Without the `0.55` multiplier, nearly every community hits the `Math.min(1, ...)` ceiling at moderate social weight — uniform dark red. Three calibration adjustments:
1. `* 0.55` cap: maximum social contribution is 0.55, preserving physical score variation
2. Normalize `socNorm` across the full community range (not just 0–1 raw)
3. Preserve at least one genuinely low-score community as a visual anchor

**What the toggle must show:** Physical-only view = what traditional hazard models predict. SVI-inclusive view = what actually happens to people. The visual shift between them IS the argument of the tool.

---

### Decision 7: Barrio/Tract Level vs. Municipal + Hex Noise

**Reality:** There is no 100m-resolution SVI dataset for Puerto Rico. The finest available data is US Census ACS / ATSDR SVI at census tract level (~900 tracts in PR).

**Approach used:** Each hex center is assigned to its containing census tract. The tract SVI score becomes the hex's base score. A small spatial noise term (±0.05 using Perlin noise on lat/lng) is added to create visual texture.

**Why noise is defensible:** The noise is small and spatially smooth. It creates visual texture without misrepresenting the data. The tool documentation is explicit that hexes within a tract carry that tract's SVI score.

**What to never do:** Apply municipal-level averages directly to all hexes in the municipio without noise. Solid-color blocks at island scale visually lie about intra-municipal heterogeneity. Even synthesized texture is better than false uniformity.

---

### Decision 8: Color Scale — From 4 Bins to 6-Stop Gradient

**Four discrete bins** produced clean maps but lost all within-bin variation.

**Continuous gradient with even stops** compressed mid-range differences — humans perceive color logarithmically.

**The 6-stop production scale:**
```javascript
var RISK_STOPS = [
  [0,    '#00E096'],  // bright teal-green
  [0.22, '#4ADE80'],  // mid green
  [0.42, '#FFD93D'],  // yellow
  [0.64, '#FF6B35'],  // orange
  [0.82, '#FF2D55'],  // hot pink-red
  [1.0,  '#B40032'],  // deep crimson
];
```

**Stop placement logic:** Stops are NOT evenly spaced. Most communities cluster in the 0.2–0.6 range. Evenly-spaced stops waste color resolution on the tails. The compressed upper-end stops mean the difference between "bad" (0.64) and "catastrophic" (1.0) is clearly visible as orange → pink → crimson.

**Why not diverging (blue → red):** A diverging scale implies a meaningful midpoint (like comparison to national average). SVI score is an absolute risk scale — green just means "lower risk," not "below average."

**Resilience/adaptive capacity scale (separate):**
```javascript
var RES_STOPS = [
  [0,    '#9CA3AF'],  // gray — no data
  [0.3,  '#D97706'],  // amber — low resilience
  [0.65, '#10B981'],  // green — moderate
  [1.0,  '#0891B2'],  // teal — high resilience
];
```
No red in the resilience scale — red means high risk, not low resilience. Users must not confuse the two visual modes.

---

### Decision 9: Hex Orientation — Flat-Top vs. Pointy-Top

**The complaint:** "The hexes don't actually nest together — they all sit horizontally."

**What was happening:** The inline H3 engine had a mismatch. `cellToBoundary` computed vertices at `a = Math.PI/3 * i` (first vertex due east = pointy-top shape). But `polygonToCells` used flat-top grid spacing (`rowStep = R * 1.5`). Wrong shape + wrong grid = hexes that don't tile.

**The fix — flat-top hexes (classic honeycomb):**

`cellToBoundary` — rotate vertices -30°:
```javascript
// BEFORE (pointy-top):
var a = Math.PI / 3 * i;
// AFTER (flat-top):
var a = Math.PI / 3 * i - Math.PI / 6;
```

`polygonToCells` — swap row and column steps:
```javascript
var S3 = Math.sqrt(3);
// BEFORE (mismatched):
var rowStep = R * 1.5;
var colStep = R * S3 / cosLat;
// AFTER (matched to flat-top vertices):
var rowStep = R * S3;
var colStep = R * 1.5 / cosLat;
```

**Why flat-top:** Rows are horizontal and staggered — the classic "honeycomb" pattern most people recognize from board games and GIS hex grids. Flat edges align with cardinal directions on a north-up map.

**Test:** At fine zoom (250m hexes), every hex should share full edges with all 6 neighbors. No gaps, no horizontal banding. If gaps appear only E-W or only N-S, the cosLat correction or step swap is still wrong.

---

### Decision 10: Dynamic Viewport Generation

**Why pre-building all hexes is impossible:** At 250m resolution over PR, ~46,000 hexes. At 100m: ~280,000. Each is a Leaflet polygon with 6 vertices, listeners, and DOM overhead. At 50,000 hexes, page init takes 30+ seconds. At 100,000, the browser crashes.

**The viewport solution:** On every `moveend`/`zoomend`, generate only hexes whose centers fall within current map bounds + buffer. Discard the previous viewport's hexes. The user only ever sees what's currently visible.

**Debounce required:**
```javascript
var hexRegen;
map.on('moveend zoomend', function() {
  clearTimeout(hexRegen);
  hexRegen = setTimeout(buildHexGrid, 180);
});
```

**Performance envelope:** <3,000 visible hexes = imperceptible. 3,000–5,000 = brief flicker on pan. >5,000 = increase hex radius to reduce count. Never trade smoothness for resolution — users stop using laggy tools.

---

### Decision 11: Coast Clipping — Why Both Layers Are Required

Ocean hexes destroy visual credibility. Users immediately distrust data floating in the Atlantic.

**Layer 1 (polygon test):** Filters hex centers. Eliminates hexes entirely in the ocean. But a hex center can be on land while the hex itself extends into the ocean — at 250m radius, a coastal hex can overhang 200m of ocean. Polygon test alone leaves visible color spikes in bays.

**Layer 2 (SVG clip):** Visually trims the canvas to the coastline shape. Handles hex overhang perfectly. But SVG clip coordinates are in screen pixels — the clip must recalculate on every pan and zoom. Missing `map.on('moveend zoomend', refreshCoastClip)` produces a clip that drifts out of alignment immediately.

**Both layers use the same `COUNTRY_POLY`.** Investing in a high-quality polygon (30+ points, GADM-sourced) pays off in both layers simultaneously.

**Canonical debugging sequence:**
1. Ocean hexes? → Check `COUNTRY_POLY` point count and coordinate order ([lat, lng] not [lng, lat])
2. Clip drifting on pan? → Add `map.on('moveend zoomend', refreshCoastClip)`
3. Island hexes disappearing? → Add island polygons as additional `<polygon>` inside `<clipPath>`
4. Entire map clipped? → `initCoastClip()` is firing before map ready; wrap in `map.whenReady()`

---

### PR-Specific Note: Cultural Record / Music Section

The PR tool includes a Cultural Record section with embedded music (`cr-songs`, `cr-song-lyric` CSS classes). This is based on thesis research specific to Puerto Rican musical culture as a preparedness narrative medium. It is a PR-specific feature — do **not** replicate it in Philippines, Mexico, or other builds. Each geography needs its own cultural narrative research before any equivalent section could be added responsibly.

---

### Summary: The Decision Hierarchy

When starting a new build, make these decisions in order:

1. **Representation** — Hexes, always, for vulnerability tools
2. **Resolution strategy** — Zoom-responsive, always
3. **Library approach** — Inline engine for offline/CSP; CDN h3-js if network guaranteed
4. **Renderer** — Canvas, always, beyond ~500 hexes
5. **Grid math** — Apply cosLat correction AND flat-top orientation from day one
6. **Coast clipping** — Budget time for a good polygon; build both layers before first demo
7. **Score formula** — Start with additive; tune the 0.55 cap against your data distribution
8. **Color scale** — 6-stop continuous; bias stops toward upper end; separate scale for resilience

Every shortcut in steps 3–6 produces a visible artifact that erodes trust in the underlying data. Fix the plumbing before tuning the colors.

