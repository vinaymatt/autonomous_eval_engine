import streamlit as st
import requests
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
from streamlit_agraph import agraph, Node, Edge, Config
import os
import base64

try:
    api_base_url = st.secrets["API_BASE_URL"]
except (FileNotFoundError, KeyError):
    api_base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
api_base_url = api_base_url.rstrip("/")


def api_url(path: str) -> str:
    return f"{api_base_url}{path}"

# Helper function to display local images with a fixed size
def get_image_as_base64(path):
    try:
        if os.path.exists(path):
            with open(path, "rb") as f:
                data = f.read()
            return f"data:image/jpeg;base64,{base64.b64encode(data).decode()}"
    except Exception:
        return None
    return None


st.set_page_config(
    page_title="AEEVE — Autonomous Enterprise Evaluation Engine",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""<style>
    .block-container { padding-top: 1rem; }
    div[data-testid="stMetric"] {
        background: #f0f2f6;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 12px 16px;
    }
    div[data-testid="stMetric"] label {
        color: #374151 !important;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #111827 !important;
    }
    div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
        color: #4b5563 !important;
    }
    div[data-testid="stExpander"] {
        border: 1px solid #e5e7eb;
        border-radius: 8px;
    }
    .compliance-critical {
        background: #fef2f2;
        border-left: 4px solid #ef4444;
        padding: 12px 16px;
        border-radius: 4px;
        margin-bottom: 8px;
        color: #1f2937;
    }
    .compliance-warning {
        background: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 12px 16px;
        border-radius: 4px;
        margin-bottom: 8px;
        color: #1f2937;
    }
    .compliance-ok {
        background: #f0fdf4;
        border-left: 4px solid #22c55e;
        padding: 12px 16px;
        border-radius: 4px;
        margin-bottom: 8px;
        color: #1f2937;
    }
    .compliance-critical strong, .compliance-warning strong, .compliance-ok strong {
        color: #111827;
    }
    .compliance-critical em, .compliance-warning em, .compliance-ok em {
        color: #3b82f6;
    }
    .team-img {
        width: 150px;
        height: 150px;
        object-fit: cover;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .goal-img {
        width: 100%;
        height: 500px;
        object-fit: cover;
        border-radius: 15px;
    }
    .large-font {
        font-size: 22px !important;
        line-height: 1.6 !important;
    }
    .header-font {
        font-size: 32px !important;
        font-weight: bold !important;
    }
</style>""", unsafe_allow_html=True)


def render_factory_3d(machines_data, conveyors_data):
    """Renders an interactive 3D factory floor using Three.js with orbit controls."""
    machines_json = json.dumps(machines_data)
    conveyors_json = json.dumps(conveyors_data)
    html = """<!DOCTYPE html>
<html><head><style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#111820;overflow:hidden;font-family:'Segoe UI',sans-serif}
#c{width:100%;height:100vh}
#lg{position:absolute;top:10px;right:10px;background:rgba(10,14,24,0.88);
border:1px solid rgba(255,255,255,0.1);border-radius:8px;padding:10px 14px;
color:#bbb;font-size:11px;backdrop-filter:blur(6px)}
#lg h4{color:#eee;margin-bottom:6px;font-size:12px;font-weight:600}
.li{display:flex;align-items:center;margin:3px 0}
.ld{width:8px;height:8px;border-radius:50%;margin-right:6px}
#tp{position:absolute;display:none;pointer-events:none;
background:rgba(10,14,24,0.92);border:1px solid rgba(255,255,255,0.12);
border-radius:6px;padding:8px 12px;color:#fff;font-size:11px;
backdrop-filter:blur(4px);z-index:10;line-height:1.6;max-width:320px}
#lo{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
color:#667;font-size:13px;letter-spacing:1px}
</style></head><body>
<div id='c'></div>
<div id='lg'>
<h4>Machine Status</h4>
<div class='li'><div class='ld' style='background:#00cc66;box-shadow:0 0 5px #00cc66'></div>Active</div>
<div class='li'><div class='ld' style='background:#ff3333;box-shadow:0 0 5px #ff3333'></div>Downtime</div>
<div class='li'><div class='ld' style='background:#ffaa00;box-shadow:0 0 5px #ffaa00'></div>Maintenance</div>
</div>
<div id='tp'></div>
<div id='lo'>LOADING 3D FACTORY...</div>
<script type='importmap'>
{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js",
"three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}
</script>
<script type='module'>
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';

const MD = %%MACHINES%%;
const CD = %%CONVEYORS%%;
const SC = {Active:0x00cc66, Downtime:0xff3333, Maintenance:0xffaa00};
const SCS = {Active:'#00cc66', Downtime:'#ff3333', Maintenance:'#ffaa00'};
const SHEIGHT = {Milling:4, Turning:2.5, Cutting:2, Inspection:3.5, Assembly:1.5};

const ct = document.getElementById('c');
const W = ct.clientWidth, H = ct.clientHeight || 700;
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x111820);
scene.fog = new THREE.FogExp2(0x111820, 0.006);

const cam = new THREE.PerspectiveCamera(50, W/H, 0.1, 500);
cam.position.set(18, 28, 44);
const ren = new THREE.WebGLRenderer({antialias:true});
ren.setSize(W, H);
ren.setPixelRatio(Math.min(devicePixelRatio, 2));
ren.shadowMap.enabled = true;
ren.shadowMap.type = THREE.PCFSoftShadowMap;
ren.toneMapping = THREE.ACESFilmicToneMapping;
ren.toneMappingExposure = 1.2;
ct.appendChild(ren.domElement);

const ctrl = new OrbitControls(cam, ren.domElement);
ctrl.target.set(18, 0, 16);
ctrl.enableDamping = true;
ctrl.dampingFactor = 0.05;
ctrl.maxPolarAngle = Math.PI / 2.1;
ctrl.minDistance = 10;
ctrl.maxDistance = 70;
ctrl.update();

scene.add(new THREE.AmbientLight(0x404060, 0.5));
scene.add(new THREE.HemisphereLight(0x8888cc, 0x443322, 0.4));
const sun = new THREE.DirectionalLight(0xffeedd, 1.0);
sun.position.set(30, 35, 25);
sun.castShadow = true;
Object.assign(sun.shadow.camera, {left:-30,right:30,top:30,bottom:-30,near:1,far:100});
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.bias = -0.001;
scene.add(sun);

const fc = document.createElement('canvas');
fc.width = fc.height = 512;
const fx = fc.getContext('2d');
fx.fillStyle = '#4a4f54';
fx.fillRect(0, 0, 512, 512);
const fd = fx.getImageData(0, 0, 512, 512);
for (let i = 0; i < fd.data.length; i += 4) {
  const n = (Math.random() - 0.5) * 15;
  fd.data[i] += n; fd.data[i+1] += n; fd.data[i+2] += n;
}
fx.putImageData(fd, 0, 0);
fx.strokeStyle = 'rgba(255,255,255,0.05)';
fx.lineWidth = 1;
for (let i = 0; i <= 512; i += 32) {
  fx.beginPath(); fx.moveTo(i,0); fx.lineTo(i,512); fx.stroke();
  fx.beginPath(); fx.moveTo(0,i); fx.lineTo(512,i); fx.stroke();
}
const floorTex = new THREE.CanvasTexture(fc);
floorTex.wrapS = floorTex.wrapT = THREE.RepeatWrapping;
floorTex.repeat.set(3, 2.5);
const floor = new THREE.Mesh(
  new THREE.PlaneGeometry(54, 44),
  new THREE.MeshStandardMaterial({map:floorTex, roughness:0.85, metalness:0.1})
);
floor.rotation.x = -Math.PI / 2;
floor.position.set(18, -0.01, 16);
floor.receiveShadow = true;
scene.add(floor);

