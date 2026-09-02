from telegram import BotCommand


def construire_recap(tous_les_resultats):
    recap = "📝 Récapitulatif des mails: \n\n"
    for mail in tous_les_resultats:
        if mail.get('alerte') != "non":
            recap += f"  -  {mail['resume_mail']} 🚨\n\n"
        else:
            recap += f"  -  {mail['resume_mail']} \n\n"
    return recap


def envoyer_par_morceaux(texte, taille_max=4000):
    morceaux = []
    while len(texte) > taille_max:
        index_coupure = texte.rfind('\n', 0, taille_max)
        if index_coupure == -1:
            index_coupure = taille_max
        morceaux.append(texte[:index_coupure])
        texte = texte[index_coupure:]
    morceaux.append(texte)
    return morceaux


async def configurer_commandes(application):
    await application.bot.set_my_commands([
        BotCommand("lancer", "Lance l'agent mail (ex: /lancer 2 pour 2 jours)"),
        BotCommand("lancer_date", "Lance l'agent pour une date précise (ex: /lancer_date 28-08-2026)"),
    ])