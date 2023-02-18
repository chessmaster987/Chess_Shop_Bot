import telebot
from telebot import types
from os import listdir

# Replace YOUR_TOKEN with the token provided by BotFather
bot = telebot.TeleBot('[YOUR_TOKEN]')

main_keyboard = types.ReplyKeyboardMarkup().add("Shop items", "Share this bot")

@bot.message_handler(commands=['start'])
def send_welcome(message):
   bot.reply_to(message, 'Welcome to the Chess Shop. Enjoy it!')
   bot.send_message(message.chat.id, "Please choose an option:", reply_markup=main_keyboard)

@bot.message_handler(content_types=['text'])
def get_text(message):
   if message.text == 'Shop items':
      inline_keyboard = types.InlineKeyboardMarkup()
      inline_keyboard.add(types.InlineKeyboardButton('Chess boards', callback_data='chess_board'), 
                          types.InlineKeyboardButton('Chess pieces', callback_data='chess_piece'))
      inline_keyboard.add(types.InlineKeyboardButton('Chess clocks', callback_data='chess_clock'))
      bot.send_message(message.chat.id, "Select a items category:", reply_markup=inline_keyboard)

@bot.callback_query_handler(lambda a: True)
def get_query(query):
   print(query.data)
   if query.data == 'chess_board':
      sub_inline_keyboard = types.InlineKeyboardMarkup()
      sub_inline_keyboard.add(types.InlineKeyboardButton('Classic', callback_data='board_classic'),
                              types.InlineKeyboardButton('3 players', callback_data='board_3p'))
      sub_inline_keyboard.add(types.InlineKeyboardButton('4 players', callback_data='board_4p'),
                              types.InlineKeyboardButton('Customise', callback_data='board_custom'))

      bot.send_message(query.message.chat.id, "Select a items subcategory:", reply_markup=sub_inline_keyboard)
   elif query.data == 'chess_piece':
      sub_inline_keyboard = types.InlineKeyboardMarkup()
      sub_inline_keyboard.add(types.InlineKeyboardButton('Classic pieces', callback_data='pieces_classic'),
                              types.InlineKeyboardButton('Stylised for the royal period', callback_data='pieces_royal'))
      sub_inline_keyboard.add(types.InlineKeyboardButton('From the Harry Potter movie', callback_data='pieces_Potter'))
      bot.send_message(query.message.chat.id, "Select a items subcategory:", reply_markup=sub_inline_keyboard)
   elif query.data == 'chess_clock':
      sub_inline_keyboard = types.InlineKeyboardMarkup()
      sub_inline_keyboard.add(types.InlineKeyboardButton('Mechanical clock', callback_data='clock_mechanical'),
                              types.InlineKeyboardButton('Electronic clock', callback_data='clock_electronic'))
      bot.send_message(query.message.chat.id, "Select a items subcategory:", reply_markup=sub_inline_keyboard)
         
bot.polling()
