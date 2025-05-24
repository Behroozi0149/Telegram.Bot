from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from gtts import gTTS
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from colorama import Fore, Style, init
import traceback
import os

init(autoreset=True)
load_dotenv('info.env')
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
USERS_FILE = Path("users.txt")
VOICES_DIR = Path("voices")
VOICES_DIR.mkdir(exist_ok=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    if user.id == ADMIN_ID:
        await update.message.reply_text("Hello Admin! 👋")
        return
    if not USERS_FILE.exists():
        USERS_FILE.touch()
    known_users = USERS_FILE.read_text().splitlines()
    if user_id not in known_users:
        USERS_FILE.write_text(USERS_FILE.read_text() + user_id + "\n")
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_info = (
            f"🟢 Hi Taha🩶, someone just entered the bot✅\n\n"
            f"👤 name: {user.full_name}\n"
            f"🆔 username: @{user.username if user.username else 'none🚫'}\n"
            f"⏰ time: {time_now}"
        )
        await context.bot.send_message(chat_id=ADMIN_ID, text=user_info)
        print(Fore.GREEN + f"New user: {user.full_name} - {user_id} at {time_now}")
    await update.message.reply_text("Hi! Send me your text so I can turn it into a voice. 🗣️🎙️")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if not text:
        await update.message.reply_text("Please send a valid text. 🚫📄")
        return
    if len(text) > MAX_TEXT_LENGTH:
        await update.message.reply_text("Text is too long. Please shorten it. ✂️")
        return
    await update.message.chat.send_action(action="record_audio")
    try:
        tts = gTTS(text=text, lang='en')
        filename = VOICES_DIR / f"voice_{datetime.now().timestamp():.0f}.mp3"
        tts.save(str(filename))
        with filename.open('rb') as audio_file:
            await update.message.reply_voice(voice=audio_file)
            await update.message.reply_text("Now you can listen to it! 🎧")
        filename.unlink()
    except Exception as e:
        await update.message.reply_text("Oops! Something went wrong. 🚨")
        with open("error.log", "a") as log:
            log.write(f"{datetime.now()} - {e}\n")
        print(Fore.RED + str(e))
        traceback.print_exc()


if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print(Fore.LIGHTGREEN_EX + "Bot is running🚀" + Style.RESET_ALL)
    app.run_polling()
