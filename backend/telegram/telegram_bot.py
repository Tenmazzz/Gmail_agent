import os
import asyncio
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, ContextTypes

from graph import graph
from gmail.gmail_agent import get_unread_emails


def construire_recap(tous_les_resultats):
    recap = "📝 Récapitulatif des mails: \n\n"
    for mail in tous_les_resultats:
        if mail.get('alerte') != "non":
            recap += f"  -  {mail['resume_mail']} 🚨\n\n"
        else:
            recap += f"  -  {mail['resume_mail']} \n\n"
    return recap


async def maintenir_typing(bot, chat_id):
    while True:
        await bot.send_chat_action(chat_id=chat_id, action="typing")
        await asyncio.sleep(4)


def envoyer_par_morceaux(texte, taille_max=4000):
    morceaux = []
    while len(texte) > taille_max:
        # coupe au dernier retour à la ligne avant la limite, pour ne pas couper un mail en deux
        index_coupure = texte.rfind('\n', 0, taille_max)
        if index_coupure == -1:
            index_coupure = taille_max
        morceaux.append(texte[:index_coupure])
        texte = texte[index_coupure:]
    morceaux.append(texte)
    return morceaux


async def lancer_agent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id_autorise = os.getenv("TELEGRAM_CHAT_ID")
    if str(update.effective_chat.id) != chat_id_autorise:
        return

    nb_jours = int(context.args[0]) if context.args else 1

    if nb_jours == 1:
        await update.message.reply_text(f"Lancement de l'agent sur les 24 dernières heures...")
    else:
        await update.message.reply_text(f"Lancement de l'agent sur les {nb_jours} derniers jours...")

    tache_typing = asyncio.create_task(maintenir_typing(context.bot, update.effective_chat.id))

    try:
        unread_emails = await asyncio.to_thread(get_unread_emails, nb_jours)

        tous_les_resultats = []
        for mail in unread_emails:
            print(f"Traitement : {mail['objet_mail']}")
            resultat = await asyncio.to_thread(graph.invoke, mail)
            tous_les_resultats.append(resultat)
            print(f"Terminé : {mail['objet_mail']}")

        recap = construire_recap(tous_les_resultats)
        await update.message.reply_text(recap)

        for resultat in tous_les_resultats:
            if resultat.get("alerte") != "non":
                await update.message.reply_text(resultat["message_urgent_telegram"])
    finally:
        tache_typing.cancel()


async def configurer_commandes(application):
    await application.bot.set_my_commands([
        BotCommand("lancer", "Lance l'agent mail (ex: /lancer 2 pour 2 jours)"),
    ])


def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    app = Application.builder().token(token).post_init(configurer_commandes).build()
    app.add_handler(CommandHandler("lancer", lancer_agent))
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()