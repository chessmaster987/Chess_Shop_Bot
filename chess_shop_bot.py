import os
from os import listdir
from random import randint
import telebot
from telebot import types
from dotenv import load_dotenv

# ------------------------------
# Load environment variables
# ------------------------------
load_dotenv()
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise ValueError("Please set BOT_TOKEN in .env file")

bot = telebot.TeleBot(TOKEN)

# ------------------------------
# Keyboards
# ------------------------------
main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add("Shop items", "Share this bot")

list_curent_id = []

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

# ------------------------------
# Helper functions
# ------------------------------
def reader(list_p, name_p, ades, mode):
    logic = False if 'rb' in mode else True
    filtered_list = [el for el in list_p if name_p in el and (".txt" in el) == logic]
    if not filtered_list:
        raise FileNotFoundError(f"No file found for {name_p} in {ades}")
    with open(f'{ades}/{filtered_list[0]}', mode, encoding='utf-8' if logic else None) as ph:
        return ph.read()

def load_prod(address, chat_id):
    global list_curent_id
    list_product = listdir(address)
    list_uniq_name = list({el.split('.')[0] for el in list_product})

    pay_keyb = types.InlineKeyboardMarkup()
    pay_keyb.add(types.InlineKeyboardButton('Pay', callback_data='pay'))

    for name_prod in list_uniq_name:
        list_curent_id.append(
            bot.send_photo(chat_id,
                           reader(list_product, name_prod, address, 'rb'),
                           caption=reader(list_product, name_prod, address, 'r'),
                           reply_markup=pay_keyb
                           ).message_id
        )

def del_mes(chat_id):
    global list_curent_id
    for id_mes in list_curent_id:
        try:
            bot.delete_message(chat_id, id_mes)
        except:
            pass
    list_curent_id.clear()

# ------------------------------
# Handlers
# ------------------------------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    first_name = message.chat.first_name or ""
    try:
        with open("imgs/logo.jpg", 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    except:
        bot.send_message(message.chat.id, "[Logo not found]")
    bot.reply_to(message, f"{first_name}, welcome to the Chess Shop. Enjoy it!")
    bot.send_message(message.chat.id, "Please choose an option:", reply_markup=main_keyboard)

@bot.message_handler(content_types=['text'])
def get_text(message):
    global list_curent_id
    if message.text == 'Shop items':
        list_curent_id.append(message.message_id)
        inline_keyboard = types.InlineKeyboardMarkup()
        inline_keyboard.add(
            types.InlineKeyboardButton('Chess boards', callback_data='chess_board'),
            types.InlineKeyboardButton('Chess pieces', callback_data='chess_piece')
        )
        inline_keyboard.add(
            types.InlineKeyboardButton('Chess clocks', callback_data='chess_clock')
        )

        del_mes(message.chat.id)
        list_curent_id.append(
            bot.send_message(message.chat.id, "Select a items category:", reply_markup=inline_keyboard).message_id
        )

    if message.text == 'Share this bot':
        list_curent_id.append(message.message_id)
        bot.send_message(message.chat.id, "https://t.me/chess_shop_bot").message_id

@bot.callback_query_handler(lambda a: True)
def get_query(query):
    global list_curent_id
    print("Callback:", query.data)

    if query.data == 'chess_board':
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton('Classic', callback_data='board_classic'),
               types.InlineKeyboardButton('3 players', callback_data='board_3p'))
        kb.add(types.InlineKeyboardButton('4 players', callback_data='board_4p'),
               types.InlineKeyboardButton('Customise', callback_data='board_custom'))
        del_mes(query.message.chat.id)
        list_curent_id.append(
            bot.send_message(query.message.chat.id, "Select a items subcategory:", reply_markup=kb).message_id
        )

    elif query.data == 'chess_piece':
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton('Classic pieces', callback_data='pieces_classic'),
               types.InlineKeyboardButton('Stylised for the royal period', callback_data='pieces_royal'))
        kb.add(types.InlineKeyboardButton('From the Harry Potter movie', callback_data='pieces_Potter'))
        del_mes(query.message.chat.id)
        list_curent_id.append(
            bot.send_message(query.message.chat.id, "Select a items subcategory:", reply_markup=kb).message_id
        )

    elif query.data == 'chess_clock':
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton('Mechanical clock', callback_data='clock_mechanical'),
               types.InlineKeyboardButton('Electronic clock', callback_data='clock_electronic'))
        kb.add(types.InlineKeyboardButton('Custom clock', callback_data='clock_custom'))
        del_mes(query.message.chat.id)
        list_curent_id.append(
            bot.send_message(query.message.chat.id, "Select a items subcategory:", reply_markup=kb).message_id
        )

    elif query.data in category_paths:
        del_mes(query.message.chat.id)
        load_prod(category_paths[query.data], query.message.chat.id)

    elif query.data == 'pay':
        id_code = '#' + ''.join([str(randint(0, 9)) for _ in range(7)])
        bot.answer_callback_query(query.id, 'Product purchased')
        bot.send_message(query.message.chat.id, f"Your order number: {id_code}")

# ------------------------------
# Start polling
# ------------------------------
if __name__ == "__main__":
    print("🤖 Bot is running locally...")
    bot.remove_webhook()
    bot.infinity_polling()