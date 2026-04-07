from fastapi import APIRouter
from datetime import date

router = APIRouter()

TODAY = date(2026, 4, 7)


def _days_until(d: date) -> int:
    return (d - TODAY).days


@router.get("/compliance/overview")
def get_compliance_overview():
    items = _build_compliance_items()
    critical = [i for i in items if i["urgency"] == "critical"]
    warning = [i for i in items if i["urgency"] == "warning"]
    ok = [i for i in items if i["urgency"] == "ok"]
    return {
        "total_items": len(items),
        "critical_count": len(critical),
        "warning_count": len(warning),
        "ok_count": len(ok),
        "items": items,
    }


@router.get("/compliance/ownership-rights")
def get_asset_transfer_guide():
    return {
        "jurisdiction": "Commonwealth of Pennsylvania",
        "transfer_type": "Asset Purchase (recommended over stock purchase for liability isolation)",
        "regulations": [
            {
                "code": "PA Title 15 — Business Corporation Law of 1988",
                "section": "§ 1932 (Sale of Assets)",
                "requirement": "Board of Directors resolution + majority shareholder approval required for sale of substantially all assets outside ordinary course of business.",
                "status": "pending",
                "action_needed": "Formal board resolution must be drafted and executed before listing. Hartwell is sole shareholder — simplified approval.",
            },
            {
                "code": "PA UCC Article 6 — Bulk Sales",
                "section": "12A § 6-101 to 6-111",
                "requirement": "Buyer must give 45 days' written notice to all of seller's creditors before taking possession of assets in a bulk transfer.",
                "status": "pending",
                "action_needed": "Compile creditor list from A/P aging. 14 trade creditors identified with $218,400 outstanding. Notice letters to be prepared.",
            },
            {
                "code": "PA Title 72 — Tax Clearance",
                "section": "§ 7240 (Bulk Sale Tax Clearance)",
                "requirement": "PA Dept. of Revenue must issue a tax clearance certificate before any bulk sale. Without it, buyer assumes seller's tax liabilities.",
                "status": "pending",
                "action_needed": "File REV-181 (Application for Tax Clearance) with PA Dept. of Revenue. Typical processing: 30-45 days.",
            },
            {
                "code": "Federal ITAR — 22 CFR 122",
                "section": "§ 122.4 (Transfer of Registration)",
                "requirement": "ITAR registration cannot be transferred. New owner must independently register with DDTC before continuing any defense-related manufacturing.",
                "status": "critical",
                "action_needed": "Buyer must file DDTC Form DS-2032 immediately upon closing. 60-90 day processing. GAP IN DEFENSE CONTRACTS EXPECTED.",
            },
        ],
        "steps_completed": [
            "Preliminary business valuation ($6.03M enterprise value)",
            "Identified all real property liens — clear title confirmed",
            "Environmental Phase I assessment — no recognized environmental conditions",
            "Confirmed no pending litigation against entity",
        ],
        "pending_actions": [
            "Draft board resolution for asset sale (§ 1932)",
            "Compile and verify creditor list for bulk sale notice",
            "File REV-181 for PA tax clearance",
            "Engage buyer's ITAR counsel for DDTC registration",
            "Negotiate seller's transition service agreement (6-12 months recommended)",
            "Transfer vehicle titles (3 company trucks) via PennDOT MV-4ST",
        ],
    }


