import json
import re
from huggingface_hub import InferenceClient

client = InferenceClient(
    model="Qwen/Qwen2.5-72B-Instruct",
    token=""
)


def classify_ticket(issue_text: str) -> dict:

    prompt = """You are an IT support triage specialist. Classify this support ticket strictly.

SEVERITY LEVELS:
- High: ANY of these: security breach, phishing, malware, data loss, credentials compromised, infrastructure down, affects multiple users
- Medium: Blocks one user's core work function, VPN issues, software not working
- Low: Minor inconvenience, cosmetic issues, workaround exists

SCOPE:
- individual: only one person is affected
- team: a group or department is affected
- company-wide: entire organization is affected

CATEGORY EXAMPLES:
- auth: login failures, password issues, VPN authentication, account lockout
- security: phishing, malware, suspicious emails, credentials stolen, data breach
- connectivity: network down, wifi issues, internet not working
- hardware: physical device issues, screen damage, keyboard broken
- software: application crashes, software not opening, update failures
- infrastructure: server down, shared drive unavailable, email server issues
- other: anything that doesn't fit above

CRITICAL RULES:
- Phishing + credentials entered = High severity + security category
- "entire team", "all users", "everyone", "12 people", "whole department" = team or company-wide scope
- Multiple users affected = High severity
- Shared drive, server, infrastructure down = infrastructure category
- If scope is team or company-wide, severity must be High
- Reply ONLY with valid JSON, no explanation, no markdown

Ticket: """ + issue_text + """

JSON:
{
  "severity": "Medium",
  "scope": "individual",
  "category": "other",
  "reason": "one sentence explanation"
}
"""

    response = client.chat_completion(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.1
    )

    message = response.choices[0].message
    content = message.content or ""
    reasoning = getattr(message, "reasoning_content", "") or ""

    if not content.strip():
        content = reasoning

    # Remove reasoning blocks
    content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()

    try:

        json_match = re.search(r'\{.*\}', content, re.DOTALL)

        if not json_match:
            raise ValueError("No JSON found")

        result = json.loads(json_match.group())

        # Ensure required fields exist
        result.setdefault("severity", "Medium")
        result.setdefault("scope", "individual")
        result.setdefault("category", "other")
        result.setdefault("reason", "No reason provided")

        # Validate values
        assert result["severity"] in ["High", "Medium", "Low"]
        assert result["scope"] in ["individual", "team", "company-wide"]

        # Policy rule: multi-user cannot be low severity
        if result["scope"] in ["team", "company-wide"] and result["severity"] == "Low":
            result["severity"] = "Medium"
            result["reason"] += " (upgraded: multi-user scope detected)"

        # -----------------------------
        # Rule-based corrections
        # -----------------------------

        issue_lower = issue_text.lower()

        # Authentication issues
        if any(word in issue_lower for word in [
            "password",
            "forgot password",
            "reset password",
            "login",
            "log in",
            "sign in",
            "cannot login",
            "cannot log in",
            "authentication",
            "account locked"
        ]):
            result["category"] = "auth"

        # Connectivity issues
        if any(word in issue_lower for word in [
            "wifi",
            "internet",
            "network",
            "vpn connection",
            "cannot connect"
        ]):
            result["category"] = "connectivity"

        # Hardware issues
        if any(word in issue_lower for word in [
            "keyboard broken",
            "screen cracked",
            "laptop not turning on",
            "hardware failure"
        ]):
            result["category"] = "hardware"

        # Infrastructure issues
        if any(word in issue_lower for word in [
            "server down",
            "shared drive",
            "file server",
            "exchange server"
        ]):
            result["category"] = "infrastructure"

        # Upgrade severity if authentication blocks work
        if result["category"] == "auth" and result["severity"] == "Low":
            result["severity"] = "Medium"

        return result

    except Exception as e:

        return {
            "severity": "Medium",
            "scope": "individual",
            "category": "other",
            "reason": f"Classification failed ({str(e)}), defaulting to Medium"
        }