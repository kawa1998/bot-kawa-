import os, threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CallbackQueryHandler

# ڕێکخستنی سێرڤەری وێب بۆ ئەوەی Koyeb نەیپچڕێنێت
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Online!", 200

# زانیارییەکانت لێرە دابنێ (وەک پێشوو)
TOKEN = "8444430154:AAGeGDuMDaXwMcWla30uDmYYqnRCBPFe0NA" # تۆکنەکەت لێرە دابنێ
OWNER_ID =1102319741# ئایدی خۆت لێرە دابنێ

async def handle_message(update: Update, context):
    if update.message.from_user.id != OWNER_ID: return
    
    url = update.message.text
    if "http" in url:
        # دروستکردنی دوگمە بۆ هەڵبژاردن
        keyboard = [
            [
                InlineKeyboardButton("ڤیدیۆ 🎬", callback_data=f"vid|{url}"),
                InlineKeyboardButton("دەنگ 🎵", callback_data=f"aud|{url}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("لینکەکە وەرگیرا، جۆری داگرتن هەڵبژێرە:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("تکایە لینکێکی ڕاست بنێرە.")

def run_flask():
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    # دەستپێکردنی Flask لە تێردێکی جیاواز
    threading.Thread(target=run_flask).start()
    
    # دەستپێکردنی بۆتی تیلیگرام
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot is running perfectly...")
    application.run_polling()
