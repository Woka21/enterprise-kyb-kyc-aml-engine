from fastapi import APIRouter

from app.schemas import ComplianceStatus, ComplianceSubmission

router = APIRouter(prefix="/compliance", tags=["compliance"])

INITIAL_CASES = [
    {
        "id": "case-1001",
        "company_name": "Nairobi Traders Ltd",
        "kra_pin": "P051234567Z",
        "status": "under_review",
        "kyb_score": 92,
        "kyc_score": 88,
        "aml_score": 96,
        "clearance": "pending",
    },
    {
        "id": "case-1002",
        "company_name": "Kenya Capital Group",
        "kra_pin": "P089876543Q",
        "status": "cleared",
        "kyb_score": 97,
        "kyc_score": 94,
        "aml_score": 99,
        "clearance": "approved",
    },
]


@router.get("/cases")
def list_cases() -> list[dict]:
    return INITIAL_CASES


@router.post("/submit")
def submit_case(payload: ComplianceSubmission) -> dict:
    case_id = f"case-{len(INITIAL_CASES) + 1000}"
    result = {
        "id": case_id,
        "company_name": payload.company_name,
        "kra_pin": payload.kra_pin,
        "director_name": payload.director_name,
        "document_type": payload.document_type,
        "risk_level": payload.risk_level,
        "status": "submitted",
        "message": "Compliance intake created successfully.",
    }
    INITIAL_CASES.insert(0, {
        "id": case_id,
        "company_name": payload.company_name,
        "kra_pin": payload.kra_pin,
        "status": "submitted",
        "kyb_score": 88,
        "kyc_score": 84,
        "aml_score": 90,
        "clearance": "pending",
    })
    return result


@router.get("/status/{case_id}")
def get_case_status(case_id: str) -> ComplianceStatus:
    match = next((item for item in INITIAL_CASES if item["id"] == case_id), None)
    if match is None:
        return ComplianceStatus(
            id=case_id,
            company_name="Unknown Client",
            kra_pin="N/A",
            status="in_progress",
            kyb_score=0,
            kyc_score=0,
            aml_score=0,
            clearance="review",
        )

    return ComplianceStatus(
        id=match["id"],
        company_name=match["company_name"],
        kra_pin=match["kra_pin"],
        status=match["status"],
        kyb_score=match["kyb_score"],
        kyc_score=match["kyc_score"],
        aml_score=match["aml_score"],
        clearance=match["clearance"],
    )
