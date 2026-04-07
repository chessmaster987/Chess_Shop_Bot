import os
from flask import Flask, request
import telebot
from telebot import types
from os import listdir
from random import randint
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get("BOT_TOKEN")
APP_URL = os.environ.get("APP_URL")

print("BOT_TOKEN:", TOKEN)
print("APP_URL:", APP_URL)

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# =========================
# Keyboard
# =========================
main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add("Shop items", "Share this bot")

# =========================
# Product folders
# =========================
category_paths = {
    'board_classic': 'imgs/boards/classic',
    'board_3p': 'imgs/boards/3p',
    'board_4p': 'imgs/boards/4p',
    'board_custom': 'imgs/boards/custom',
    'pieces_classic': 'imgs/pieces/classic',
    'pieces_royal': 'imgs/pieces/royal',
    'pieces_Potter': 'imgs/pieces/potter',
    'clock_mechanical': 'imgs/clocks/mechanical',
    'clock_electronic': 'imgs/clocks/electronic',
    'clock_custom': 'imgs/clocks/custom'
}

# =========================
# Store sent message IDs per chat
# =========================
sent_messages = {}

def add_sent(chat_id, message_id):
    sent_messages.setdefault(chat_id, []).append(message_id)

def clear_sent(chat_id):
    for msg_id in sent_messages.get(chat_id, []):
        try:
            bot.delete_message(chat_id, msg_id)
        except Exception:
            pass
    sent_messages[chat_id] = []

# =========================
# Read files
# =========================
def reader(list_p, name_p, path, mode):
    logic = False if 'rb' in mode else True
    filtered = [f for f in list_p if name_p in f and (".txt" in f) == logic]
    if not filtered:
        raise FileNotFoundError(f"No file for {name_p} in {path}")
    with open(f"{path}/{filtered[0]}", mode, encoding=None if 'b' in mode else 'utf-8') as f:
        return f.read() if 'b' not in mode else f.read()

def load_prod(path, chat_id):
    files = listdir(path)
    names = list({f.split('.')[0] for f in files})
    for name in names:
        try:
            caption = reader(files, name, path, 'r')
            photo = reader(files, name, path, 'rb')
            pay_keyb = types.InlineKeyboardMarkup()
            pay_keyb.add(types.InlineKeyboardButton('Pay', callback_data='pay'))
            msg = bot.send_photo(chat_id, photo, caption=caption, reply_markup=pay_keyb)
            add_sent(chat_id, msg.message_id)
        except Exception as e:
            print("Error sending product:", e)

# =========================
# /start handler
# =========================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    first_name = message.chat.first_name or ""
    try:
        if os.path.exists("imgs/logo.jpg"):
            with open("imgs/logo.jpg", 'rb') as photo:
                bot.send_photo(chat_id, photo)
    except Exception as e:
        print("Error sending logo:", e)
    bot.reply_to(message, f"{first_name}, welcome to the Chess Shop. Enjoy it!")
    msg = bot.send_message(chat_id, "Please choose an option:", reply_markup=main_keyboard)
    add_sent(chat_id, msg.message_id)

# =========================
# Text handler
# =========================
@bot.message_handler(content_types=['text'])
def get_text(message):
    chat_id = message.chat.id
    clear_sent(chat_id)
    if message.text == "Shop items":
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton('Chess boards', callback_data='chess_board'),
                     types.InlineKeyboardButton('Chess pieces', callback_data='chess_piece'))
        keyboard.add(types.InlineKeyboardButton('Chess clocks', callback_data='chess_clock'))
        msg = bot.send_message(chat_id, "Select a items category:", reply_markup=keyboard)
        add_sent(chat_id, msg.message_id)
    elif message.text == "Share this bot":
        bot.send_message(chat_id, "https://t.me/chess_shop_bot")

# =========================
# Callback queries
# =========================
@bot.callback_query_handler(lambda c: True)
def get_query(query):
    chat_id = query.message.chat.id
    clear_sent(chat_id)
    print("Callback data:", query.data)

    if query.data in ["chess_board", "chess_piece", "chess_clock"]:
        keyboard = types.InlineKeyboardMarkup()
        if query.data == "chess_board":
            keyboard.add(types.InlineKeyboardButton('Classic', callback_data='board_classic'),
                         types.InlineKeyboardButton('3 players', callback_data='board_3p'))
            keyboard.add(types.InlineKeyboardButton('4 players', callback_data='board_4p'),
                         types.InlineKeyboardButton('Customise', callback_data='board_custom'))
        elif query.data == "chess_piece":
            keyboard.add(types.InlineKeyboardButton('Classic pieces', callback_data='pieces_classic'),
                         types.InlineKeyboardButton('Stylised for the royal period', callback_data='pieces_royal'))
            keyboard.add(types.InlineKeyboardButton('From the Harry Potter movie', callback_data='pieces_Potter'))
        elif query.data == "chess_clock":
            keyboard.add(types.InlineKeyboardButton('Mechanical clock', callback_data='clock_mechanical'),
                         types.InlineKeyboardButton('Electronic clock', callback_data='clock_electronic'))
            keyboard.add(types.InlineKeyboardButton('Custom clock', callback_data='clock_custom'))
        msg = bot.send_message(chat_id, "Select a items subcategory:", reply_markup=keyboard)
        add_sent(chat_id, msg.message_id)

    elif query.data in category_paths:
        load_prod(category_paths[query.data], chat_id)

    elif query.data == "pay":
        code = "#" + "".join(str(randint(0, 9)) for _ in range(7))
        bot.answer_callback_query(query.id, "Product purchased")
        bot.send_message(chat_id, f"Your order number: {code}")

# =========================
# Webhook route
# =========================
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/", methods=["GET"])
def index():
    return "Chess Shop Bot is running!", 200

# =========================
# Set webhook on startup
# =========================
bot.remove_webhook()
bot.set_webhook(url=f"{APP_URL}/{TOKEN}")
print(f"✅ Webhook set to {APP_URL}/{TOKEN}")

# =========================
# Run Flask
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)