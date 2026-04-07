from fastapi import APIRouter
from core.simulation.digital_twin import DigitalTwinSimulator
from datetime import date

router = APIRouter()
simulator = DigitalTwinSimulator(facility_id="SMM-1247")
TODAY = date(2026, 4, 7)


@router.get("/digital-twin/kpis")
def get_digital_twin_kpis():
    return simulator.fetch_live_kpis()


@router.get("/company-profile")
def get_company_profile():
    return {
        "id": "SMM-1247",
        "name": "Hartwell Precision Manufacturing, Inc.",
        "dba": "Hartwell Precision",
        "founded": 1978,
        "owner": "Robert E. Hartwell",
        "owner_age": 72,
        "succession_status": "No identified successor — owner plans full retirement by Q4 2027",
        "address": "1840 Union Blvd, Allentown, PA 18109",
        "county": "Lehigh",
        "region": "Lehigh Valley",
        "naics": "332710 — Machine Shops",
        "employees": 47,
        "facility_sqft": 28000,
        "annual_revenue_usd": 8200000,
        "ebitda_usd": 1148000,
        "ebitda_margin_pct": 14.0,
        "certifications": [
            "ISO 9001:2015",
            "AS9100D (Aerospace Quality)",
            "ITAR Registered",
            "NADCAP (pending)",
        ],
        "key_markets": [
            "Defense / Aerospace",
            "Medical Devices",
            "Automotive / Drivetrain",
            "Industrial Equipment",
        ],
    }


