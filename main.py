import os, threading, yt_dlp, asyncio
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CallbackQueryHandler

# ڕێکخستنی Flask بۆ ئەوەی سێرڤەرەکە نەکەوێت (Health Check)
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Online!", 200

# زانیارییەکانت لێرە دابنێ
TOKEN = "8444430154:AAH6ZGD94WssDR5eL4IpNTnWrWXHvrcCSh0"
OWNER_ID = 1102319741  # ئایدی خۆت لێرە دابنێ

async def handle_message(update: Update, context):
    if update.message.from_user.id != OWNER_ID: return
    url = update.message.text
    if "http" in url:
        kb = InlineKeyboardMarkup([[
            InlineKeyboardButton("ڤیدیۆ 🎬", callback_data=f"vid|{url}"),
            InlineKeyboardButton("دەنگ 🎵", callback_data=f"aud|{url}")
        ]])
        await update.message.reply_text("📥 لینکەکە وەرگیرا، جۆرەکە هەڵبژێرە:", reply_markup=kb)

async def button_callback(update: Update, context):
    query = update.callback_query
    await query.answer("خەریکی داگرتنم... ⏳")
    data, url = query.data.split("|")
    
    ydl_opts = {
        'format': 'best' if data == 'vid' else 'bestaudio/best',
        'outtmpl': 'downloaded_file.%(ext)s',
        'quiet': True,
        'no_warnings': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        with open(filename, 'rb') as f:
            if data == 'vid':
                await query.message.reply_video(video=f, caption="فەرموو ڤیدیۆکەت ✨")
            else:
                await query.message.reply_audio(audio=f, caption="فەرموو دەنگەکە ✨")
        os.remove(filename)
    except Exception as e:
        await query.message.reply_text(f"❌ هەڵەیەک ڕوویدا: {e}")

def run_flask():
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    # دەستپێکردنی Flask
    threading.Thread(target=run_flask, daemon=True).start()
    
    # دروستکردنی بۆت بە پاککردنەوەی نامە کۆنەکان
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    print("Bot is starting...")
    application.run_polling(drop_pending_updates=True)
