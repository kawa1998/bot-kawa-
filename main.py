import os, yt_dlp, requests, threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CallbackQueryHandler

app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Online!", 200

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

TOKEN = os.environ.get('TOKEN')
OWNER_ID = int(os.environ.get('OWNER_ID'))

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != OWNER_ID: return
    url = update.message.text
    try:
        res = requests.head(url, allow_redirects=True, timeout=10)
        url = res.url
    except: pass
            kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("ڤیدیۆ 🎬", callback_data=f"vid|{url}"),
             InlineKeyboardButton("دەنگ 🎵", callback_data=f"aud|{url}")]
        ])
        await update.message.reply_text("تکایە هەڵبژێرە:", reply_markup=kb)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data, url = query.data.split("|")
    path = f"file_{query.from_user.id}"
    msg = await query.edit_message_text("📥 خەریکی داگرتنم...")
    ydl_opts = {'format': 'best[height<=480]/best', 'outtmpl': path + '.%(ext)s'}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            if data == 'a': ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}]
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if data == 'a': filename = filename.rsplit('.', 1)[0] + '.mp3'
        if data == 'v': await query.message.reply_video(video=open(filename, 'rb'))
        else: await query.message.reply_audio(audio=open(filename, 'rb'))
        os.remove(filename)
        await msg.delete()
    except: await query.edit_message_text("❌ هەڵەیەک ڕوویدا.")

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot = Application.builder().token(TOKEN).build()
    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    bot.add_handler(CallbackQueryHandler(button_handler))
    bot.run_polling()