@router.get("/human-capital/wage-skill")
def get_wage_skill_demographics():
    return {
        "nodes": [
            # Management
            {"employee_id": "MGT-001", "role": "Plant Manager", "name": "D. Kowalski", "years_tenure": 22, "skill_level": 9.4, "wage_usd_hr": 45.00, "flight_risk": 0.68, "dept": "Management"},
            {"employee_id": "MGT-002", "role": "Quality Manager", "name": "L. Chen", "years_tenure": 11, "skill_level": 9.1, "wage_usd_hr": 42.00, "flight_risk": 0.25, "dept": "Management"},
            {"employee_id": "MGT-003", "role": "Shop Foreman", "name": "M. Reyes", "years_tenure": 18, "skill_level": 8.8, "wage_usd_hr": 38.50, "flight_risk": 0.72, "dept": "Management"},
            # Engineering
            {"employee_id": "ENG-001", "role": "Sr. CNC Programmer", "name": "T. Novak", "years_tenure": 15, "skill_level": 9.6, "wage_usd_hr": 38.00, "flight_risk": 0.81, "dept": "Engineering"},
            {"employee_id": "ENG-002", "role": "CNC Programmer", "name": "J. Park", "years_tenure": 6, "skill_level": 8.2, "wage_usd_hr": 34.00, "flight_risk": 0.45, "dept": "Engineering"},
            {"employee_id": "ENG-003", "role": "Process Engineer", "name": "A. Patel", "years_tenure": 4, "skill_level": 8.5, "wage_usd_hr": 36.50, "flight_risk": 0.38, "dept": "Engineering"},
            {"employee_id": "ENG-004", "role": "Jr. CNC Programmer", "name": "R. Kim", "years_tenure": 2, "skill_level": 6.8, "wage_usd_hr": 32.00, "flight_risk": 0.22, "dept": "Engineering"},
            # Senior CNC Operators
            {"employee_id": "OPS-001", "role": "Sr. CNC Operator", "name": "G. Hartwell", "years_tenure": 28, "skill_level": 9.2, "wage_usd_hr": 32.00, "flight_risk": 0.88, "dept": "Operations"},
            {"employee_id": "OPS-002", "role": "Sr. CNC Operator", "name": "B. Zielinski", "years_tenure": 20, "skill_level": 8.9, "wage_usd_hr": 31.00, "flight_risk": 0.75, "dept": "Operations"},
            {"employee_id": "OPS-003", "role": "Sr. CNC Operator", "name": "W. Torres", "years_tenure": 16, "skill_level": 8.6, "wage_usd_hr": 30.00, "flight_risk": 0.60, "dept": "Operations"},
            {"employee_id": "OPS-004", "role": "Sr. CNC Operator", "name": "K. Mueller", "years_tenure": 14, "skill_level": 8.4, "wage_usd_hr": 29.50, "flight_risk": 0.55, "dept": "Operations"},
            {"employee_id": "OPS-005", "role": "Sr. CNC Operator", "name": "F. DeLuca", "years_tenure": 12, "skill_level": 8.1, "wage_usd_hr": 28.50, "flight_risk": 0.50, "dept": "Operations"},
            {"employee_id": "OPS-006", "role": "Sr. CNC Operator", "name": "P. Okafor", "years_tenure": 10, "skill_level": 7.9, "wage_usd_hr": 27.50, "flight_risk": 0.42, "dept": "Operations"},
            # Junior CNC Operators
            {"employee_id": "OPS-007", "role": "CNC Operator", "name": "S. Vega", "years_tenure": 5, "skill_level": 6.5, "wage_usd_hr": 23.00, "flight_risk": 0.30, "dept": "Operations"},
            {"employee_id": "OPS-008", "role": "CNC Operator", "name": "D. Yoder", "years_tenure": 4, "skill_level": 6.2, "wage_usd_hr": 22.00, "flight_risk": 0.28, "dept": "Operations"},
            {"employee_id": "OPS-009", "role": "CNC Operator", "name": "H. Tran", "years_tenure": 3, "skill_level": 5.8, "wage_usd_hr": 21.00, "flight_risk": 0.25, "dept": "Operations"},
            {"employee_id": "OPS-010", "role": "CNC Operator", "name": "C. Rivera", "years_tenure": 3, "skill_level": 5.5, "wage_usd_hr": 20.50, "flight_risk": 0.22, "dept": "Operations"},
            {"employee_id": "OPS-011", "role": "CNC Operator", "name": "E. Wojcik", "years_tenure": 2, "skill_level": 5.2, "wage_usd_hr": 19.50, "flight_risk": 0.20, "dept": "Operations"},
            {"employee_id": "OPS-012", "role": "CNC Operator", "name": "L. Huang", "years_tenure": 1, "skill_level": 4.8, "wage_usd_hr": 19.00, "flight_risk": 0.18, "dept": "Operations"},
            {"employee_id": "OPS-013", "role": "CNC Operator", "name": "N. Brooks", "years_tenure": 1, "skill_level": 4.5, "wage_usd_hr": 18.50, "flight_risk": 0.15, "dept": "Operations"},
            {"employee_id": "OPS-014", "role": "Apprentice Machinist", "name": "J. Ortiz", "years_tenure": 0.5, "skill_level": 3.2, "wage_usd_hr": 17.50, "flight_risk": 0.10, "dept": "Operations"},
            # Manual Machinists
            {"employee_id": "MAN-001", "role": "Manual Machinist", "name": "R. Stefanik", "years_tenure": 31, "skill_level": 9.0, "wage_usd_hr": 34.00, "flight_risk": 0.85, "dept": "Operations"},
            {"employee_id": "MAN-002", "role": "Manual Machinist", "name": "V. Popov", "years_tenure": 19, "skill_level": 8.3, "wage_usd_hr": 30.00, "flight_risk": 0.62, "dept": "Operations"},
            {"employee_id": "MAN-003", "role": "Manual Machinist", "name": "A. Snyder", "years_tenure": 25, "skill_level": 8.7, "wage_usd_hr": 32.00, "flight_risk": 0.78, "dept": "Operations"},
            {"employee_id": "MAN-004", "role": "Manual Machinist", "name": "T. Washington", "years_tenure": 8, "skill_level": 7.1, "wage_usd_hr": 28.00, "flight_risk": 0.35, "dept": "Operations"},
            # Inspection / QC
            {"employee_id": "QC-001", "role": "CMM Operator", "name": "M. Fischer", "years_tenure": 9, "skill_level": 8.0, "wage_usd_hr": 28.00, "flight_risk": 0.40, "dept": "Quality"},
            {"employee_id": "QC-002", "role": "QC Inspector", "name": "D. Alvarez", "years_tenure": 7, "skill_level": 7.2, "wage_usd_hr": 26.00, "flight_risk": 0.32, "dept": "Quality"},
            {"employee_id": "QC-003", "role": "QC Inspector", "name": "S. Bennett", "years_tenure": 3, "skill_level": 5.9, "wage_usd_hr": 24.00, "flight_risk": 0.20, "dept": "Quality"},
            # Maintenance
            {"employee_id": "MNT-001", "role": "Maintenance Tech", "name": "J. Kline", "years_tenure": 17, "skill_level": 8.5, "wage_usd_hr": 30.00, "flight_risk": 0.58, "dept": "Maintenance"},
            {"employee_id": "MNT-002", "role": "Maintenance Tech", "name": "C. Nguyen", "years_tenure": 6, "skill_level": 7.0, "wage_usd_hr": 26.50, "flight_risk": 0.30, "dept": "Maintenance"},
            # Shipping / Receiving
            {"employee_id": "LOG-001", "role": "Shipping Lead", "name": "R. Gonzalez", "years_tenure": 11, "skill_level": 6.0, "wage_usd_hr": 20.00, "flight_risk": 0.35, "dept": "Logistics"},
            {"employee_id": "LOG-002", "role": "Shipping/Receiving", "name": "T. Hayes", "years_tenure": 4, "skill_level": 4.5, "wage_usd_hr": 18.00, "flight_risk": 0.18, "dept": "Logistics"},
            {"employee_id": "LOG-003", "role": "Shipping/Receiving", "name": "A. Morales", "years_tenure": 2, "skill_level": 4.0, "wage_usd_hr": 17.50, "flight_risk": 0.15, "dept": "Logistics"},
            # Office / Admin
            {"employee_id": "ADM-001", "role": "Office Manager", "name": "P. Hartwell", "years_tenure": 30, "skill_level": 7.5, "wage_usd_hr": 25.00, "flight_risk": 0.90, "dept": "Admin"},
            {"employee_id": "ADM-002", "role": "Bookkeeper", "name": "N. Schmidt", "years_tenure": 12, "skill_level": 6.8, "wage_usd_hr": 22.00, "flight_risk": 0.48, "dept": "Admin"},
            {"employee_id": "ADM-003", "role": "Receptionist", "name": "K. Williams", "years_tenure": 3, "skill_level": 4.2, "wage_usd_hr": 18.00, "flight_risk": 0.12, "dept": "Admin"},
            {"employee_id": "ADM-004", "role": "Purchasing Coordinator", "name": "L. Becker", "years_tenure": 8, "skill_level": 7.0, "wage_usd_hr": 23.50, "flight_risk": 0.40, "dept": "Admin"},
            # Sales
            {"employee_id": "SLS-001", "role": "Sales Manager", "name": "B. Crawford", "years_tenure": 14, "skill_level": 8.0, "wage_usd_hr": 35.00, "flight_risk": 0.70, "dept": "Sales"},
            {"employee_id": "SLS-002", "role": "Account Manager", "name": "M. Perez", "years_tenure": 5, "skill_level": 6.5, "wage_usd_hr": 30.00, "flight_risk": 0.38, "dept": "Sales"},
        ],
        "summary": {
            "total_employees": 47,
            "avg_tenure_years": 10.3,
            "avg_wage_usd_hr": 26.84,
            "high_flight_risk_count": 12,
            "employees_over_55": 8,
            "annual_payroll_usd": 2680000,
            "employees_needing_govt_assistance_if_shutdown": 19,
        },
    }


