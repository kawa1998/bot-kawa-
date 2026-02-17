import os, subprocess, threading, asyncio
from flask import Flask
from telegram import Update
from telegram.ext import Application, MessageHandler, filters

# ڕێکخستنی Flask بۆ سێرڤەری Koyeb
app = Flask(__name__)
@app.route('/')
def home(): return "Advanced Python Terminal is Running!", 200

# زانیارییەکانت لێرە دابنێ
TOKEN = "8444430154:AAH6ZGD94WssDR5eL4IpNTnWrWXHvrcCSh0"
OWNER_ID =1102319741

async def execute_command(update: Update, context):
    if update.message.from_user.id != OWNER_ID:
        return

    command = update.message.text
    # ناردنی پەیامێکی کاتی تا فەرمانەکە تەواو دەبێت
    status_msg = await update.message.reply_text("⏳ خەریکی جێبەجێکردنە...")

    try:
        # بەکارهێنانی subprocess بۆ کارپێکردنی فەرمانەکان بە کاتی دیاریکراو (Timeout)
        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        
        # ڕێگە دەگرێت لەوەی فەرمانەکە سێرڤەرەکە بۆ هەمیشە سەرقاڵ بکات
        try:
            stdout, stderr = process.communicate(timeout=60) 
        except subprocess.TimeoutExpired:
            process.kill()
            await status_msg.edit_text("❌ کاتەکە کۆتایی هات (Timeout). فەرمانەکە زۆر درێژەی کێشا.")
            return

        # کۆکردنەوەی ئەنجامەکان
        output = stdout if stdout else ""
        errors = stderr if stderr else ""
        full_response = output + errors

        if not full_response.strip():
            await status_msg.edit_text("✅ فەرمانەکە بە سەرکەوتوویی جێبەجێ کرا (هیچ دەرئەنجامێکی نەبوو).")
        else:
            # ناردنی ئەنجام بە شێوازی کۆد بۆ ئەوەی ئاسان کۆپی بکرێت
            if len(full_response) > 4000:
                # ئەگەر ئەنجامەکە زۆر درێژ بوو، وەک فایل دەینێرێت
                with open("output.txt", "w") as f:
                    f.write(full_response)
                await update.message.reply_document(document=open("output.txt", "rb"), caption="📄 ئەنجامەکە زۆر درێژ بوو، وەک فایل نێردرا.")
                os.remove("output.txt")
                await status_msg.delete()
            else:
                await status_msg.edit_text(f"```bash\n{full_response}\n```", parse_mode='MarkdownV2')

    except Exception as e:
        await status_msg.edit_text(f"❌ هەڵەیەک ڕوویدا:\n`{str(e)}`", parse_mode='MarkdownV2')

def run_flask():
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    # دەستپێکردنی Flask لە تێردێکی جیاواز
    threading.Thread(target=run_flask, daemon=True).start()
    
    # دەستپێکردنی بۆتەکە بە شێوازێکی پێشکەوتوو
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, execute_command))
    
    print("Advanced Bot is starting...")
    application.run_polling(drop_pending_updates=True)
