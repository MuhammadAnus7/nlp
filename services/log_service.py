"""Event logging service."""
import json
from database.db import session


def log_event(event_type: str, message: str, metadata: dict | None = None):
    with session() as conn:
        conn.execute(
            "INSERT INTO logs(event_type, event_message, metadata) VALUES (?, ?, ?)",
            (event_type, message, json.dumps(metadata or {})),
        )
