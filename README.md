#  Business Context Memory Engine (BCME)

##  Project Overview

The **Business Context Memory Engine (BCME)** is a production-style backend system that implements structured context and memory management for AI agents operating in business environments.

In real-world enterprise systems, decisions are rarely made in isolation. Human professionals rely on:

- Immediate transaction context  
- Historical performance records  
- Time-sensitive relevance  
- Experiential insights  

BCME models this layered contextual reasoning using structured storage, temporal decay, lifecycle management, and ranked retrieval mechanisms.

This project demonstrates how AI agents can:

- Persist contextual knowledge across interactions  
- Retrieve relevant historical data dynamically  
- Manage memory staleness and freshness  
- Prioritize important contextual signals  
- Generate explainable decision outputs  

---

# System Architecture

The system follows a modular production-style architecture:

```
Business Input (Invoice)
        ↓
Lifecycle Manager
        ↓
Context Retrieval Engine
        ↓
Relevance Scoring Engine
        ↓
Risk Aggregation
        ↓
Decision Recommendation
        ↓
Explainable Output
```

### Core Components

1. **FastAPI API Layer** – Exposes endpoints  
2. **SQLAlchemy ORM** – Manages database interactions  
3. **SQLite Database** – Stores structured business memory  
4. **Lifecycle Manager** – Handles staleness rules  
5. **Scoring Engine** – Computes contextual relevance  
6. **Retrieval Engine** – Ranks and filters memory  

---

#  Memory Model & Data Structures

BCME uses an entity-centric relational memory model.

## Entities Implemented

###  Supplier
Represents business partners.

- id  
- name  
- risk_score  

###  Invoice
Represents current transactional context.

- id  
- supplier_id  
- amount  
- created_at  

###  QualityIssue
Represents historical performance memory.

- id  
- supplier_id  
- invoice_id  
- severity (1–10 scale)  
- financial_impact  
- issue_date  
- status (active / dormant)  

---

#  Context Hierarchy & Relevance Model

Relevance Score is computed dynamically:

```
Relevance =
(0.4 × Temporal Score)
+ (0.4 × Severity Score)
+ (0.2 × Financial Impact Score)
```

---

##  Temporal Proximity

Recent events carry more influence.

Temporal score uses exponential decay:

```
Temporal Score = e^( -λ × age_in_days )
```

This ensures:

- Recent issues heavily influence decisions  
- Older issues gradually lose relevance  

---

##  Severity Weighting

Higher severity issues (1–10 scale) are normalized and weighted.

---

##  Financial Impact Weighting

Higher financial impact increases contextual importance.

---

## Conflict Resolution Strategy

If a supplier had issues in the past but recently improved:

- Temporal decay reduces influence of old issues  
- Recent issues dominate scoring  

This simulates human-like recency bias.

---

#   Memory Lifecycle Management

BCME automatically manages memory freshness.

## Lifecycle Rules

- Issues older than 365 days are marked as **dormant**  
- Dormant issues are excluded from retrieval  
- Lifecycle rules are applied automatically during invoice processing  

This ensures:

- Stale information does not bias decisions  
- Time-sensitive facts are handled correctly  

---

#  Retrieval Mechanism

The retrieval pipeline works as follows:

1. Identify supplier  
2. Fetch active historical issues  
3. Compute relevance score  
4. Rank by relevance  
5. Apply Top-K filtering (default: 3)  
6. Aggregate risk score  
7. Generate recommendation  

---

#  Risk Aggregation & Decision Logic

The system computes an aggregate risk score:

```
Average relevance of Top-K issues
```

Risk levels:

| Risk Score | Risk Level | Action |
|------------|------------|--------|
| ≤ 0.5 | Low | Approve |
| 0.5 – 0.75 | Medium | Require Quality Inspection |
| > 0.75 | High | Escalate to Procurement Head |

---

#  Explainability

Every decision includes:

- Risk score  
- Risk level  
- Recommendation  
- Context used  
- Individual scoring breakdown  

Example response:

```json
{
  "invoice_id": 1,
  "risk_score": 0.72,
  "risk_level": "Medium",
  "recommendation": "Require Quality Inspection",
  "context_used": [
    {
      "issue_id": 2,
      "relevance": 0.81,
      "temporal_score": 0.91,
      "severity_score": 0.8,
      "impact_score": 0.5
    }
  ]
}
```

---

#  Installation & Running

##  Clone Repository

```bash
git clone <repo_url>
cd business-context-memory-engine
```

##  Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

##  Install Dependencies

```bash
pip install -r requirements.txt
```

##  Run Application

```bash
uvicorn app.main:app --reload
```

Visit:

```
http://127.0.0.1:8000/docs
```

---

#  How to Test

1. Call `POST /seed`
2. Call `POST /process-invoice/1`
3. Observe ranked contextual output

---

#  Scalability Considerations

In production, the system can scale using:

- PostgreSQL with indexing  
- Graph databases for relationship modeling  
- Redis caching  
- Precomputed risk summaries  
- Entity partitioning  

---

#  Security Considerations

- Role-based access control  
- Audit logging  
- Sensitive data encryption  
- Masking personally identifiable information  

---

#  Future Enhancements

- Pattern memory (seasonal trends)  
- Semantic similarity scoring  
- Graph-based memory linking  
- Multi-agent contextual weighting  
- Distributed microservice deployment  

---

#  Assignment Coverage

This project satisfies:

- Memory Types & Structure  
- Context Hierarchy  
- Temporal Proximity  
- Memory Lifecycle Management  
- Retrieval & Ranking  
- Conflict Handling  
- Information Overload Prevention  
- Explainability  
- Scalability Discussion  

---

#  Key Takeaway

BCME demonstrates how structured memory architecture enables AI agents to approximate human-like contextual reasoning while maintaining scalability and explainability in business environments.
