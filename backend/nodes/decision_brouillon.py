from nodes.node_state.state import GmailActionState
from clients.ollama_client import llm

def decision_brouillon_node(state: GmailActionState):
    # Lire le fichier prompt resume
    with open("prompts/decision_reponse.md", "r", encoding="utf-8") as f:
        prompt_template = f.read()

    # remplacer les variables par les val du state
    prompt_rempli = prompt_template.format(
        expediteur=state["expediteur"],
        objet_mail=state["objet_mail"],
        resume_mail=state["resume_mail"]
    )

    # Envoyer au llm et recup la reponse
    reponse = llm.invoke(prompt_rempli)
    decision = reponse.content.lower()
    reponse_attendue = "oui" in decision

    return {"reponse_attendue": reponse_attendue}