@router.get("/supply-chain/graph")
def get_supply_chain_graph():
    return {
        "nodes": [
            # === CORE FIRM ===
            {"id": "SMM-1247", "label": "Hartwell Precision Mfg.", "color": "#1a73e8", "size": 40, "group": "core", "detail": "$8.2M rev · 47 employees · Allentown, PA"},

            # === TIER 1 SUPPLIERS (Raw Materials) ===
            {"id": "SUP-RYERSON", "label": "Ryerson Steel", "color": "#2e7d32", "size": 22, "group": "supplier_t1", "detail": "Carbon & alloy steel bar stock · Chicago, IL"},
            {"id": "SUP-ALCOA", "label": "Alcoa Corporation", "color": "#2e7d32", "size": 22, "group": "supplier_t1", "detail": "Aluminum billets (6061-T6, 7075) · Pittsburgh, PA"},
            {"id": "SUP-TITANIUM", "label": "Titanium Industries", "color": "#c62828", "size": 24, "group": "supplier_t1_critical", "detail": "Ti-6Al-4V aerospace grade · Rockaway, NJ · SINGLE SOURCE"},
            {"id": "SUP-SPECIALTY", "label": "Specialty Steel Supply", "color": "#2e7d32", "size": 18, "group": "supplier_t1", "detail": "Stainless 304/316L, Inconel · Reading, PA"},

            # === TIER 1 SUPPLIERS (Tooling & Consumables) ===
            {"id": "SUP-SANDVIK", "label": "Sandvik Coromant", "color": "#1565c0", "size": 20, "group": "supplier_t1", "detail": "Cutting tools & carbide inserts · Fair Lawn, NJ"},
            {"id": "SUP-KENNAMETAL", "label": "Kennametal", "color": "#1565c0", "size": 20, "group": "supplier_t1", "detail": "End mills, drills, taps · Latrobe, PA"},
            {"id": "SUP-MCMASTER", "label": "McMaster-Carr", "color": "#1565c0", "size": 18, "group": "supplier_t1", "detail": "Fixtures, hardware, consumables · Robbinsville, NJ"},

            # === TIER 1 SUPPLIERS (Services & Chemicals) ===
            {"id": "SUP-HOUGHTON", "label": "Quaker Houghton", "color": "#6a1b9a", "size": 18, "group": "supplier_t1", "detail": "Metalworking fluids & coolants · Conshohocken, PA"},
            {"id": "SUP-LINDE", "label": "Linde Gas", "color": "#6a1b9a", "size": 16, "group": "supplier_t1", "detail": "Argon, nitrogen, welding gases · Bethlehem, PA"},
            {"id": "SUP-ELECTROCOAT", "label": "Electro-Coatings Inc.", "color": "#c62828", "size": 20, "group": "supplier_t1_critical", "detail": "Hard chrome & anodizing · Lancaster, PA · SINGLE SOURCE for Mil-Spec"},
            {"id": "SUP-ANOPLATE", "label": "Anoplate Corporation", "color": "#6a1b9a", "size": 18, "group": "supplier_t1", "detail": "Cadmium & nickel plating · Syracuse, NY"},
            {"id": "SUP-HEATTREAT", "label": "Bodycote Thermal", "color": "#c62828", "size": 20, "group": "supplier_t1_critical", "detail": "Heat treat & HIP processing · Reading, PA · SINGLE SOURCE for NADCAP HT"},

            # === TIER 1 SUPPLIERS (Logistics & Packaging) ===
            {"id": "SUP-PCA", "label": "Packaging Corp America", "color": "#795548", "size": 14, "group": "supplier_t1", "detail": "Shipping crates & VCI packaging · Allentown, PA"},
            {"id": "SUP-FEDEX", "label": "FedEx Freight", "color": "#795548", "size": 14, "group": "supplier_t1", "detail": "LTL & expedited freight · Regional"},

            # === TIER 2 SUPPLIERS (upstream of Tier 1) ===
            {"id": "SUP-USSTEEL", "label": "U.S. Steel", "color": "#9e9e9e", "size": 16, "group": "supplier_t2", "detail": "Hot-rolled coil to Ryerson · Pittsburgh, PA"},
            {"id": "SUP-TIMET", "label": "TIMET (PCC)", "color": "#9e9e9e", "size": 16, "group": "supplier_t2", "detail": "Ti sponge & ingot to Titanium Industries · Henderson, NV"},
            {"id": "SUP-WOLFRAM", "label": "Wolfram Bergbau", "color": "#9e9e9e", "size": 14, "group": "supplier_t2", "detail": "Tungsten carbide powder to Kennametal · Austria"},

            # === DOWNSTREAM CUSTOMERS ===
            {"id": "CUST-BAE", "label": "BAE Systems", "color": "#e65100", "size": 26, "group": "customer", "detail": "Turret components & armor brackets · York, PA · 28% of revenue"},
            {"id": "CUST-STRYKER", "label": "Stryker Corp.", "color": "#e65100", "size": 22, "group": "customer", "detail": "Surgical instrument housings · Mahwah, NJ · 18% of revenue"},
            {"id": "CUST-DANA", "label": "Dana Incorporated", "color": "#e65100", "size": 20, "group": "customer", "detail": "Drivetrain components · Maumee, OH · 14% of revenue"},
            {"id": "CUST-GDLS", "label": "General Dynamics", "color": "#e65100", "size": 22, "group": "customer", "detail": "Weapons system housings · Scranton, PA · 16% of revenue"},
            {"id": "CUST-LOCKHEED", "label": "Lockheed Martin", "color": "#e65100", "size": 20, "group": "customer", "detail": "Aerospace structural brackets · Moorestown, NJ · 10% of revenue"},
            {"id": "CUST-PARKER", "label": "Parker Hannifin", "color": "#ff8f00", "size": 18, "group": "customer", "detail": "Hydraulic valve bodies · Elyria, OH · 7% of revenue"},
            {"id": "CUST-REGIONAL", "label": "Regional Job Shops (5)", "color": "#ff8f00", "size": 16, "group": "customer", "detail": "Overflow & specialty work · Lehigh Valley · 5% of revenue"},
            {"id": "CUST-CURTISS", "label": "Curtiss-Wright", "color": "#ff8f00", "size": 18, "group": "customer", "detail": "Nuclear valve components · Cheswick, PA · 2% of revenue"},
        ],
        "edges": [
            # Tier 2 → Tier 1
            {"source": "SUP-USSTEEL", "target": "SUP-RYERSON", "label": "Hot-rolled coil"},
            {"source": "SUP-TIMET", "target": "SUP-TITANIUM", "label": "Ti sponge & ingot"},
            {"source": "SUP-WOLFRAM", "target": "SUP-KENNAMETAL", "label": "WC powder"},

            # Tier 1 → Core (Raw Materials)
            {"source": "SUP-RYERSON", "target": "SMM-1247", "label": "Steel bar · 10d lead"},
            {"source": "SUP-ALCOA", "target": "SMM-1247", "label": "Al billet · 14d lead"},
            {"source": "SUP-TITANIUM", "target": "SMM-1247", "label": "Ti-6Al-4V · 42d lead ⚠"},
            {"source": "SUP-SPECIALTY", "target": "SMM-1247", "label": "SS/Inconel · 18d lead"},

            # Tier 1 → Core (Tooling)
            {"source": "SUP-SANDVIK", "target": "SMM-1247", "label": "Inserts · 5d lead"},
            {"source": "SUP-KENNAMETAL", "target": "SMM-1247", "label": "End mills · 7d lead"},
            {"source": "SUP-MCMASTER", "target": "SMM-1247", "label": "Fixtures · 2d lead"},

            # Tier 1 → Core (Services)
            {"source": "SUP-HOUGHTON", "target": "SMM-1247", "label": "Coolant · 8d lead"},
            {"source": "SUP-LINDE", "target": "SMM-1247", "label": "Gas delivery · 3d lead"},
            {"source": "SUP-ELECTROCOAT", "target": "SMM-1247", "label": "Anodize/Chrome · 21d lead ⚠"},
            {"source": "SUP-ANOPLATE", "target": "SMM-1247", "label": "Plating · 18d lead"},
            {"source": "SUP-HEATTREAT", "target": "SMM-1247", "label": "Heat treat · 14d lead ⚠"},
            {"source": "SUP-PCA", "target": "SMM-1247", "label": "Packaging · 4d lead"},
            {"source": "SUP-FEDEX", "target": "SMM-1247", "label": "Freight services"},

            # Core → Customers
            {"source": "SMM-1247", "target": "CUST-BAE", "label": "Turret parts · $2.3M/yr"},
            {"source": "SMM-1247", "target": "CUST-STRYKER", "label": "Surgical housings · $1.5M/yr"},
            {"source": "SMM-1247", "target": "CUST-DANA", "label": "Drivetrain · $1.1M/yr"},
            {"source": "SMM-1247", "target": "CUST-GDLS", "label": "Weapons sys. · $1.3M/yr"},
            {"source": "SMM-1247", "target": "CUST-LOCKHEED", "label": "Aero brackets · $820K/yr"},
            {"source": "SMM-1247", "target": "CUST-PARKER", "label": "Valve bodies · $574K/yr"},
            {"source": "SMM-1247", "target": "CUST-REGIONAL", "label": "Overflow · $410K/yr"},
            {"source": "SMM-1247", "target": "CUST-CURTISS", "label": "Nuclear valves · $164K/yr"},
        ],
        "gnn_insights": [
            {
                "severity": "critical",
                "message": "Titanium Industries is a single source of failure for Ti-6Al-4V aerospace-grade material. Loss of this supplier would halt all BAE Systems and Lockheed Martin production lines within 6 weeks.",
                "affected_revenue_usd": 3120000,
            },
            {
                "severity": "critical",
                "message": "Electro-Coatings Inc. is the only Mil-Spec qualified anodizer within 200 miles. Lead time already at 21 days and trending upward. Alternative qualification would take 9-12 months.",
                "affected_revenue_usd": 2300000,
            },
            {
                "severity": "high",
                "message": "Bodycote Thermal Processing is the sole NADCAP-certified heat treat provider for Hartwell. Any disruption would ground all AS9100D aerospace work.",
                "affected_revenue_usd": 3120000,
            },
            {
                "severity": "medium",
                "message": "BAE Systems represents 28% of total revenue — customer concentration risk exceeds recommended 20% threshold per SBA guidelines.",
                "affected_revenue_usd": 2300000,
            },
            {
                "severity": "low",
                "message": "Wolfram Bergbau (Austria) exposes Kennametal's tungsten carbide supply to EU export control changes. Second-order risk to Hartwell tooling costs.",
                "affected_revenue_usd": 0,
            },
        ],
    }


