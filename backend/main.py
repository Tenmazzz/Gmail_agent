from graph import graph
import asyncio
from clients.telegram_client import envoyer_message
from gmail.gmail_agent import get_unread_emails

unread_emails = get_unread_emails(2) 

# Sert à lancer la commande python


def construire_recap(tous_les_resultats):
    recap = "📝 Récapitulatif des mails: \n\n"
    for mail in tous_les_resultats:
        if mail.get('alerte') != "non":
            recap += f"  -  {mail['resume_mail']} 🚨\n\n"
        else:
            recap += f"  -  {mail['resume_mail']} \n\n"
    return recap


tous_les_resultats = []

# pour chaque mails non lus j'effectue le graph et j'ajoute à la liste totale
for mail in unread_emails:
    print(f"Traitement : {mail['objet_mail']}")
    resultat = graph.invoke(mail)
    tous_les_resultats.append(resultat)
    print(f"Terminé : {mail['objet_mail']}")

# 1. Construire et envoyer le récap global en premier
recap = construire_recap(tous_les_resultats)
asyncio.run(envoyer_message(recap))

# 2. Puis envoyer un message détaillé pour chaque mail urgent
for resultat in tous_les_resultats:
    if resultat.get("alerte") != "non":
        asyncio.run(envoyer_message(resultat["message_urgent_telegram"]))