from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel, Field


@dataclass
class AppConfig:
    database_url: str = "postgresql://compliance:compliance_secret@postgres:5432/compliance"
    app_env: str = "development"


class ComplianceSubmission(BaseModel):
    company_name: str = Field(..., min_length=2)
    kra_pin: str = Field(..., min_length=3)
    director_name: str = Field(..., min_length=2)
    document_type: str = Field(default="certificate_of_incorporation")
    risk_level: Optional[str] = Field(default="medium")


class ComplianceStatus(BaseModel):
    id: str
    company_name: str
    kra_pin: str
    status: str
    kyb_score: int
    kyc_score: int
    aml_score: int
    clearance: str
