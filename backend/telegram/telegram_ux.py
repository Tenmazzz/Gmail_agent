import asyncio


async def maintenir_typing(bot, chat_id):
    while True:
        await bot.send_chat_action(chat_id=chat_id, action="typing")
        await asyncio.sleep(4)