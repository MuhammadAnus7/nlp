"""Analytics aggregations for dashboard charts."""
from database.db import session


def get_dashboard_metrics():
    with session() as conn:
        by_department = [dict(row) for row in conn.execute(
            "SELECT department AS label, COUNT(*) AS value FROM complaints GROUP BY department"
        ).fetchall()]
        by_priority = [dict(row) for row in conn.execute(
            "SELECT priority AS label, COUNT(*) AS value FROM complaints GROUP BY priority"
        ).fetchall()]
        response_time = [dict(row) for row in conn.execute(
            """
            SELECT DATE(created_at) AS label,
                   AVG((julianday(COALESCE(resolved_at, CURRENT_TIMESTAMP)) - julianday(created_at)) * 24) AS value
            FROM complaints
            GROUP BY DATE(created_at)
            ORDER BY DATE(created_at)
            """
        ).fetchall()]
        trend = [dict(row) for row in conn.execute(
            "SELECT DATE(created_at) AS label, COUNT(*) AS value FROM complaints GROUP BY DATE(created_at) ORDER BY DATE(created_at)"
        ).fetchall()]

    return {
        "department": by_department,
        "priority": by_priority,
        "response_time": response_time,
        "trend": trend,
    }
