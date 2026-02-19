from fastapi import FastAPI
from .database import Base, engine, SessionLocal
from .models import Supplier, Invoice, QualityIssue
from .retrieval import retrieve_context
from datetime import datetime, timedelta
from .lifecycle import apply_lifecycle_rules


app = FastAPI(title="Business Context Memory Engine")

Base.metadata.create_all(bind=engine)


@app.get("/")
def health_check():
    return {"status": "BCME is running"}


@app.post("/seed")
def seed_data():
    db = SessionLocal()

    # Clear old data
    db.query(QualityIssue).delete()
    db.query(Invoice).delete()
    db.query(Supplier).delete()
    db.commit()

    supplier = Supplier(name="Supplier XYZ")
    db.add(supplier)
    db.commit()
    db.refresh(supplier)

    invoice = Invoice(
        supplier_id=supplier.id,
        amount=250000
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    issue_recent = QualityIssue(
        supplier_id=supplier.id,
        invoice_id=invoice.id,
        severity=8,
        financial_impact=50000,
        issue_date=datetime.utcnow() - timedelta(days=30)
    )

    issue_old = QualityIssue(
        supplier_id=supplier.id,
        invoice_id=invoice.id,
        severity=6,
        financial_impact=20000,
        issue_date=datetime.utcnow() - timedelta(days=300)
    )

    db.add(issue_recent)
    db.add(issue_old)

    db.commit()
    db.close()

    return {"message": "Sample business memory created successfully"}


@app.post("/process-invoice/{invoice_id}")
def process_invoice(invoice_id: int):
    db = SessionLocal()

    apply_lifecycle_rules(db)


    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id
    ).first()

    if not invoice:
        db.close()
        return {"error": "Invoice not found"}

    context = retrieve_context(db, invoice.supplier_id)

    if context:
        risk_score = sum(item["relevance"] for item in context) / len(context)
    else:
        risk_score = 0

    if risk_score > 0.75:
        recommendation = "Escalate to Procurement Head"
    elif risk_score > 0.5:
        recommendation = "Require Quality Inspection"
    else:
        recommendation = "Approve"

    if risk_score > 0.75:
        risk_level = "High"
    elif risk_score > 0.5:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    db.close()

    return {
        "invoice_id": invoice_id,
        "risk_score": round(risk_score, 3),
        "risk_level": risk_level,
        "recommendation": recommendation,
        "context_used": context
    }

   
