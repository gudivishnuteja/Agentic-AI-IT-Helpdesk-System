
# 🤖 AI-Powered IT Helpdesk System (RAG-Based Multi-Agent Architecture)

An AI-driven IT Helpdesk system that automatically analyzes support
tickets, retrieves solutions from enterprise IT documentation, generates
structured troubleshooting steps using Large Language Models, and
determines whether the issue can be automatically resolved or escalated
to human support.

This project demonstrates how **Retrieval-Augmented Generation (RAG)**
combined with **multi-agent workflows** can automate IT support
operations.

------------------------------------------------------------------------

# 🚀 Features

-   AI-based support ticket analysis
-   Multi-agent workflow architecture
-   Knowledge retrieval using vector similarity search
-   Step-by-step troubleshooting generation
-   Automatic risk evaluation and escalation
-   Admin dashboard for monitoring tickets

------------------------------------------------------------------------

# 🧠 System Workflow

User submits a ticket → Classification Agent → Retrieval Agent →
Solution Agent → Risk Agent → Ticket Decision

**Possible outcomes** - Auto-Resolved - Pending Review - Escalated to
Human Support

------------------------------------------------------------------------

# ⚙️ Tech Stack

  Component         Technology
  ----------------- ----------------------------------------
  Frontend          Streamlit
  Backend           Python
  LLM               Qwen2.5-72B-Instruct (HuggingFace API)
  Vector Database   ChromaDB
  Embedding Model   BAAI/bge-m3
  Framework         LangChain
  Knowledge Base    Enterprise IT Troubleshooting PDFs

------------------------------------------------------------------------

# 🤖 Agents

## Classification Agent

Analyzes the support ticket and determines: - Severity - Scope -
Category

## Retrieval Agent

Searches the knowledge base using vector similarity search in
**ChromaDB**.

## Solution Agent

Uses the **LLM** to generate a structured troubleshooting solution using
retrieved documents.

## Risk Agent

Evaluates: - Similarity score - Severity - LLM confidence

Then decides whether to: - Auto-resolve - Send to review queue -
Escalate to human support

------------------------------------------------------------------------

# 📂 Project Structure

    ai-it-helpdesk/
    │
    ├── agents/
    │   ├── classification_agent.py
    │   ├── retrieval_agent.py
    │   ├── solution_agent.py
    │   ├── risk_agent.py
    │   └── orchestrator.py
    │
    ├── rag/
    │   └── vector_store.py
    │
    ├── data/
    │   └── IT troubleshooting PDFs
    │
    ├── chroma_db/
    │
    ├── app.py
    ├── requirements.txt
    └── README.md

------------------------------------------------------------------------

# 🛠️ Setup Instructions

## 1. Clone the Repository

    git clone https://github.com/yourusername/ai-it-helpdesk.git
    cd ai-it-helpdesk

## 2. Create Virtual Environment

    python -m venv venv

Activate environment:

Windows

    venv\Scripts\activate

Mac/Linux

    source venv/bin/activate

------------------------------------------------------------------------

## 3. Install Dependencies

    pip install -r requirements.txt

------------------------------------------------------------------------

## 4. Add Knowledge Base Documents

Place all troubleshooting PDF documents inside:

    data/

Example documents: - Email Troubleshooting Guide - VPN Troubleshooting
Guide - Hardware Troubleshooting Guide - Security Incident Guide -
Password Reset Guide

------------------------------------------------------------------------

## 5. Build the Vector Database

Run the document ingestion script to create embeddings and store them in
ChromaDB.

    python ingest_documents.py

This will: - Load PDF documents - Split them into chunks - Generate
embeddings - Store them in the **ChromaDB vector database**

------------------------------------------------------------------------

## 6. Run the Application

    streamlit run app.py

Open the browser at:

    http://localhost:8501

------------------------------------------------------------------------

# 🧪 Example Demo Queries

    Emails are stuck in Outlook Outbox and not sending

    VPN authentication failed after password change

    Laptop screen flickering and showing horizontal lines

    I clicked a phishing email link and entered my password

------------------------------------------------------------------------

# 📊 Example Ticket Outcomes

  Scenario                            Result
  ----------------------------------- ----------------
  Common issue with strong KB match   Auto-Resolved
  Moderate similarity                 Pending Review
  Security or high severity issue     Escalated

------------------------------------------------------------------------

# 📌 Author

**Gudi Vishnu Teja**

AI / Machine Learning Enthusiast\
Focused on LLMs, RAG systems, and AI automation.
