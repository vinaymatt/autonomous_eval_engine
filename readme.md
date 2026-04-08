# Autonomous Enterprise Evaluation & Visualization Engine

This project is a browser-based demo pipeline designed to automate the digitization, evaluation, and transfer of **Small and Medium Manufacturing (SMM)** entities. It utilizes a three-layer architecture to transform opaque industrial assets into transparent, data-driven digital twins.

## 🚀 Quick Start

### Prerequisites

-   **Anaconda** or **Miniconda** installed on your system.
-   A terminal or command prompt (e.g., Anaconda Prompt).

### Installation

1.  **Navigate to the project root:**    
```bash
cd autonomous_eval_engine
```
    
2.  **Create the Conda environment:** This will install all necessary dependencies, including PyTorch, PyTorch Geometric, FastAPI, and Scikit-learn.    
```bash
conda env create -f environment.yml
```
    
3.  **Activate the environment:**
```bash
conda activate eval_engine_env
```

## 🩹 Required Library Patch: Disabling Graph Double-Click

By default, the `streamlit-agraph` component contains hardcoded JavaScript that forces a broken new browser tab to open when a node is double-clicked. To keep users securely on the dashboard during a demo, you must manually patch the compiled React build inside your Conda environment.

**Step 1: Locate the JavaScript file** Navigate to the `streamlit_agraph` build directory inside your Conda environment. The path will look similar to this depending on your OS and Conda installation path:

-   **Windows:** `...\miniconda3\envs\eval_engine_env\Lib\site-packages\streamlit_agraph\frontend\build\static\js`
-   **Mac/Linux:** `.../miniconda3/envs/eval_engine_env/lib/python3.10/site-packages/streamlit_agraph/frontend/build/static/js`

**Step 2: Modify the Chunk File**

1.  Open the main JavaScript chunk file (named `main.<hash>.chunk.js`) in a code editor (e.g., VS Code).
2.  Search (`Ctrl+F`) for the `doubleClick` event listener. Because the code is minified, it will look like a dense block:
    
    
    
```JavaScript
doubleClick:function(e){console.log(e.nodes);var t=function(e,t){var n,r=Object(c.a)(t);try{for(r.s();!(n=r.n()).done;){var a=n.value;if(a.id===e)return a}}catch(o){r.e(o)}finally{r.f()}}(e.nodes[0],n).div.innerHTML;t&&window.open(t)}
```
    
3.  Replace that entire `doubleClick` function block with an empty function:
    
    
```JavaScript
doubleClick:function(e){}
```
    
4.  Save the file.

**Step 3: Hard Refresh** When you run the frontend, you must perform a **Hard Refresh** (`Ctrl + F5` or `Cmd + Shift + R`) in your web browser to clear the cached JavaScript. The double-click bug will now be neutralized.

    

## 🖥️ Running the Full Demo
You need to run two processes (open two terminal tabs):

Start the FastAPI backend server using the entry point:

1. **Start the Backend (API):**
```bash
conda activate eval_engine_env
python main.py
```

2. **Start the Frontend (UI):**
In another terminal run
```bash
conda activate eval_engine_env
streamlit run frontend.py
```


The API will be available at `http://127.0.0.1:8000`. You can access the interactive documentation (Swagger UI) at `http://127.0.0.1:8000/docs`.

## 🌐 Deploying the API on Netlify

This repository is configured to deploy the **FastAPI backend** as a Netlify Python Function.

### What gets deployed

- FastAPI API endpoints from `main.py` and `api/routers/*`
- Serverless entrypoint: `netlify/functions/api.py`
- Netlify configuration: `netlify.toml`

> Note: The Streamlit UI (`frontend.py`) is not hosted by Netlify Functions. Keep it local or deploy it on a Streamlit-compatible host.

### Steps

1. Push this repository to GitHub.
2. In Netlify, create a new site from that repository.
3. Netlify should auto-detect `netlify.toml` and use:
   - Build command: `mkdir -p public && printf 'Autonomous Evaluation Engine API is live.\n' > public/index.html`
   - Publish directory: `public`
   - Functions directory: `netlify/functions`
4. Deploy.

### API base path on Netlify

The redirect config maps:

- `/api/*` -> `/.netlify/functions/api/:splat`

So your endpoint example becomes:

- `https://<your-netlify-site>.netlify.app/api/api/v1/operational/digital-twin/kpis`

## 🖼️ Assets & Images

The application uses local images for the "About Us" and "Goals" sections. To update these:

1.  Add your images to the `assets/images/` directory.
2.  The following filenames are expected:
    -   `goal_hero.jpg`: Main goal section image.
    -   `team1.jpg`, `team2.jpg`, `team3.jpg`, `team4.jpg`: Profile pictures for team members.
3.  Commit and push the images to GitHub:
    ```bash
    git add assets/images/
    git commit -m "Add team and goal images"
    git push origin main
    ```

## 🏗 Project Structure

```text
autonomous_eval_engine/
├── environment.yml          # Conda environment configuration
├── readme.md                # Project documentation and setup guide
├── main.py                  # Application entry point (FastAPI + Uvicorn)
├── api/                     # Web Layer
│   ├── __init__.py
│   └── routers/
│       ├── operational.py   # Endpoints for Digital Twin & Human Capital
│       ├── market.py        # Endpoints for ML Risk Prediction & Valuation
│       └── legal.py         # Endpoints for Legal & Compliance Frameworks
├── core/                    # Logic Layer
│   ├── __init__.py
│   ├── models/
│   │   ├── gnn_supply.py    # PyTorch GNN for Supply Chain failure prediction
│   │   └── rf_survival.py   # Random Forest for SMM exit/distress prediction
│   └── simulation/
│       └── digital_twin.py  # IoT data simulation and production logic
└── data/                    # Data Layer
    └── dummy_smm_data.json  # Mock SMM entity, graphs, and layout metadata
```


## 🛠 Core Components

### 1\. Operational Core (Digital Twin Layer)

-   **Digital Twin:** Simulates real-time IoT data and factory KPIs.
-   **Human Capital:** Analyzes workforce demographics via "Wage-Skill" scatter plots to identify high-flight-risk talent.
-   **Supply Chain:** Visualizes stakeholder graphs and identifies single-source failure points.

### 2\. Market Dynamics & Resilience Layer

-   **Socio-Economic Impact:** Uses **Random Forests** to predict firm exits and potential economic shocks.
-   **Resilience:** Deploys **Graph Neural Networks (GNNs)** on Temporal Production Graphs to learn latent dependencies between suppliers.

### 3\. Legal & Disclosure Framework

-   **Ownership Rights:** Guides through PA Title 15 and Bulk Sales regulations.
-   **Knowledge Disclosure:** Manages trade secret preservation (PA UTSA) and data breach protocols (BPINA).


## 🔧 Geek Notes

-   The GNN implementation uses **PyTorch Geometric (PyG)** to handle non-linear supplier dependencies.
-   The backend is built with **FastAPI** for high-performance asynchronous request handling, ideal for real-time digital twin simulations.

