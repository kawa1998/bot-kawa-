import os, threading, yt_dlp
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CallbackQueryHandler

app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Online!", 200

# زانیارییەکانت لێرە دابنێ
TOKEN = "8444430154:AAH6ZGD94WssDR5eL4IpNTnWrWXHvrcCSh0" # تۆکنەکەت لێرە دابنێ
OWNER_ID =1102319741 # ئایدی خۆت لێرە دابنێ

async def handle_message(update: Update, context):
    if update.message.from_user.id != OWNER_ID: return
    url = update.message.text
    if "http" in url:
        kb = InlineKeyboardMarkup([[
            InlineKeyboardButton("ڤیدیۆ 🎬", callback_data=f"vid|{url}"),
            InlineKeyboardButton("دەنگ 🎵", callback_data=f"aud|{url}")
        ]])
        await update.message.reply_text("جۆری داگرتن هەڵبژێرە:", reply_markup=kb)

async def button_callback(update: Update, context):
    query = update.callback_query
    await query.answer("خەریکی داگرتنم... چاوەڕێ بکە ⏳")
    data, url = query.data.split("|")
    
    ydl_opts = {
        'format': 'best' if data == 'vid' else 'bestaudio/best',
        'outtmpl': 'downloaded_file.%(ext)s',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        
    with open(filename, 'rb') as f:
        if data == 'vid':
            await query.message.reply_video(video=f)
        else:
            await query.message.reply_audio(audio=f)
    os.remove(filename)

if __name__ == '__main__':
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()
    bot = Application.builder().token(TOKEN).build()
    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    bot.add_handler(CallbackQueryHandler(button_callback))
    bot.run_polling()