function makeLane(x1, z1, x2, z2) {
  const dx = x2-x1, dz = z2-z1, len = Math.sqrt(dx*dx + dz*dz);
  const m = new THREE.Mesh(
    new THREE.PlaneGeometry(0.12, len),
    new THREE.MeshBasicMaterial({color:0xccaa00, transparent:true, opacity:0.45})
  );
  m.rotation.x = -Math.PI/2;
  m.rotation.z = -Math.atan2(dx, dz);
  m.position.set((x1+x2)/2, 0.005, (z1+z2)/2);
  scene.add(m);
}
makeLane(1,20,35,20);
makeLane(20,1,20,33);

[[-3,-1],[-3,33],[39,-1],[39,33],[18,-1],[18,33]].forEach(p => {
  const c = new THREE.Mesh(
    new THREE.CylinderGeometry(0.25,0.25,7,8),
    new THREE.MeshStandardMaterial({color:0x556666, metalness:0.6, roughness:0.3})
  );
  c.position.set(p[0], 3.5, p[1]);
  c.castShadow = true;
  scene.add(c);
});

for (let x = 6; x <= 30; x += 8) {
  for (let z = 6; z <= 28; z += 8) {
    const fix = new THREE.Mesh(
      new THREE.BoxGeometry(2.5, 0.1, 0.3),
      new THREE.MeshStandardMaterial({color:0x777777, metalness:0.7})
    );
    fix.position.set(x, 6.9, z);
    scene.add(fix);
    const glow = new THREE.Mesh(
      new THREE.PlaneGeometry(2, 0.2),
      new THREE.MeshBasicMaterial({color:0xffffee, transparent:true, opacity:0.6})
    );
    glow.rotation.x = Math.PI / 2;
    glow.position.set(x, 6.8, z);
    scene.add(glow);
    const pl = new THREE.PointLight(0xfff5e0, 0.2, 18);
    pl.position.set(x, 6.5, z);
    scene.add(pl);
  }
}

[4, 16, 28].forEach(z => {
  const b = new THREE.Mesh(
    new THREE.BoxGeometry(46, 0.3, 0.15),
    new THREE.MeshStandardMaterial({color:0x555555, metalness:0.6})
  );
  b.position.set(18, 7.1, z);
  scene.add(b);
});

const MAT = {
  body:    new THREE.MeshStandardMaterial({color:0x6b7d8e, metalness:0.5, roughness:0.4}),
  dark:    new THREE.MeshStandardMaterial({color:0x445566, metalness:0.6, roughness:0.3}),
  chrome:  new THREE.MeshStandardMaterial({color:0x99aabc, metalness:0.8, roughness:0.15}),
  bench:   new THREE.MeshStandardMaterial({color:0x8B7355, metalness:0.1, roughness:0.7}),
  granite: new THREE.MeshStandardMaterial({color:0x222222, metalness:0.2, roughness:0.05}),
};

const anims = [];
const machineGroups = [];

function addBox(grp, size, pos, mat, castSh) {
  const m = new THREE.Mesh(new THREE.BoxGeometry(...size), mat.clone());
  m.position.set(...pos);
  if (castSh !== false) { m.castShadow = true; m.receiveShadow = true; }
  grp.add(m);
  return m;
}
function addCyl(grp, args, pos, mat) {
  const m = new THREE.Mesh(new THREE.CylinderGeometry(...args), mat.clone());
  m.position.set(...pos);
  grp.add(m);
  return m;
}
function roundRect(ctx, x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x+r, y);
  ctx.lineTo(x+w-r, y); ctx.quadraticCurveTo(x+w, y, x+w, y+r);
  ctx.lineTo(x+w, y+h-r); ctx.quadraticCurveTo(x+w, y+h, x+w-r, y+h);
  ctx.lineTo(x+r, y+h); ctx.quadraticCurveTo(x, y+h, x, y+h-r);
  ctx.lineTo(x, y+r); ctx.quadraticCurveTo(x, y, x+r, y);
  ctx.closePath();
}

