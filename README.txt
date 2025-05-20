
📄 Text-to-Speech Telegram Bot (by Taha)

🧠 Description:
A secure and efficient Telegram bot that converts user text messages into voice using Google Text-to-Speech (gTTS). Built with Python and `python-telegram-bot`, it features real-time voice generation, admin notifications, and clean logging.

⚙️ Features:
- Converts any English text message into a voice message.
- Sends a private notification to the admin when a user starts the bot.
- Logs user details (name, username, timestamp) with colored console output.
- Deletes generated voice files automatically after sending.
- Stores sensitive data (bot token and admin ID) securely using `.env` file.

🧩 Requirements:
- Python 3.10+
- Libraries:
  - `python-telegram-bot`
  - `gTTS`
  - `colorama`
  - `python-dotenv`

🛠️ Installation:
1. Install the required libraries:
   ```
   pip install python-telegram-bot gTTS colorama python-dotenv
   ```

2. Create a file named `info.env` in the same directory as your script and add:
   ```
   TOKEN=your_bot_token_here
   ADMIN_ID=your_telegram_user_id_here
   ```

3. (Optional but recommended) Create a `.gitignore` file with the following content to keep your secrets safe:
   ```
   info.env
   __pycache__/
   *.pyc
   voice_*.mp3
   ```

4. Run the bot:
   ```
   python bot.py
   ```

🚀 Usage:
1. Start the bot with `/start`
2. Send any English sentence.
3. The bot responds with the voice version of your message.

📌 Notes:
- Currently supports English (`lang='en'` in gTTS).
- Do **not** upload your `info.env` or bot token publicly (especially if using GitHub).

👤 Admin Logging:
Whenever someone starts the bot, a private message is sent to the admin containing their name, username, and timestamp.

---

Made with 💻 by Behroozi0149
