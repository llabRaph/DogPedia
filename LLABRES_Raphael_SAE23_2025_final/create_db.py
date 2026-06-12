# create_db.py
import sqlite3

DB_PATH = "SAE23.db"

def create_database():
    conn = sqlite3.connect(DB_PATH)
    with open("schema.sql", "r") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print(f"Database '{DB_PATH}' created successfully.")

if __name__ == "__main__":
    create_database()