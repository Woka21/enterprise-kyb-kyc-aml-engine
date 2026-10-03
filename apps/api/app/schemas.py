from pydantic import BaseModel, Field
from typing import Optional


class ComplianceSubmission(BaseModel):
    company_name: str = Field(..., min_length=2, description="Company name")
    kra_pin: str = Field(..., min_length=3, description="KRA PIN or registration number")
    director_name: str = Field(..., min_length=2, description="Director or beneficial owner name")
    document_type: str = Field(default="certificate_of_incorporation", description="Document uploaded")
    risk_level: Optional[str] = Field(default="medium", description="Risk profile level")


class ComplianceStatus(BaseModel):
    id: str
    company_name: str
    kra_pin: str
    status: str
    kyb_score: int
    kyc_score: int
    aml_score: int
    clearance: str


class ComplianceCaseRecord(BaseModel):
    id: str
    company_name: str
    kra_pin: str
    status: str
    kyb_score: int
    kyc_score: int
    aml_score: int
    clearance: str
