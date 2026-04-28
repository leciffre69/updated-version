"""
rebuild.py  —  Run this whenever you update:
  - graveyard_plots.json
  - plot_coords.json
  - img/sketch.png  (or any image)

Usage:  python rebuild.py
Output: start.html  (fully self-contained, no server needed)
"""
import json, re, pathlib, base64, mimetypes

ROOT = pathlib.Path(__file__).parent

plots_data  = json.loads((ROOT / 'graveyard_plots.json').read_text(encoding='utf-8'))
coords_data = json.loads((ROOT / 'plot_coords.json').read_text(encoding='utf-8'))

def data_uri(rel_path):
    p = ROOT / rel_path
    if not p.exists():
        print(f'  WARNING: missing {rel_path}')
        return rel_path
    mime, _ = mimetypes.guess_type(str(p))
    mime = mime or 'image/png'
    b64 = base64.b64encode(p.read_bytes()).decode()
    return f'data:{mime};base64,{b64}'

logo   = data_uri('img/logo.png')
img2   = data_uri('img/2.png')
img4   = data_uri('img/4.png')
img5   = data_uri('img/5.png')
sketch = data_uri('img/sketch.png')

plots_json  = json.dumps(plots_data,  ensure_ascii=False)
coords_json = json.dumps(coords_data, ensure_ascii=False)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" type="image/png" href="{logo}">
<title>Sardis Baptist Church Graveyard - Interactive Map</title>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html,body{{height:100%;overflow:hidden}}
body{{
  font-family:Georgia,'Times New Roman',serif;
  color:#2c2416;
  display:flex;flex-direction:column;
  height:100vh;overflow:hidden;
  background-image:linear-gradient(rgba(10,8,4,0.60),rgba(10,8,4,0.60)),url('{img4}');
  background-size:cover;background-position:center top;background-attachment:fixed;background-repeat:no-repeat;
}}
header{{
  background:rgba(10,6,2,0.86);backdrop-filter:blur(6px);color:#e8dfc8;
  padding:14px 28px;display:grid;grid-template-columns:1fr auto;align-items:center;
  gap:16px;flex-shrink:0;z-index:20;border-bottom:1px solid rgba(200,168,75,0.25);
}}
#site-title{{display:flex;align-items:center;gap:14px;}}
#site-title img{{width:48px;height:48px;object-fit:cover;border-radius:50%;border:2px solid rgba(200,168,75,0.6);flex-shrink:0;filter:brightness(0.85);}}
#site-title h1{{font-size:1.35rem;font-weight:normal;letter-spacing:.06em;line-height:1.2;color:#e8dfc8;}}
#site-title h1 span{{font-size:.78rem;opacity:.6;display:block;letter-spacing:.03em;margin-top:2px;}}
#search-wrap{{position:relative;display:flex;gap:0;width:340px;}}
#search-input{{flex:1;padding:9px 14px;border:1px solid rgba(200,168,75,0.5);border-right:none;border-radius:4px 0 0 4px;font-size:.9rem;font-family:inherit;background:rgba(255,248,238,0.12);color:#e8dfc8;outline:none;}}
#search-input::placeholder{{color:rgba(232,223,200,0.45)}}
#search-input:focus{{background:rgba(255,248,238,0.22);border-color:rgba(200,168,75,0.9);}}
#search-btn{{padding:9px 18px;background:#8b6914;color:#fff;border:1px solid #8b6914;border-radius:0 4px 4px 0;cursor:pointer;font-size:.88rem;font-family:inherit;white-space:nowrap;letter-spacing:.03em;}}
#search-btn:hover{{background:#a07c1a;border-color:#a07c1a;}}
#search-results{{position:absolute;top:calc(100% + 4px);left:0;right:0;background:#fff8ee;border:1px solid #c8a84b;border-radius:4px;max-height:260px;overflow-y:auto;z-index:300;display:none;box-shadow:0 6px 20px rgba(0,0,0,0.35);}}
#search-results.visible{{display:block}}
.result-item{{padding:8px 12px;cursor:pointer;border-bottom:1px solid #e8dfc8;font-size:.85rem;line-height:1.3;color:#2c2416;}}
.result-item:hover{{background:#f0e4c0}}
.result-item .pn{{font-weight:bold;color:#8b6914;margin-right:5px}}
.no-results{{padding:8px 12px;font-style:italic;color:#8b7050;font-size:.85rem}}
#toolbar{{background:rgba(18,12,4,0.82);backdrop-filter:blur(4px);display:flex;align-items:center;gap:8px;padding:6px 20px;flex-shrink:0;border-bottom:1px solid rgba(200,168,75,0.2);}}
.tb-btn{{padding:5px 13px;background:rgba(90,72,32,0.7);color:#e8dfc8;border:1px solid rgba(200,168,75,0.4);border-radius:3px;cursor:pointer;font-size:.78rem;font-family:inherit;white-space:nowrap;letter-spacing:.02em;transition:background .15s;}}
.tb-btn:hover{{background:rgba(122,96,48,0.9);}}
#zoom-label{{color:#c8a84b;font-size:.78rem;min-width:38px;text-align:center;font-variant-numeric:tabular-nums;}}
#coord-info{{color:rgba(180,160,120,0.7);font-size:.7rem;margin-left:auto;letter-spacing:.02em;}}
main{{display:flex;flex:1;overflow:hidden;min-height:0}}
#map-panel{{flex:1;overflow:hidden;background-image:linear-gradient(rgba(15,12,6,0.45),rgba(15,12,6,0.45)),url('{img4}');background-size:cover;background-position:center;position:relative;cursor:grab;user-select:none;}}
#map-panel.dragging{{cursor:grabbing}}
#map-wrap{{position:absolute;top:0;left:0;transform-origin:0 0;will-change:transform;}}
#map-wrap img{{display:block;user-select:none;-webkit-user-drag:none;pointer-events:none}}
.hit-dot{{position:absolute;width:22px;height:22px;border-radius:50%;background:rgba(224,92,42,0.85);border:2.5px solid #fff;transform:translate(-50%,-50%);pointer-events:none;box-shadow:0 0 0 3px rgba(224,92,42,.4);}}
.hit-dot.pulse{{animation:pulse 1s ease-out 1}}
@keyframes pulse{{0%{{box-shadow:0 0 0 0 rgba(224,92,42,.8)}}70%{{box-shadow:0 0 0 14px rgba(224,92,42,0)}}100%{{box-shadow:0 0 0 0 rgba(224,92,42,0)}}}}
#click-hint{{position:absolute;pointer-events:none;border:1.5px dashed rgba(200,168,75,.8);border-radius:50%;transform:translate(-50%,-50%);display:none;}}
#detail-panel{{width:380px;min-width:300px;background-image:linear-gradient(rgba(255,248,238,0.78),rgba(255,248,238,0.78)),url('{img2}');background-size:cover;background-position:center;backdrop-filter:blur(6px);border-left:2px solid rgba(200,168,75,0.6);display:flex;flex-direction:column;flex-shrink:0;overflow:visible;}}
#detail-header{{background-image:linear-gradient(rgba(10,6,2,0.72),rgba(10,6,2,0.72)),url('{img5}');background-size:cover;background-position:center 40%;color:#e8dfc8;padding:10px 14px;flex-shrink:0;border-bottom:1px solid rgba(200,168,75,0.4);}}
#dp-plot{{font-size:1.3rem;font-weight:bold;color:#c8a84b;line-height:1.1}}
#dp-status{{font-size:.78rem;opacity:.75;margin-top:2px}}
#detail-body{{padding:12px 14px;flex:1 1 0;overflow-y:auto;}}
.empty-msg{{color:#8b7050;font-style:italic;font-size:.88rem;margin-top:16px;text-align:center;line-height:1.6}}
.occupant-card{{border:1px solid #d8c890;border-radius:5px;padding:9px 11px;margin-bottom:10px;background:#fffdf5}}
.occ-name{{font-size:1rem;font-weight:bold;color:#2c2416;margin-bottom:3px}}
.occ-dates{{font-size:.8rem;color:#6a5030;margin-bottom:5px}}
.occ-epitaph{{font-size:.79rem;color:#4a3820;line-height:1.55;font-style:italic;border-top:1px solid #e8dfc8;padding-top:5px;margin-top:3px}}
#legend{{padding:9px 14px;border-top:1px solid rgba(200,168,75,0.4);flex-shrink:0;background-image:linear-gradient(rgba(255,253,245,0.78),rgba(255,253,245,0.78)),url('{img5}');background-size:cover;background-position:center bottom;}}
#legend h3{{font-size:.78rem;margin-bottom:5px;color:#2c2416}}
.leg-row{{display:flex;align-items:center;gap:5px;margin-bottom:3px;font-size:.75rem;color:#6a5030}}
.leg-sw{{width:13px;height:13px;border-radius:50%;border:2px solid #fff;box-shadow:0 0 0 1px #8b6914;flex-shrink:0}}
#no-coords-banner{{background:rgba(122,64,16,0.9);color:#ffe8c0;padding:8px 16px;font-size:.82rem;text-align:center;flex-shrink:0;display:none;backdrop-filter:blur(4px)}}
@media(max-width:640px){{main{{flex-direction:column}}#detail-panel{{width:100%;min-width:unset;border-left:none;border-top:2px solid #c8a84b;flex:0 0 45vh}}}}
</style>
</head>
<body>
<header>
  <div id="site-title">
    <img src="{logo}" alt="Graveyard logo">
    <h1>Sardis Baptist Church Graveyard<span>Lower Llangynidr</span></h1>
  </div>
  <div id="search-wrap">
    <input id="search-input" type="search" placeholder="Search name or plot number..." autocomplete="off" aria-label="Search">
    <button id="search-btn">Search</button>
    <div id="search-results" role="listbox"></div>
  </div>
</header>
<div id="no-coords-banner">No plot coordinates mapped yet.</div>
<div id="toolbar">
  <button class="tb-btn" id="zoom-in">+ Zoom in</button>
  <button class="tb-btn" id="zoom-out">- Zoom out</button>
  <button class="tb-btn" id="zoom-fit">Fit</button>
  <span id="zoom-label">100%</span>
  <span id="coord-info">Click+drag to pan  |  Click a plot number to select</span>
</div>
<main>
  <div id="map-panel" aria-label="Graveyard map">
    <div id="map-wrap">
      <img id="sketch" src="{sketch}" alt="Sardis Baptist Church graveyard layout" draggable="false">
      <div id="click-hint"></div>
    </div>
  </div>
  <div id="detail-panel" aria-live="polite">
    <div id="detail-header">
      <div id="dp-plot">-</div>
      <div id="dp-status">Click a plot or search above</div>
    </div>
    <div id="detail-body">
      <p class="empty-msg">Click+drag to pan the map.<br>Click any plot number to see occupant details.</p>
    </div>
    <div id="legend">
      <h3>How to use</h3>
      <div class="leg-row"><div class="leg-sw" style="background:#e05c2a"></div>Selected plot</div>
      <div class="leg-row" style="margin-top:6px;font-size:.72rem;color:#8b7050;line-height:1.5">Drag to pan &nbsp;|&nbsp; +/- to zoom<br>Ctrl+scroll to zoom &nbsp;|&nbsp; Fit to reset view</div>
    </div>
  </div>
</main>
<script>
'use strict';
const _PLOTS_DATA  = {plots_json};
const _COORDS_DATA = {coords_json};

let plotCoords  = {{}};
let plotRecords = {{}};
let scale=1, panX=0, panY=0;
let isDragging=false, dragStartX=0, dragStartY=0, panStartX=0, panStartY=0, dragMoved=false;
const DRAG_THRESHOLD=4;
let activeDot=null, activeId=null;
const CLICK_RADIUS=40;

async function init() {{
  for (const p of _PLOTS_DATA.plots) plotRecords[p.plot] = p.occupants || [];
  for (const [pid, v] of Object.entries(_COORDS_DATA)) {{
    const x = v.x !== undefined ? v.x : v.cx;
    const y = v.y !== undefined ? v.y : v.cy;
    if (x !== undefined && y !== undefined) plotCoords[pid] = {{ x, y }};
  }}
  setupPanZoom();
  setupSearch();
  const img = document.getElementById('sketch');
  if (img.complete && img.naturalWidth) {{ fitToView(); }}
  else {{ img.addEventListener('load', fitToView); }}
}}

function applyTransform() {{
  document.getElementById('map-wrap').style.transform = `translate(${{panX}}px,${{panY}}px) scale(${{scale}})`;
  document.getElementById('zoom-label').textContent = Math.round(scale*100)+'%';
}}

function fitToView() {{
  const panel=document.getElementById('map-panel'), img=document.getElementById('sketch');
  if (!img.naturalWidth) return;
  scale=Math.min(panel.clientWidth/img.naturalWidth, panel.clientHeight/img.naturalHeight)*0.97;
  panX=(panel.clientWidth-img.naturalWidth*scale)/2;
  panY=(panel.clientHeight-img.naturalHeight*scale)/2;
  applyTransform();
}}

function zoomBy(factor,cx,cy) {{
  const panel=document.getElementById('map-panel');
  if (cx===undefined) cx=panel.clientWidth/2;
  if (cy===undefined) cy=panel.clientHeight/2;
  const newScale=Math.min(Math.max(scale*factor,0.15),8);
  const ratio=newScale/scale;
  panX=cx-ratio*(cx-panX); panY=cy-ratio*(cy-panY); scale=newScale;
  applyTransform();
}}

function setupPanZoom() {{
  const panel=document.getElementById('map-panel');
  panel.addEventListener('mousedown',e=>{{
    if (e.button!==0) return;
    isDragging=true; dragMoved=false;
    dragStartX=e.clientX; dragStartY=e.clientY; panStartX=panX; panStartY=panY;
    panel.classList.add('dragging'); e.preventDefault();
  }});
  window.addEventListener('mousemove',e=>{{
    if (!isDragging) {{ onMapHover(e); return; }}
    const dx=e.clientX-dragStartX, dy=e.clientY-dragStartY;
    if (!dragMoved && Math.hypot(dx,dy)>DRAG_THRESHOLD) dragMoved=true;
    if (dragMoved) {{ panX=panStartX+dx; panY=panStartY+dy; applyTransform(); }}
  }});
  window.addEventListener('mouseup',e=>{{
    if (!isDragging) return;
    isDragging=false; panel.classList.remove('dragging');
    if (!dragMoved) onMapClick(e);
  }});
  let lastTouchX,lastTouchY,touchMoved=false,touchStartX,touchStartY;
  panel.addEventListener('touchstart',e=>{{
    if (e.touches.length===1) {{ touchMoved=false; touchStartX=lastTouchX=e.touches[0].clientX; touchStartY=lastTouchY=e.touches[0].clientY; }}
  }},{{passive:true}});
  panel.addEventListener('touchmove',e=>{{
    if (e.touches.length===1) {{
      const dx=e.touches[0].clientX-lastTouchX, dy=e.touches[0].clientY-lastTouchY;
      if (Math.hypot(e.touches[0].clientX-touchStartX,e.touches[0].clientY-touchStartY)>DRAG_THRESHOLD) touchMoved=true;
      panX+=dx; panY+=dy; lastTouchX=e.touches[0].clientX; lastTouchY=e.touches[0].clientY;
      applyTransform(); e.preventDefault();
    }}
  }},{{passive:false}});
  panel.addEventListener('touchend',e=>{{ if (!touchMoved&&e.changedTouches.length===1) onMapClick(e.changedTouches[0]); }});
  panel.addEventListener('wheel',e=>{{
    e.preventDefault();
    const r=panel.getBoundingClientRect();
    zoomBy(e.deltaY<0?1.1:0.9, e.clientX-r.left, e.clientY-r.top);
  }},{{passive:false}});
  document.getElementById('zoom-in').addEventListener('click',()=>zoomBy(1.25));
  document.getElementById('zoom-out').addEventListener('click',()=>zoomBy(0.8));
  document.getElementById('zoom-fit').addEventListener('click',fitToView);
}}

function toImageCoords(clientX,clientY) {{
  const panel=document.getElementById('map-panel'), pr=panel.getBoundingClientRect();
  return {{ ix:(clientX-pr.left-panX)/scale, iy:(clientY-pr.top-panY)/scale }};
}}

function onMapClick(e) {{
  const {{ix,iy}}=toImageCoords(e.clientX,e.clientY);
  document.getElementById('coord-info').textContent='Last click: x='+Math.round(ix)+'  y='+Math.round(iy);
  const match=findNearest(ix,iy);
  if (match) {{ selectPlot(match.id,match.x,match.y); }}
  else {{
    clearDot();
    document.getElementById('dp-plot').textContent='-';
    document.getElementById('dp-status').textContent='No plot selected';
    document.getElementById('detail-body').innerHTML='<p class="empty-msg">No plot found near that click.<br>Try clicking closer to a plot number.</p>';
  }}
}}

function onMapHover(e) {{
  const panel=document.getElementById('map-panel'), pr=panel.getBoundingClientRect();
  if (e.clientX<pr.left||e.clientX>pr.right||e.clientY<pr.top||e.clientY>pr.bottom) return;
  const {{ix,iy}}=toImageCoords(e.clientX,e.clientY);
  const match=findNearest(ix,iy), hint=document.getElementById('click-hint');
  if (match&&match.dist<CLICK_RADIUS) {{
    hint.style.display='block'; hint.style.left=match.x+'px'; hint.style.top=match.y+'px';
    hint.style.width=(CLICK_RADIUS*2)+'px'; hint.style.height=(CLICK_RADIUS*2)+'px';
    panel.style.cursor='pointer';
  }} else {{
    hint.style.display='none'; panel.style.cursor=isDragging?'grabbing':'grab';
  }}
}}

function findNearest(ix,iy) {{
  let best=null, bestDist=Infinity;
  for (const [pid,c] of Object.entries(plotCoords)) {{
    const d=Math.hypot(c.x-ix,c.y-iy);
    if (d<bestDist) {{ bestDist=d; best={{id:pid,x:c.x,y:c.y,dist:d}}; }}
  }}
  if (!best||best.dist>CLICK_RADIUS) return null;
  return best;
}}

function selectPlot(plotId,dotX,dotY) {{
  clearDot(); activeId=plotId;
  if (dotX!==undefined&&dotY!==undefined) {{
    const wrap=document.getElementById('map-wrap'), dot=document.createElement('div');
    dot.className='hit-dot pulse'; dot.id='active-dot';
    dot.style.left=dotX+'px'; dot.style.top=dotY+'px';
    wrap.appendChild(dot); activeDot=dot;
    const panel=document.getElementById('map-panel');
    panX=panel.clientWidth/2-dotX*scale; panY=panel.clientHeight/2-dotY*scale;
    applyTransform();
  }}
  showDetail(plotId);
}}

function clearDot() {{ if (activeDot) {{ activeDot.remove(); activeDot=null; }} }}

function showDetail(plotId) {{
  document.getElementById('dp-plot').textContent='Plot '+plotId;
  const occupants=plotRecords[plotId]||[];
  let status='No record';
  if (occupants.length) {{
    const s=occupants[0].surname||'', ep=(occupants[0].epitaph||'').toLowerCase();
    if (s.toLowerCase().includes('[not used]')) status='Not used';
    else if (ep.includes('eroded')||s.toLowerCase().includes('eroded')) status='Eroded / illegible';
    else if (ep.includes('vacant')) status='Vacant';
    else if (s) status=occupants.length+' occupant'+(occupants.length>1?'s':'');
  }}
  document.getElementById('dp-status').textContent=status;
  const body=document.getElementById('detail-body');
  if (!occupants.length) {{ body.innerHTML='<p class="empty-msg">No data recorded for this plot.</p>'; return; }}
  const s0=occupants[0].surname||'';
  if (s0.toLowerCase().includes('[not used]')||s0.toLowerCase().includes('[vacant]')) {{
    body.innerHTML='<p class="empty-msg">'+esc(occupants[0].epitaph||'Not used.')+'</p>'; return;
  }}
  let html='';
  for (const occ of occupants) {{
    if (!occ.surname&&!occ.forename&&!occ.epitaph) continue;
    const name=[occ.forename,occ.surname].filter(Boolean).join(' ')||'(name unknown)';
    let dates='';
    if (occ.dob||occ.dod) {{
      dates='Born: '+(occ.dob||'?')+' &nbsp;&middot;&nbsp; Died: '+(occ.dod||'?');
      if (occ.age) dates+=' &nbsp;&middot;&nbsp; Age: '+esc(String(occ.age));
    }}
    html+='<div class="occupant-card"><div class="occ-name">'+esc(name)+'</div>'+(dates?'<div class="occ-dates">'+dates+'</div>':'')+(occ.epitaph?'<div class="occ-epitaph">'+esc(occ.epitaph)+'</div>':'')+'</div>';
  }}
  body.innerHTML=html||'<p class="empty-msg">No inscription recorded.</p>';
}}

function esc(s) {{ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }}

function setupSearch() {{
  const input=document.getElementById('search-input'), btn=document.getElementById('search-btn'), results=document.getElementById('search-results');
  function doSearch() {{
    const q=input.value.trim().toLowerCase(); results.innerHTML='';
    if (!q) {{ results.classList.remove('visible'); return; }}
    const matches=[], seen=new Set();
    for (const [pid,occs] of Object.entries(plotRecords)) {{
      if (pid.toLowerCase().startsWith(q)&&!seen.has(pid)) {{
        const label=occs[0]?[occs[0].forename,occs[0].surname].filter(Boolean).join(' '):'';
        matches.push({{pid,label:label||'Plot '+pid}}); seen.add(pid); continue;
      }}
      for (const occ of occs) {{
        const full=(occ.forename+' '+occ.surname).toLowerCase();
        if (full.includes(q)||occ.surname.toLowerCase().includes(q)||occ.forename.toLowerCase().includes(q)) {{
          if (!seen.has(pid)) {{ matches.push({{pid,label:[occ.forename,occ.surname].filter(Boolean).join(' ')}}); seen.add(pid); }} break;
        }}
      }}
    }}
    if (!matches.length) {{ results.innerHTML='<div class="no-results">No results found.</div>'; results.classList.add('visible'); return; }}
    if (matches.length===1) {{ results.classList.remove('visible'); jumpToPlot(matches[0].pid); return; }}
    const frag=document.createDocumentFragment();
    for (const m of matches.slice(0,40)) {{
      const div=document.createElement('div'); div.className='result-item';
      div.innerHTML='<span class="pn">#'+esc(m.pid)+'</span>'+esc(m.label);
      div.addEventListener('click',()=>{{ results.classList.remove('visible'); input.value=''; jumpToPlot(m.pid); }});
      frag.appendChild(div);
    }}
    if (matches.length>40) {{ const more=document.createElement('div'); more.className='no-results'; more.textContent='...and '+(matches.length-40)+' more - refine your search.'; frag.appendChild(more); }}
    results.appendChild(frag); results.classList.add('visible');
  }}
  input.addEventListener('input',doSearch);
  btn.addEventListener('click',doSearch);
  input.addEventListener('keydown',e=>{{ if (e.key==='Enter') doSearch(); }});
  document.addEventListener('click',e=>{{ if (!document.getElementById('search-wrap').contains(e.target)) results.classList.remove('visible'); }});
}}

function jumpToPlot(pid) {{
  const c=plotCoords[pid];
  if (c) {{ selectPlot(pid,c.x,c.y); }}
  else {{ selectPlot(pid); document.getElementById('dp-status').textContent+=' (position not mapped)'; }}
}}

window.addEventListener('DOMContentLoaded', init);
</script>
</body>
</html>"""

out = ROOT / 'start.html'
out.write_text(html, encoding='utf-8')
print(f'Done -> start.html  ({out.stat().st_size // 1024} KB)')