@router.get("/digital-twin/layout-3d")
def get_3d_layout():
    return {
        "machines": [
            # CNC Milling Centers
            {"id": "Haas_VF4SS_01", "type": "Milling", "x": 6, "y": 6, "z": 0, "status": "Active", "efficiency": 0.94, "detail": "Haas VF-4SS · 5-axis · 12,000 RPM · Installed 2019"},
            {"id": "Haas_VF4SS_02", "type": "Milling", "x": 12, "y": 6, "z": 0, "status": "Active", "efficiency": 0.91, "detail": "Haas VF-4SS · 5-axis · 12,000 RPM · Installed 2019"},
            {"id": "Haas_VF2_01", "type": "Milling", "x": 6, "y": 12, "z": 0, "status": "Maintenance", "efficiency": 0.0, "detail": "Haas VF-2 · 3-axis · Spindle bearing replacement in progress"},
            {"id": "DMG_NHX4000", "type": "Milling", "x": 12, "y": 12, "z": 0, "status": "Active", "efficiency": 0.88, "detail": "DMG Mori NHX 4000 · Horizontal · Pallet changer · Installed 2021"},
            # CNC Lathes
            {"id": "DMG_NLX2500_01", "type": "Turning", "x": 24, "y": 6, "z": 0, "status": "Active", "efficiency": 0.93, "detail": "DMG Mori NLX 2500/700 · Live tooling · Installed 2020"},
            {"id": "DMG_NLX2500_02", "type": "Turning", "x": 30, "y": 6, "z": 0, "status": "Active", "efficiency": 0.89, "detail": "DMG Mori NLX 2500/700 · Live tooling · Installed 2020"},
            {"id": "Mazak_QT250", "type": "Turning", "x": 24, "y": 12, "z": 0, "status": "Downtime", "efficiency": 0.0, "detail": "Mazak Quick Turn 250M · Awaiting Fanuc servo motor (on backorder 6 wks)"},
            # Cutting
            {"id": "Trumpf_TL3030", "type": "Cutting", "x": 6, "y": 24, "z": 0, "status": "Active", "efficiency": 0.92, "detail": "Trumpf TruLaser 3030 · 6kW fiber · Sheet capacity 60x120\" · Installed 2018"},
            {"id": "Amada_HRB", "type": "Cutting", "x": 12, "y": 24, "z": 0, "status": "Active", "efficiency": 0.87, "detail": "Amada HRB 1003 · 100-ton press brake · 10' bed · Installed 2015"},
            # Inspection
            {"id": "Mitutoyo_CMM", "type": "Inspection", "x": 30, "y": 24, "z": 0, "status": "Active", "efficiency": 0.98, "detail": "Mitutoyo Crysta-Apex S · 0.0001\" accuracy · Climate-controlled enclosure"},
            {"id": "Keyence_Vision", "type": "Inspection", "x": 30, "y": 18, "z": 0, "status": "Active", "efficiency": 0.96, "detail": "Keyence IM-8000 · Optical comparator · Automated inspection"},
            # Manual / Grinding
            {"id": "Bridgeport_01", "type": "Milling", "x": 18, "y": 24, "z": 0, "status": "Active", "efficiency": 0.78, "detail": "Bridgeport Series I · Manual mill · Prototype & one-offs"},
            {"id": "Okamoto_Grinder", "type": "Assembly", "x": 24, "y": 24, "z": 0, "status": "Active", "efficiency": 0.85, "detail": "Okamoto ACC-6-18DX · Surface grinder · 0.0002\" flatness"},
            # Assembly & Deburring
            {"id": "Assembly_Bench", "type": "Assembly", "x": 18, "y": 16, "z": 0, "status": "Active", "efficiency": 0.90, "detail": "Assembly station · Torque-controlled tools · Kitting area"},
            {"id": "Deburr_Station", "type": "Assembly", "x": 18, "y": 20, "z": 0, "status": "Active", "efficiency": 0.82, "detail": "Deburring & tumbling station · Vibratory finisher"},
        ],
        "conveyors": [
            {"from": [14, 6], "to": [22, 6]},
            {"from": [14, 12], "to": [22, 12]},
            {"from": [14, 24], "to": [16, 24]},
            {"from": [20, 24], "to": [22, 24]},
            {"from": [6, 14], "to": [6, 22]},
            {"from": [30, 14], "to": [30, 22]},
            {"from": [18, 14], "to": [18, 22]},
        ],
    }


