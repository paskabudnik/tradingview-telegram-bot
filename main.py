import os
from flask import Flask, request
import requests
from dotenv import load_dotenv
from db import init_db, add_user, get_all_users  # предполагается, что у тебя есть этот модуль

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

app = Flask(__name__)

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(url, json=payload)

@app.route("/bot/<token>", methods=["POST"])
def telegram(token):
    if token != BOT_TOKEN:
        return {"error": "unauthorized"}, 403

    data = request.get_json()
    msg = data.get("message", {})
    chat = msg.get("chat", {})
    chat_id = chat.get("id")
    name = chat.get("first_name", "User")
    text = msg.get("text", "")

    if text == "/start":
        add_user(chat_id, name)
        send_message(chat_id, "✅ Вы успешно подписались на сигналы!")
    else:
        send_message(chat_id, "Напиши /start, чтобы получать сигналы.")

    return {"ok": True}

@app.route("/webhook", methods=["POST"])
def tradingview_webhook():
    if request.args.get("secret") != WEBHOOK_SECRET:
        return {"error": "unauthorized"}, 401

    data = request.json
    ticker = data.get("ticker", "N/A")
    signal = data.get("signal", "N/A")

    message = f"<b>📈 Сигнал от TradingView</b>\nТикер: <code>{ticker}</code>\nСигнал: <b>{signal}</b>"

    for user in get_all_users():
        send_message(user["chat_id"], message)

    return {"status": "ok"}, 200

@app.route("/")
def root():
    return "✅ Бот работает!"

if __name__ == "__main__":
    init_db()
   # app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

