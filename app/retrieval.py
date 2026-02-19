from .models import QualityIssue
from .scoring import compute_relevance


def retrieve_context(db, supplier_id, top_k=3):
    """
    Fetch historical issues for supplier,
    compute relevance, rank and return top_k.
    """

    issues = db.query(QualityIssue).filter(
        QualityIssue.supplier_id == supplier_id,
        QualityIssue.status == "active"
    ).all()

    scored_context = []

    for issue in issues:
        score_data = compute_relevance(issue)

        scored_context.append({
            "issue_id": issue.id,
            "severity": issue.severity,
            "financial_impact": issue.financial_impact,
            "issue_date": issue.issue_date.isoformat(),
            **score_data
        })

    # Rank by relevance descending
    scored_context.sort(
        key=lambda x: x["relevance"],
        reverse=True
    )

    # Prevent overload using Top-K filtering
    return scored_context[:top_k]
