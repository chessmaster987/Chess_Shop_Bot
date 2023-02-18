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
      inline_keyboard.add(types.InlineKeyboardButton('chess clocks', callback_data='chess_clock'))
      bot.send_message(message.chat.id, "Оберіть категорію товарів:", reply_markup=inline_keyboard)

bot.polling()
