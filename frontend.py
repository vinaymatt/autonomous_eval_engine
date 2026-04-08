import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_agraph import agraph, Node, Edge, Config
import streamlit.components.v1 as components
import os
import base64
import json

api_base_url = st.secrets.get("API_BASE_URL", os.getenv("API_BASE_URL", "http://localhost:8000")).rstrip("/")


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

# Set page config for a professional look
st.set_page_config(page_title="SMM Evaluation Engine", layout="wide")

# Custom CSS for uniform image sizing and larger fonts
st.markdown("""
    <style>
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
    /* Teammate styles */
    .compliance-critical { background: rgba(255, 68, 68, 0.1); border-left: 5px solid #ff4444; padding: 12px; margin-bottom: 10px; border-radius: 4px; }
    .compliance-warning { background: rgba(255, 170, 0, 0.1); border-left: 5px solid #ffaa00; padding: 12px; margin-bottom: 10px; border-radius: 4px; }
    .compliance-ok { background: rgba(0, 204, 102, 0.1); border-left: 5px solid #00cc66; padding: 12px; margin-bottom: 10px; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

# ── 3D Factory Renderer (Teammate Logic Restored) ───────────────────────────
def render_factory_3d(machines, conveyors):
    machines_json = json.dumps(machines)
    conveyors_json = json.dumps(conveyors)
    
    html = """<!DOCTYPE html><html><head><style>body{margin:0;overflow:hidden;background:#080c18}#ct{width:100vw;height:750px}#tp{position:absolute;display:none;background:rgba(8,12,24,0.9);color:#fff;padding:10px;border:1px solid #1a73e8;border-radius:6px;font-family:sans-serif;font-size:12px;pointer-events:none;z-index:100;box-shadow:0 4px 15px rgba(0,0,0,0.5)}#lo{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);color:#1a73e8;font-family:sans-serif;font-weight:bold}</style></head>
    <body><div id="lo">INITIALIZING DIGITAL TWIN...</div><div id="tp"></div><div id="ct"></div><script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script><script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <script>const ct=document.getElementById('ct'),MD=%%MACHINES%%,CD=%%CONVEYORS%%;const scene=new THREE.Scene();scene.background=new THREE.Color(0x080c18);scene.fog=new THREE.Fog(0x080c18,20,100);const cam=new THREE.PerspectiveCamera(45,ct.clientWidth/ct.clientHeight,0.1,1000);cam.position.set(40,30,40);const ren=new THREE.WebGLRenderer({antialias:true});ren.setSize(ct.clientWidth,ct.clientHeight);ren.shadowMap.enabled=true;ct.appendChild(ren.domElement);const ctrl=new THREE.OrbitControls(cam,ren.domElement);ctrl.enableDamping=true;ctrl.dampingFactor=0.05;ctrl.maxPolarAngle=Math.PI/2.1;const amb=new THREE.AmbientLight(0xffffff,0.4);scene.add(amb);const dir=new THREE.DirectionalLight(0xffffff,0.8);dir.position.set(20,40,20);dir.castShadow=true;dir.shadow.mapSize.width=2048;dir.shadow.mapSize.height=2048;scene.add(dir);const grid=new THREE.GridHelper(100,50,0x1a73e8,0x0d1b3a);grid.position.y=0.01;scene.add(grid);const floor=new THREE.Mesh(new THREE.PlaneGeometry(100,100),new THREE.MeshStandardMaterial({color:0x0a0f1e,roughness:0.8}));floor.rotation.x=-Math.PI/2;floor.receiveShadow=true;scene.add(floor);const MAT={body:new THREE.MeshStandardMaterial({color:0x2c3e50,roughness:0.3,metalness:0.6}),accent:new THREE.MeshStandardMaterial({color:0x1a73e8,emissive:0x1a73e8,emissiveIntensity:0.2}),chrome:new THREE.MeshStandardMaterial({color:0xbdc3c7,metalness:0.9,roughness:0.1}),dark:new THREE.MeshStandardMaterial({color:0x111111}),granite:new THREE.MeshStandardMaterial({color:0x333333,roughness:0.9}),bench:new THREE.MeshStandardMaterial({color:0x444444})};const SC={Active:0x00ff00,Downtime:0xff0000,Maintenance:0xffaa00},SCS={Active:'#00ff00',Downtime:'#ff4444',Maintenance:'#ffaa00'},SHEIGHT={Milling:3.5,Turning:2.8,Inspection:4,Assembly:1.5},anims=[],machineGroups=[];function roundRect(ctx,x,y,w,h,r){ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.quadraticCurveTo(x+w,y,x+w,y+r);ctx.lineTo(x+w,y+h-r);ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);ctx.lineTo(x+r,y+h);ctx.quadraticCurveTo(x,y+h,x,y+h-r);ctx.lineTo(x,y+r);ctx.quadraticCurveTo(x,y,x+r,y);ctx.closePath()}function addBox(g,s,p,m,sh=true){const b=new THREE.Mesh(new THREE.BoxGeometry(...s),m);b.position.set(...p);if(sh){b.castShadow=true;b.receiveShadow=true}g.add(b);return b}function addCyl(g,s,p,m,sh=true){const c=new THREE.Mesh(new THREE.CylinderGeometry(...s),m);c.position.set(...p);if(sh){c.castShadow=true;c.receiveShadow=true}g.add(c);return c}function buildMachine(d){const g=new THREE.Group();switch(d.type){case 'Milling':{addBox(g,[3,3,3],[0,1.5,0],MAT.body);addBox(g,[3.1,0.8,2],[0,2.5,0.6],MAT.accent);addBox(g,[2.4,1.8,0.1],[0,1.4,1.51],new THREE.MeshStandardMaterial({color:0x88ccff,transparent:true,opacity:0.3}));const sp=addCyl(g,[0.1,0.1,0.8,16],[0,1.2,0],MAT.chrome);if(d.status==='Active')anims.push({m:sp,t:'ry',s:0.2});break}case 'Turning':{addBox(g,[4,2,2.5],[0,1.25,0],MAT.body);addBox(g,[1,1,1],[1.8,1,0],MAT.accent);const ck=addCyl(g,[0.4,0.4,0.6,32],[-1.4,1.5,0],MAT.chrome);ck.rotation.z=Math.PI/2;if(d.status==='Active')anims.push({m:ck,t:'rx',s:0.15});break}case 'Cutting':{addBox(g,[2.8,1.4,2.2],[0,0.7,0],MAT.body);const win=new THREE.Mesh(new THREE.PlaneGeometry(2.4,0.8),new THREE.MeshStandardMaterial({color:0x88ccff,transparent:true,opacity:0.25,metalness:0.1,roughness:0.05}));win.position.set(0,1.05,1.11);g.add(win);addBox(g,[2.2,0.08,0.08],[0,1.5,0],MAT.chrome);const lh=addBox(g,[0.2,0.25,0.2],[0,1.3,0],new THREE.MeshStandardMaterial({color:0xff4444,emissive:0xff2222,emissiveIntensity:0.4}),false);if(d.status==='Active')anims.push({m:lh,t:'ox',s:0.02,r:0.9,ix:0});break}case 'Inspection':{addBox(g,[3,0.35,2],[0,0.5,0],MAT.granite);addCyl(g,[0.06,0.06,2.5,6],[-1.2,2,0],MAT.chrome);addCyl(g,[0.06,0.06,2.5,6],[1.2,2,0],MAT.chrome);addBox(g,[2.4,0.12,0.12],[0,3.15,0],MAT.chrome);const pr=addCyl(g,[0.03,0.03,1.2,6],[0,2.3,0],MAT.chrome);if(d.status==='Active')anims.push({m:pr,t:'oz',s:0.01,r:0.4,iz:0});const tip=new THREE.Mesh(new THREE.SphereGeometry(0.06,8,8),new THREE.MeshStandardMaterial({color:0xff0000}));tip.position.set(0,1.7,0);g.add(tip);break}default:{addBox(g,[3,0.85,1.5],[0,0.425,0],MAT.bench);[[-1.3,0.425,-0.6],[-1.3,0.425,0.6],[1.3,0.425,-0.6],[1.3,0.425,0.6]].forEach(p=>addBox(g,[0.08,0.85,0.08],p,MAT.dark));[0x3366cc,0xcc3333,0x33cc33].forEach((col,i)=>{const part=new THREE.Mesh(new THREE.BoxGeometry(0.25,0.15,0.25),new THREE.MeshStandardMaterial({color:col}));part.position.set(-0.7+i*0.7,1,0);g.add(part)});break}}const sh=SHEIGHT[d.type]||3,sc=SC[d.status]||SC.Active;addCyl(g,[0.02,0.02,0.7,6],[1.4,sh-0.5,-0.9],MAT.dark);const bulb=new THREE.Mesh(new THREE.SphereGeometry(0.1,8,8),new THREE.MeshBasicMaterial({color:sc,transparent:true}));bulb.position.set(1.4,sh+0.1,-0.9);g.add(bulb);const ptLight=new THREE.PointLight(sc,0.4,5);ptLight.position.copy(bulb.position);scene.add(ptLight);const ring=new THREE.Mesh(new THREE.RingGeometry(1.8,2,32),new THREE.MeshBasicMaterial({color:sc,transparent:true,opacity:0.2,side:THREE.DoubleSide}));ring.rotation.x=-Math.PI/2;ring.position.y=0.01;g.add(ring);if(d.status==='Downtime'){anims.push({m:bulb,t:'pulse',s:2.5});anims.push({m:ring,t:'po',s:2.5,mt:ring.material,bo:0.2})}g.position.set(d.x,0,d.y);g.userData = d;machineGroups.push(g);scene.add(g);const lc=document.createElement('canvas');lc.width=512;lc.height=100;const lx=lc.getContext('2d');lx.fillStyle='rgba(8,12,24,0.8)';roundRect(lx,2,2,508,96,10);lx.fill();lx.strokeStyle='rgba(255,255,255,0.1)';lx.lineWidth=1.5;roundRect(lx,2,2,508,96,10);lx.stroke();lx.fillStyle='#fff';lx.font='bold 26px sans-serif';lx.textAlign='center';lx.fillText(d.id.replace(/_/g,' '),256,38);const scolor=SCS[d.status]||'#888';lx.fillStyle=scolor;lx.font='20px sans-serif';lx.fillText(d.status+' \u00b7 '+Math.round(d.efficiency*100)+'%',256,72);lx.strokeStyle=scolor;lx.lineWidth=1.5;lx.beginPath();lx.moveTo(80,48);lx.lineTo(432,48);lx.stroke();const labelTex=new THREE.CanvasTexture(lc);const labelSprite=new THREE.Sprite(new THREE.SpriteMaterial({map:labelTex,transparent:true,depthTest:false}));labelSprite.position.set(d.x,sh+2,d.y);labelSprite.scale.set(5,1,1);scene.add(labelSprite)}MD.forEach(buildMachine);CD.forEach(cv=>{const [x1,z1]=cv.from,[x2,z2]=cv.to,dx=x2-x1,dz=z2-z1,len=Math.sqrt(dx*dx+dz*dz),ang=Math.atan2(dx,dz);const belt=new THREE.Mesh(new THREE.BoxGeometry(0.5,0.04,len),new THREE.MeshStandardMaterial({color:0x333333,metalness:0.4,roughness:0.6}));belt.position.set((x1+x2)/2,0.42,(z1+z2)/2);belt.rotation.y=ang;belt.receiveShadow=true;scene.add(belt);const nItems=Math.max(2,Math.floor(len/4));for(let i=0;i<nItems;i++){const item=new THREE.Mesh(new THREE.BoxGeometry(0.25,0.15,0.25),new THREE.MeshStandardMaterial({color:0xddaa44}));item.castShadow=true;scene.add(item);anims.push({m:item,t:'cv',from:cv.from,to:cv.to,p:i/nItems,s:0.003})}});const ray=new THREE.Raycaster(),mouse=new THREE.Vector2(),tooltipEl=document.getElementById('tp');document.addEventListener('mousemove',e=>{const rect=ren.domElement.getBoundingClientRect();mouse.x=((e.clientX-rect.left)/rect.width)*2-1;mouse.y=-((e.clientY-rect.top)/rect.height)*2+1;ray.setFromCamera(mouse,cam);let hit=null;for(const grp of machineGroups){const meshes=[];grp.traverse(ch=>{if(ch.isMesh)meshes.push(ch)});if(ray.intersectObjects(meshes).length){hit=grp.userData;break}}if(hit){tooltipEl.style.display='block';tooltipEl.style.left=(e.clientX+12)+'px';tooltipEl.style.top=(e.clientY-10)+'px';const sc=SCS[hit.status]||'#888';tooltipEl.innerHTML='<b>'+hit.id.replace(/_/g,' ')+'</b><br>'+(hit.detail?'<span style="color:#aaa">'+hit.detail+'</span><br>':'')+'Status: <span style="color:'+sc+'">'+hit.status+'</span><br>Efficiency: '+Math.round(hit.efficiency*100)+'%'}else{tooltipEl.style.display='none'}});const clock=new THREE.Clock();function animate(){requestAnimationFrame(animate);const t=clock.getElapsedTime();anims.forEach(a=>{switch(a.t){case 'ry':a.m.rotation.y+=a.s;break;case 'rx':a.m.rotation.x+=a.s;break;case 'ox':a.m.position.x=a.ix+Math.sin(t*60*a.s)*a.r;break;case 'oz':a.m.position.z=(a.iz||0)+Math.sin(t*60*a.s)*a.r;break;case 'pulse':{const v=0.5+0.5*Math.sin(t*a.s*Math.PI);a.m.scale.setScalar(0.8+v*0.5);break}case 'po':a.mt.opacity=a.bo*(0.3+0.7*Math.abs(Math.sin(t*a.s)));break;case 'cv':{a.p+=a.s;if(a.p>1)a.p=0;const cdx=a.to[0]-a.from[0],cdz=a.to[1]-a.from[1];a.m.position.set(a.from[0]+cdx*a.p,0.55,a.from[1]+cdz*a.p);break}}});ctrl.update();ren.render(scene,cam)}window.addEventListener('resize',()=>{const w=ct.clientWidth,h=ct.clientHeight;cam.aspect=w/h;cam.updateProjectionMatrix();ren.setSize(w,h)});document.getElementById('lo').remove();animate();</script></body></html>"""
    html = html.replace('%%MACHINES%%', machines_json)
    html = html.replace('%%CONVEYORS%%', conveyors_json)
    components.html(html, height=750)

st.title("🛡️ Autonomous Enterprise Evaluation & Visualization Engine")
st.caption("Preventing cascading economic failures from manufacturing succession gaps")
st.markdown("---")

# Sidebar for Navigation
st.sidebar.header("Navigation")
layer = st.sidebar.radio("Select Layer", ["0. Welcome & Overview", "Company Profile", "1. Digital Twin", "2. Market Dynamics", "3. Legal & Disclosure"])

# 0. WELCOME & OVERVIEW LAYER
if layer == "0. Welcome & Overview":
  
    # Goal Section
    st.markdown('<p class="header-font">🎯 Our Mission</p>', unsafe_allow_html=True)
    col_goal_text, col_goal_img = st.columns([1.2, 1])
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
#  COMPANY PROFILE (Restored Teammate Logic)
# ════════════════════════════════════════════════════════════════════════════  
elif layer == "Company Profile":
    try:
        profile = requests.get(api_url("/api/v1/operational/company-profile")).json()
    except Exception:
        st.error("Could not load company profile. Ensure the backend is running.")
        st.stop()

    st.markdown(f'<p class="header-font">{profile["name"]}</p>', unsafe_allow_html=True)
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
        the owner's planned retirement.
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
    try:
        ehi = requests.get(api_url("/api/v1/operational/health-index/composite")).json()
        score = ehi['enterprise_health_index']
        int_score = ehi['internal_health']
        ext_score = ehi['external_health']

        eh1, eh2, eh3 = st.columns(3)
        if score >= 0.75: eh1.metric("Enterprise Health", f"{score:.1%}", "Healthy")
        elif score >= 0.55: eh1.metric("Enterprise Health", f"{score:.1%}", "Fair")
        else: eh1.metric("Enterprise Health", f"{score:.1%}", "At Risk", delta_color="inverse")

        eh2.metric("Internal Health", f"{int_score:.1%}")
        eh3.metric("External Health", f"{ext_score:.1%}")
        st.progress(score, text=f"Enterprise Health Index: {score:.1%}")
    except:
        st.warning("Health index not available.")


# ════════════════════════════════════════════════════════════════════════════  
#  1. DIGITAL TWIN (Restored Teammate Logic)
# ════════════════════════════════════════════════════════════════════════════  
elif layer == "1. Digital Twin":
    st.markdown('<p class="header-font">Digital Twin Layer</p>', unsafe_allow_html=True)
    st.info("Constructing a precise digital replica to monitor physical assets, workforce, and operational connectivity.")

    # ── Live Production KPIs ──────────────────────────────────────────────    
    st.subheader("Live Production KPIs (Simulated IoT Feed)")
    try:
        res = requests.get(api_url("/api/v1/operational/digital-twin/kpis"), timeout=2).json()
        k1, k2, k3, k4, k5, k6 = st.columns(6)
        k1.metric("Machine Utilization", f"{res['machine_utilization_pct']}%")  
        k2.metric("Throughput", f"{res['production_throughput_units_per_hr']} units/hr")
        k3.metric("OEE", f"{res['overall_equipment_effectiveness_pct']}%")      
        k4.metric("Scrap Rate", f"{res['scrap_rate_pct']}%")
        k5.metric("Machines Online", f"{res['machines_online']}/{res['machines_total']}")
        k6.metric("On-Time Delivery", f"{res['on_time_delivery_pct']}%")        
    except:
        st.error("Could not fetch KPIs.")

    st.markdown("---")
    # 3D Facility Layout
    st.subheader("3D Facility Layout")
    try:
        layout_res = requests.get(api_url("/api/v1/operational/digital-twin/layout-3d"), timeout=2).json()
        render_factory_3d(layout_res['machines'], layout_res.get('conveyors', []))
    except:
        st.error("Could not load 3D layout data.")

    st.markdown("---")
    # Human Capital
    st.subheader("Human Capital — Wage-Skill Vulnerability Assessment")
    try:
        hc_res = requests.get(api_url("/api/v1/operational/human-capital/wage-skill")).json()
        df = pd.DataFrame(hc_res['nodes'])
        fig = px.scatter(df, x="skill_level", y="wage_usd_hr", size="flight_risk", color="dept", hover_name="employee_id", height=550)
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.error("Could not load workforce data.")

# ════════════════════════════════════════════════════════════════════════════  
#  2. MARKET DYNAMICS (Restored Teammate Logic)
# ════════════════════════════════════════════════════════════════════════════  
elif layer == "2. Market Dynamics":
    st.markdown('<p class="header-font">Market Dynamics & Resilience</p>', unsafe_allow_html=True)
    st.info("Quantifying non-linear economic shocks with ML and mapping hidden supply chain dependencies.")

    # ── Socio-Economic Impact Predictor ───────────────────────────────────    
    st.subheader("Firm Exit Probability — ML Ensemble Predictor")
    with st.expander("Adjust Firm Parameters & Run Prediction", expanded=True): 
        l_ratio = st.slider("Liquidity Ratio", 0.0, 2.0, 0.72)
        d_equity = st.slider("Debt-to-Equity", 0.0, 5.0, 1.8)
        turnover = st.slider("Employee Turnover", 0.0, 0.5, 0.14)
        demand = st.slider("Market Demand Trend", -1.0, 1.0, 0.22)
        if st.button("Run Exit Prediction Model", type="primary"):
            payload = {"liquidity_ratio": l_ratio, "debt_to_equity": d_equity, "employee_turnover": turnover, "market_demand_trend": demand}
            try:
                res = requests.post(api_url("/api/v1/market/predict-exit"), json=payload).json()
                st.warning(f"Exit Probability: {res['exit_probability']:.1%}")
            except:
                st.error("Prediction failed.")

    st.markdown("---")
    # ── Supply Chain Graph ────────────────────────────────────────────────    
    st.subheader("Supply Chain Topology — Temporal Production Graph (GNN Analysis)")
    try:
        graph_data = requests.get(api_url("/api/v1/operational/supply-chain/graph")).json()
        nodes = [Node(id=n['id'], label=n['label'], size=n['size'], color=n['color']) for n in graph_data['nodes']]
        edges = [Edge(source=e['source'], target=e['target'], label=e['label'], length=500) for e in graph_data['edges']]
        config = Config(width=700, height=850, directed=True)
        clicked_node_id = agraph(nodes=nodes, edges=edges, config=config)
        if clicked_node_id:
            val_res = requests.get(api_url(f"/api/v1/market/valuation/{clicked_node_id}")).json()
            st.sidebar.metric("Stability Index", val_res['stability_index'])
    except:
        st.error("Could not load graph data.")


# ════════════════════════════════════════════════════════════════════════════  
#  3. LEGAL & DISCLOSURE (Restored Teammate Logic)
# ════════════════════════════════════════════════════════════════════════════  
elif layer == "3. Legal & Disclosure":
    st.markdown('<p class="header-font">Legal & Disclosure Compliance</p>', unsafe_allow_html=True)
    st.info("Operationalizing compliance for asset transfer and data governance.")

    # Compliance Tracker
    st.subheader("License & Certification Expiry Tracker")
    try:
        comp = requests.get(api_url("/api/v1/legal/compliance/overview")).json()
        for item in comp['items']:
            urgency = item['urgency']
            st.markdown(f"""<div class='compliance-{urgency}'>
                <strong>{item['name']}</strong> — Expires: {item['expiry_date']}<br>
                <em>Notes: {item['notes']}</em>
            </div>""", unsafe_allow_html=True)
    except:
        st.error("Could not load compliance data.")