function buildMachine(d) {
  const g = new THREE.Group();
  switch (d.type) {
    case 'Milling': {
      addBox(g, [2.5,1.2,2], [0,0.6,0], MAT.body);
      addBox(g, [0.8,2.5,1.5], [-0.7,2.45,0], MAT.dark);
      addBox(g, [1.8,0.6,0.8], [0.2,3.2,0], MAT.body);
      const sp = addCyl(g, [0.12,0.18,0.7,8], [0.2,2.5,0], MAT.chrome);
      if (d.status === 'Active') anims.push({m:sp, t:'ry', s:0.12});
      addBox(g, [0.3,0.8,0.05], [1.3,1.2,0.8], MAT.dark);
      break;
    }
    case 'Turning': {
      addBox(g, [3.5,0.6,1.5], [0,0.3,0], MAT.dark);
      addBox(g, [1,1.8,1.5], [-1.2,1.2,0], MAT.body);
      const ch = addCyl(g, [0.45,0.45,0.15,6], [-0.6,1.2,0], MAT.chrome);
      ch.rotation.z = Math.PI / 2;
      if (d.status === 'Active') anims.push({m:ch, t:'rx', s:0.1});
      addBox(g, [0.5,1,1], [1.5,0.9,0], MAT.body);
      break;
    }
    case 'Cutting': {
      addBox(g, [2.8,1.4,2.2], [0,0.7,0], MAT.body);
      const win = new THREE.Mesh(
        new THREE.PlaneGeometry(2.4, 0.8),
        new THREE.MeshStandardMaterial({color:0x88ccff, transparent:true, opacity:0.25, metalness:0.1, roughness:0.05})
      );
      win.position.set(0, 1.05, 1.11);
      g.add(win);
      addBox(g, [2.2,0.08,0.08], [0,1.5,0], MAT.chrome);
      const lh = addBox(g, [0.2,0.25,0.2], [0,1.3,0],
        new THREE.MeshStandardMaterial({color:0xff4444, emissive:0xff2222, emissiveIntensity:0.4}), false);
      if (d.status === 'Active') anims.push({m:lh, t:'ox', s:0.02, r:0.9, ix:0});
      break;
    }
    case 'Inspection': {
      addBox(g, [3,0.35,2], [0,0.5,0], MAT.granite);
      addCyl(g, [0.06,0.06,2.5,6], [-1.2,2,0], MAT.chrome);
      addCyl(g, [0.06,0.06,2.5,6], [1.2,2,0], MAT.chrome);
      addBox(g, [2.4,0.12,0.12], [0,3.15,0], MAT.chrome);
      const pr = addCyl(g, [0.03,0.03,1.2,6], [0,2.3,0], MAT.chrome);
      if (d.status === 'Active') anims.push({m:pr, t:'oz', s:0.01, r:0.4, iz:0});
      const tip = new THREE.Mesh(
        new THREE.SphereGeometry(0.06, 8, 8),
        new THREE.MeshStandardMaterial({color:0xff0000})
      );
      tip.position.set(0, 1.7, 0);
      g.add(tip);
      break;
    }
    default: {
      addBox(g, [3,0.85,1.5], [0,0.425,0], MAT.bench);
      [[-1.3,0.425,-0.6],[-1.3,0.425,0.6],[1.3,0.425,-0.6],[1.3,0.425,0.6]].forEach(
        p => addBox(g, [0.08,0.85,0.08], p, MAT.dark)
      );
      [0x3366cc, 0xcc3333, 0x33cc33].forEach((col, i) => {
        const part = new THREE.Mesh(
          new THREE.BoxGeometry(0.25, 0.15, 0.25),
          new THREE.MeshStandardMaterial({color:col})
        );
        part.position.set(-0.7 + i * 0.7, 1, 0);
        g.add(part);
      });
      break;
    }
  }

  const sh = SHEIGHT[d.type] || 3;
  const sc = SC[d.status] || SC.Active;
  addCyl(g, [0.02,0.02,0.7,6], [1.4,sh-0.5,-0.9], MAT.dark);
  const bulb = new THREE.Mesh(
    new THREE.SphereGeometry(0.1, 8, 8),
    new THREE.MeshBasicMaterial({color:sc, transparent:true})
  );
  bulb.position.set(1.4, sh+0.1, -0.9);
  g.add(bulb);
  const ptLight = new THREE.PointLight(sc, 0.4, 5);
  ptLight.position.copy(bulb.position);
  g.add(ptLight);

  const ring = new THREE.Mesh(
    new THREE.RingGeometry(1.8, 2, 32),
    new THREE.MeshBasicMaterial({color:sc, transparent:true, opacity:0.2, side:THREE.DoubleSide})
  );
  ring.rotation.x = -Math.PI / 2;
  ring.position.y = 0.01;
  g.add(ring);

  if (d.status === 'Downtime') {
    anims.push({m:bulb, t:'pulse', s:2.5});
    anims.push({m:ring, t:'po', s:2.5, mt:ring.material, bo:0.2});
  }

  g.position.set(d.x, 0, d.y);
  g.userData = d;
  machineGroups.push(g);
  scene.add(g);

  const lc = document.createElement('canvas');
  lc.width = 512; lc.height = 100;
  const lx = lc.getContext('2d');
  lx.fillStyle = 'rgba(8,12,24,0.8)';
  roundRect(lx, 2, 2, 508, 96, 10); lx.fill();
  lx.strokeStyle = 'rgba(255,255,255,0.1)';
  lx.lineWidth = 1.5;
  roundRect(lx, 2, 2, 508, 96, 10); lx.stroke();
  lx.fillStyle = '#fff';
  lx.font = 'bold 26px sans-serif';
  lx.textAlign = 'center';
  lx.fillText(d.id.replace(/_/g, ' '), 256, 38);
  const scolor = SCS[d.status] || '#888';
  lx.fillStyle = scolor;
  lx.font = '20px sans-serif';
  lx.fillText(d.status + ' \\u00b7 ' + Math.round(d.efficiency * 100) + '%', 256, 72);
  lx.strokeStyle = scolor; lx.lineWidth = 1.5;
  lx.beginPath(); lx.moveTo(80, 48); lx.lineTo(432, 48); lx.stroke();
  const labelTex = new THREE.CanvasTexture(lc);
  const labelSprite = new THREE.Sprite(
    new THREE.SpriteMaterial({map:labelTex, transparent:true, depthTest:false})
  );
  labelSprite.position.set(d.x, sh + 2, d.y);
  labelSprite.scale.set(5, 1, 1);
  scene.add(labelSprite);
}
MD.forEach(buildMachine);

function zoneLabel(txt, x, z) {
  const c = document.createElement('canvas');
  c.width = 512; c.height = 128;
  const cx = c.getContext('2d');
  cx.fillStyle = 'rgba(255,255,255,0.06)';
  cx.font = 'bold 56px sans-serif';
  cx.textAlign = 'center';
  cx.textBaseline = 'middle';
  cx.fillText(txt, 256, 64);
  const t = new THREE.CanvasTexture(c);
  const m = new THREE.Mesh(
    new THREE.PlaneGeometry(8, 2),
    new THREE.MeshBasicMaterial({map:t, transparent:true})
  );
  m.rotation.x = -Math.PI / 2;
  m.position.set(x, 0.015, z);
  scene.add(m);
}
zoneLabel('CNC MILLING', 9, 3);
zoneLabel('CNC TURNING', 27, 3);
zoneLabel('LASER / PRESS', 9, 28);
zoneLabel('INSPECTION', 30, 28);
zoneLabel('ASSEMBLY', 18, 19);

CD.forEach(cv => {
  const [x1, z1] = cv.from, [x2, z2] = cv.to;
  const dx = x2-x1, dz = z2-z1;
  const len = Math.sqrt(dx*dx + dz*dz);
  const ang = Math.atan2(dx, dz);

  const belt = new THREE.Mesh(
    new THREE.BoxGeometry(0.5, 0.04, len),
    new THREE.MeshStandardMaterial({color:0x333333, metalness:0.4, roughness:0.6})
  );
  belt.position.set((x1+x2)/2, 0.42, (z1+z2)/2);
  belt.rotation.y = ang;
  belt.receiveShadow = true;
  scene.add(belt);

  [-0.3, 0.3].forEach(off => {
    const rail = new THREE.Mesh(
      new THREE.BoxGeometry(0.04, 0.15, len),
      new THREE.MeshStandardMaterial({color:0x555555, metalness:0.6})
    );
    rail.position.set(
      (x1+x2)/2 + Math.cos(ang)*off, 0.5,
      (z1+z2)/2 - Math.sin(ang)*off
    );
    rail.rotation.y = ang;
    scene.add(rail);
  });

  const nSupports = Math.max(2, Math.floor(len / 3));
  for (let i = 0; i <= nSupports; i++) {
    const t = i / nSupports;
    const sup = new THREE.Mesh(
      new THREE.BoxGeometry(0.06, 0.42, 0.06),
      new THREE.MeshStandardMaterial({color:0x555555, metalness:0.5})
    );
    sup.position.set(x1 + dx*t, 0.21, z1 + dz*t);
    scene.add(sup);
  }

  const nearDowntime = MD.some(m => m.status === 'Downtime' &&
    (Math.abs(m.x-x1)+Math.abs(m.y-z1) < 4 || Math.abs(m.x-x2)+Math.abs(m.y-z2) < 4));

  if (!nearDowntime) {
    const nItems = Math.max(2, Math.floor(len / 4));
    for (let i = 0; i < nItems; i++) {
      const item = new THREE.Mesh(
        new THREE.BoxGeometry(0.25, 0.15, 0.25),
        new THREE.MeshStandardMaterial({color:0xddaa44})
      );
      item.castShadow = true;
      scene.add(item);
      anims.push({m:item, t:'cv', from:cv.from, to:cv.to, p:i/nItems, s:0.003});
    }
  }
});

const ray = new THREE.Raycaster();
const mouse = new THREE.Vector2();
const tooltipEl = document.getElementById('tp');

