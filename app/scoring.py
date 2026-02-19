import math
from datetime import datetime

# Controls how fast memory decays
LAMBDA = 0.02


def compute_temporal_score(issue_date):
    """
    Exponential decay function
    More recent events get higher score
    """
    days = (datetime.utcnow() - issue_date).days
    return math.exp(-LAMBDA * days)


def compute_relevance(issue):
    """
    Combines temporal, severity, and financial impact
    """

    temporal_score = compute_temporal_score(issue.issue_date)

    # Normalize severity (1–10 → 0–1)
    severity_score = issue.severity / 10

    # Normalize financial impact (cap at 1)
    impact_score = min(issue.financial_impact / 100000, 1)

    relevance_score = (
        0.4 * temporal_score +
        0.4 * severity_score +
        0.2 * impact_score
    )

    return {
        "relevance": round(relevance_score, 3),
        "temporal_score": round(temporal_score, 3),
        "severity_score": round(severity_score, 3),
        "impact_score": round(impact_score, 3)
    }
