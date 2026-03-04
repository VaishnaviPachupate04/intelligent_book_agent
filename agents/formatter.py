from llm import call_llm

def formatter_node(state):

    sql_results = state["sql_results"]
    vector_results = state["vector_results"]

    # ✅ NEW: prevent hallucination if no books found
    if not sql_results and not vector_results:
        state["final_response"] = (
            "Sorry, I couldn't find any matching books in our current inventory. "
            "Could you try a different title, author, or category?"
        )
        return state

    prompt = f"""

You are a knowledgeable bookstore assistant having an ongoing conversation.

IMPORTANT:
- This is NOT a new conversation.
- Use the full conversation history to maintain context.
- Combine previous user preferences and constraints.
- Do NOT restart with greetings every turn.
- Do NOT reset the topic unless the user clearly changes it.

CRITICAL RULES:
- Only recommend books that appear in SQL Results or Vector Results.
- Do NOT invent books.
- If results contain books from a specific publisher, language, or category, prefer those.
- If both SQL and Vector results exist, combine them intelligently.

Conversation history:
{state["conversation_history"]}

Current message:
{state["current_user_input"]}

SQL Results:
{sql_results}

Vector Results:
{vector_results}

Respond naturally, intelligently, and contextually.
"""

    response = call_llm(prompt)

    state["final_response"] = response

    return state