# ── Health Index Endpoints ──────────────────────────────────────────────────

@router.get("/health-index/internal")
def get_internal_health_index():
    """
    Composite health index for internal assets: machinery condition, workforce
    stability, process capability, and facility infrastructure.
    """
    machines = [
        {
            "id": "Haas_VF4SS_01",
            "name": "Haas VF-4SS #1",
            "category": "CNC Vertical Mill",
            "installed": "2019-03",
            "age_years": 7.1,
            "hours_run": 18420,
            "hours_to_next_overhaul": 6580,
            "condition_score": 0.87,
            "maintenance_compliance_pct": 96,
            "mtbf_hours": 1240,
            "mttr_hours": 3.2,
            "replacement_cost_usd": 285000,
            "current_book_value_usd": 142000,
            "health_factors": [
                {"factor": "Spindle bearing wear", "status": "nominal", "detail": "Last replaced Feb 2025, ~6,000 hrs remaining"},
                {"factor": "Ballscrew backlash", "status": "nominal", "detail": "0.0003\" measured, threshold 0.001\""},
                {"factor": "Coolant system", "status": "nominal", "detail": "Quaker Houghton Hocut 4000 — fluid life OK"},
            ],
        },
        {
            "id": "Haas_VF4SS_02",
            "name": "Haas VF-4SS #2",
            "category": "CNC Vertical Mill",
            "installed": "2019-03",
            "age_years": 7.1,
            "hours_run": 19100,
            "hours_to_next_overhaul": 5900,
            "condition_score": 0.82,
            "maintenance_compliance_pct": 93,
            "mtbf_hours": 1080,
            "mttr_hours": 4.1,
            "replacement_cost_usd": 285000,
            "current_book_value_usd": 138000,
            "health_factors": [
                {"factor": "Spindle vibration", "status": "warning", "detail": "Vibration trending upward — bearing wear pattern detected, ~3,000 hrs to failure"},
                {"factor": "Ballscrew backlash", "status": "nominal", "detail": "0.0005\" measured, within spec"},
                {"factor": "Way cover", "status": "warning", "detail": "Minor chip intrusion — cover seal degrading"},
            ],
        },
        {
            "id": "Haas_VF2_01",
            "name": "Haas VF-2",
            "category": "CNC Vertical Mill",
            "installed": "2014-06",
            "age_years": 11.8,
            "hours_run": 34200,
            "hours_to_next_overhaul": 800,
            "condition_score": 0.35,
            "maintenance_compliance_pct": 78,
            "mtbf_hours": 480,
            "mttr_hours": 8.5,
            "replacement_cost_usd": 165000,
            "current_book_value_usd": 28000,
            "health_factors": [
                {"factor": "Spindle bearing", "status": "critical", "detail": "ACTIVE: Bearing replacement in progress — 2 weeks downtime est."},
                {"factor": "Control unit", "status": "warning", "detail": "Haas NGC controller — intermittent fault codes, board aging"},
                {"factor": "Hydraulic system", "status": "nominal", "detail": "Pressure stable at 725 PSI"},
            ],
        },
        {
            "id": "DMG_NHX4000",
            "name": "DMG Mori NHX 4000",
            "category": "CNC Horizontal Mill",
            "installed": "2021-09",
            "age_years": 4.6,
            "hours_run": 11800,
            "hours_to_next_overhaul": 13200,
            "condition_score": 0.93,
            "maintenance_compliance_pct": 99,
            "mtbf_hours": 2100,
            "mttr_hours": 2.0,
            "replacement_cost_usd": 420000,
            "current_book_value_usd": 310000,
            "health_factors": [
                {"factor": "Pallet changer", "status": "nominal", "detail": "Cycle count 24,600 — rated for 500,000"},
                {"factor": "Spindle", "status": "nominal", "detail": "15,000 RPM — no thermal drift detected"},
                {"factor": "Coolant through spindle", "status": "nominal", "detail": "Pressure: 1,000 PSI — filter replaced March 2026"},
            ],
        },
        {
            "id": "DMG_NLX2500_01",
            "name": "DMG Mori NLX 2500 #1",
            "category": "CNC Lathe",
            "installed": "2020-01",
            "age_years": 6.3,
            "hours_run": 16400,
            "hours_to_next_overhaul": 8600,
            "condition_score": 0.88,
            "maintenance_compliance_pct": 95,
            "mtbf_hours": 1350,
            "mttr_hours": 3.0,
            "replacement_cost_usd": 340000,
            "current_book_value_usd": 204000,
            "health_factors": [
                {"factor": "Chuck accuracy", "status": "nominal", "detail": "TIR 0.0002\" — within AS9100D spec"},
                {"factor": "Turret indexing", "status": "nominal", "detail": "12-station turret, indexing time 0.15s"},
                {"factor": "Tailstock", "status": "nominal", "detail": "Quill runout 0.0001\""},
            ],
        },
        {
            "id": "DMG_NLX2500_02",
            "name": "DMG Mori NLX 2500 #2",
            "category": "CNC Lathe",
            "installed": "2020-01",
            "age_years": 6.3,
            "hours_run": 15800,
            "hours_to_next_overhaul": 9200,
            "condition_score": 0.86,
            "maintenance_compliance_pct": 94,
            "mtbf_hours": 1280,
            "mttr_hours": 3.5,
            "replacement_cost_usd": 340000,
            "current_book_value_usd": 198000,
            "health_factors": [
                {"factor": "Chuck accuracy", "status": "nominal", "detail": "TIR 0.0003\" — within spec"},
                {"factor": "Turret indexing", "status": "warning", "detail": "Slight hesitation on station 7 — solenoid may need replacement"},
                {"factor": "Chip conveyor", "status": "nominal", "detail": "Operating normally"},
            ],
        },
        {
            "id": "Mazak_QT250",
            "name": "Mazak Quick Turn 250M",
            "category": "CNC Lathe",
            "installed": "2016-11",
            "age_years": 9.4,
            "hours_run": 28100,
            "hours_to_next_overhaul": 1900,
            "condition_score": 0.22,
            "maintenance_compliance_pct": 68,
            "mtbf_hours": 320,
            "mttr_hours": 12.0,
            "replacement_cost_usd": 280000,
            "current_book_value_usd": 62000,
            "health_factors": [
                {"factor": "Fanuc servo motor (X-axis)", "status": "critical", "detail": "FAILED: Replacement on backorder — 6 week lead time from Fanuc. Machine DOWN."},
                {"factor": "Spindle bearing", "status": "warning", "detail": "Approaching end of life — 1,900 hrs to scheduled overhaul"},
                {"factor": "CNC control", "status": "warning", "detail": "Mazak SmoothG — occasional comm timeout with tool presetter"},
            ],
        },
        {
            "id": "Trumpf_TL3030",
            "name": "Trumpf TruLaser 3030",
            "category": "Fiber Laser Cutter",
            "installed": "2018-05",
            "age_years": 7.9,
            "hours_run": 22600,
            "hours_to_next_overhaul": 7400,
            "condition_score": 0.84,
            "maintenance_compliance_pct": 97,
            "mtbf_hours": 1500,
            "mttr_hours": 2.5,
            "replacement_cost_usd": 520000,
            "current_book_value_usd": 245000,
            "health_factors": [
                {"factor": "Laser source", "status": "nominal", "detail": "6kW IPG fiber source — 22,600 hrs on module, rated 100,000 hrs"},
                {"factor": "Cutting head lens", "status": "nominal", "detail": "Last replaced Jan 2026 — ~1,200 pierce cycles remaining"},
                {"factor": "Assist gas consumption", "status": "warning", "detail": "N2 consumption up 12% — nozzle wear suspected. Linde delivery surcharges currently ~18% above Q4 2025 baseline due to elevated energy prices."},
            ],
        },
        {
            "id": "Mitutoyo_CMM",
            "name": "Mitutoyo Crysta-Apex S",
            "category": "Coordinate Measuring Machine",
            "installed": "2017-02",
            "age_years": 9.2,
            "hours_run": 14200,
            "hours_to_next_overhaul": 10800,
            "condition_score": 0.91,
            "maintenance_compliance_pct": 100,
            "mtbf_hours": 4500,
            "mttr_hours": 1.5,
            "replacement_cost_usd": 185000,
            "current_book_value_usd": 78000,
            "health_factors": [
                {"factor": "Probe calibration", "status": "warning", "detail": "Annual calibration expires June 1, 2026 — MUST schedule with Mitutoyo immediately"},
                {"factor": "Air bearing", "status": "nominal", "detail": "Granite surface flatness verified Q1 2026"},
                {"factor": "Software", "status": "nominal", "detail": "MCOSMOS v5.1 — current version"},
            ],
        },
    ]

    total_replacement = sum(m["replacement_cost_usd"] for m in machines)
    total_book = sum(m["current_book_value_usd"] for m in machines)
    avg_condition = round(sum(m["condition_score"] for m in machines) / len(machines), 3)

    critical_count = sum(
        1 for m in machines
        for f in m["health_factors"]
        if f["status"] == "critical"
    )
    warning_count = sum(
        1 for m in machines
        for f in m["health_factors"]
        if f["status"] == "warning"
    )

    composite_internal = round(
        0.40 * avg_condition
        + 0.25 * (1.0 - critical_count * 0.15 - warning_count * 0.03)
        + 0.20 * 0.82  # workforce stability factor (based on avg flight risk inverse)
        + 0.15 * 0.88,  # process capability (Cpk proxy from QC pass rate)
        3,
    )

    return {
        "composite_internal_health_index": min(1.0, max(0.0, composite_internal)),
        "components": {
            "machinery_condition_avg": avg_condition,
            "workforce_stability": 0.82,
            "process_capability_cpk_proxy": 0.88,
            "facility_infrastructure": 0.85,
        },
        "machinery_summary": {
            "total_machines_assessed": len(machines),
            "total_replacement_cost_usd": total_replacement,
            "total_book_value_usd": total_book,
            "depreciation_gap_usd": total_replacement - total_book,
            "critical_issues": critical_count,
            "warning_issues": warning_count,
        },
        "machines": machines,
    }


