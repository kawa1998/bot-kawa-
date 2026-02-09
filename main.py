import os, threading, yt_dlp
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CallbackQueryHandler

# ١. ڕێکخستنی سێرڤەری وێب بۆ مانەوەی بۆتەکە بە زیندوویی لە Koyeb
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Online!", 200

# ٢. زانیارییە تایبەتەکانی بۆتەکە (تۆکن و ئایدی خۆت لێرە دابنێ)
TOKEN = "8444430154:AAH6ZGD94WssDR5eL4IpNTnWrWXHvrcCSh0" # تۆکنە نوێیەکە لێرە دابنێ
OWNER_ID = 1102319741 # ئایدی خۆت لێرە دابنێ

# ٣. فەرمانی وەرگرتنی لینک و نیشاندانی دوگمەکان
async def handle_message(update: Update, context):
    if update.message.from_user.id != OWNER_ID: return
    url = update.message.text
    if "http" in url:
        kb = InlineKeyboardMarkup([[
            InlineKeyboardButton("ڤیدیۆ 🎬", callback_data=f"vid|{url}"),
            InlineKeyboardButton("دەنگ 🎵", callback_data=f"aud|{url}")
        ]])
        await update.message.reply_text("📥 لینکەکە وەرگیرا، جۆرەکە هەڵبژێرە:", reply_markup=kb)

# ٤. فەرمانی داگرتن و ناردنی فایلەکە (چارەسەری کێشەی یوتیوب لێرەدایە)
async def button_callback(update: Update, context):
    query = update.callback_query
    await query.answer("خەریکی داگرتنم... ⏳")
    data, url = query.data.split("|")
    
    ydl_opts = {
        'format': 'best' if data == 'vid' else 'bestaudio/best',
        'outtmpl': 'downloaded_file.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        # بەکارهێنانی فێڵێک بۆ تێپەڕاندنی ڕێگرییەکانی یوتیوب
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
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
        os.remove(filename) # سڕینەوەی فایلەکە لە سێرڤەر دوای ناردن
    except Exception as e:
        await query.message.reply_text(f"❌ هەڵەیەک ڕوویدا: {e}")

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# ٥. دەستپێکردنی هەموو بەشەکان بەیەکەوە
if __name__ == '__main__':
    # کارپێکردنی سێرڤەری Flask لە پشتەوە
    threading.Thread(target=run_flask, daemon=True).start()
    
    # کارپێکردنی بۆتی تیلیگرام
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    print("Bot is starting perfectly...")
    application.run_polling(drop_pending_updates=True)
