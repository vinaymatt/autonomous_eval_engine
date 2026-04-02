from fastapi import APIRouter
from core.simulation.digital_twin import DigitalTwinSimulator

router = APIRouter()
simulator = DigitalTwinSimulator(facility_id="SMM-774")

@router.get("/digital-twin/kpis")
def get_digital_twin_kpis():
    """Returns simulated live production scenarios using real-time IoT data."""
    return simulator.fetch_live_kpis()

@router.get("/human-capital/wage-skill")
def get_wage_skill_demographics():
    """
    Returns data for 'Wage-Skill' scatter plots to analyze workforce demographics.
    Identifies high-flight-risk talent and vulnerable employees.
    """
    return {
        "nodes": [
            {"employee_id": "E1", "skill_level": 8.5, "wage_usd_hr": 35.0, "flight_risk": 0.82},
            {"employee_id": "E2", "skill_level": 4.0, "wage_usd_hr": 20.0, "flight_risk": 0.15},
            {"employee_id": "E3", "skill_level": 9.2, "wage_usd_hr": 42.0, "flight_risk": 0.45}
        ]
    }

@router.get("/supply-chain/graph")
def get_supply_chain_graph():
    return {
        "nodes": [
            {"id": "SMM-774", "label": "Apex Machining (Core)", "color": "#1f77b4", "size": 30},
            {"id": "Supplier_A", "label": "Raw Steel", "color": "#2ca02c", "size": 20},
            {"id": "Supplier_B", "label": "Specialty Coatings", "color": "#d62728", "size": 25}
        ],
        "edges": [
            {"source": "Supplier_A", "target": "SMM-774", "label": "14d Lead Time"},
            {"source": "Supplier_B", "target": "SMM-774", "label": "45d Lead Time (Critical)"}
        ]
    }

@router.get("/digital-twin/layout-3d")
def get_3d_layout():
    """Returns spatial coordinates, live status, and conveyor topology of factory machinery."""
    return {
        "machines": [
            {"id": "CNC_Mill_01", "type": "Milling", "x": 8, "y": 8, "z": 0, "status": "Active", "efficiency": 0.95},
            {"id": "CNC_Mill_02", "type": "Milling", "x": 14, "y": 8, "z": 0, "status": "Active", "efficiency": 0.88},
            {"id": "CNC_Mill_03", "type": "Milling", "x": 8, "y": 14, "z": 0, "status": "Maintenance", "efficiency": 0.50},
            {"id": "Lathe_01", "type": "Turning", "x": 26, "y": 8, "z": 0, "status": "Active", "efficiency": 0.92},
            {"id": "Lathe_02", "type": "Turning", "x": 26, "y": 14, "z": 0, "status": "Downtime", "efficiency": 0.0},
            {"id": "Laser_Cut_01", "type": "Cutting", "x": 8, "y": 24, "z": 0, "status": "Active", "efficiency": 0.91},
            {"id": "Plasma_Cut_01", "type": "Cutting", "x": 14, "y": 24, "z": 0, "status": "Active", "efficiency": 0.85},
            {"id": "CMM_01", "type": "Inspection", "x": 26, "y": 24, "z": 0, "status": "Active", "efficiency": 0.99},
            {"id": "Assembly_01", "type": "Assembly", "x": 18, "y": 16, "z": 0, "status": "Active", "efficiency": 0.90},
        ],
        "conveyors": [
            {"from": [16, 8], "to": [24, 8]},
            {"from": [16, 24], "to": [24, 24]},
            {"from": [8, 16], "to": [8, 22]},
            {"from": [26, 16], "to": [26, 22]},
        ]
    }