@router.get("/health-index/external")
def get_external_health_index():
    """
    External health index: supply chain resilience, customer concentration,
    market conditions, and geopolitical risk factors.
    """
    supply_chain_factors = [
        {
            "factor": "Single-source supplier exposure",
            "score": 0.45,
            "weight": 0.25,
            "status": "critical",
            "detail": "3 single-source suppliers identified (Titanium Industries, Electro-Coatings, Bodycote). Loss of any one halts major production lines.",
        },
        {
            "factor": "Average lead time trend",
            "score": 0.62,
            "weight": 0.15,
            "status": "warning",
            "detail": "Avg lead time increased from 18.2 days (Q1 2025) to 21.4 days (Q1 2026). Titanium lead time at 42 days and rising.",
        },
        {
            "factor": "Supplier financial health",
            "score": 0.71,
            "weight": 0.15,
            "status": "warning",
            "detail": "Electro-Coatings owner is 68 — also facing succession risk. Bodycote Reading facility at capacity.",
        },
        {
            "factor": "Geographic concentration",
            "score": 0.78,
            "weight": 0.10,
            "status": "nominal",
            "detail": "12 of 14 Tier 1 suppliers within 300 miles (Mid-Atlantic corridor). Low logistics disruption risk for domestic supply.",
        },
    ]

    customer_factors = [
        {
            "factor": "Customer concentration (Herfindahl index)",
            "score": 0.58,
            "weight": 0.15,
            "status": "warning",
            "detail": "BAE Systems at 28%, General Dynamics at 16%. Top 2 customers = 44% of revenue. SBA recommends <20% per customer.",
        },
        {
            "factor": "Customer creditworthiness",
            "score": 0.95,
            "weight": 0.05,
            "status": "nominal",
            "detail": "All major customers are Fortune 500 / investment-grade. Avg DSO: 42 days.",
        },
        {
            "factor": "Contract backlog strength",
            "score": 0.82,
            "weight": 0.10,
            "status": "nominal",
            "detail": "12-month backlog: $6.8M (83% of annual revenue). Defense orders up 14% YoY due to increased DoD spending.",
        },
    ]

    geopolitical_factors = [
        {
            "factor": "Iran conflict — Strait of Hormuz disruption (current)",
            "score": 0.38,
            "weight": 0.20,
            "status": "critical",
            "detail": (
                "As of April 2026, Brent crude is trading near $108/bbl (+77% since Dec 2025) "
                "and US gasoline has reached ~$3.98/gal, driven by disruptions to Strait of Hormuz shipping. "
                "Current observed impacts on Hartwell: Linde Gas delivery surcharges up ~18%; "
                "diesel freight (FedEx, Ryerson) up ~33%; Quaker Houghton coolant pricing up ~22%. "
                "If these conditions persist through the next 12 months, projected additional operating cost: ~$147,000/yr. "
                "Should the conflict de-escalate, energy prices could normalize within 2-3 quarters, reducing this pressure significantly."
            ),
        },
        {
            "factor": "Defense spending tailwind",
            "score": 0.88,
            "weight": 0.10,
            "status": "nominal",
            "detail": (
                "FY2026 DoD budget increased 8.4% to $895B. BAE Systems and General Dynamics are expanding "
                "procurement — Hartwell order backlog for defense components is up 14% YoY. "
                "This creates a positive demand signal, though it also presents a paradox: "
                "rising demand coincides with rising input costs, compressing margins if energy prices remain elevated."
            ),
        },
        {
            "factor": "Titanium supply chain geopolitical exposure",
            "score": 0.42,
            "weight": 0.10,
            "status": "critical",
            "detail": (
                "TIMET (Titanium Industries' upstream supplier) sources ~15% of Ti sponge from Kazakhstan. "
                "Ongoing regional instability and surging aerospace demand have pushed Ti-6Al-4V spot prices up ~34% since Jan 2026. "
                "If current pricing holds, Hartwell's projected additional titanium material cost is ~$89,000/yr. "
                "Mitigation option: negotiate 6-month fixed-price contracts with Titanium Industries to lock in current rates."
            ),
        },
    ]

    all_factors = supply_chain_factors + customer_factors + geopolitical_factors
    total_weight = sum(f["weight"] for f in all_factors)
    composite = round(
        sum(f["score"] * f["weight"] for f in all_factors) / total_weight, 3
    )

    return {
        "composite_external_health_index": composite,
        "assessment_date": str(TODAY),
        "categories": {
            "supply_chain_resilience": {
                "score": round(sum(f["score"] * f["weight"] for f in supply_chain_factors) / sum(f["weight"] for f in supply_chain_factors), 3),
                "factors": supply_chain_factors,
            },
            "customer_stability": {
                "score": round(sum(f["score"] * f["weight"] for f in customer_factors) / sum(f["weight"] for f in customer_factors), 3),
                "factors": customer_factors,
            },
            "geopolitical_macro": {
                "score": round(sum(f["score"] * f["weight"] for f in geopolitical_factors) / sum(f["weight"] for f in geopolitical_factors), 3),
                "factors": geopolitical_factors,
            },
        },
        "cost_impact_summary": {
            "label": "Projected 12-month impact if current conditions persist",
            "iran_conflict_annual_cost_increase_usd": 147000,
            "titanium_price_increase_annual_usd": 89000,
            "total_external_cost_pressure_usd": 236000,
            "pct_of_ebitda": round(236000 / 1148000 * 100, 1),
        },
    }


