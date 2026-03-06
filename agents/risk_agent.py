def evaluate_risk(
    avg_similarity: float,
    best_similarity: float,
    severity: str,
    confidence: int,
    scope: str
) -> tuple[str, str]:

    if severity == "High":
        return "Escalated to Human Support", "high_severity_policy"

    if scope == "company-wide":
        return "Escalated to Human Support", "company_wide_scope"

    # Strong KB match — auto-resolve regardless of LLM confidence
    if best_similarity >= 0.70 and avg_similarity >= 0.65:
        return "Auto-Resolved", "high_similarity_override"

    # Good KB match — auto-resolve
    if best_similarity >= 0.65 and avg_similarity >= 0.60:
        return "Auto-Resolved", "good_similarity_override"

    # Moderate KB match with good confidence
    if avg_similarity >= 0.60 and confidence >= 3:
        return "Auto-Resolved", "good_similarity_high_confidence"

    # Low similarity — escalate
    if best_similarity < 0.55:
        return "Escalated to Human Support", "no_relevant_documents"

    # Everything else — review queue
    if avg_similarity >= 0.50 and severity in ["Low", "Medium"]:
        return "Review Queue", "moderate_confidence_needs_review"

    return "Escalated to Human Support", "insufficient_signal"