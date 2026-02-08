import os, yt_dlp, requests, threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CallbackQueryHandler

app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Online!", 200

# لێرەدا زانیارییەکانت بنووسە
TOKEN = 8444430154:AAGeGDuMDaXwMcWla30uDmYYqnRCBPFe0NA
OWNER_ID = 1102319741# لێرە ئایدی خۆت دابنێ

async def handle_link(update: Update, context):
    if update.message.from_user.id != OWNER_ID: return
    url = update.message.text
    try:
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("ڤیدیۆ 🎬", callback_data=f"vid|{url}"),
             InlineKeyboardButton("دەنگ 🎵", callback_data=f"aud|{url}")]
        ])
        await update.message.reply_text("تکایە جۆرەکە هەڵبژێرە:", reply_markup=kb)
    except Exception as e:
        print(f"Error: {e}")

def run():
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    threading.Thread(target=run).start()
    bot = Application.builder().token(TOKEN).build()
    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    bot.run_polling()
