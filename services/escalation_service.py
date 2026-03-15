"""Escalation checks for unresolved complaints."""
from database.db import session
from services.log_service import log_event


class EscalationService:
    @staticmethod
    def run_escalation_checks():
        with session() as conn:
            rows = conn.execute(
                """
                SELECT id, department, escalation_level,
                       CAST((julianday('now') - julianday(created_at)) * 24 AS INTEGER) AS open_hours
                FROM complaints
                WHERE status != 'RESOLVED'
                """
            ).fetchall()

            for row in rows:
                complaint_id = row["id"]
                open_hours = row["open_hours"]
                current_level = row["escalation_level"]

                if open_hours >= 24 and current_level < 2:
                    EscalationService._escalate(conn, complaint_id, current_level, 2, "Management", "Unresolved for 24+ hours")
                elif open_hours >= 8 and current_level < 1:
                    target = f"Senior {row['department']}"
                    EscalationService._escalate(conn, complaint_id, current_level, 1, target, "Unresolved for 8+ hours")

    @staticmethod
    def _escalate(conn, complaint_id: int, from_level: int, to_level: int, escalated_to: str, reason: str):
        conn.execute(
            "UPDATE complaints SET escalation_level=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
            (to_level, complaint_id),
        )
        conn.execute(
            "INSERT INTO escalation_history(complaint_id, from_level, to_level, escalated_to, reason) VALUES (?, ?, ?, ?, ?)",
            (complaint_id, from_level, to_level, escalated_to, reason),
        )
        log_event("COMPLAINT_ESCALATED", f"Complaint #{complaint_id} escalated", {"to": escalated_to})
