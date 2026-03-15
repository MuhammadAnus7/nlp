"""Project-structure compatibility wrapper for database helpers."""
from database.db import get_connection, init_db, session

__all__ = ["get_connection", "init_db", "session"]
