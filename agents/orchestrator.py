from agents.classification_agent import classify_ticket
from agents.retrieval_agent import retrieve_documents
from agents.solution_agent import generate_solution
from agents.risk_agent import evaluate_risk
from memory.ticket_memory import save_ticket


def run_workflow(ticket_id, department, issue_text):

    logs = []

    # 1. Classification
    logs.append("Classification Agent running...")
    classification = classify_ticket(issue_text)
    severity = classification["severity"]
    scope = classification["scope"]
    category = classification["category"]
    logs.append(f"Severity: {severity} | Scope: {scope} | Category: {category}")

    # 2. Retrieval
    logs.append("Retrieval Agent querying ChromaDB...")
    retrieved_docs, avg_similarity, best_similarity = retrieve_documents(issue_text)
    logs.append(f"Avg Similarity: {avg_similarity} | Best Similarity: {best_similarity}")

    # 3. Solution Generation
    logs.append("Solution Agent generating resolution...")
    resolution, confidence = generate_solution(issue_text, retrieved_docs)
    logs.append(f"LLM Confidence: {confidence}/5")

    # 4. Risk Evaluation
    logs.append("Risk Agent evaluating confidence...")
    decision, reason = evaluate_risk(
        avg_similarity=avg_similarity,
        best_similarity=best_similarity,
        severity=severity,
        confidence=confidence,
        scope=scope
    )
    logs.append(f"Decision: {decision} | Reason: {reason}")

    # 5. Ticket Status
    if decision == "Auto-Resolved":
        ticket_status = "Closed"
    elif decision == "Review Queue":
        ticket_status = "Pending Review"
    else:
        ticket_status = "Open - Escalated"

    # 6. Save Ticket
    ticket_data = {
        "ticket_id": ticket_id,
        "department": department,
        "issue": issue_text,
        "severity": severity,
        "scope": scope,
        "category": category,
        "avg_similarity": avg_similarity,
        "best_similarity": best_similarity,
        "confidence": confidence,
        "decision": decision,
        "escalation_reason": reason,
        "status": ticket_status,
        "resolution": resolution
    }

    save_ticket(ticket_data)

    # 7. Return result
    result = {
        "resolution": resolution,
        "decision": decision,
        "escalation_reason": reason,
        "confidence": confidence,
        "status": ticket_status,
        "severity": severity,
        "scope": scope,
        "category": category,
        "retrieved_sources": [
            {
                "document": doc["source"],
                "similarity": doc["similarity"]
            }
            for doc in retrieved_docs
        ]
    }

    return result, logs