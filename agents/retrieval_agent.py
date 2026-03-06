from rag.vector_store import get_vector_db


def retrieve_documents(query: str, k: int = 5) -> tuple[list, float, float]:
    db = get_vector_db()

    results = db.similarity_search_with_score(query, k=10)

    retrieved_docs = []
    scores = []

    for doc, distance in results:
        similarity = round(1 - (distance / 2), 4)

        if similarity < 0.45:
            continue

        retrieved_docs.append({
            "content": doc.page_content,
            "source": doc.metadata.get("source", "Unknown"),
            "similarity": similarity
        })
        scores.append(similarity)

    retrieved_docs = retrieved_docs[:k]
    scores = scores[:k]

    if not scores:
        return [], 0.0, 0.0

    avg_similarity = round(sum(scores) / len(scores), 4)
    best_similarity = round(max(scores), 4)

    return retrieved_docs, avg_similarity, best_similarity