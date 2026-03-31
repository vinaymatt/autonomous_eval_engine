import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from streamlit_agraph import agraph, Node, Edge, Config
import os

api_base_url = st.secrets.get("API_BASE_URL", os.getenv("API_BASE_URL", "http://localhost:8000")).rstrip("/")


def api_url(path: str) -> str:
    return f"{api_base_url}{path}"

# Set page config for a professional look
st.set_page_config(page_title="SMM Evaluation Engine", layout="wide")

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

    # Show Digital Twin 3D Layout with IoT status
    st.markdown("---")
    st.subheader("3D Facility Layout (Live IoT Status)")
    st.write("Spatial mapping of physical assets and current operational health.")
    
    try:
        # Fetch the coordinates and status
        layout_res = requests.get(api_url("/api/v1/operational/digital-twin/layout-3d")).json()
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