import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import uuid
from agents.orchestrator import run_workflow

st.set_page_config(page_title="AI IT Helpdesk", layout="wide")

st.title("🤖 AI-Powered IT Helpdesk System")

if "ticket_history" not in st.session_state:
    st.session_state.ticket_history = []

role = st.sidebar.selectbox("Select Role", ["User", "Admin"])

# ===========================
# USER VIEW
# ===========================
if role == "User":

    st.subheader("🎫 Submit Support Ticket")

    ticket_id = str(uuid.uuid4())[:8]
    department = st.selectbox("Department", ["IT", "HR", "Finance"])
    issue_text = st.text_area("Describe the Issue")

    if st.button("Analyze Ticket"):

        with st.spinner("Analyzing your ticket... this may take 20-30 seconds"):
            result, logs = run_workflow(ticket_id, department, issue_text)

        # Logs
        st.subheader("🧠 Agent Execution Flow")
        for log in logs:
            st.write(f"• {log}")

        # Retrieved Sources
        st.subheader("📚 Retrieved Knowledge Sources")
        st.table(result["retrieved_sources"])

        # Resolution
        st.subheader("🛠 Resolution Plan")
        st.write(result["resolution"])

        # Status
        st.subheader("📌 Ticket Status")
        if result["status"] == "Closed":
            st.success("✅ Ticket Automatically Closed by AI")
        elif result["status"] == "Pending Review":
            st.warning("🔍 Ticket Queued for Human Review")
        else:
            st.error("🚨 Ticket Escalated to Human Support")

        # Decision Summary
        st.subheader("🚨 Decision Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Severity", result["severity"])
        col2.metric("LLM Confidence", f"{result['confidence']}/5")
        col3.metric("Scope", result["scope"])

        st.write(f"**Ticket ID:** {ticket_id}")
        st.write(f"**Category:** {result['category']}")
        st.write(f"**Decision:** {result['decision']}")
        st.write(f"**Reason:** {result['escalation_reason']}")

        # Save to session history
        st.session_state.ticket_history.append({
            "ticket_id": ticket_id,
            "department": department,
            "issue": issue_text,
            "severity": result["severity"],
            "scope": result["scope"],
            "category": result["category"],
            "resolution": result["resolution"],
            "status": result["status"],
            "confidence": result["confidence"],
            "decision": result["decision"],
            "escalation_reason": result["escalation_reason"]
        })

# ===========================
# ADMIN VIEW
# ===========================
elif role == "Admin":

    st.subheader("📊 Admin Dashboard")

    if st.session_state.ticket_history:

        total = len(st.session_state.ticket_history)
        auto_resolved = sum(1 for t in st.session_state.ticket_history if t["status"] == "Closed")
        escalated = sum(1 for t in st.session_state.ticket_history if t["status"] == "Open - Escalated")
        review = sum(1 for t in st.session_state.ticket_history if t["status"] == "Pending Review")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Tickets", total)
        col2.metric("Auto-Resolved", auto_resolved)
        col3.metric("Pending Review", review)
        col4.metric("Escalated", escalated)

        st.divider()

        for ticket in st.session_state.ticket_history:
            with st.expander(f"Ticket ID: {ticket['ticket_id']} | {ticket['severity']} | {ticket['status']}"):
                st.write("**Department:**", ticket["department"])
                st.write("**Issue:**", ticket["issue"])
                st.write("**Category:**", ticket["category"])
                st.write("**Scope:**", ticket["scope"])
                st.write("**Resolution:**", ticket["resolution"])
                st.write("**Decision:**", ticket["decision"])
                st.write("**Reason:**", ticket["escalation_reason"])
                st.write("**LLM Confidence:**", f"{ticket['confidence']}/5")

    else:
        st.info("No tickets processed yet.")