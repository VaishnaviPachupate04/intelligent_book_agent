from langgraph.graph import StateGraph

from agents.decider import decider_node
from agents.sql_agent import sql_agent_node
from agents.vector_agent import vector_agent_node
from agents.formatter import formatter_node


def route_after_decider(state):
    if state["sql_needed"] and state["vector_needed"]:
        return "sql_agent"
    if state["sql_needed"]:
        return "sql_agent"
    if state["vector_needed"]:
        return "vector_agent"
    return "formatter"


def route_after_sql(state):
    if state["vector_needed"]:
        return "vector_agent"
    return "formatter"


def build_graph():

    builder = StateGraph(dict)

    builder.add_node("decider", decider_node)
    builder.add_node("sql_agent", sql_agent_node)
    builder.add_node("vector_agent", vector_agent_node)
    builder.add_node("formatter", formatter_node)

    builder.set_entry_point("decider")

    builder.add_conditional_edges("decider", route_after_decider)
    builder.add_conditional_edges("sql_agent", route_after_sql)

    builder.add_edge("vector_agent", "formatter")

    builder.set_finish_point("formatter")

    return builder.compile()