document.addEventListener('mousemove', e => {
  const rect = ren.domElement.getBoundingClientRect();
  mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
  mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
  ray.setFromCamera(mouse, cam);

  let hit = null;
  for (const grp of machineGroups) {
    const meshes = [];
    grp.traverse(ch => { if (ch.isMesh) meshes.push(ch); });
    if (ray.intersectObjects(meshes).length) { hit = grp.userData; break; }
  }
  if (hit) {
    tooltipEl.style.display = 'block';
    tooltipEl.style.left = (e.clientX + 12) + 'px';
    tooltipEl.style.top = (e.clientY - 10) + 'px';
    const sc = SCS[hit.status] || '#888';
    tooltipEl.innerHTML =
      '<b>' + hit.id.replace(/_/g, ' ') + '</b><br>' +
      (hit.detail ? '<span style="color:#aaa">' + hit.detail + '</span><br>' : '') +
      'Status: <span style="color:' + sc + '">' + hit.status + '</span><br>' +
      'Efficiency: ' + Math.round(hit.efficiency * 100) + '%';
  } else {
    tooltipEl.style.display = 'none';
  }
});

const clock = new THREE.Clock();
function animate() {
  requestAnimationFrame(animate);
  const t = clock.getElapsedTime();

  anims.forEach(a => {
    switch (a.t) {
      case 'ry': a.m.rotation.y += a.s; break;
      case 'rx': a.m.rotation.x += a.s; break;
      case 'ox': a.m.position.x = a.ix + Math.sin(t * 60 * a.s) * a.r; break;
      case 'oz': a.m.position.z = (a.iz || 0) + Math.sin(t * 60 * a.s) * a.r; break;
      case 'pulse': {
        const v = 0.5 + 0.5 * Math.sin(t * a.s * Math.PI);
        a.m.scale.setScalar(0.8 + v * 0.5);
        break;
      }
      case 'po': a.mt.opacity = a.bo * (0.3 + 0.7 * Math.abs(Math.sin(t * a.s))); break;
      case 'cv': {
        a.p += a.s; if (a.p > 1) a.p = 0;
        const cdx = a.to[0]-a.from[0], cdz = a.to[1]-a.from[1];
        a.m.position.set(a.from[0]+cdx*a.p, 0.55, a.from[1]+cdz*a.p);
        break;
      }
    }
  });

  ctrl.update();
  ren.render(scene, cam);
}

window.addEventListener('resize', () => {
  const w = ct.clientWidth, h = ct.clientHeight;
  cam.aspect = w / h;
  cam.updateProjectionMatrix();
  ren.setSize(w, h);
});

document.getElementById('lo').remove();
animate();
</script></body></html>"""
    html = html.replace('%%MACHINES%%', machines_json)
    html = html.replace('%%CONVEYORS%%', conveyors_json)
    components.html(html, height=750)


# ════════════════════════════════════════════════════════════════════════════
#  HEADER
# ════════════════════════════════════════════════════════════════════════════
st.title("🛡️ Autonomous Enterprise Evaluation & Visualization Engine")
st.caption("Keystone Future Factories Initiative (KFFI) — Preventing cascading economic failures from manufacturing succession gaps")
st.markdown("---")

# ── Sidebar ─────────────────────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/ios-filled/50/ffffff/factory.png", width=40)
st.sidebar.header("AEEVE Navigation")
layer = st.sidebar.radio(
    "Select Module",
    [   
        "Overview & Mission",
        "Company Profile",
        "1. Digital Twin Layer",
        "2. Market Dynamics & Resilience",
        "3. Legal & Compliance Framework",
    ],
)

# ════════════════════════════════════════════════════════════════════════════
#  Welcome & Overview
# ════════════════════════════════════════════════════════════════════════════
if layer == "Overview & Mission":
  
    # Goal Section
    st.markdown('<p class="header-font">🎯 Our Mission</p>', unsafe_allow_html=True)
    col_goal_text, col_goal_img = st.columns([1, 1.2], gap="large", vertical_alignment="center")
    with col_goal_text:
        st.markdown("""
            <p class="large-font">
            Our goal is to revolutionize the evaluation and digitization of Small and Medium Manufacturing (SMM) enterprises. 
            By leveraging advanced AI, Graph Neural Networks, and Digital Twin technology, we transform opaque industrial 
            assets into transparent, data-driven insights. Our platform enables seamless asset transfer, 
            valuation accuracy, and operational resilience for the next generation of manufacturing.
            </p>
        """, unsafe_allow_html=True)
    with col_goal_img:
        # Use local image if available, else placeholder
        goal_img_path = "assets/images/front.jpg"
        img_b64 = get_image_as_base64(goal_img_path)
        if img_b64:
            st.markdown(f'<img src="{img_b64}" class="goal-img" alt="Industrial Innovation">', unsafe_allow_html=True)
        else:
            st.image("https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&q=80&w=400", caption="Industrial Innovation (Placeholder)")

    st.markdown("---")

    # About US Section
    st.markdown('<p class="header-font">👥 About Us</p>', unsafe_allow_html=True)
    st.markdown('<p class="large-font">We are a group of PHD students and a professor from Lisa Lab of Industrial Engineering Department at Penn State University.</p>', unsafe_allow_html=True)
    
    # 4 columns for team members
    team_cols = st.columns(4)
    team_members = [
        {"name": "Soundar Kumara", "email": "Skumara@psu.edu", "img": "assets/images/team1.jpg"},
        {"name": "Xiaowen You", "email": "xxy5196@psu.edu", "img": "assets/images/team2.jpg"},
        {"name": "Dyutimoy Das", "email": "dnd5258@psu.edu", "img": "assets/images/team3.jpeg"},
        {"name": "Vinay Mathew", "email": "vinaysmathew@psu.edu​", "img": "assets/images/team4.jpg"},
    ]
    
    for i, member in enumerate(team_members):
        with team_cols[i]:
            img_b64 = get_image_as_base64(member["img"])
            if img_b64:
                st.markdown(f'<img src="{img_b64}" class="team-img" alt="{member["name"]}">', unsafe_allow_html=True)
            else:
                st.image("https://via.placeholder.com/150", width=150, caption="(Image missing)")
            st.markdown(f'<p style="font-size: 18px; font-weight: bold; margin-bottom: 0px;">{member["name"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="font-size: 16px;">📧 {member["email"]}</p>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<p class="header-font">🚀 Our Strategic Impact</p>', unsafe_allow_html=True)
    st.markdown("""
        <p class="large-font">
        This initiative aims to counter the economic threat posed by retiring business owners by automating the 
        evaluation and transfer of legacy firms. By constructing a digital twin that visualizes machinery, workflows, 
        and hidden supply chain dependencies, we eliminate the information asymmetry that often forces 
        liquidation. This system transforms an opaque, risky transaction into a transparent, data-driven acquisition. 
        Ultimately, AEEVE preserves critical institutions and prevents the cascading economic failure that occurs 
        when a viable company shuts down simply because it cannot find a successor.
        </p>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
