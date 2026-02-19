from datetime import datetime, timedelta
from .models import QualityIssue


def apply_lifecycle_rules(db):
    """
    Marks issues older than 1 year as dormant.
    """

    cutoff_date = datetime.utcnow() - timedelta(days=365)

    old_issues = db.query(QualityIssue).filter(
        QualityIssue.issue_date < cutoff_date,
        QualityIssue.status == "active"
    ).all()

    for issue in old_issues:
        issue.status = "dormant"

    db.commit()
