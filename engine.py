from workflow import build_graph
from agents.vector_agent import vector_agent_node
from agents.sql_agent import sql_agent_node
from agents.formatter import formatter_node

graph = build_graph()

def run_agent(user_input, conversation_history):

    state = {
        "conversation_history": conversation_history,
        "current_user_input": user_input,
        "query_type": "",
        "sql_needed": False,
        "vector_needed": False,
        "sql_params": {},
        "vector_params": {},
        "sql_results": [],
        "vector_results": [],
        "sub_questions": [],
        "final_response": ""
    }

    result = graph.invoke(state)

    # 1️⃣ SQL fallback if user mentioned something specific
    if not result["sql_results"]:
        result["sql_needed"] = True
        result = sql_agent_node(result)

    # 2️⃣ Vector fallback if still nothing found
    if not result["sql_results"] and not result["vector_results"]:
        result["vector_needed"] = True
        result = vector_agent_node(result)

    # 3️⃣ Format response
    result = formatter_node(result)

    shown_ids = []

    for r in result["sql_results"]:
        if "id" in r:
            shown_ids.append(r["id"])

    for r in result["vector_results"]:
        if "id" in r:
            shown_ids.append(r["id"])

    assistant_message = {
        "role": "assistant",
        "content": result["final_response"],
        "metadata": {
            "book_ids": shown_ids,
            "query_type": result["query_type"]
        }
    }

    return assistant_message