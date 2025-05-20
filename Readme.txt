
📄 Text-to-Speech Telegram Bot (by Taha)

🧠 Description:
This is a simple yet powerful Telegram bot that converts user text messages into voice messages using Google Text-to-Speech (gTTS). Built with Python and the `python-telegram-bot` library, it supports real-time interaction and audio file generation.

⚙️ Features:
- Converts any English text message into a voice message.
- Notifies the admin (you) whenever a user starts the bot.
- Logs user info (name, username, time) in console with colored output.
- Uses `gTTS` for text-to-speech conversion.
- Automatically deletes the generated audio file after sending.

🧩 Requirements:
- Python 3.10+
- Libraries:
  - `python-telegram-bot`
  - `gTTS`
  - `colorama`

🛠️ Installation:
1. Install required libraries:
   ```
   pip install python-telegram-bot gTTS colorama
   ```

2. Replace the `TOKEN` with your bot's token from @BotFather.
3. Replace `ADMIN_ID` with your Telegram user ID.
4. Run the script:
   ```
   python bot.py
   ```

🚀 Usage:
1. Start the bot with `/start`
2. Send any English sentence.
3. The bot replies with the audio version of your message.

📌 Notes:
- The bot only supports English for now (`lang='en'` in gTTS).
- Don’t share your bot token publicly.

👤 Admin Logging:
Every user who starts the bot triggers a private message to the admin with their name, username, and timestamp.

---

Made by Behroozi0149
