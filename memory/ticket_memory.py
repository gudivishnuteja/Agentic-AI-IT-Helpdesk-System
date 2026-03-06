import json
import os

MEMORY_FILE = "ticket_memory.json"


def save_ticket(ticket):

    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "w") as f:
            json.dump([], f)

    with open(MEMORY_FILE, "r") as f:
        data = json.load(f)

    data.append(ticket)

    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)