@router.get("/health-index/composite")
def get_composite_health_index():
    """Overall enterprise health combining internal and external indices."""
    internal = get_internal_health_index()
    external = get_external_health_index()

    int_score = internal["composite_internal_health_index"]
    ext_score = external["composite_external_health_index"]

    enterprise_health = round(0.55 * int_score + 0.45 * ext_score, 3)

    if enterprise_health >= 0.75:
        assessment = "HEALTHY — Enterprise is operationally sound with manageable external pressures. Strong acquisition candidate."
    elif enterprise_health >= 0.55:
        assessment = "FAIR — Enterprise viable but faces meaningful headwinds. Valuation should reflect risk factors. Transition planning recommended within 12 months."
    else:
        assessment = "AT RISK — Significant internal or external deterioration. Immediate intervention required to preserve enterprise value."

    return {
        "enterprise_health_index": enterprise_health,
        "internal_health": int_score,
        "external_health": ext_score,
        "weighting": "55% internal / 45% external",
        "assessment": assessment,
        "valuation_implications": {
            "base_enterprise_value_usd": 6030000,
            "health_adjusted_multiplier": round(0.7 + 0.6 * enterprise_health, 3),
            "health_adjusted_value_usd": round(6030000 * (0.7 + 0.6 * enterprise_health)),
            "external_cost_pressure_annual_usd": external["cost_impact_summary"]["total_external_cost_pressure_usd"],
        },
    }
