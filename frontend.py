import streamlit as st
import requests
import pandas as pd
import json
import plotly.express as px
import streamlit.components.v1 as components
from streamlit_agraph import agraph, Node, Edge, Config
import os

api_base_url = st.secrets.get("API_BASE_URL", os.getenv("API_BASE_URL", "http://localhost:8000")).rstrip("/")


def api_url(path: str) -> str:
    return f"{api_base_url}{path}"

# Set page config for a professional look
st.set_page_config(page_title="SMM Evaluation Engine", layout="wide")


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
backdrop-filter:blur(4px);z-index:10;line-height:1.6}
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

// --- Scene Setup ---
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

// --- Lighting ---
scene.add(new THREE.AmbientLight(0x404060, 0.5));
scene.add(new THREE.HemisphereLight(0x8888cc, 0x443322, 0.4));
const sun = new THREE.DirectionalLight(0xffeedd, 1.0);
sun.position.set(30, 35, 25);
sun.castShadow = true;
Object.assign(sun.shadow.camera, {left:-30,right:30,top:30,bottom:-30,near:1,far:100});
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.bias = -0.001;
scene.add(sun);

// --- Floor with procedural concrete texture ---
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

// --- Safety lane markings ---
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

// --- Structural columns ---
[[-3,-1],[-3,33],[39,-1],[39,33],[18,-1],[18,33]].forEach(p => {
  const c = new THREE.Mesh(
    new THREE.CylinderGeometry(0.25,0.25,7,8),
    new THREE.MeshStandardMaterial({color:0x556666, metalness:0.6, roughness:0.3})
  );
  c.position.set(p[0], 3.5, p[1]);
  c.castShadow = true;
  scene.add(c);
});

// --- Overhead industrial lights ---
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

// --- Ceiling beams ---
[4, 16, 28].forEach(z => {
  const b = new THREE.Mesh(
    new THREE.BoxGeometry(46, 0.3, 0.15),
    new THREE.MeshStandardMaterial({color:0x555555, metalness:0.6})
  );
  b.position.set(18, 7.1, z);
  scene.add(b);
});

// --- Shared Materials ---
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

// --- Machine Builder ---
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

  // Status indicator light + pole
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

  // Glowing floor ring
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

  // Floating label sprite
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
  lx.fillText(d.status + ' \u00b7 ' + Math.round(d.efficiency * 100) + '%', 256, 72);
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

// --- Zone labels painted on the floor ---
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
zoneLabel('MILLING', 11, 5);
zoneLabel('TURNING', 26, 5);
zoneLabel('CUTTING', 11, 28);
zoneLabel('INSPECTION', 26, 28);
zoneLabel('ASSEMBLY', 18, 19);

// --- Conveyor belts ---
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
});

// --- Mouse hover tooltip ---
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
      'Type: ' + hit.type + '<br>' +
      'Status: <span style="color:' + sc + '">' + hit.status + '</span><br>' +
      'Efficiency: ' + Math.round(hit.efficiency * 100) + '%';
  } else {
    tooltipEl.style.display = 'none';
  }
});

// --- Animation loop ---
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


st.title("🛡️ Autonomous Enterprise Evaluation & Visualization Engine")
st.markdown("---")

# Sidebar for Navigation
st.sidebar.header("Navigation")
layer = st.sidebar.radio("Select Layer", ["1. Digital Twin", "2. Market Dynamics", "3. Legal & Disclosure"])

# 1. OPERATIONAL CORE LAYER
if layer == "1. Digital Twin":
    st.header("Digital Twin")
    st.info("Constructing a precise digital replica to monitor physical assets.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Live Production KPIs")
        if st.button("Fetch Live IoT Data"):
            res = requests.get(api_url("/api/v1/operational/digital-twin/kpis")).json()
            st.metric("Machine Utilization", f"{res['machine_utilization_pct']}%")
            st.metric("Throughput (Units/Hr)", res['production_throughput_units_per_hr'])
            if res['anomaly_detected']:
                st.error("⚠️ Anomaly Detected in Facility Layout")
    
    with col2:
        st.subheader("Human Capital: Wage-Skill Plot")
        res = requests.get(api_url("/api/v1/operational/human-capital/wage-skill")).json()
        df = pd.DataFrame(res['nodes'])
        fig = px.scatter(df, x="skill_level", y="wage_usd_hr", size="flight_risk", 
                         color="flight_risk", hover_name="employee_id",
                         title="Workforce Vulnerability Assessment")
        st.plotly_chart(fig, width='stretch')

    st.markdown("---")
    st.subheader("3D Facility Layout (Live IoT Status)")
    st.caption("Interactive factory simulation \u2014 orbit with mouse, hover machines for details.")

    try:
        layout_res = requests.get("http://localhost:8000/api/v1/operational/digital-twin/layout-3d").json()
        render_factory_3d(layout_res['machines'], layout_res.get('conveyors', []))
    except Exception as e:
        st.error(f"Could not load 3D layout data: {e}")

