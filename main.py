from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from gtts import gTTS
import os
from colorama import Fore, Style, init
from datetime import datetime

init(autoreset=True)
TOKEN = '7903945210:AAHElbdlaU_7izKEpJnwWfSSAuh0Azfz67k'
ADMIN_ID = 6076118283


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Send me your text so I can turn it into a voice. 🗣️🎙️")
    user = update.effective_user
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_info = f"🟢 Hi my dear Taha, someone just entered the bot✅\n\n"
    user_info += f"👤 name: {user.full_name}\n"
    user_info += f"🆔 username: @{user.username if user.username else 'none🚫'}\n"
    user_info += f"⏰ time: {time_now}"
    await context.bot.send_message(chat_id=ADMIN_ID, text=user_info)
    print()
    print(Fore.LIGHTGREEN_EX + f"User {user.full_name} started the bot at {time_now}" + Style.RESET_ALL)
    print()


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text.strip():
        await update.message.reply_text("Please send a valid text. 🚫📄")
        await update.message.reply_text(":(")
        return
    tts = gTTS(text=text, lang='en')
    filename = "voice.mp3"
    tts.save(filename)
    with open(filename, 'rb') as audio_file:
        await update.message.reply_text("Here you go, kiddo 👇🏻😏")
        await update.message.reply_voice(voice=audio_file)
    os.remove(filename)


if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
    print(Fore.LIGHTGREEN_EX + "bot is running... 🙂⚙️" + Style.RESET_ALL)
    app.run_polling()