@router.get("/compliance/knowledge-disclosure")
def get_trade_secret_protocols():
    return {
        "trade_secret_protection": {
            "governing_law": "PA Uniform Trade Secrets Act (12 Pa.C.S. § 5301-5308)",
            "status": "active",
            "protections_in_place": [
                "Non-disclosure agreements with all 47 employees — last audit March 2026",
                "CAD files encrypted with AES-256 content-based partial encryption",
                "CNC program files stored on air-gapped FANUC server (no internet access)",
                "Visitor access log enforced per ITAR § 122.15",
                "Due diligence data room uses Intralinks VDR with watermarked access",
            ],
            "cad_files_protected": 2847,
            "cnc_programs_protected": 1203,
            "encryption_method": "AES-256-GCM content-based partial encryption",
        },
        "data_breach_notification": {
            "governing_law": "PA Breach of Personal Information Notification Act (73 P.S. § 2301-2329)",
            "employee_pii_records": 47,
            "data_types_held": [
                "Social Security numbers",
                "Direct deposit bank account info",
                "Health insurance records (HIPAA-adjacent)",
                "I-9 employment verification documents",
            ],
            "breach_notification_required_within_days": "Unreasonable delay prohibited — generally interpreted as 30-60 days",
            "last_breach_incident": None,
            "transfer_protocol": "Employee PII must be transferred via encrypted channel with explicit consent or be destroyed. Buyer must sign data processing agreement.",
        },
        "cybersecurity_compliance": {
            "governing_regulation": "DFARS 252.204-7012 — Safeguarding Covered Defense Information",
            "cmmc_level": "Level 2 (Advanced) — required for BAE Systems & General Dynamics contracts",
            "nist_sp_800_171_score": 94,
            "nist_sp_800_171_max": 110,
            "poa_m_items_open": 3,
            "last_assessment_date": "2025-11-15",
            "status": "Conditionally compliant — 3 POA&M items due by August 2026",
        },
        "is_compliant": True,
    }