# 2. MARKET DYNAMICS LAYER
elif layer == "2. Market Dynamics":
    st.header("Market Dynamics & Resilience")
    st.info("Quantifying non-linear economic shocks using Machine Learning.")
    
    # --- Module 2.1: Socio-Economic Impact ---
    with st.expander("Run Socio-Economic Impact Assessment"):
        l_ratio = st.slider("Liquidity Ratio", 0.0, 1.0, 0.5)
        d_equity = st.slider("Debt-to-Equity", 0.0, 5.0, 1.2)
        turnover = st.slider("Employee Turnover", 0.0, 1.0, 0.2)
        demand = st.slider("Market Demand Trend", -1.0, 1.0, 0.1)
        
        if st.button("Predict Exit Probability"):
            payload = {
                "liquidity_ratio": l_ratio,
                "debt_to_equity": d_equity,
                "employee_turnover": turnover,
                "market_demand_trend": demand
            }
            res = requests.post(api_url("/api/v1/market/predict-exit"), json=payload).json()
            st.warning(f"Exit Probability: {res['exit_probability']:.2%}")
            st.write(f"**Recommendation:** {res['recommendation']}")

    st.markdown("---")

    # --- Module 2.3: Supply Chain Resilience (FIXED INDENTATION) ---
    st.subheader("Temporal Production Graph (GNN Analysis)")
    st.write("Visualizing latent dependencies and hidden supplier failures.")
    
    try:
        graph_data = requests.get(api_url("/api/v1/operational/supply-chain/graph")).json()

        nodes = [Node(id=n['id'], label=n['label'], size=n['size'], color=n['color']) for n in graph_data['nodes']]
        edges = [Edge(source=e['source'], target=e['target'], label=e['label'], length=300) for e in graph_data['edges']]
        # INJECT a custom physics dictionary to tame the rubber-band effect
        custom_physics = {
            "solver": "repulsion",
            "repulsion": {
                "nodeDistance": 200,      # Pushes nodes away from each other
                "springLength": 400,      # Stretches the resting length of the edges
                "springConstant": 0.02    # Lowers the tension so dragging feels natural
            }
        }
        config = Config(width=700, height=500, directed=True, hierarchical=False)
        # Inject the advanced physics and responsive dimensions post-initialization
        config.physics = custom_physics
        config.width = "100%"
        config.height = "700px"
        # Disable scroll hijacking using setattr to bypass Pylance/Linter
        setattr(config, "interaction", {
            "zoomView": False,  # Disables the scroll-to-zoom behavior
            "dragView": True    # Keeps the ability to pan around the canvas
        })

        # Use # type: ignore to hide the 'no parameter named key' linter error
        clicked_node_id = agraph(nodes=nodes, edges=edges, config=config) # type: ignore

        if clicked_node_id:
            st.sidebar.markdown("---")
            st.sidebar.subheader(f"🔍 Asset Valuation: {clicked_node_id}")
            
            val_url = api_url(f"/api/v1/market/valuation/{clicked_node_id}")
            val_res = requests.get(val_url).json()
            
            st.sidebar.metric("Stability Index", val_res['stability_index'])
            st.sidebar.write(f"**Intangible Assets (ML Valued):** ${val_res['intangible_value_usd']:,}")
            st.sidebar.write(f"**Registered Patents:** {val_res['patent_count']}")
            
            if val_res['risk_status'] == "High Risk":
                st.sidebar.error("⚠️ Warning: Hidden financial risks detected.")
            else:
                st.sidebar.success("✅ Stable anchor firm identified.")
        else:
            st.sidebar.info("💡 Click a node in the graph to run a Dynamic Asset Valuation.")
            
        st.error("🚨 GNN Insight: 'Supplier_B' identified as a single source of failure.")
        
    except Exception as e:
        st.error("Could not load graph data. Ensure the backend server is running.")

# 3. LEGAL & DISCLOSURE LAYER
elif layer == "3. Legal & Disclosure":
    st.header("Legal & Disclosure Compliance")
    st.info("Operationalizing compliance for asset transfer.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Ownership Rights (PA Title 15)")
        res = requests.get(api_url("/api/v1/legal/compliance/ownership-rights")).json()
        st.write(f"**Regulation:** {res['regulation']}")
        st.write(f"**Status:** {res['liability_status']}")
        
    with col2:
        st.subheader("Knowledge Disclosure (PA UTSA)")
        res = requests.get(api_url("/api/v1/legal/compliance/knowledge-disclosure")).json()
        st.write(f"**CAD Encryption:** {'✅ Active' if res['cad_encryption_status'] else '❌ Inactive'}")
        st.write(f"**Compliance:** {'Verified' if res['is_compliant'] else 'Attention Required'}")