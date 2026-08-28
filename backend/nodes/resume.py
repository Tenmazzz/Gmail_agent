from nodes.node_state.state import GmailActionState
from clients.ollama_client import llm

def resume_mail_node(state: GmailActionState):
    # Lire le fichier prompt resume
    with open("prompts/resume.md", "r", encoding="utf-8") as f:
        prompt_template = f.read()

    # remplacer les variables par les val du state
    prompt_rempli = prompt_template.format(
        expediteur=state["expediteur"],
        objet_mail=state["objet_mail"],
        contenu_mail=state["contenu_mail"]
    )

    # Envoyer au llm et recup la reponse
    resume = llm.invoke(prompt_rempli)

    return {"resume_mail": resume.content}