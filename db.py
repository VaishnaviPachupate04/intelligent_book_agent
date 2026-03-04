import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg.connect(DB_URL)


def get_schema():

    conn = get_connection()

    query = """
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_name = 'books'
    """

    with conn.cursor() as cur:
        cur.execute(query)
        rows = cur.fetchall()

    conn.close()

    schema = "\n".join([f"{r[0]} ({r[1]})" for r in rows])

    return schema