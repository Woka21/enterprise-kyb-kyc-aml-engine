from sqlalchemy import Column, Integer, String, Float, DateTime, func
from sqlalchemy.orm import relationship

from app.db import Base


class ComplianceCase(Base):
    __tablename__ = "compliance_cases"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(String, unique=True, index=True, nullable=False)
    company_name = Column(String, nullable=False)
    kra_pin = Column(String, nullable=False)
    director_name = Column(String, nullable=False)
    document_type = Column(String, nullable=False)
    risk_level = Column(String, default="medium")
    status = Column(String, default="submitted")
    kyb_score = Column(Float, default=0.0)
    kyc_score = Column(Float, default=0.0)
    aml_score = Column(Float, default=0.0)
    clearance = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
