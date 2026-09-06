"""Project Volusia — Gamification module for the FastAPI backend.
Tracks user engagement via a lightweight leaderboard, achievements,
streaks, and XP. All state lives in the SQLite DB (no separate server)."""
import time
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import sqlite3, json
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "volusia.db"

# ---------------------------------------------------------------------------
# XP multipliers — tied to data-source difficulty (mirrors refresh_v2.py)
# ---------------------------------------------------------------------------
SOURCE_XP = {
    "US Census ACS 5-Year DP03": 10,
    "US Census ACS 5-Year DP05": 10,
    "Census PEP": 8,
    "BLS LAUS": 12,
    "BLS QCEW": 12,
    "BEA Regional": 15,
    "NOAA NCEI": 8,
    "C2ER (Daytona Beach, cached)": 6,
    "Volusia County CVB": 20,
    "Census ACS DP03 (C2ER proxy)": 6,
}

ACHIEVEMENTS = {
    "first_visit":       {"name": "First Visit",        "desc": "View the portal for the first time",      "icon": "🎯", "xp": 5},
    "explorer_first":    {"name": "Explorer",            "desc": "Visit the Data Explorer page",            "icon": "🔍", "xp": 10},
    "maps_first":        {"name": "Cartographer",        "desc": "Visit the Maps page",                     "icon": "🗺️", "xp": 10},
    "business_first":    {"name": "Entrepreneur",        "desc": "Visit the Business page",                 "icon": "📊", "xp": 10},
    "residents_first":   {"name": "Neighbor",            "desc": "Visit the Residents page",                "icon": "🏠", "xp": 10},
    "tourists_first":    {"name": "Visitor",             "desc": "Visit the Tourists page",                 "icon": "🌊", "xp": 10},
    "leaders_first":     {"name": "Visionary",           "desc": "Visit the Leaders page",                  "icon": "🚀", "xp": 10},
    "data_download":     {"name": "Data Hoarder",        "desc": "Download a CSV dataset",                  "icon": "📥", "xp": 15},
    "refresh_triggered": {"name": "Pipeline Driver",     "desc": "Trigger a data refresh",                  "icon": "🔄", "xp": 25},
    "all_pages":         {"name": "Portal Master",       "desc": "Visit all 7 pages",                       "icon": "🏆", "xp": 50},
}

XP_PER_INDICATOR_VIEW = 3       # XP per indicator card viewed
XP_PER_DATASET_VIEW   = 2       # XP per dataset card viewed
XP_PER_MAP_LAYER      = 1       # XP per map layer viewed
STREAK_DAYS_BASE      = 2       # XP bonus per consecutive day

def _now() -> int:
    return int(time.time())

