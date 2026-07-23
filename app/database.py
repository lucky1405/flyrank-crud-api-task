import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row
    )

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    create table if not exists tasks (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        done BOOLEAN NOT NULL DEFAULT FALSE       
    )
    """)

    cursor.execute("SELECT COUNT(*) AS count FROM tasks")
    count = cursor.fetchone()["count"]  

    if count == 0:
        cursor.executemany(
            "INSERT INTO tasks (title, done) VALUES (%s, %s)",
            [
                ("Learn FastAPI", False),
                ("Connect SQLite", False),
                ("Complete FlyRank Assignment", False),
            ],
        )

    conn.commit()
    conn.close()

def get_all_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")
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

def get_task_by_id(task_id : int) :
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    "SELECT * FROM tasks WHERE id = %s",
    (task_id,)
)

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
        """
        INSERT INTO tasks (title, done)
        VALUES (%s, %s)
        RETURNING *
        """,
        (title, False)
    )
    row = cursor.fetchone()
    conn.commit()
    conn.close()

    return row

def update_task_db(task_id : int, title : str, done : bool):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
         """
        UPDATE tasks
        SET title = %s, done = %s
        WHERE id = %s
        """,
        (title, done, task_id)
    )

    if cursor.rowcount == 0:
        conn.close()
        return None
    
    conn.commit()
    cursor.execute(
        "select * from tasks where id = %s",
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
        "DELETE FROM tasks WHERE id = %s",
        (task_id,)
    )
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted > 0