def _build_compliance_items():
    items = [
        {
            "id": "LIC-001",
            "category": "Quality Certification",
            "name": "ISO 9001:2015 — Quality Management System",
            "issuer": "BSI Group (Registrar)",
            "expiry_date": "2026-07-18",
            "days_until_expiry": _days_until(date(2026, 7, 18)),
            "urgency": "warning",
            "notes": "Recertification audit scheduled. Must pass before expiry or all customer purchase orders referencing ISO 9001 become non-compliant.",
            "transfer_impact": "Certificate is non-transferable. New owner must schedule transition audit within 6 months of closing.",
        },
        {
            "id": "LIC-002",
            "category": "Aerospace Certification",
            "name": "AS9100D — Aerospace Quality Management",
            "issuer": "BSI Group / IAQG",
            "expiry_date": "2026-11-02",
            "days_until_expiry": _days_until(date(2026, 11, 2)),
            "urgency": "ok",
            "notes": "Surveillance audit due. Required for BAE Systems, Lockheed Martin, and General Dynamics contracts ($4.4M revenue at risk).",
            "transfer_impact": "Non-transferable. New owner must reapply under new legal entity. 3-6 month qualification timeline.",
        },
        {
            "id": "LIC-003",
            "category": "Defense Registration",
            "name": "ITAR Registration — DDTC",
            "issuer": "U.S. Dept. of State, DDTC",
            "expiry_date": "2026-09-30",
            "days_until_expiry": _days_until(date(2026, 9, 30)),
            "urgency": "warning",
            "notes": "Annual renewal fee $2,250. Must be current to manufacture, export, or broker defense articles. 44% of revenue is ITAR-controlled.",
            "transfer_impact": "CRITICAL: Cannot be transferred. New owner must independently register. 60-90 day processing creates potential gap in defense production authority.",
        },
        {
            "id": "LIC-004",
            "category": "Fire & Safety",
            "name": "Fire Safety Inspection Certificate",
            "issuer": "City of Allentown Fire Marshal",
            "expiry_date": "2026-05-15",
            "days_until_expiry": _days_until(date(2026, 5, 15)),
            "urgency": "critical",
            "notes": "Expires in 38 days. Facility cannot operate without valid certificate. Last inspection flagged need to replace 2 fire extinguishers near laser cutter area.",
            "transfer_impact": "Transfers with property. New inspection required if facility layout changes.",
        },
        {
            "id": "LIC-005",
            "category": "Environmental",
            "name": "PA DEP Air Quality Plan Approval (GP-14)",
            "issuer": "PA Dept. of Environmental Protection",
            "expiry_date": "2026-08-20",
            "days_until_expiry": _days_until(date(2026, 8, 20)),
            "urgency": "warning",
            "notes": "General Permit 14 covers metalworking fluid mist and grinding dust emissions. Renewal application must be filed 90 days before expiry.",
            "transfer_impact": "Must be transferred or reissued to new owner. PA DEP Form 27-00GP-14 required. 60-90 day processing.",
        },
        {
            "id": "LIC-006",
            "category": "Environmental",
            "name": "NPDES Wastewater Discharge Permit",
            "issuer": "PA Dept. of Environmental Protection",
            "expiry_date": "2027-03-01",
            "days_until_expiry": _days_until(date(2027, 3, 1)),
            "urgency": "ok",
            "notes": "Covers coolant wastewater and chrome plating rinse discharge to Lehigh County Authority POTW. Quarterly DMR reports current.",
            "transfer_impact": "Transfer requires written notice to PA DEP and Lehigh County Authority. 30-day comment period.",
        },
        {
            "id": "LIC-007",
            "category": "Safety",
            "name": "Boiler & Pressure Vessel Inspection",
            "issuer": "PA Dept. of Labor & Industry",
            "expiry_date": "2026-08-10",
            "days_until_expiry": _days_until(date(2026, 8, 10)),
            "urgency": "warning",
            "notes": "Covers 2 air compressors (Kaeser BSD 72) and 1 steam boiler for parts washers. PA Act 85 of 1998 requires annual inspection.",
            "transfer_impact": "Inspection transfers with equipment. No reapplication needed.",
        },
        {
            "id": "LIC-008",
            "category": "Business Filing",
            "name": "PA Annual Business Entity Report",
            "issuer": "PA Dept. of State — Bureau of Corporations",
            "expiry_date": "2026-12-31",
            "days_until_expiry": _days_until(date(2026, 12, 31)),
            "urgency": "ok",
            "notes": "Annual decennial report for domestic business corporation. Filing fee $7. Required to maintain good standing.",
            "transfer_impact": "Entity will be dissolved or transferred as part of sale structure. New entity filing required for buyer.",
        },
        {
            "id": "LIC-009",
            "category": "Insurance",
            "name": "Workers' Compensation Insurance Policy",
            "issuer": "State Workers' Insurance Fund (SWIF)",
            "expiry_date": "2026-10-01",
            "days_until_expiry": _days_until(date(2026, 10, 1)),
            "urgency": "ok",
            "notes": "Current EMR (Experience Modification Rate): 0.87 — better than industry average of 1.00. Annual premium $142,000. Manufacturing class code 3612.",
            "transfer_impact": "EMR history may not transfer. Buyer should negotiate transitional experience rating with insurer.",
        },
        {
            "id": "LIC-010",
            "category": "Defense Compliance",
            "name": "CMMC Level 2 Assessment",
            "issuer": "Cyber AB (C3PAO)",
            "expiry_date": "2026-11-15",
            "days_until_expiry": _days_until(date(2026, 11, 15)),
            "urgency": "ok",
            "notes": "NIST SP 800-171 score: 94/110. 3 POA&M items open. Required for all DoD CUI-handling contracts (BAE Systems, General Dynamics). Assessment valid 3 years.",
            "transfer_impact": "Assessment is entity-specific. New owner must commission fresh C3PAO assessment. Cost: $35,000-$75,000.",
        },
        {
            "id": "LIC-011",
            "category": "Calibration",
            "name": "Mitutoyo CMM Calibration Certificate",
            "issuer": "Mitutoyo America (ISO 17025 accredited lab)",
            "expiry_date": "2026-06-01",
            "days_until_expiry": _days_until(date(2026, 6, 1)),
            "urgency": "critical",
            "notes": "Annual calibration required to maintain ISO 9001 and AS9100D compliance. All inspection data generated after expiry is non-conforming. Backlog at Mitutoyo — must schedule immediately.",
            "transfer_impact": "Calibration certificate is tied to equipment serial number, not owner. Transfers automatically.",
        },
        {
            "id": "LIC-012",
            "category": "Trade Compliance",
            "name": "EAR/Export License — Dual-Use Components",
            "issuer": "U.S. Bureau of Industry & Security (BIS)",
            "expiry_date": "2027-06-30",
            "days_until_expiry": _days_until(date(2027, 6, 30)),
            "urgency": "ok",
            "notes": "Covers export of finished machined components classified under ECCN 2B001. Current shipments to allied NATO countries only.",
            "transfer_impact": "License is entity-specific. New owner must apply for new export license. 60-120 day BIS processing.",
        },
    ]

    for item in items:
        d = _days_until(date.fromisoformat(item["expiry_date"]))
        if d <= 60:
            item["urgency"] = "critical"
        elif d <= 135:
            item["urgency"] = "warning"
        else:
            item["urgency"] = "ok"
        item["days_until_expiry"] = d

    return items
