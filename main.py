from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from gtts import gTTS
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
import os, traceback

load_dotenv('confidential.env')
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
USERS_FILE = Path("users.txt")
VOICE_DIR = Path("voices")
MAX_TEXT_LENGTH = 600

VOICE_DIR.mkdir(exist_ok=True)


def log_error(error: Exception):
    with open("error.log", "a") as log:
        log.write(f"{datetime.now()} - {str(error)}\n")
    traceback.print_exc()


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)

    if user.id == ADMIN_ID:
        await update.message.reply_text("Welcome admin.")
        return

    if user_id not in USERS_FILE.read_text().splitlines():
        USERS_FILE.open("a").write(user_id + "\n")
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
        info = f"New user:\n\nName: {user.full_name}\nUsername: @{user.username or 'no username!'}"
        await context.bot.send_message(chat_id=ADMIN_ID, text=info)

    await update.message.reply_text("Hi! Send me your text so I can turn it into a voice. 🗣️🎙️")


async def feedback_command(update: Update, _: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please send your feedback to @tahabehroozibot 🙏")


async def help_command(update: Update, _: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hey there, buddy! 👋\n"
        "Thanks a lot for using my text-to-speech bot.\n"
        "Hope you're enjoying it! 😊🎧\n\n"
        "Here’s how it works:\n\n"
        "🔹 /start → Activate bot & convert your texts to voice. 🕐🔊\n"
        "🔹 /feedback → Send your suggestions or complaints. 💬📩\n"
        "🔹 /help → Show how this bot works. 🤖🆓\n\n"
        "✨ Created by @dev_taha_behroozi 🛠️❤️"
    )


async def handle_text(update: Update, _: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if not text:
        await update.message.reply_text("Please send a valid text. 🚫📄")
        return

    if len(text) > MAX_TEXT_LENGTH:
        await update.message.reply_text("Text is too long. Please shorten it. ✂️")
        return

    await update.message.chat.send_action(action="record_audio")
    filename = VOICE_DIR / f"voice_{update.effective_user.id}.mp3"

    try:
        gTTS(text=text, lang='en').save(str(filename))
        await update.message.reply_voice(voice=open(filename, 'rb'))
        await update.message.reply_text("Now you can listen to it 🎧")
    except Exception as e:
        await update.message.reply_text("Oops! Something went wrong. 🚨")
        log_error(e)
    finally:
        if filename.exists():
            filename.unlink()


if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('feedback', feedback_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print("Bot is running. Press CTRL+C to exit.")
    app.run_polling()