def _today() -> int:
    return int(time.time() // 86400)

def _xp_for_source(source: str) -> int:
    return SOURCE_XP.get(source, 5)

def _init_gamification_db(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS gamification (
        user_id TEXT PRIMARY KEY,
        total_xp INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1,
        streak_days INTEGER DEFAULT 0,
        last_active_date INTEGER DEFAULT 0,
        pages_visited TEXT DEFAULT '[]',
        achievements TEXT DEFAULT '[]',
        indicators_viewed INTEGER DEFAULT 0,
        datasets_downloaded INTEGER DEFAULT 0,
        refresh_triggered INTEGER DEFAULT 0,
        created_at INTEGER,
        updated_at INTEGER
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS gamification_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        event_type TEXT,
        detail TEXT,
        xp_earned INTEGER,
        timestamp INTEGER
    )""")
    conn.commit()

def _get_or_create(conn: sqlite3.Connection, user_id: str) -> dict:
    cur = conn.cursor()
    cur.execute("SELECT * FROM gamification WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    if row:
        return dict(row)
    now = _now()
    cur.execute("""INSERT INTO gamification
        (user_id, total_xp, level, streak_days, last_active_date, pages_visited,
         achievements, indicators_viewed, datasets_downloaded, refresh_triggered,
         created_at, updated_at)
        VALUES (?, 0, 1, 0, 0, '[]', '[]', 0, 0, 0, ?, ?)""",
        (user_id, now, now))
    conn.commit()
    return _get_or_create(conn, user_id)

def _compute_level(total_xp: int) -> int:
    # Level = floor(sqrt(total_xp / 100)) + 1, min 1
    import math
    return max(1, int(math.isqrt(total_xp // 100)) + 1)

def _add_xp(conn: sqlite3.Connection, user_id: str, xp: int, reason: str) -> int:
    """Add XP, return the earned amount (capped at 200/session to prevent abuse)."""
    if xp <= 0:
        return 0
    user = _get_or_create(conn, user_id)
    earned = min(xp, 200)  # session cap
    conn.execute("UPDATE gamification SET total_xp = total_xp + ?, updated_at = ? WHERE user_id = ?",
                 (earned, _now(), user_id))
    conn.execute("""INSERT INTO gamification_history (user_id, event_type, detail, xp_earned, timestamp)
                    VALUES (?, ?, ?, ?, ?)""",
                 (user_id, "xp", reason, earned, _now()))
    conn.commit()
    return earned

def _record_event(conn: sqlite3.Connection, user_id: str, event_type: str, detail: str = ""):
    conn.execute("""INSERT INTO gamification_history (user_id, event_type, detail, xp_earned, timestamp)
                    VALUES (?, ?, ?, 0, ?)""",
                 (user_id, event_type, detail, _now()))
    conn.commit()

def _update_streak(conn: sqlite3.Connection, user_id: str) -> int:
    """Return bonus XP from streak."""
    user = _get_or_create(conn, user_id)
    today = _today()
    last = user.get("last_active_date", 0) or 0
    streak = user.get("streak_days", 0) or 0
    if last == 0:
        streak = 0
    elif last == today:
        streak = streak  # same day, no change
    elif last == today - 1:
        streak = streak + 1
    else:
        streak = 0
    bonus = streak * STREAK_DAYS_BASE
    conn.execute("""UPDATE gamification SET last_active_date = ?, streak_days = ?, updated_at = ?
                    WHERE user_id = ?""",
                 (today, streak, _now(), user_id))
    conn.commit()
    return bonus

def _check_achievements(conn: sqlite3.Connection, user_id: str, new_pages: list) -> list:
    """Check and return newly unlocked achievements with their XP."""
    cur = conn.cursor()
    cur.execute("SELECT pages_visited, achievements FROM gamification WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    if not row:
        return []
    pages_raw = row[0]
    achieved_raw = row[1]
    pages = json.loads(pages_raw) if pages_raw else []
    achieved = json.loads(achieved_raw) if achieved_raw else []
    new_unlocks = []
    for pid, ach in ACHIEVEMENTS.items():
        if pid in achieved:
            continue
        if _check_condition(pid, pages):
            achieved.append(pid)
            new_unlocks.append((pid, ach))
    if achieved:
        conn.execute("UPDATE gamification SET achievements = ?, updated_at = ? WHERE user_id = ?",
                     (json.dumps(achieved), _now(), user_id))
        conn.commit()
    return new_unlocks

def _check_condition(pid: str, pages: list) -> bool:
    """Check if a page visit satisfies an achievement condition."""
    if pid == "first_visit":
        return len(pages) >= 1
    if pid == "explorer_first" and "/data" in pages:
        return True
    if pid == "maps_first" and "/maps" in pages:
        return True
    if pid == "business_first" and "/business" in pages:
        return True
    if pid == "residents_first" and "/residents" in pages:
        return True
    if pid == "tourists_first" and "/tourists" in pages:
        return True
    if pid == "leaders_first" and "/leaders" in pages:
        return True
    if pid == "all_pages":
        required = ["/", "/data", "/maps", "/business", "/residents", "/tourists", "/leaders"]
        return all(p in pages for p in required)
    return False

def _get_leaderboard(conn: sqlite3.Connection, limit: int = 20) -> list:
    cur = conn.cursor()
    cur.execute("""SELECT user_id, total_xp, level, streak_days, indicators_viewed, datasets_downloaded
                   FROM gamification ORDER BY total_xp DESC LIMIT ?""", (limit,))
    return [dict(r) for r in cur.fetchall()]

def _get_history(conn: sqlite3.Connection, user_id: str, limit: int = 30) -> list:
    cur = conn.cursor()
    cur.execute("""SELECT event_type, detail, xp_earned, timestamp FROM gamification_history
                   WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?""", (user_id, limit))
    return [dict(r) for r in cur.fetchall()]

def get_gamification_routes(app: FastAPI):
    """Register all gamification endpoints on the given FastAPI app."""

    @app.get("/gamification/profile/{user_id}")
    def profile(user_id: str):
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        try:
            user = _get_or_create(conn, user_id)
            conn.close()
            pages = json.loads(user.get("pages_visited") or "[]")
            achieved = json.loads(user.get("achievements") or "[]")
            return {
                "user_id": user_id,
                "total_xp": user["total_xp"] or 0,
                "level": user["level"] or 1,
                "streak_days": user["streak_days"] or 0,
                "last_active_date": user["last_active_date"] or 0,
                "pages_visited": pages,
                "achievements_unlocked": achieved,
                "indicators_viewed": user["indicators_viewed"] or 0,
                "datasets_downloaded": user["datasets_downloaded"] or 0,
                "refresh_triggered": user["refresh_triggered"] or 0,
            }
        except Exception:
            conn.close()
            raise

    @app.post("/gamification/visit/{user_id}")
    def visit_page(user_id: str, payload: dict = None):
        """Record a page visit. Returns XP earned and new achievements."""
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        try:
            page = (payload or {}).get("page", "")
            streak_bonus = _update_streak(conn, user_id)
            # Update pages visited
            cur = conn.cursor()
            cur.execute("SELECT pages_visited FROM gamification WHERE user_id = ?", (user_id,))
            row = cur.fetchone()
            pages = json.loads(row[0] or "[]") if row else []
            if page and page not in pages:
                pages.append(page)
                cur.execute("UPDATE gamification SET pages_visited = ?, updated_at = ? WHERE user_id = ?",
                            (json.dumps(pages), _now(), user_id))
            _record_event(conn, user_id, "page_visit", page)
            conn.commit()
            # Check achievements
            new_ach = _check_achievements(conn, user_id, [page] if page else [])
            # Compute total XP earned this visit
            conn2 = sqlite3.connect(str(DB_PATH))
            conn2.row_factory = sqlite3.Row
            cur2 = conn2.cursor()
            cur2.execute("SELECT total_xp FROM gamification WHERE user_id = ?", (user_id,))
            total = cur2.fetchone()["total_xp"] or 0
            level = _compute_level(total)
            conn2.close()
            conn.close()
            return {
                "xp_earned": streak_bonus * XP_PER_INDICATOR_VIEW,
                "streak_bonus_days": streak_bonus,
                "level": level,
                "new_achievements": [{"id": pid, **a} for pid, a in new_ach],
            }
        except Exception:
            conn.close()
            raise

    @app.post("/gamification/xp/{user_id}")
    def add_xp(user_id: str, payload: dict = None):
        """Award XP for an action (indicator view, dataset download, etc.)."""
        conn = sqlite3.connect(str(DB_PATH))
        try:
            action = (payload or {}).get("action", "")
            source = (payload or {}).get("source", "")
            xp = _xp_for_source(source)
            if action == "indicator_view":
                xp = XP_PER_INDICATOR_VIEW
            elif action == "dataset_download":
                xp = XP_PER_DATASET_VIEW
            elif action == "map_layer_view":
                xp = XP_PER_MAP_LAYER
            elif action == "refresh":
                xp = 25
            earned = _add_xp(conn, user_id, xp, f"{action} via {source}")
            streak_bonus = _update_streak(conn, user_id)
            total = conn.execute("SELECT total_xp FROM gamification WHERE user_id = ?", (user_id,)).fetchone()[0]
            level = _compute_level(total)
            conn.close()
            return {"xp_earned": earned, "streak_bonus": streak_bonus, "total_xp": total, "level": level}
        except Exception:
            conn.close()
            raise

    @app.get("/gamification/achievements/{user_id}")
    def achievements(user_id: str):
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        try:
            cur = conn.cursor()
            cur.execute("SELECT achievements FROM gamification WHERE user_id = ?", (user_id,))
            row = cur.fetchone()
            unlocked = json.loads(row[0] or "[]") if row else []
            # Build full list with unlocked status
            result = []
            for pid, ach in ACHIEVEMENTS.items():
                result.append({
                    "id": pid, "name": ach["name"], "desc": ach["desc"],
                    "icon": ach["icon"], "xp": ach["xp"],
                    "unlocked": pid in unlocked,
                })
            conn.close()
            return {"achievements": result, "unlocked_count": len(unlocked), "total_count": len(ACHIEVEMENTS)}
        except Exception:
            conn.close()
            raise

    @app.get("/gamification/leaderboard")
    def leaderboard(limit: int = Query(20)):
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        try:
            rows = _get_leaderboard(conn, limit)
            conn.close()
            return {"leaderboard": rows, "count": len(rows)}
        except Exception:
            conn.close()
            raise

    @app.get("/gamification/history/{user_id}")
    def history(user_id: str, limit: int = Query(30)):
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        try:
            rows = _get_history(conn, user_id, limit)
            conn.close()
            return {"history": rows, "count": len(rows)}
        except Exception:
            conn.close()
            raise

    @app.get("/gamification/stats/{user_id}")
    def stats(user_id: str):
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        try:
            cur = conn.cursor()
            # Total users
            cur.execute("SELECT COUNT(*) FROM gamification")
            total_users = cur.fetchone()[0]
            # Average stats
            cur.execute("SELECT AVG(total_xp), AVG(level), AVG(streak_days) FROM gamification")
            row = cur.fetchone()
            avg_xp = round(row[0] or 0, 1)
            avg_level = round(row[1] or 0, 1)
            avg_streak = round(row[2] or 0, 1)
            # Total visits = count distinct users with pages_visited
            cur.execute("SELECT COUNT(*) FROM gamification")
            total_visits = cur.fetchone()[0]
            conn.close()
            return {
                "total_users": total_users,
                "avg_xp": avg_xp,
                "avg_level": avg_level,
                "avg_streak": avg_streak,
                "total_visits": total_visits,
            }
        except Exception:
            conn.close()
            raise

    return get_gamification_routes