import pandas as pd
import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg.connect(
    host="localhost",
    dbname="book_agent_db",
    user="postgres",
    password="postgres",
    port=5432
)

df = pd.read_csv("sample_books.csv", encoding="latin-1")

# Rename code → id
df = df.rename(columns={"code": "id"})

with conn.cursor() as cur:
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO books (
                id, title, author, category,
                language, price, availability, description
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row["id"],
            row["title"],
            row["author"],
            row["category"],
            row["language"],
            row["price"],
            row["availability"],   # ← no conversion
            row["description"]
        ))

conn.commit()
conn.close()

print("Data inserted successfully.")