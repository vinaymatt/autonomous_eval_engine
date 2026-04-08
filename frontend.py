import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from streamlit_agraph import agraph, Node, Edge, Config
import os
import base64

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
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ Autonomous Enterprise Evaluation & Visualization Engine")
st.markdown("---")

# Sidebar for Navigation
st.sidebar.header("Navigation")
layer = st.sidebar.radio("Select Layer", ["0. Welcome & Overview", "1. Digital Twin", "2. Market Dynamics", "3. Legal & Disclosure"])

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

# 1. OPERATIONAL CORE LAYER
elif layer == "1. Digital Twin":
    st.markdown('<p class="header-font">Digital Twin</p>', unsafe_allow_html=True)
    st.info("Constructing a precise digital replica to monitor physical assets.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p style="font-size: 24px; font-weight: bold;">Live Production KPIs</p>', unsafe_allow_html=True)
        if st.button("Fetch Live IoT Data"):
            try:
                res = requests.get(api_url("/api/v1/operational/digital-twin/kpis"), timeout=2).json()
                st.metric("Machine Utilization", f"{res['machine_utilization_pct']}%")
                st.metric("Throughput (Units/Hr)", res['production_throughput_units_per_hr'])
                if res['anomaly_detected']:
                    st.error("⚠️ Anomaly Detected in Facility Layout")
            except Exception as e:
                st.error("Could not fetch KPIs: Backend unreachable.")
    
    with col2:
        st.markdown('<p style="font-size: 24px; font-weight: bold;">Human Capital: Wage-Skill Plot</p>', unsafe_allow_html=True)
        try:
            res = requests.get(api_url("/api/v1/operational/human-capital/wage-skill"), timeout=2).json()
            df = pd.DataFrame(res['nodes'])
            fig = px.scatter(df, x="skill_level", y="wage_usd_hr", size="flight_risk", 
                             color="flight_risk", hover_name="employee_id",
                             title="Workforce Vulnerability Assessment")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error("Could not fetch Workforce data.")

    # Show Digital Twin 3D Layout with IoT status
    st.markdown("---")
    st.markdown('<p style="font-size: 24px; font-weight: bold;">3D Facility Layout (Live IoT Status)</p>', unsafe_allow_html=True)
    st.markdown('<p class="large-font">Spatial mapping of physical assets and current operational health.</p>', unsafe_allow_html=True)
    
    try:
        # Fetch the coordinates and status
        layout_res = requests.get(api_url("/api/v1/operational/digital-twin/layout-3d"), timeout=2).json()
        df_3d = pd.DataFrame(layout_res['machines'])

        # Hardcode the colors so "Downtime" is always red, etc.
        status_colors = {"Active": "#2ca02c", "Downtime": "#d62728", "Maintenance": "#ff7f0e"}

        # Generate the 3D Scatter Plot
        fig_3d = px.scatter_3d(
            df_3d, x="x", y="y", z="z", 
            color="status", 
            hover_name="id", 
            hover_data=["type", "efficiency"],
            color_discrete_map=status_colors
        )
        
        # Geek tweak: Make the markers look like big square machines, and flatten the Z-axis
        fig_3d.update_traces(marker=dict(size=15, symbol='square')) 
        
        fig_3d.update_layout(
            height=700,                 # 1. Increases the vertical canvas size
            dragmode="turntable",       # 2. Locks Z-axis UP to prevent upside-down flipping
            scene=dict(
                zaxis=dict(range=[-1, 5], showbackground=False, showticklabels=False, title=""),
                xaxis=dict(title="Factory X-Axis (meters)"),
                yaxis=dict(title="Factory Y-Axis (meters)")
            ),
            margin=dict(l=0, r=0, b=0, t=0) # Keeps the chart flush with the container
        )     
        # Create columns to handle the width (10% | 80% | 10%)
        spacer_left, chart_col, spacer_right = st.columns([1, 8, 1])
        with chart_col:
            # 2. Render the chart inside the middle 80% column
            st.plotly_chart(
                fig_3d, 
                use_container_width=True,  # Tells Plotly to fill the 80% column
                config={'scrollZoom': True} 
            )
        
    except Exception as e:
        st.error(f"Could not load 3D layout data: {e}")

# 2. MARKET DYNAMICS LAYER
elif layer == "2. Market Dynamics":
    st.markdown('<p class="header-font">Market Dynamics & Resilience</p>', unsafe_allow_html=True)
    st.info("Quantifying non-linear economic shocks using Machine Learning.")
    
    # --- Module 2.1: Socio-Economic Impact ---
    with st.expander("Run Socio-Economic Impact Assessment"):
        l_ratio = st.slider("Liquidity Ratio", 0.0, 1.0, 0.5)
        d_equity = st.slider("Debt-to-Equity", 0.0, 5.0, 1.2)
        turnover = st.slider("Employee Turnover", 0.0, 1.0, 0.2)
        demand = st.slider("Market Demand Trend", -1.0, 1.0, 0.1)
        
        if st.button("Predict Exit Probability"):
            try:
                payload = {
                    "liquidity_ratio": l_ratio,
                    "debt_to_equity": d_equity,
                    "employee_turnover": turnover,
                    "market_demand_trend": demand
                }
                res = requests.post(api_url("/api/v1/market/predict-exit"), json=payload, timeout=2).json()
                st.warning(f"Exit Probability: {res['exit_probability']:.2%}")
                st.write(f"**Recommendation:** {res['recommendation']}")
            except Exception as e:
                st.error("Prediction service unavailable.")

    st.markdown("---")

    # --- Module 2.3: Supply Chain Resilience (FIXED INDENTATION) ---
    st.markdown('<p style="font-size: 24px; font-weight: bold;">Temporal Production Graph (GNN Analysis)</p>', unsafe_allow_html=True)
    st.markdown('<p class="large-font">Visualizing latent dependencies and hidden supplier failures.</p>', unsafe_allow_html=True)
    
    try:
        graph_data = requests.get(api_url("/api/v1/operational/supply-chain/graph"), timeout=2).json()

        nodes = [Node(id=n['id'], label=n['label'], size=n['size'], color=n['color']) for n in graph_data['nodes']]
        edges = [Edge(source=e['source'], target=e['target'], label=e['label'], length=300) for e in graph_data['edges']]
        # INJECT a custom physics dictionary to tame the rubber-band effect
        custom_physics = {
            "solver": "repulsion",
            "repulsion": {
                "nodeDistance": 200,      # Pushes nodes away from each other
                "springLength": 350,      # Stretches the resting length of the edges
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
    st.markdown('<p class="header-font">Legal & Disclosure Compliance</p>', unsafe_allow_html=True)
    st.info("Operationalizing compliance for asset transfer.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p style="font-size: 24px; font-weight: bold;">Ownership Rights (PA Title 15)</p>', unsafe_allow_html=True)
        try:
            res = requests.get(api_url("/api/v1/legal/compliance/ownership-rights"), timeout=2).json()
            st.markdown(f'<p class="large-font"><b>Regulation:</b> {res["regulation"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="large-font"><b>Status:</b> {res["liability_status"]}</p>', unsafe_allow_html=True)
        except:
            st.error("Could not fetch legal data.")
        
    with col2:
        st.markdown('<p style="font-size: 24px; font-weight: bold;">Knowledge Disclosure (PA UTSA)</p>', unsafe_allow_html=True)
        try:
            res = requests.get(api_url("/api/v1/legal/compliance/knowledge-disclosure"), timeout=2).json()
            st.markdown(f'<p class="large-font"><b>CAD Encryption:</b> {"✅ Active" if res["cad_encryption_status"] else "❌ Inactive"}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="large-font"><b>Compliance:</b> {"Verified" if res["is_compliant"] else "Attention Required"}</p>', unsafe_allow_html=True)
        except:
            st.error("Could not fetch disclosure data.")