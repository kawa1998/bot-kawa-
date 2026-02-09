import os
from telegram.ext import Application, MessageHandler, filters

TOKEN = "8444430154:AAGeGDuMDaXwMcWla30uDmYYqnRCBPFe0NA"

async def start(update, context):
    await update.message.reply_text("سڵاو، من ئیش دەکەم!")

if __name__ == '__main__':
    bot = Application.builder().token(TOKEN).build()
    bot.add_handler(MessageHandler(filters.TEXT, start))
    bot.run_polling()
