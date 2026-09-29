# Telegram bot with a ChatGPT button

This bot uses Telegram's built-in menu button to open a small hosted launcher, which navigates to `https://chatgpt.com/` in Telegram's web view. It sends no messages and needs no running bot server.

Configure it with Python 3.10 or newer:

```bash
TELEGRAM_BOT_TOKEN='your-token' python3 configure_bot.py
```

Check the current configuration without changing it:

```bash
TELEGRAM_BOT_TOKEN='your-token' python3 configure_bot.py --inspect
```

Telegram requires text on the menu button, so its label is `Открыть ChatGPT`. The bot has no commands or description. The launcher is in `index.html` and is hosted on GitHub Pages. ChatGPT login and web-view behavior are controlled by `chatgpt.com` and Telegram.

Keep the token secret. If it has been shared publicly, rotate it through @BotFather and run the command with the new token.
