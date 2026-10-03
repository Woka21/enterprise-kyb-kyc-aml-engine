from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from app.db import get_db
from app.models import ComplianceCase
from app.schemas import ComplianceStatus, ComplianceSubmission

router = APIRouter(prefix="/compliance", tags=["compliance"])


@router.get("/cases")
def list_cases(db: Session = Depends(get_db)) -> list[dict]:
    """List all compliance cases."""
    cases = db.query(ComplianceCase).order_by(ComplianceCase.created_at.desc()).all()
    return [
        {
            "id": case.case_id,
            "company_name": case.company_name,
            "kra_pin": case.kra_pin,
            "status": case.status,
            "kyb_score": int(case.kyb_score),
            "kyc_score": int(case.kyc_score),
            "aml_score": int(case.aml_score),
            "clearance": case.clearance,
        }
        for case in cases
    ]


@router.post("/submit")
def submit_case(payload: ComplianceSubmission, db: Session = Depends(get_db)) -> dict:
    """Submit a new compliance case."""
    case_id = str(uuid.uuid4())[:8]
    
    new_case = ComplianceCase(
        case_id=f"case-{case_id}",
        company_name=payload.company_name,
        kra_pin=payload.kra_pin,
        director_name=payload.director_name,
        document_type=payload.document_type,
        risk_level=payload.risk_level,
        status="submitted",
        kyb_score=88,
        kyc_score=84,
        aml_score=90,
        clearance="pending",
    )
    
    db.add(new_case)
    db.commit()
    db.refresh(new_case)
    
    return {
        "id": new_case.case_id,
        "company_name": new_case.company_name,
        "kra_pin": new_case.kra_pin,
        "director_name": new_case.director_name,
        "document_type": new_case.document_type,
        "risk_level": new_case.risk_level,
        "status": new_case.status,
        "message": "Compliance intake created successfully.",
    }


@router.get("/status/{case_id}")
def get_case_status(case_id: str, db: Session = Depends(get_db)) -> ComplianceStatus:
    """Get detailed status of a specific compliance case."""
    case = db.query(ComplianceCase).filter(ComplianceCase.case_id == case_id).first()
    
    if not case:
        raise HTTPException(status_code=404, detail=f"Case {case_id} not found")

    return ComplianceStatus(
        id=case.case_id,
        company_name=case.company_name,
        kra_pin=case.kra_pin,
        status=case.status,
        kyb_score=int(case.kyb_score),
        kyc_score=int(case.kyc_score),
        aml_score=int(case.aml_score),
        clearance=case.clearance,
    )
