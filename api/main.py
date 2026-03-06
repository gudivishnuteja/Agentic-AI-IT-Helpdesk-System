import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from pydantic import BaseModel
from agents.orchestrator import run_workflow

app = FastAPI()


class TicketRequest(BaseModel):
    ticket_id: str
    department: str
    issue: str


@app.post("/analyze")
def analyze(ticket: TicketRequest):
    result, logs = run_workflow(ticket.ticket_id, ticket.department, ticket.issue)
    return {
        "result": result,
        "reasoning": logs
    }