import sqlite3
import os

# Automatically store the database file inside the database folder
DB_PATH = os.path.join(os.path.dirname(__file__), 'geovista.db')

def create_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            country TEXT,
            searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database and table created successfully at:", DB_PATH)

if __name__ == "__main__":
    create_db()
