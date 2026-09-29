"""Configure a silent Telegram bot with a ChatGPT menu button.

Usage: TELEGRAM_BOT_TOKEN=... python3 configure_bot.py [--inspect]
"""

import argparse
import http.client
import json
import os
import sys


WEB_APP_URL = "https://logreding228.github.io/tgbot-chatgpt-launcher/"
BUTTON_TEXT = "Открыть ChatGPT"


def telegram(token: str, method: str, payload: dict | None = None):
    connection = http.client.HTTPSConnection("api.telegram.org", timeout=15)
    body = json.dumps(payload or {}).encode("utf-8")
    try:
        connection.request(
            "POST",
            f"/bot{token}/{method}",
            body=body,
            headers={"Content-Type": "application/json"},
        )
        response = connection.getresponse()
        data = json.loads(response.read())
    finally:
        connection.close()
    if not data.get("ok"):
        raise RuntimeError(f"{method}: {data.get('description', 'Telegram API error')}")
    return data["result"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inspect", action="store_true", help="Show current settings only")
    args = parser.parse_args()
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        parser.error("Set TELEGRAM_BOT_TOKEN in the environment")

    bot = telegram(token, "getMe")
    if not args.inspect:
        telegram(
            token,
            "setChatMenuButton",
            {
                "menu_button": {
                    "type": "web_app",
                    "text": BUTTON_TEXT,
                    "web_app": {"url": WEB_APP_URL},
                }
            },
        )
        telegram(token, "deleteMyCommands")
        telegram(token, "setMyDescription", {"description": ""})
        telegram(token, "setMyShortDescription", {"short_description": ""})

    menu = telegram(token, "getChatMenuButton")
    if not args.inspect and menu.get("web_app", {}).get("url") != WEB_APP_URL:
        raise RuntimeError(f"Menu button was not saved: {menu}")

    print(f"Bot: https://t.me/{bot['username']}")
    print("Menu button:", menu)
    print("Commands:", telegram(token, "getMyCommands"))
    print("Description:", telegram(token, "getMyDescription"))
    print("Short description:", telegram(token, "getMyShortDescription"))
    print("Webhook:", telegram(token, "getWebhookInfo"))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
