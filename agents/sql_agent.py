import json
import google.generativeai as genai
from db import get_connection, get_schema
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_sql(user_query, conversation_history, schema):

    prompt = f"""
You are an expert PostgreSQL query generator.

Database table: books

Schema:
{schema}

Conversation history:
{conversation_history}

User request:
{user_query}

Rules:
- Use ONLY columns from schema
- Only SELECT queries are allowed
- Never modify database
- Always include LIMIT 10
- Prefer ILIKE with partial matching for title or author searches
- Return ONLY SQL query
- No explanation
"""

    response = model.generate_content(
        prompt,
        generation_config={"temperature": 0}
    )

    sql = response.text.strip()

    sql = sql.replace("```sql", "").replace("```", "").strip()

    return sql


def validate_sql(sql):

    forbidden = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER"]

    for word in forbidden:
        if word in sql.upper():
            raise ValueError("Unsafe SQL detected")

    if "books" not in sql.lower():
        raise ValueError("Query must target books table")

    return True


def sql_agent_node(state):

    if not state.get("sql_needed"):
        return state

    user_query = state.get("current_user_input", "")
    conversation_history = state.get("conversation_history", "")

    schema = get_schema()

    sql = generate_sql(user_query, conversation_history, schema)

    validate_sql(sql)

    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()

        columns = [desc[0] for desc in cur.description]

    conn.close()

    results = []

    for row in rows:
        results.append(dict(zip(columns, row)))

    state["sql_results"] = results

    return state

