import os, yt_dlp, requests, threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CallbackQueryHandler

# ڕێکخستنی سێرڤەری وێب بۆ Koyeb
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Online!", 200

# لێرەدا تۆکن و ئایدییەکەت بە دەست بنووسە
TOKEN = "8444430154:AAGeGDuMDaXwMcWla30uDmYYqnRCBPFe0NA"  # تۆکنەکەت بخە ناو ئەم نیشانانە ""
OWNER_ID = 1102319741     # ئایدییەکەت تەنها وەک ژمارە بنووسە

async def handle_link(update: Update, context):
    # پشکنینی ئەوەی کە ئایا بەکارهێنەرەکە خاوەنی بۆتەکەیە
    if update.message.from_user.id != OWNER_ID: return
    
    url = update.message.text
    try:
        # دروستکردنی دوگمەکان بۆ هەڵبژاردنی جۆری داگرتن
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("ڤیدیۆ 🎬", callback_data=f"vid|{url}"),
             InlineKeyboardButton("دەنگ 🎵", callback_data=f"aud|{url}")]
        ])
        await update.message.reply_text("تکایە جۆرەکە هەڵبژێرە:", reply_markup=kb)
    except Exception as e:
        print(f"Error in handle_link: {e}")

def run_flask():
    # کارپێکردنی Flask لەسەر پۆرتێک کە Koyeb پشتگیری دەکات
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    # دەستپێکردنی Flask لە تێردێکی جیاواز
    threading.Thread(target=run_flask).start()
    
    # دەستپێکردنی بۆتی تیلیگرام
    bot = Application.builder().token(TOKEN).build()
    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    
    print("Bot is starting...")
    bot.run_polling()
