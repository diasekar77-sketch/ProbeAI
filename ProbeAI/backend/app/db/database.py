import sqlite3
import json
import os

class SessionManager:
    def __init__(self, db_path="probeai_sessions.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                title TEXT,
                messages TEXT
            )
            """
        )
        conn.commit()
        conn.close()

    def list_sessions(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT session_id, title FROM sessions ORDER BY rowid DESC")
        rows = cursor.fetchall()
        conn.close()
        return [{"session_id": r[0], "title": r[1]} for r in rows]

    def get_session(self, session_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT messages FROM sessions WHERE session_id = ?", (session_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"messages": json.loads(row[0])}
        return None

    def save_session(self, session_id, title, messages):
        import uuid
        if not session_id:
            session_id = str(uuid.uuid4())
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO sessions (session_id, title, messages)
            VALUES (?, ?, ?)
            """,
            (session_id, title, json.dumps(messages))
        )
        conn.commit()
        conn.close()
        return session_id

    def delete_session(self, session_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
        conn.commit()
        conn.close()

    def clear_sessions(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sessions")
        conn.commit()
        conn.close()