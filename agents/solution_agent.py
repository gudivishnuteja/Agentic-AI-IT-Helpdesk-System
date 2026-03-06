import re
from huggingface_hub import InferenceClient

client = InferenceClient(
    model="Qwen/Qwen2.5-72B-Instruct",
    token=""
)


def generate_solution(issue_text: str, retrieved_docs: list):

    if not retrieved_docs:
        return "No relevant knowledge base information found.", 1

    # Only use chunks from the top matching document to avoid mixing sources
    top_source = retrieved_docs[0].get("source", "") or retrieved_docs[0].get("metadata", {}).get("source", "")
    filtered_docs = [
        doc for doc in retrieved_docs
        if (doc.get("source", "") or doc.get("metadata", {}).get("source", "")) == top_source
    ]

    if not filtered_docs:
        filtered_docs = retrieved_docs[:2]

    context = "\n\n".join([doc["content"] for doc in filtered_docs[:3]])

    prompt = f"""You are an IT support assistant. Read the knowledge base below and answer the issue.

STRICT RULES:
- Output ONLY the fields below, nothing else
- Do NOT output any thinking, reasoning, or explanation before the fields
- Do NOT say "Okay" or "Let me" or any preamble
- Follow the exact sequence of steps from the knowledge base
- Do not skip steps or jump ahead in the process
- Do not summarize or compress steps — keep each step detailed
- Output ONLY the steps that exist in the knowledge base
- Do NOT add placeholder steps like "[No additional steps]" if there are no more steps
- Stop after the last real step
- NEVER say contact support or escalate
- Only use content from the knowledge base provided below

Issue: {issue_text}

Knowledge Base:
{context}

OUTPUT EXACTLY IN THIS FORMAT:

Problem Summary:
[one sentence describing the problem]

Likely Cause:
[one sentence describing the cause]

Step-by-Step Resolution:

Step 1.
[full action from knowledge base]

Step 2.
[full action from knowledge base]

[continue only if more steps exist in the knowledge base, stop when done]

CONFIDENCE: [1-5]"""

    try:
        response = client.chat_completion(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=0.1
        )
        message = response.choices[0].message
        content = message.content or ""
        reasoning = getattr(message, "reasoning_content", "") or ""

        if not content.strip():
            content = reasoning

        # Strip thinking tags
        content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()

        # Strip any preamble before "Problem Summary"
        summary_start = re.search(r'Problem Summary:', content, re.IGNORECASE)
        if summary_start:
            content = content[summary_start.start():]

        # Remove placeholder steps
        content = re.sub(r'\nStep \d+\.\s*\[No additional steps.*?\]', '', content, flags=re.IGNORECASE)
        content = re.sub(r'\nStep \d+\.\s*\[.*?not.*?knowledge base.*?\]', '', content, flags=re.IGNORECASE)

    except Exception as e:
        content = f"Problem Summary:\nUnable to generate solution.\n\nLikely Cause:\nSystem error: {str(e)}\n\nStep-by-Step Resolution:\n\nStep 1.\nPlease contact IT helpdesk directly."

    # Extract confidence
    match = re.search(r'CONFIDENCE[^:]*:\s*([1-5])', content, re.IGNORECASE)
    confidence = int(match.group(1)) if match else 3

    # Remove confidence line from displayed solution
    solution_text = re.sub(r'\nCONFIDENCE.*', '', content, flags=re.MULTILINE | re.IGNORECASE).strip()

    return solution_text, confidence