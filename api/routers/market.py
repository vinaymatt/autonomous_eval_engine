from fastapi import APIRouter
from pydantic import BaseModel
from core.models.rf_survival import FirmExitPredictor

router = APIRouter()
rf_predictor = FirmExitPredictor()

VALUATION_DB = {
    "SMM-1247": {
        "node_id": "SMM-1247",
        "name": "Hartwell Precision Mfg.",
        "intangible_value_usd": 2180000,
        "tangible_value_usd": 3850000,
        "total_enterprise_value_usd": 6030000,
        "stability_index": 0.71,
        "patent_count": 4,
        "risk_status": "Moderate Risk — Succession Uncertainty",
        "risk_factors": [
            "Owner retirement imminent (age 72, no successor)",
            "Key-man dependency on Plant Manager (22-yr tenure)",
            "44% revenue concentration in ITAR-controlled defense work",
        ],
    },
    "CUST-BAE": {
        "node_id": "CUST-BAE",
        "name": "BAE Systems",
        "intangible_value_usd": None,
        "tangible_value_usd": None,
        "total_enterprise_value_usd": None,
        "stability_index": 0.92,
        "patent_count": None,
        "risk_status": "Stable",
        "risk_factors": ["Fortune 500 defense prime — minimal counterparty risk"],
    },
    "CUST-STRYKER": {
        "node_id": "CUST-STRYKER",
        "name": "Stryker Corporation",
        "intangible_value_usd": None,
        "tangible_value_usd": None,
        "total_enterprise_value_usd": None,
        "stability_index": 0.89,
        "patent_count": None,
        "risk_status": "Stable",
        "risk_factors": ["S&P 500 medical device company — strong demand pipeline"],
    },
    "CUST-DANA": {
        "node_id": "CUST-DANA",
        "name": "Dana Incorporated",
        "intangible_value_usd": None,
        "tangible_value_usd": None,
        "total_enterprise_value_usd": None,
        "stability_index": 0.74,
        "patent_count": None,
        "risk_status": "Moderate Risk",
        "risk_factors": ["EV transition reducing ICE drivetrain demand by ~8% annually"],
    },
    "CUST-GDLS": {
        "node_id": "CUST-GDLS",
        "name": "General Dynamics",
        "intangible_value_usd": None,
        "tangible_value_usd": None,
        "total_enterprise_value_usd": None,
        "stability_index": 0.91,
        "patent_count": None,
        "risk_status": "Stable",
        "risk_factors": ["Major defense prime — Scranton Army Ammunition Plant"],
    },
    "CUST-LOCKHEED": {
        "node_id": "CUST-LOCKHEED",
        "name": "Lockheed Martin",
        "intangible_value_usd": None,
        "tangible_value_usd": None,
        "total_enterprise_value_usd": None,
        "stability_index": 0.94,
        "patent_count": None,
        "risk_status": "Stable",
        "risk_factors": ["Largest defense contractor globally — Moorestown facility"],
    },
    "SUP-TITANIUM": {
        "node_id": "SUP-TITANIUM",
        "name": "Titanium Industries",
        "intangible_value_usd": None,
        "tangible_value_usd": None,
        "total_enterprise_value_usd": None,
        "stability_index": 0.52,
        "patent_count": None,
        "risk_status": "High Risk — Single Source",
        "risk_factors": [
            "Only qualified Ti-6Al-4V source for Hartwell aerospace work",
            "Upstream dependency on TIMET (PCC) for sponge & ingot",
            "42-day lead time and trending upward",
        ],
    },
    "SUP-ELECTROCOAT": {
        "node_id": "SUP-ELECTROCOAT",
        "name": "Electro-Coatings Inc.",
        "intangible_value_usd": None,
        "tangible_value_usd": None,
        "total_enterprise_value_usd": None,
        "stability_index": 0.48,
        "patent_count": None,
        "risk_status": "High Risk — Single Source",
        "risk_factors": [
            "Only Mil-Spec anodizer within 200 miles",
            "Owner is 68 — also facing succession risk",
            "Alternative qualification would take 9-12 months",
        ],
    },
    "SUP-HEATTREAT": {
        "node_id": "SUP-HEATTREAT",
        "name": "Bodycote Thermal Processing",
        "intangible_value_usd": None,
        "tangible_value_usd": None,
        "total_enterprise_value_usd": None,
        "stability_index": 0.61,
        "patent_count": None,
        "risk_status": "High Risk — Sole NADCAP Provider",
        "risk_factors": [
            "Only NADCAP-certified heat treat for Hartwell aerospace",
            "Reading, PA facility at capacity — 14-day lead and growing",
        ],
    },
    "SUP-RYERSON": {
        "node_id": "SUP-RYERSON",
        "name": "Ryerson Steel",
        "intangible_value_usd": None,
        "tangible_value_usd": None,
        "total_enterprise_value_usd": None,
        "stability_index": 0.82,
        "patent_count": None,
        "risk_status": "Stable",
        "risk_factors": ["Major metals distributor — multiple alternative sources available"],
    },
    "SUP-ALCOA": {
        "node_id": "SUP-ALCOA",
        "name": "Alcoa Corporation",
        "intangible_value_usd": None,
        "tangible_value_usd": None,
        "total_enterprise_value_usd": None,
        "stability_index": 0.85,
        "patent_count": None,
        "risk_status": "Stable",
        "risk_factors": ["Pittsburgh-based — established PA supply relationship"],
    },
}


