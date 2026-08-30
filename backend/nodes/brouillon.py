from nodes.node_state.state import GmailActionState
from clients.ollama_client import llm

# Lire le fichier prompt resume
with open("prompts/brouillon.md", "r", encoding="utf-8") as f:
    prompt_template = f.read()

def brouillon_node(state: GmailActionState):

    # remplacer les variables par les val du state
    prompt_brouillon_rempli = prompt_template.format(
        expediteur=state["expediteur"],
        objet_mail=state["objet_mail"],
        resume_mail=state["resume_mail"]
    )

    # Envoyer au llm et recup la reponse
    reponse = llm.invoke(prompt_brouillon_rempli)

    return {"brouillon": reponse.content}