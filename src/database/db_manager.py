import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data', 'totem.db')

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    print(f"DEBUG: Connecting to DB at {os.path.abspath(DB_PATH)}")
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database with the necessary tables."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            sensor_type TEXT NOT NULL,
            value TEXT,
            duration REAL
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

def log_interaction(sensor_type, value, duration=0.0):
    """Logs a new interaction to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO interactions (timestamp, sensor_type, value, duration)
        VALUES (?, ?, ?, ?)
    ''', (datetime.now(), sensor_type, str(value), duration))
    
    conn.commit()
    conn.close()
    # print(f"Logged: {sensor_type} - {value}")

if __name__ == "__main__":
    init_db()