#  COMPANY PROFILE
# ════════════════════════════════════════════════════════════════════════════
elif layer == "Company Profile":
    try:
        profile = requests.get(api_url("/api/v1/operational/company-profile")).json()
    except Exception:
        st.error("Could not load company profile. Ensure the backend is running.")
        st.stop()

    st.header(f"{profile['name']}")
    st.markdown(f"*{profile['address']}* — Founded {profile['founded']} — NAICS {profile['naics']}")

    st.markdown("---")

    # Top-level metrics
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Annual Revenue", f"${profile['annual_revenue_usd']:,.0f}")
    c2.metric("EBITDA", f"${profile['ebitda_usd']:,.0f}", f"{profile['ebitda_margin_pct']}% margin")
    c3.metric("Employees", profile['employees'])
    c4.metric("Facility", f"{profile['facility_sqft']:,} sq ft")
    c5.metric("Owner Age", profile['owner_age'], "Retirement planned Q4 2027")

    st.markdown("---")

    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("Succession Risk")
        st.error(f"**{profile['succession_status']}**")
        st.markdown(f"""
        **Owner:** {profile['owner']} (age {profile['owner_age']})

        Robert Hartwell founded this company in {profile['founded']} and has operated it for
        {2026 - profile['founded']} years. With no family member or internal candidate identified
        as successor, this firm faces **involuntary liquidation** if a buyer is not matched before
        the owner's planned retirement. The loss would cascade through the Lehigh Valley
        manufacturing ecosystem.
        """)

    with col_r:
        st.subheader("Certifications & Market Access")
        for cert in profile['certifications']:
            st.markdown(f"- {cert}")
        st.markdown("**Key Markets Served:**")
        for mkt in profile['key_markets']:
            st.markdown(f"- {mkt}")

    # Socioeconomic impact preview
    st.markdown("---")
    st.subheader("Projected Socioeconomic Impact if Firm Shuts Down")
    ic1, ic2, ic3, ic4 = st.columns(4)
    ic1.metric("Direct Jobs Lost", "47")
    ic2.metric("Indirect Jobs at Risk", "134")
    ic3.metric("Regional GDP Impact", "$14.6M")
    ic4.metric("Govt. Assistance Cost", "$890K", "Unemployment, retraining, aid")

    # ── Enterprise Health Index (top-level) ────────────────────────────────
    st.markdown("---")
    st.subheader("Enterprise Health Index")
    st.write("Composite score combining internal asset condition with external market and geopolitical factors. Used to adjust valuation and predict transition readiness.")

    try:
        ehi = requests.get(api_url("/api/v1/operational/health-index/composite")).json()
        score = ehi['enterprise_health_index']
        int_score = ehi['internal_health']
        ext_score = ehi['external_health']

        eh1, eh2, eh3 = st.columns(3)

        if score >= 0.75:
            eh1.metric("Enterprise Health", f"{score:.1%}", "Healthy")
        elif score >= 0.55:
            eh1.metric("Enterprise Health", f"{score:.1%}", "Fair — headwinds present")
        else:
            eh1.metric("Enterprise Health", f"{score:.1%}", "At Risk", delta_color="inverse")

        eh2.metric("Internal Health", f"{int_score:.1%}", "Machinery, workforce, process")
        eh3.metric("External Health", f"{ext_score:.1%}", "Supply chain, market, geopolitical")

        st.progress(score, text=f"Enterprise Health Index: {score:.1%} ({ehi['weighting']})")
        st.markdown(f"**Assessment:** {ehi['assessment']}")

        if 'valuation_implications' in ehi:
            vi = ehi['valuation_implications']
            v1, v2, v3 = st.columns(3)
            v1.metric("Base Enterprise Value", f"${vi['base_enterprise_value_usd']:,.0f}")
            v2.metric("Health-Adjusted Value", f"${vi['health_adjusted_value_usd']:,.0f}", f"{vi['health_adjusted_multiplier']:.2f}x multiplier")
            v3.metric("Projected External Pressure", f"${vi['external_cost_pressure_annual_usd']:,.0f}/yr", "If current conditions persist", delta_color="inverse")

    except Exception as e:
        st.warning(f"Health index not available: {e}")


