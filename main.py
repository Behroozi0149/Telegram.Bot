from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from gtts import gTTS
import os
from colorama import Fore, Style, init
from datetime import datetime
from dotenv import load_dotenv
import traceback

init(autoreset=True)
load_dotenv('info.env')
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    if user.id == ADMIN_ID:
        await update.message.reply_text("Hello Admin! 👋")
        return
    if not os.path.exists("users.txt"):
        with open("users.txt", "w"): pass
    with open("users.txt", "r") as f:
        known_users = f.read().splitlines()
    is_new_user = user_id not in known_users
    if is_new_user:
        with open("users.txt", "a") as f:
            f.write(user_id + "\n")
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_info = f"🟢 Hi Taha🩶, someone just entered the bot✅\n\n"
        user_info += f"👤 name: {user.full_name}\n"
        user_info += f"🆔 username: @{user.username if user.username else 'none🚫'}\n"
        user_info += f"⏰ time: {time_now}"
        await context.bot.send_message(chat_id=ADMIN_ID, text=user_info)
        print(Fore.GREEN + f"New user: {user.full_name} - {user_id} at {time_now}")
    await update.message.reply_text("Hi! Send me your text so I can turn it into a voice. 🗣️🎙️")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text.strip():
        await update.message.reply_text("Please send a valid text. 🚫📄")
        return
    try:
        tts = gTTS(text=text, lang='en')
        filename = f"voice_{datetime.now().timestamp()}.mp3"
        tts.save(filename)
        with open(filename, 'rb') as audio_file:
            await update.message.reply_voice(voice=audio_file)
            await update.message.reply_text("Now you can listen to it! 🎧")
        os.remove(filename)
    except Exception as e:
        await update.message.reply_text("Oops! Something went wrong. 🚨")
        print(Fore.RED + str(e))
        traceback.print_exc()


if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
    print(Fore.LIGHTGREEN_EX + "Bot is running🚀" + Style.RESET_ALL)
    app.run_polling()
