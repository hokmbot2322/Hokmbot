import os
import telebot
from flask import Flask, request

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is not set!")

CHANNEL_ID = os.getenv("CHANNEL_ID", "@HokmRush")  # optional
WEBHOOK_BASE = os.getenv("WEBHOOK_URL")            # e.g. https://your-app.up.railway.app/

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def cmd_start(msg):
    bot.reply_to(msg, "👋 خوش آمدی! دستور /create را برای ساخت اتاق حکم بفرست.")

@bot.message_handler(commands=['create'])
def cmd_create(msg):
    room_code = "6209"
    invite = f"https://t.me/{bot.get_me().username}?start=room{room_code}"
    caption = (f"🎩 <b>اتاق حکم کلاسیک ساخته شد</b>\n"
               f"🃏 <b>کد اتاق:</b> <code>{room_code}</code>\n"
               f"🔗 <b>دعوت‌نامه:</b> <a href=\"{invite}\">{invite}</a>")
    try:
        bot.send_message(CHANNEL_ID, caption, parse_mode="HTML")
        bot.reply_to(msg, "📤 بنر ارسال شد.")
    except Exception as e:
        bot.reply_to(msg, f"❌ خطا: {e}")

# --- Webhook endpoints ---
@app.route(f"/{BOT_TOKEN}", methods=['POST'])
def receive_update():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def set_webhook():
    if not WEBHOOK_BASE:
        return "WEBHOOK_URL env var not set", 500
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_BASE.rstrip('/') + f"/{BOT_TOKEN}")
    return "Webhook set!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
