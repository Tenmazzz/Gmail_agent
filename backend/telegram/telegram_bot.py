import os
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from graph import graph
from gmail.gmail_agent import get_unread_emails, get_unread_emails_par_date
from telegram_ux import maintenir_typing
from telegram_format import construire_recap, envoyer_par_morceaux, configurer_commandes


async def _traiter_mails(update: Update, unread_emails):
    tous_les_resultats = []
    mails_en_echec = []

    for mail in unread_emails:
        print(f"Traitement : {mail['objet_mail']}")
        try:
            resultat = await asyncio.to_thread(graph.invoke, mail)
            tous_les_resultats.append(resultat)
            print(f"Terminé : {mail['objet_mail']}")
        except Exception as e:
            print(f"Erreur sur le mail '{mail['objet_mail']}' : {e}")
            mails_en_echec.append(mail)

    if tous_les_resultats:
        recap = construire_recap(tous_les_resultats)
        for morceau in envoyer_par_morceaux(recap):
            await update.message.reply_text(morceau)

    for resultat in tous_les_resultats:
        if resultat.get("alerte") != "non":
            for morceau in envoyer_par_morceaux(resultat["message_urgent_telegram"]):
                await update.message.reply_text(morceau)

    if mails_en_echec:
        message_echec = f"⚠️ {len(mails_en_echec)} mail(s) n'ont pas pu être traité(s) :\n\n"
        for mail in mails_en_echec:
            message_echec += f"  - {mail['objet_mail']}\n"
        for morceau in envoyer_par_morceaux(message_echec):
            await update.message.reply_text(morceau)


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
        await _traiter_mails(update, unread_emails)
    finally:
        tache_typing.cancel()


async def lancer_agent_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id_autorise = os.getenv("TELEGRAM_CHAT_ID")
    if str(update.effective_chat.id) != chat_id_autorise:
        return

    if not context.args:
        await update.message.reply_text("Utilise le format : /lancer_date JJ-MM-AAAA (ex: /lancer_date 28-08-2026)")
        return

    try:
        date_cible = datetime.strptime(context.args[0], "%d-%m-%Y").date()
    except ValueError:
        await update.message.reply_text("Format de date invalide. Utilise JJ-MM-AAAA (ex: /lancer_date 28-08-2026)")
        return

    await update.message.reply_text(f"Lancement de l'agent pour le {context.args[0]}...")

    tache_typing = asyncio.create_task(maintenir_typing(context.bot, update.effective_chat.id))

    try:
        unread_emails = await asyncio.to_thread(get_unread_emails_par_date, date_cible)
        await _traiter_mails(update, unread_emails)
    finally:
        tache_typing.cancel()


def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    app = Application.builder().token(token).post_init(configurer_commandes).build()
    app.add_handler(CommandHandler("lancer", lancer_agent))
    app.add_handler(CommandHandler("lancer_date", lancer_agent_date))
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()