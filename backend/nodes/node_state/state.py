from typing import TypedDict

class GmailActionState(TypedDict):
    expediteur: str
    objet_mail: str
    contenu_mail: str
    resume_mail: str
    brouillon: str
    alerte: str
    reponse_attendue: bool
    message_urgent_telegram: str