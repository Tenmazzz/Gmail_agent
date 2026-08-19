from nodes.node_state.state import GmailActionState

def router_brouillon(state: GmailActionState):
    if state["reponse_attendue"]:
        return "brouillon_node"
    else:
        return "message_telegram_node"