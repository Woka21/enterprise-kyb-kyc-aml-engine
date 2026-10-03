from fastapi import APIRouter

from app.config import ComplianceStatus, ComplianceSubmission

router = APIRouter(prefix="/compliance", tags=["compliance"])


@router.get("/cases")
def list_cases() -> list[dict]:
    return [
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


@router.post("/submit")
def submit_case(payload: ComplianceSubmission) -> dict:
    return {
        "id": "case-generated-001",
        "company_name": payload.company_name,
        "kra_pin": payload.kra_pin,
        "status": "submitted",
        "message": "Compliance intake created successfully.",
    }


@router.get("/status/{case_id}")
def get_case_status(case_id: str) -> ComplianceStatus:
    return ComplianceStatus(
        id=case_id,
        company_name="Sample Company",
        kra_pin="P012345678P",
        status="in_progress",
        kyb_score=90,
        kyc_score=85,
        aml_score=93,
        clearance="review",
    )
