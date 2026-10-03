from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
import requests

from app.db import get_db
from app.models import ComplianceCase
from app.schemas import ComplianceStatus, ComplianceSubmission
from services.kra_service import verify_kra_pin
from services.kyc_service import verify_director_identity
from services.aml_service import check_aml_watchlist

router = APIRouter(prefix="/compliance", tags=["compliance"])


def generate_compliance_certificate_pdf(case: ComplianceCase) -> str:
    """Generate a comprehensive PDF compliance certificate with audit trail."""
    output_dir = Path("/tmp/compliance-certificates")
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = output_dir / f"{case.case_id}_compliance_certificate.pdf"

    doc = SimpleDocTemplate(str(pdf_path), pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#0066cc'),
        spaceAfter=30,
        alignment=1,
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#003366'),
        spaceAfter=12,
    )

    # Title
    elements.append(Paragraph("ENTERPRISE COMPLIANCE CLEARANCE CERTIFICATE", title_style))
    elements.append(Spacer(1, 0.3*inch))

    # Company details section
    elements.append(Paragraph("Company Information", heading_style))
    company_data = [
        ["Field", "Value"],
        ["Company Name", case.company_name],
        ["KRA PIN", case.kra_pin],
        ["Director/Owner", case.director_name],
        ["Risk Level", case.risk_level.upper()],
        ["Document Type", case.document_type.replace('_', ' ').title()],
    ]
    company_table = Table(company_data, colWidths=[2*inch, 4*inch])
    company_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066cc')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
    ]))
    elements.append(company_table)
    elements.append(Spacer(1, 0.3*inch))

    # Compliance scores section
    elements.append(Paragraph("Compliance Verification Scores", heading_style))
    scores_data = [
        ["Check Type", "Score", "Status"],
        ["KYB (Corporate Verification)", f"{int(case.kyb_score)}%", "✓ PASSED" if case.kyb_score >= 80 else "✗ REVIEW"],
        ["KYC (Identity Verification)", f"{int(case.kyc_score)}%", "✓ PASSED" if case.kyc_score >= 80 else "✗ REVIEW"],
        ["AML (Sanctions Screening)", f"{int(case.aml_score)}%", "✓ PASSED" if case.aml_score >= 80 else "✗ REVIEW"],
    ]
    scores_table = Table(scores_data, colWidths=[2.5*inch, 1.5*inch, 2*inch])
    scores_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#e8f4f8')]),
    ]))
    elements.append(scores_table)
    elements.append(Spacer(1, 0.3*inch))

    # Clearance status section
    elements.append(Paragraph("Clearance Status", heading_style))
    clearance_color = colors.green if case.clearance == "approved" else colors.orange if case.clearance == "pending" else colors.red
    clearance_text = f"<font color='{clearance_color}' size=16><b>{case.clearance.upper()}</b></font>"
    elements.append(Paragraph(clearance_text, styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))

    # Audit trail section
    elements.append(Paragraph("Audit Trail", heading_style))
    audit_text = f"<b>Case ID:</b> {case.case_id}<br/><b>Status:</b> {case.status.replace('_', ' ').title()}<br/><b>Created:</b> {case.created_at.strftime('%Y-%m-%d %H:%M:%S') if case.created_at else 'N/A'}<br/><b>Updated:</b> {case.updated_at.strftime('%Y-%m-%d %H:%M:%S') if case.updated_at else 'N/A'}"
    elements.append(Paragraph(audit_text, styles['Normal']))
    elements.append(Spacer(1, 0.4*inch))

    # Footer
    footer_text = "<i>This document is an official compliance clearance certificate generated by the Enterprise KYB/KYC/AML Compliance Engine. For verification or queries, contact compliance@yourcompany.com</i>"
    elements.append(Paragraph(footer_text, styles['Normal']))

    doc.build(elements)
    return str(pdf_path)


@router.get("/cases")
def list_cases(db: Session = Depends(get_db)) -> list[dict]:
    """List all compliance cases with live scores."""
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
    """Submit a new compliance case with automated KRA/KYC/AML checks."""
    case_id = str(uuid.uuid4())[:8]

    # Run live KRA verification
    kyb_result = verify_kra_pin(payload.kra_pin)
    kyb_score = 95 if kyb_result.get("valid") else 40

    # Run live KYC verification
    kyc_result = verify_director_identity(payload.director_name)
    kyc_score = 92 if kyc_result.get("verified") else 50

    # Run live AML watchlist check
    aml_result = check_aml_watchlist(payload.director_name)
    aml_score = 95 if not aml_result.get("match") else 10

    # Determine clearance status
    avg_score = (kyb_score + kyc_score + aml_score) / 3
    if aml_result.get("match"):
        clearance = "rejected"
    elif avg_score >= 85:
        clearance = "approved"
    else:
        clearance = "pending"

    new_case = ComplianceCase(
        case_id=f"case-{case_id}",
        company_name=payload.company_name,
        kra_pin=payload.kra_pin,
        director_name=payload.director_name,
        document_type=payload.document_type,
        risk_level=payload.risk_level,
        status="submitted",
        kyb_score=kyb_score,
        kyc_score=kyc_score,
        aml_score=aml_score,
        clearance=clearance,
    )

    db.add(new_case)
    db.commit()
    db.refresh(new_case)

    return {
        "id": new_case.case_id,
        "company_name": new_case.company_name,
        "kra_pin": new_case.kra_pin,
        "director_name": new_case.director_name,
        "status": new_case.status,
        "kyb_score": int(new_case.kyb_score),
        "kyc_score": int(new_case.kyc_score),
        "aml_score": int(new_case.aml_score),
        "clearance": new_case.clearance,
        "message": "Compliance intake created with automated verification checks.",
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


@router.post("/certificate/{case_id}")
def generate_certificate(case_id: str, db: Session = Depends(get_db)) -> dict:
    """Generate and export a compliance clearance PDF certificate."""
    case = db.query(ComplianceCase).filter(ComplianceCase.case_id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail=f"Case {case_id} not found")

    pdf_path = generate_compliance_certificate_pdf(case)
    return {
        "case_id": case.case_id,
        "company_name": case.company_name,
        "pdf_path": pdf_path,
        "pdf_filename": f"{case.case_id}_compliance_certificate.pdf",
        "status": "certificate_generated",
        "clearance": case.clearance,
        "message": "Compliance certificate generated successfully. Ready for download.",
    }
