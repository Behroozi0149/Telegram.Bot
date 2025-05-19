from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from gtts import gTTS
import os

TOKEN = '7307621135:AAEtDz5g5jxexa4LVfMVskjulQVoSWe3AFA'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! متن خودتو بفرست تا تبدیل به صداش کنم.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text.strip():
        await update.message.reply_text("لطفا یک متن معتبر بفرست.")
        return

    tts = gTTS(text=text, lang='en')
    filename = "voice.mp3"
    tts.save(filename)

    with open(filename, 'rb') as audio_file:
        await update.message.reply_voice(voice=audio_file)

    os.remove(filename)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))

    print("Bot is running...")
    app.run_polling()
