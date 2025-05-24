from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from gtts import gTTS
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
from colorama import Fore, Style, init
import traceback, os, time

init(autoreset=True)
load_dotenv('confidential.env')
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
USERS_FILE = Path("users.txt")
MAX_TEXT_LENGTH = 600


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    if user.id == ADMIN_ID:
        await update.message.reply_text("Hello Admin!")
        return
    if not USERS_FILE.exists():
        USERS_FILE.touch()
    known_users = USERS_FILE.read_text().splitlines()
    if user_id not in known_users:
        with USERS_FILE.open("a") as f: f.write(user_id + "\n")
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
        user_info = f"New user:\n\nName: {user.full_name}\nUsername: @{user.username if user.username else 'no username!'}\n"
        await context.bot.send_message(chat_id=ADMIN_ID, text=user_info)
        print(Fore.BLUE + f"New user: {user.full_name} - {user_id} at {time_now}")
    await update.message.reply_text("Hi! Send me your text so I can turn it into a voice. 🗣️🎙️")


async def feedback(update: Update, _: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please send your feedback to @tahabehroozibot 🙏")


async def handle_text(update: Update, _: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if not text:
        await update.message.reply_text("Please send a valid text. 🚫📄")
        return
    if len(text) > MAX_TEXT_LENGTH:
        await update.message.reply_text("Text is too long. Please shorten it. ✂️")
        return
    await update.message.chat.send_action(action="record_audio")
    filename = Path(f"voice_{update.effective_user.id}.mp3")
    try:
        tts = gTTS(text=text, lang='en')
        tts.save(str(filename))
        with filename.open('rb') as audio_file:
            await update.message.reply_voice(voice=audio_file)
            await update.message.reply_text("Now you can listen to it 🎧")
    except Exception as e:
        await update.message.reply_text("Oops! Something went wrong. 🚨")
        print(Fore.LIGHTRED_EX + "you have a error👇🏻" + Style.RESET_ALL)
        with open("error.log", "a") as log:
            log.write(f"{datetime.now()} - {e}\n")
        print(Fore.RED + str(e))
        traceback.print_exc()
    finally:
        if filename.exists(): filename.unlink()


if __name__ == '__main__':
    print('please turn on your VPN')
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(CommandHandler('feedback', feedback))
    print(Fore.GREEN + "Bot is running" + Style.RESET_ALL)
    time.sleep(1)
    print("Press CTRL+C to exit.\n")
    app.run_polling()
