import os
from telegram import Bot

async def envoyer_message(texte: str):
    bot = Bot(os.getenv("TELEGRAM_BOT_TOKEN"))
    await bot.send_message(chat_id=os.getenv("TELEGRAM_CHAT_ID"), text=texte)