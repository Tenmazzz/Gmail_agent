from langgraph.graph import StateGraph, START, END
from nodes.node_state.state import GmailActionState
from nodes.node_router.router import router_brouillon
from nodes.resume import resume_mail_node
from nodes.decision_brouillon import decision_brouillon_node
from nodes.brouillon import brouillon_node
from nodes.alerte import alerte_node
from nodes.message_urgent_telegram import message_telegram_node
from pprint import pprint


builder = StateGraph(GmailActionState)

# Implémentation des nodes 
builder.add_node("resume_mail_node", resume_mail_node)
builder.add_node("decision_brouillon_node", decision_brouillon_node)
builder.add_node("brouillon_node", brouillon_node)
builder.add_node("alerte_node", alerte_node)
builder.add_node("message_telegram_node", message_telegram_node)


# Construction du graph
builder.add_edge(START, "resume_mail_node")
builder.add_edge("resume_mail_node", "decision_brouillon_node")

builder.add_conditional_edges(
    "decision_brouillon_node",
    router_brouillon,
    {
        "brouillon_node" : "brouillon_node",
        "message_telegram_node" : "message_telegram_node"
    }
)

# Se passe seulement si brouillon node a choisi la bonne route
builder.add_edge("brouillon_node", "message_telegram_node")

# Suite du graph indépendante
builder.add_edge("resume_mail_node", "alerte_node")
builder.add_edge("alerte_node", "message_telegram_node")
builder.add_edge("message_telegram_node", END)

graph = builder.compile()