# ════════════════════════════════════════════════════════════════════════════
#  1. DIGITAL TWIN LAYER
# ════════════════════════════════════════════════════════════════════════════
elif layer == "1. Digital Twin Layer":
    st.header("Operational Core — Digital Twin Layer")
    st.info("Constructing a precise digital replica of Hartwell Precision to monitor physical assets, workforce, and operational connectivity.")

    # ── Live Production KPIs ──────────────────────────────────────────────
    st.subheader("Live Production KPIs (Simulated IoT Feed)")
    if st.button("Refresh IoT Data", type="primary"):
        st.rerun()

    try:
        res = requests.get(api_url("/api/v1/operational/digital-twin/kpis")).json()
        k1, k2, k3, k4, k5, k6 = st.columns(6)
        k1.metric("Machine Utilization", f"{res['machine_utilization_pct']}%")
        k2.metric("Throughput", f"{res['production_throughput_units_per_hr']} units/hr")
        k3.metric("OEE", f"{res['overall_equipment_effectiveness_pct']}%")
        k4.metric("Scrap Rate", f"{res['scrap_rate_pct']}%")
        k5.metric("Machines Online", f"{res['machines_online']}/{res['machines_total']}")
        k6.metric("On-Time Delivery", f"{res['on_time_delivery_pct']}%")

        if res['anomaly_detected']:
            st.error(f"**Anomaly Detected:** {res.get('anomaly_detail', 'Unknown anomaly')}")

        st.caption(f"Active IoT sensors: {res['active_iot_sensors']} — Active work orders: {res['active_work_orders']}")
    except Exception as e:
        st.error(f"Could not fetch KPIs: {e}")

    st.markdown("---")

    # ── 3D Facility Layout ────────────────────────────────────────────────
    st.subheader("3D Facility Layout — 28,000 sq ft CNC Shop")
    st.caption("Interactive factory simulation — orbit with mouse, hover machines for details. Real equipment: Haas, DMG Mori, Mazak, Trumpf, Mitutoyo.")
    try:
        layout_res = requests.get(api_url("/api/v1/operational/digital-twin/layout-3d")).json()
        render_factory_3d(layout_res['machines'], layout_res.get('conveyors', []))
    except Exception as e:
        st.error(f"Could not load 3D layout data: {e}")

    st.markdown("---")

    # ── Human Capital ─────────────────────────────────────────────────────
    st.subheader("Human Capital — Wage-Skill Vulnerability Assessment")
    st.write("Identifying high-flight-risk talent and employees vulnerable to displacement if firm closes.")

    try:
        hc_res = requests.get(api_url("/api/v1/operational/human-capital/wage-skill")).json()
        df = pd.DataFrame(hc_res['nodes'])
        summary = hc_res['summary']

        # Summary metrics
        h1, h2, h3, h4 = st.columns(4)
        h1.metric("Total Workforce", summary['total_employees'])
        h2.metric("Avg. Tenure", f"{summary['avg_tenure_years']} yrs")
        h3.metric("High Flight Risk", summary['high_flight_risk_count'], "Would leave within 6 months of ownership change")
        h4.metric("Need Govt. Assistance", summary['employees_needing_govt_assistance_if_shutdown'], "If firm shuts down")

        fig = px.scatter(
            df,
            x="skill_level",
            y="wage_usd_hr",
            size="flight_risk",
            color="dept",
            hover_name="employee_id",
            hover_data={"role": True, "name": True, "years_tenure": True, "flight_risk": ":.0%", "wage_usd_hr": ":$.2f", "skill_level": True, "dept": False},
            title="Workforce Flight Risk — Wage vs. Skill Level (bubble size = flight risk probability)",
            labels={"skill_level": "Skill Level (1-10)", "wage_usd_hr": "Hourly Wage (USD)", "dept": "Department"},
            color_discrete_sequence=px.colors.qualitative.Set2,
            height=550,
        )
        fig.update_layout(
            xaxis=dict(range=[2, 10.5]),
            yaxis=dict(range=[15, 50], tickprefix="$"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        fig.add_annotation(
            x=9.4, y=45, text="HIGH SKILL / HIGH WAGE<br><b>Key-man risk zone</b>",
            showarrow=False, font=dict(size=10, color="#ff6666"),
            bgcolor="rgba(255,50,50,0.1)", bordercolor="#ff4444",
        )
        fig.add_annotation(
            x=4.2, y=18, text="LOW SKILL / LOW WAGE<br><b>Govt. assistance likely</b>",
            showarrow=False, font=dict(size=10, color="#ffaa00"),
            bgcolor="rgba(255,170,0,0.1)", bordercolor="#ffaa00",
        )
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("View Full Workforce Table"):
            display_df = df[["employee_id", "name", "role", "dept", "years_tenure", "skill_level", "wage_usd_hr", "flight_risk"]].copy()
            display_df["flight_risk"] = display_df["flight_risk"].apply(lambda x: f"{x:.0%}")
            display_df["wage_usd_hr"] = display_df["wage_usd_hr"].apply(lambda x: f"${x:.2f}")
            display_df.columns = ["ID", "Name", "Role", "Department", "Tenure (yrs)", "Skill", "Wage/Hr", "Flight Risk"]
            st.dataframe(display_df, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Could not load workforce data: {e}")

    st.markdown("---")

    # ── Internal Health Index — Machine-by-Machine ────────────────────────
    st.subheader("Internal Health Index — Machinery Condition Assessment")
    st.write("Per-machine health scores derived from runtime hours, MTBF, maintenance compliance, and active fault conditions. Drives asset valuation accuracy.")

    try:
        ihi = requests.get(api_url("/api/v1/operational/health-index/internal")).json()

        # Summary
        ms = ihi['machinery_summary']
        ih1, ih2, ih3, ih4, ih5 = st.columns(5)
        ih1.metric("Composite Internal Health", f"{ihi['composite_internal_health_index']:.1%}")
        ih2.metric("Machines Assessed", ms['total_machines_assessed'])
        ih3.metric("Replacement Cost", f"${ms['total_replacement_cost_usd']:,.0f}")
        ih4.metric("Book Value", f"${ms['total_book_value_usd']:,.0f}")
        ih5.metric("Depreciation Gap", f"${ms['depreciation_gap_usd']:,.0f}")

        if ms['critical_issues'] > 0:
            st.error(f"**{ms['critical_issues']} critical issue(s)** and **{ms['warning_issues']} warning(s)** across fleet")

        # Machine health chart
        m_df = pd.DataFrame([
            {"Machine": m['name'], "Health Score": m['condition_score'], "Hours Run": m['hours_run'], "Book Value": m['current_book_value_usd']}
            for m in ihi['machines']
        ])
        m_df = m_df.sort_values("Health Score")

        fig_mh = go.Figure()
        colors = ["#ff4444" if s < 0.4 else "#ffaa00" if s < 0.7 else "#00cc66" for s in m_df["Health Score"]]
        fig_mh.add_trace(go.Bar(
            x=m_df["Health Score"],
            y=m_df["Machine"],
            orientation='h',
            marker_color=colors,
            text=[f"{s:.0%}" for s in m_df["Health Score"]],
            textposition='outside',
        ))
        fig_mh.update_layout(
            title="Machine Condition Scores (0% = failed, 100% = like-new)",
            xaxis=dict(range=[0, 1.1], tickformat=".0%"),
            yaxis=dict(autorange="reversed"),
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
        )
        fig_mh.add_vline(x=0.4, line_dash="dash", line_color="#ff4444", annotation_text="Critical")
        fig_mh.add_vline(x=0.7, line_dash="dash", line_color="#ffaa00", annotation_text="Warning")
        st.plotly_chart(fig_mh, use_container_width=True)

        # Detailed per-machine expandable
        with st.expander("View Detailed Machine Health Factors"):
            for machine in ihi['machines']:
                status_icon = {True: "🔴", False: "🟢"}.get(machine['condition_score'] < 0.4, "🟡") if machine['condition_score'] < 0.7 else "🟢"
                st.markdown(f"**{status_icon} {machine['name']}** — {machine['category']} — Health: **{machine['condition_score']:.0%}** — {machine['hours_run']:,} hrs — Book: ${machine['current_book_value_usd']:,.0f}")
                for hf in machine['health_factors']:
                    icon = {"critical": "🔴", "warning": "🟡", "nominal": "🟢"}.get(hf['status'], "⚪")
                    st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;{icon} **{hf['factor']}**: {hf['detail']}")
                st.markdown("")

    except Exception as e:
        st.error(f"Could not load internal health data: {e}")

    st.markdown("---")

    # ── External Health Index — Geopolitical & Supply Chain ────────────────
    st.subheader("External Health Index — Supply Chain, Market & Geopolitical Risks")
    st.write("Quantifying external pressures on the enterprise, including the ongoing Iran conflict's impact on energy costs and material supply.")

    try:
        ehi = requests.get(api_url("/api/v1/operational/health-index/external")).json()

        # Top-level scores
        ex1, ex2, ex3, ex4 = st.columns(4)
        ex1.metric("Composite External Health", f"{ehi['composite_external_health_index']:.1%}")

        for cat_name, cat_label in [("supply_chain_resilience", "Supply Chain"), ("customer_stability", "Customer Stability"), ("geopolitical_macro", "Geopolitical / Macro")]:
            cat = ehi['categories'][cat_name]
            col = {"supply_chain_resilience": ex2, "customer_stability": ex3, "geopolitical_macro": ex4}[cat_name]
            col.metric(cat_label, f"{cat['score']:.1%}")

        # Cost impact callout
        cost = ehi['cost_impact_summary']
        st.warning(
            f"**Projected 12-Month Impact (if current conditions persist):** "
            f"Iran-driven energy & freight: +${cost['iran_conflict_annual_cost_increase_usd']:,.0f}/yr — "
            f"Ti price pressure: +${cost['titanium_price_increase_annual_usd']:,.0f}/yr — "
            f"**Total projected external pressure: ${cost['total_external_cost_pressure_usd']:,.0f}/yr "
            f"({cost['pct_of_ebitda']}% of EBITDA)**"
        )

        # Detailed factor list
        for cat_name, cat_label in [("geopolitical_macro", "Geopolitical & Macro Risks"), ("supply_chain_resilience", "Supply Chain Resilience"), ("customer_stability", "Customer Stability")]:
            cat = ehi['categories'][cat_name]
            with st.expander(f"{cat_label} (Score: {cat['score']:.0%})", expanded=(cat_name == "geopolitical_macro")):
                for f in cat['factors']:
                    icon = {"critical": "🔴", "warning": "🟡", "nominal": "🟢"}.get(f['status'], "⚪")
                    st.markdown(f"{icon} **{f['factor']}** — Score: {f['score']:.0%} (weight: {f['weight']:.0%})")
                    st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;{f['detail']}")
                    st.markdown("")

    except Exception as e:
        st.error(f"Could not load external health data: {e}")


# ════════════════════════════════════════════════════════════════════════════
#  2. MARKET DYNAMICS & RESILIENCE
# ════════════════════════════════════════════════════════════════════════════
elif layer == "2. Market Dynamics & Resilience":
    st.header("Market Dynamics & Resilience Layer")
    st.info("Quantifying non-linear economic shocks with ML and mapping hidden supply chain dependencies with Graph Neural Networks.")

    # ── Socio-Economic Impact Predictor ───────────────────────────────────
    st.subheader("Firm Exit Probability — ML Ensemble Predictor")
    st.write("Uses Random Forest + Gradient Boosting ensemble to predict firm exit probability based on financial health, owner demographics, and market conditions.")

    with st.expander("Adjust Firm Parameters & Run Prediction", expanded=True):
        p1, p2, p3, p4 = st.columns(4)
        l_ratio = p1.slider("Liquidity Ratio", 0.0, 2.0, 0.72, help="Current assets / current liabilities. Hartwell current: 0.72")
        d_equity = p2.slider("Debt-to-Equity", 0.0, 5.0, 1.8, help="Total debt / total equity. Hartwell current: 1.8")
        turnover = p3.slider("Employee Turnover", 0.0, 0.5, 0.14, help="Annual turnover rate. Hartwell current: 14%")
        demand = p4.slider("Market Demand Trend", -1.0, 1.0, 0.22, help="YoY demand change. Lehigh Valley mfg: +22%")

        p5, p6, p7, p8 = st.columns(4)
        owner_age = p5.slider("Owner Age", 50, 85, 72)
        yrs_no_succ = p6.slider("Years Without Successor", 0, 15, 3)
        rev_conc = p7.slider("Top Customer Revenue %", 0.0, 0.6, 0.28, help="BAE Systems = 28% of revenue")
        certs_risk = p8.slider("Certifications at Risk", 0, 8, 2, help="ISO, ITAR, AS9100 renewals pending")

        if st.button("Run Exit Prediction Model", type="primary"):
            payload = {
                "liquidity_ratio": l_ratio,
                "debt_to_equity": d_equity,
                "employee_turnover": turnover,
                "market_demand_trend": demand,
                "owner_age": float(owner_age),
                "years_without_successor": float(yrs_no_succ),
                "revenue_concentration_top_customer_pct": rev_conc,
                "certifications_at_risk_count": float(certs_risk),
            }
            try:
                res = requests.post(api_url("/api/v1/market/predict-exit"), json=payload).json()

                prob = res['exit_probability']
                if prob > 0.7:
                    st.error(f"**Exit Probability: {prob:.1%}** — CRITICAL RISK")
                elif prob > 0.4:
                    st.warning(f"**Exit Probability: {prob:.1%}** — ELEVATED RISK")
                else:
                    st.success(f"**Exit Probability: {prob:.1%}** — MANAGEABLE")

                st.write(f"**Model:** {res['model']}")
                st.write(f"**Recommendation:** {res['recommendation']}")

                if 'socioeconomic_impact' in res:
                    st.markdown("---")
                    st.markdown("**Projected Regional Impact if Firm Exits:**")
                    sei = res['socioeconomic_impact']
                    s1, s2, s3 = st.columns(3)
                    s1.metric("Direct + Indirect Jobs", f"{sei['direct_jobs_lost'] + sei['indirect_jobs_at_risk']}")
                    s2.metric("Regional GDP Impact", f"${sei['estimated_regional_gdp_impact_usd']:,.0f}")
                    s3.metric("Payroll + Tax Revenue Lost", f"${sei['annual_payroll_lost_usd'] + sei['annual_tax_revenue_lost_usd']:,.0f}/yr")
            except Exception as e:
                st.error(f"Prediction failed: {e}")

    st.markdown("---")

    # ── Supply Chain Graph ────────────────────────────────────────────────
    st.subheader("Supply Chain Topology — Temporal Production Graph (GNN Analysis)")
    st.write("Mapping Tier 1, Tier 2, and downstream dependencies. Click any node for asset valuation.")

    try:
        graph_data = requests.get(api_url("/api/v1/operational/supply-chain/graph")).json()

        nodes = [
            Node(
                id=n['id'],
                label=n['label'],
                size=n['size'],
                color=n['color'],
                title=n.get('detail', ''),
            )
            for n in graph_data['nodes']
        ]
        edges = [
            Edge(source=e['source'], target=e['target'], label=e['label'], length=500)
            for e in graph_data['edges']
        ]

        custom_physics = {
            "solver": "repulsion",
            "repulsion": {
                "nodeDistance": 350,
                "springLength": 600,
                "springConstant": 0.008,
                "damping": 0.12,
            },
            "stabilization": {
                "iterations": 200,
            },
        }
        config = Config(width=700, height=500, directed=True, hierarchical=False)
        config.physics = custom_physics
        config.width = "100%"
        config.height = "850px"
        setattr(config, "interaction", {"zoomView": True, "dragView": True})
        setattr(config, "edges", {
            "font": {"size": 11, "strokeWidth": 3, "strokeColor": "#ffffff"},
            "color": {"color": "#cccccc", "highlight": "#1a73e8"},
            "smooth": {"type": "curvedCW", "roundness": 0.15},
        })

        clicked_node_id = agraph(nodes=nodes, edges=edges, config=config)  # type: ignore

        if clicked_node_id:
            st.sidebar.markdown("---")
            st.sidebar.subheader(f"Asset Valuation: {clicked_node_id}")

            val_res = requests.get(api_url(f"/api/v1/market/valuation/{clicked_node_id}")).json()

            st.sidebar.markdown(f"**{val_res.get('name', clicked_node_id)}**")
            st.sidebar.metric("Stability Index", val_res['stability_index'])

            if val_res.get('intangible_value_usd'):
                st.sidebar.write(f"**Intangible Assets (ML):** ${val_res['intangible_value_usd']:,}")
            if val_res.get('tangible_value_usd'):
                st.sidebar.write(f"**Tangible Assets:** ${val_res['tangible_value_usd']:,}")
            if val_res.get('total_enterprise_value_usd'):
                st.sidebar.write(f"**Total Enterprise Value:** ${val_res['total_enterprise_value_usd']:,}")
            if val_res.get('patent_count'):
                st.sidebar.write(f"**Patents:** {val_res['patent_count']}")

            status = val_res.get('risk_status', '')
            if "High Risk" in status or "Critical" in status:
                st.sidebar.error(f"**{status}**")
            elif "Moderate" in status:
                st.sidebar.warning(f"**{status}**")
            elif "Stable" in status:
                st.sidebar.success(f"**{status}**")
            else:
                st.sidebar.info(f"**{status}**")

            if val_res.get('risk_factors'):
                st.sidebar.markdown("**Risk Factors:**")
                for rf in val_res['risk_factors']:
                    st.sidebar.markdown(f"- {rf}")
        else:
            st.sidebar.info("Click a node in the supply chain graph to run Dynamic Asset Valuation.")

        # GNN Insights
        if 'gnn_insights' in graph_data:
            st.markdown("---")
            st.subheader("GNN Risk Insights")
            for insight in graph_data['gnn_insights']:
                sev = insight['severity']
                msg = insight['message']
                rev = insight.get('affected_revenue_usd', 0)
                rev_str = f" — **${rev:,.0f}** revenue at risk" if rev else ""

                if sev == "critical":
                    st.error(f"**CRITICAL:** {msg}{rev_str}")
                elif sev == "high":
                    st.warning(f"**HIGH:** {msg}{rev_str}")
                elif sev == "medium":
                    st.info(f"**MEDIUM:** {msg}{rev_str}")
                else:
                    st.caption(f"LOW: {msg}{rev_str}")

    except Exception as e:
        st.error(f"Could not load graph data. Ensure the backend server is running. ({e})")


# ════════════════════════════════════════════════════════════════════════════
#  3. LEGAL & COMPLIANCE FRAMEWORK
# ════════════════════════════════════════════════════════════════════════════
elif layer == "3. Legal & Compliance Framework":
    st.header("Legal & Disclosure Compliance Framework")
    st.info("Operationalizing compliance for asset transfer, data governance, and regulatory continuity under Pennsylvania law.")

    # ── Compliance Dashboard ──────────────────────────────────────────────
    st.subheader("License & Certification Expiry Tracker")

    try:
        comp = requests.get(api_url("/api/v1/legal/compliance/overview")).json()

        # Summary metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Tracked Items", comp['total_items'])
        m2.metric("Critical (< 60 days)", comp['critical_count'], delta_color="inverse" if comp['critical_count'] > 0 else "off")
        m3.metric("Warning (60-135 days)", comp['warning_count'])
        m4.metric("OK (> 135 days)", comp['ok_count'])

        # Timeline visualization
        items_df = pd.DataFrame(comp['items'])
        items_df['expiry_date'] = pd.to_datetime(items_df['expiry_date'])
        items_df = items_df.sort_values('days_until_expiry')

        color_map = {"critical": "#ff4444", "warning": "#ffaa00", "ok": "#00cc66"}
        items_df['color'] = items_df['urgency'].map(color_map)

        fig = go.Figure()
        for _, row in items_df.iterrows():
            fig.add_trace(go.Bar(
                x=[row['days_until_expiry']],
                y=[row['name'][:45]],
                orientation='h',
                marker_color=row['color'],
                text=f"{row['days_until_expiry']}d",
                textposition='outside',
                hovertext=f"{row['name']}<br>Category: {row['category']}<br>Issuer: {row['issuer']}<br>Expires: {row['expiry_date'].strftime('%b %d, %Y')}<br>{row['notes'][:150]}...",
                showlegend=False,
            ))

        n_items = len(items_df)
        fig.update_layout(
            title="Days Until Expiry (from April 7, 2026)",
            xaxis_title="Days Remaining",
            yaxis=dict(autorange="reversed"),
            height=max(400, n_items * 42 + 80),
            margin=dict(l=20, r=60, t=60, b=40),
            xaxis=dict(range=[0, max(items_df['days_until_expiry']) + 80]),
        )
        fig.add_vline(
            x=60, line_dash="dash", line_color="#ef4444",
            annotation_text="60d", annotation_position="top right",
            annotation_font_size=10, annotation_font_color="#ef4444",
        )
        fig.add_vline(
            x=135, line_dash="dash", line_color="#f59e0b",
            annotation_text="135d", annotation_position="top right",
            annotation_font_size=10, annotation_font_color="#f59e0b",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Detailed cards
        st.markdown("---")
        for item in comp['items']:
            urgency = item['urgency']
            css_class = f"compliance-{urgency}"
            icon = {"critical": "🔴", "warning": "🟡", "ok": "🟢"}.get(urgency, "⚪")
            days = item['days_until_expiry']

            st.markdown(f"""<div class='{css_class}'>
                <strong>{icon} {item['name']}</strong><br>
                <span style='color:#aaa'>Issuer: {item['issuer']} — Category: {item['category']}</span><br>
                <span style='color:#ddd'>Expires: {item['expiry_date']} ({days} days)</span><br>
                <span style='color:#ccc'>{item['notes']}</span><br>
                <span style='color:#88aaff'><em>Transfer Impact: {item['transfer_impact']}</em></span>
            </div>""", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Could not load compliance data: {e}")

    st.markdown("---")

    # ── Ownership Rights ──────────────────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Ownership Transfer — PA Regulations")
        try:
            rights = requests.get(api_url("/api/v1/legal/compliance/ownership-rights")).json()

            st.markdown(f"**Jurisdiction:** {rights['jurisdiction']}")
            st.markdown(f"**Recommended Structure:** {rights['transfer_type']}")

            for reg in rights['regulations']:
                status_icon = {"pending": "🟡", "critical": "🔴", "complete": "🟢"}.get(reg['status'], "⚪")
                with st.expander(f"{status_icon} {reg['code']}"):
                    st.markdown(f"**Section:** {reg['section']}")
                    st.markdown(f"**Requirement:** {reg['requirement']}")
                    st.markdown(f"**Action Needed:** {reg['action_needed']}")

            st.markdown("**Completed Steps:**")
            for step in rights['steps_completed']:
                st.markdown(f"- :white_check_mark: {step}")

            st.markdown("**Pending Actions:**")
            for action in rights['pending_actions']:
                st.markdown(f"- :hourglass_flowing_sand: {action}")

        except Exception as e:
            st.error(f"Could not load ownership data: {e}")

    with col2:
        st.subheader("Knowledge Disclosure & Cybersecurity")
        try:
            kd = requests.get(api_url("/api/v1/legal/compliance/knowledge-disclosure")).json()

            # Trade secrets
            ts = kd['trade_secret_protection']
            st.markdown(f"**Governing Law:** {ts['governing_law']}")
            st.markdown(f"**CAD Files Protected:** {ts['cad_files_protected']:,}")
            st.markdown(f"**CNC Programs Protected:** {ts['cnc_programs_protected']:,}")
            st.markdown(f"**Encryption:** {ts['encryption_method']}")

            st.markdown("**Active Protections:**")
            for p in ts['protections_in_place']:
                st.markdown(f"- {p}")

            st.markdown("---")

            # Cybersecurity / CMMC
            cyber = kd['cybersecurity_compliance']
            st.markdown(f"**{cyber['governing_regulation']}**")
            st.markdown(f"CMMC Level: **{cyber['cmmc_level']}**")

            score = cyber['nist_sp_800_171_score']
            max_score = cyber['nist_sp_800_171_max']
            pct = score / max_score * 100
            st.progress(pct / 100, text=f"NIST SP 800-171 Score: {score}/{max_score} ({pct:.0f}%)")

            if cyber['poa_m_items_open'] > 0:
                st.warning(f"**{cyber['poa_m_items_open']} POA&M items open** — {cyber['status']}")

            st.markdown("---")

            # Data breach
            breach = kd['data_breach_notification']
            st.markdown(f"**{breach['governing_law']}**")
            st.markdown(f"Employee PII records: **{breach['employee_pii_records']}**")
            st.markdown(f"**Transfer Protocol:** {breach['transfer_protocol']}")

        except Exception as e:
            st.error(f"Could not load disclosure data: {e}")