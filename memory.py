# memory.py
import sqlite3
from datetime import datetime

DB = "assistant_memory.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS sessions (
                   session_id TEXT PRIMARY KEY,
                   created_at TEXT
                 )""")
    c.execute("""CREATE TABLE IF NOT EXISTS messages (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   session_id TEXT,
                   role TEXT,
                   content TEXT,
                   timestamp TEXT
                 )""")
    conn.commit()
    conn.close()

def add_message(session_id, role, content):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO sessions(session_id, created_at) VALUES(?,?)", (session_id, datetime.utcnow().isoformat()))
    c.execute("INSERT INTO messages(session_id, role, content, timestamp) VALUES(?,?,?,?)", (session_id, role, content, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

def get_history(session_id, limit=50):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT role, content, timestamp FROM messages WHERE session_id=? ORDER BY id DESC LIMIT ?", (session_id, limit))
    rows = c.fetchall()
    conn.close()
    return [{"role": r[0], "content": r[1], "ts": r[2]} for r in rows[::-1]]
