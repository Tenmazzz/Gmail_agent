from nodes.node_state.state import GmailActionState
from clients.ollama_client import llm

def message_telegram_node(state: GmailActionState):
    message = f"Expéditeur : {state.get('expediteur')}\n\n"
    message += f"Résumé : \n\n {state.get('resume_mail')}\n\n"

    if state.get("alerte") and state["alerte"] != "non":
        message += f"⚠️ Urgent : \n\n {state['alerte']}\n\n"
        
    if state.get("brouillon"):
        message += f"Brouillon : \n\n {state['brouillon']}\n\n"

    return {"message_urgent_telegram": message}