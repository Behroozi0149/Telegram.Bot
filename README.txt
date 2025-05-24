📄 Text-to-Speech Telegram Bot

🧠 Description:
A fast, clean Telegram bot that converts user text messages into voice messages using Google Text-to-Speech (gTTS). Built with `python-telegram-bot`, it includes real-time voice generation, admin notifications, user tracking, and automatic voice cleanup.

⚙️ Features:
- 🔊 Converts English text to voice using gTTS.
- 🛎️ Notifies the admin privately when a new user starts the bot.
- 📁 Saves user IDs in `users.txt` to avoid duplicate notifications.
- 🎨 Uses `colorama` for pretty console logs (green for users, red for errors).
- 🔒 Secures API token and admin ID with `.env` file.
- 🧹 Automatically deletes voice files after sending them.
- ❌ Limits text length (with optional `MAX_TEXT_LENGTH` definition).

🧩 Requirements:
- Python 3.10+
- Python libraries:
  - `python-telegram-bot`
  - `gTTS`
  - `colorama`
  - `python-dotenv`

🛠️ Installation:
1. Install required libraries:
   ```
   pip install python-telegram-bot gTTS colorama python-dotenv
   ```

2. Create an `.env` file named `info.env` in the root directory:
   ```
   TOKEN=your_bot_token_here
   ADMIN_ID=your_telegram_user_id_here
   ```

3. Recommended `.gitignore` setup:
   ```
   info.env
   __pycache__/
   *.pyc
   voice_*.mp3
   users.txt
   error.log
   ```

4. Run the bot:
   ```
   python bot.py
   ```

🚀 Usage:
1. Send `/start` to the bot.
2. Send a short English message.
3. Get a voice response instantly. 🎙️

📌 Notes:
- Supports English only (`lang='en'` in gTTS).
- Automatically filters out empty or overly long messages.
- Deletes voice files after sending to save space.
- Logs any runtime error to `error.log`.

👤 Admin Panel:
- When a user starts the bot, their name, username (or 🚫), and timestamp are sent to the admin privately via Telegram.

🌟 To-Do (for future improvements):
- [ ] Add language detection and support.
- [ ] Add voice gender/style customization.
- [ ] Add /help command.

---

Made by Behroozi0149.