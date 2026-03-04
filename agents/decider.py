from dotenv import load_dotenv
import os
import json
import google.generativeai as genai
from db import get_schema

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")


def decider_node(state):

    conversation_history = state["conversation_history"]
    current_user_input = state["current_user_input"]
    schema = get_schema()

    prompt = f"""
You are the routing engine of a book chatbot.

Your task is to decide whether answering the user requires
structured database access or semantic search.

Database schema columns:
{schema}

Rules:
If answering the question requires retrieving or filtering
data using these columns, enable SQL search.

If the user is asking for recommendations, themes,
or vague descriptions, enable vector search.

If both are required, enable both.

Return JSON only.

Conversation history:
{conversation_history}

Current message:
{current_user_input}
"""


    response = model.generate_content(
        prompt,
        generation_config={"temperature": 0}
    )

    raw = response.text.strip()

    if "```" in raw:
        raw = raw.replace("```json", "").replace("```", "").strip()

    start = raw.find("{")
    end = raw.rfind("}") + 1
    json_string = raw[start:end]

    output = json.loads(json_string)

    state.update(output)

    return state