class FirmData(BaseModel):
    liquidity_ratio: float
    debt_to_equity: float
    employee_turnover: float
    market_demand_trend: float
    owner_age: float = 72.0
    years_without_successor: float = 3.0
    revenue_concentration_top_customer_pct: float = 0.28
    certifications_at_risk_count: float = 2.0


@router.post("/predict-exit")
def predict_firm_exit(data: FirmData):
    features = [
        data.liquidity_ratio,
        data.debt_to_equity,
        data.employee_turnover,
        data.market_demand_trend,
        data.owner_age / 100.0,
        data.years_without_successor / 10.0,
        data.revenue_concentration_top_customer_pct,
        data.certifications_at_risk_count / 10.0,
    ]

    risk_prob = rf_predictor.predict_exit_probability(features)

    if risk_prob > 0.7:
        recommendation = "CRITICAL: High probability of firm exit. Immediate intervention recommended — begin buyer outreach and government transition assistance (PA WDB Rapid Response)."
    elif risk_prob > 0.4:
        recommendation = "ELEVATED: Moderate exit risk. Firm viable but succession timeline is compressed. Recommend proactive buyer matching and transition planning within 12 months."
    else:
        recommendation = "STABLE: Low near-term exit risk. Continue monitoring. Recommend initiating succession planning conversations with owner."

    return {
        "status": "success",
        "exit_probability": risk_prob,
        "model": "Random Forest + Gradient Boosting Ensemble (100 estimators)",
        "features_used": [
            "Liquidity Ratio",
            "Debt-to-Equity",
            "Employee Turnover Rate",
            "Market Demand Trend",
            "Owner Age (normalized)",
            "Years Without Successor",
            "Revenue Concentration (top customer)",
            "Certifications at Risk",
        ],
        "recommendation": recommendation,
        "socioeconomic_impact": {
            "direct_jobs_lost": 47,
            "indirect_jobs_at_risk": 134,
            "annual_payroll_lost_usd": 2680000,
            "annual_tax_revenue_lost_usd": 412000,
            "estimated_regional_gdp_impact_usd": 14600000,
            "govt_assistance_cost_usd": 890000,
        },
    }


@router.get("/valuation/{node_id}")
def get_node_valuation(node_id: str):
    if node_id in VALUATION_DB:
        return VALUATION_DB[node_id]

    return {
        "node_id": node_id,
        "name": node_id,
        "intangible_value_usd": None,
        "tangible_value_usd": None,
        "total_enterprise_value_usd": None,
        "stability_index": 0.65,
        "patent_count": None,
        "risk_status": "Unknown — Insufficient Data",
        "risk_factors": ["Node not in primary valuation database"],
    }
