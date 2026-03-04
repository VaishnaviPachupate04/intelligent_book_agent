from vector_store import collection, model

def vector_agent_node(state):

    if not state["vector_needed"]:
        return state

    search_text = state["vector_params"].get("search_text", "")

    embedding = model.encode(search_text)

    results = collection.query(
        query_embeddings=[embedding],
        n_results=5
    )

    state["vector_results"] = results["metadatas"][0]

    return state