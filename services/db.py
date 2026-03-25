import sqlite3
import json
import os
from pathlib import Path

DB_PATH = Path("workout_planner.db")

def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = _get_conn()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash BLOB NOT NULL,
            salt BLOB NOT NULL,
            name TEXT,
            preferences_json TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_user(username: str, password_hash: bytes, salt: bytes, name: str = "") -> bool:
    try:
        conn = _get_conn()
        c = conn.cursor()
        c.execute('''
            INSERT INTO users (username, password_hash, salt, name, preferences_json)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, password_hash, salt, name, '{}'))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def get_user(username: str) -> sqlite3.Row:
    conn = _get_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    return user

def update_preferences(username: str, preferences: dict) -> bool:
    try:
        conn = _get_conn()
        c = conn.cursor()
        prefs_json = json.dumps(preferences)
        c.execute('UPDATE users SET preferences_json = ? WHERE username = ?', (prefs_json, username))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating preferences: {e}")
        return False

# Initialize the database on import
init_db()
