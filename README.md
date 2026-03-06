
# AIOps Copilot – Enterprise Agentic RAG System

## Setup

1. Install Ollama
   ollama pull llama3

2. Install dependencies
   pip install -r requirements.txt

3. Ingest Documents
   python -c "from rag.vector_store import ingest_documents; ingest_documents()"

4. Start API
   uvicorn api.main:app --reload

5. Start UI
   streamlit run ui/app.py
