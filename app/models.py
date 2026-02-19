from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from .database import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    risk_score = Column(Float, default=0.0)


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    amount = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


class QualityIssue(Base):
    __tablename__ = "quality_issues"

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer)
    invoice_id = Column(Integer)
    severity = Column(Integer)  # 1-10 scale
    financial_impact = Column(Float)
    status = Column(String, default="active")  # active/dormant
    issue_date = Column(DateTime, default=datetime.utcnow)
