import os
from telegram.ext import Application, MessageHandler, filters

# تۆکنەکەت لێرە بە ڕاستی دابنێ
TOKEN = "AAGeGDuMDaXwMcWla30uDmYYqnRCBPFe0NA" # ئەو تۆکنەی لە وێنەی ٤١ هەیە لێرە دایبنێ

async def start(update, context):
    await update.message.reply_text("سڵاو، من ئێستا بە باشی ئیش دەکەم! ✅")

if __name__ == '__main__':
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT, start))
    print("Bot is starting...")
    application.run_polling()
