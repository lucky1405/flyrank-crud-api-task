import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "tasks.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    create table if not exists tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        done INTEGER NOT NULL DEFAULT 0                   
    )
    """)

    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [
                ("Learn FastAPI", 0),
                ("Connect SQLite", 0),
                ("Complete FlyRank Assignment", 0),
            ],
        )

    conn.commit()
    conn.close()

def get_all_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("select * from tasks")
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"])
        }
        for row in rows
    ]

def get_task_by_id(task_id : id) :
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("select * from tasks where id = ?", (task_id,))

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None
    
    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }

def create_task_db(title : str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "insert into tasks (title,done) values (?,?)",
        (title,0)
    )
    task_id = cursor.lastrowid
    conn.commit()
    cursor.execute(
        "select * from tasks where id = ?",
        (task_id,)
    )
    row = cursor.fetchone()
    conn.close()

    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }

def update_task_db(task_id : int, title : str, done : bool):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
         """
        UPDATE tasks
        SET title = ?, done = ?
        WHERE id = ?
        """,
        (title, int(done), task_id)
    )

    if cursor.rowcount == 0:
        conn.close()
        return None
    
    conn.commit()
    cursor.execute(
        "select * from tasks where id = ?",
        (task_id,)
    )
    row = cursor.fetchone()
    conn.close()

    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }

def delete_task_db(task_id : int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "delete from tasks where id = ?",
        (task_id,)
    )
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted > 0