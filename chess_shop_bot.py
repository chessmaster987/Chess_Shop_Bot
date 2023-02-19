import telebot
from telebot import types
from os import listdir
from random import randint

# Replace YOUR_TOKEN with the token provided by BotFather
bot = telebot.TeleBot('[YOUR_TOKEN]')

main_keyboard = types.ReplyKeyboardMarkup().add("Shop items", "Share this bot")

list_curent_id = []

def reader(list_p, name_p, ades, mode):
   #list_p - list of product resources
   #name_p - name of the currently loaded product
   #ades - address of subcategory resources
   #mode - file reading mode

   logic = False if 'rb' in mode else True

   with open(f'{ades}/{ [el for el in list_p if name_p in el and (".txt" in el) == logic ][0] }', mode, encoding='utf-8' if logic else None) as ph:
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

@bot.message_handler(commands=['start'])
def send_welcome(message):
   first_name = message.chat.first_name
   photo = open(r"Hillel_online_course_PYTHON/logo.jpg", 'rb')
   if message.text == '/start':
      bot.send_photo(message.chat.id, photo=photo)
      bot.reply_to(message, f'{first_name}, welcome to the Chess Shop. Enjoy it!')
   bot.send_message(message.chat.id, "Please choose an option:", reply_markup=main_keyboard)

def del_mes(chat_id):
   global list_curent_id
   for id_mes in list_curent_id:
      bot.delete_message(chat_id, id_mes)
      
   list_curent_id.clear()
   
@bot.message_handler(content_types=['text'])
def get_text(message):
   global list_curent_id
   if message.text == 'Shop items':
      list_curent_id.append(message.message_id)
      inline_keyboard = types.InlineKeyboardMarkup()
      inline_keyboard.add(types.InlineKeyboardButton('Chess boards', callback_data='chess_board'), 
                          types.InlineKeyboardButton('Chess pieces', callback_data='chess_piece'))
      inline_keyboard.add(types.InlineKeyboardButton('Chess clocks', callback_data='chess_clock'))
      
      del_mes(message.chat.id) 
      list_curent_id.append(
            bot.send_message(message.chat.id,
                         "Select a items category:",
                         reply_markup=inline_keyboard).message_id
      )
   if message.text == 'Share this bot':
      list_curent_id.append(message.message_id)
      bot.send_message(message.chat.id, "https://t.me/chess_shop_bot").message_id



@bot.callback_query_handler(lambda a: True)
def get_query(query):
   global list_curent_id
   print(query.data)
   if query.data == 'chess_board':
      sub_inline_keyboard = types.InlineKeyboardMarkup()
      sub_inline_keyboard.add(types.InlineKeyboardButton('Classic', callback_data='board_classic'),
                              types.InlineKeyboardButton('3 players', callback_data='board_3p'))
      sub_inline_keyboard.add(types.InlineKeyboardButton('4 players', callback_data='board_4p'),
                              types.InlineKeyboardButton('Customise', callback_data='board_custom'))   
   
      del_mes(query.message.chat.id)

      list_curent_id.append(
            bot.send_message(query.message.chat.id,
                         "Select a items subcategory:",
                         reply_markup=sub_inline_keyboard).message_id
      )

   if query.data == 'chess_piece':
      sub_inline_keyboard = types.InlineKeyboardMarkup()
      sub_inline_keyboard.add(types.InlineKeyboardButton('Classic pieces', callback_data='pieces_classic'),
                              types.InlineKeyboardButton('Stylised for the royal period', callback_data='pieces_royal'))
      sub_inline_keyboard.add(types.InlineKeyboardButton('From the Harry Potter movie', callback_data='pieces_Potter'))
      del_mes(query.message.chat.id)
      list_curent_id.append(
            bot.send_message(query.message.chat.id,
                         "Select a items subcategory:",
                         reply_markup=sub_inline_keyboard).message_id
      )

   if query.data == 'chess_clock':
      sub_inline_keyboard = types.InlineKeyboardMarkup()
      sub_inline_keyboard.add(types.InlineKeyboardButton('Mechanical clock', callback_data='clock_mechanical'),
                              types.InlineKeyboardButton('Electronic clock', callback_data='clock_electronic'))
      sub_inline_keyboard.add(types.InlineKeyboardButton('Custom clock', callback_data='clock_custom'))

      del_mes(query.message.chat.id)
      list_curent_id.append(
            bot.send_message(query.message.chat.id,
                         "Select a items subcategory:",
                         reply_markup=sub_inline_keyboard).message_id
      )

  
   
   elif query.data == 'board_classic' or query.data == 'board_3p' or query.data == 'board_4p' or query.data == 'board_custom':
      del_mes(query.message.chat.id)
      load_prod('Hillel_online_course_PYTHON/chess_shop/boards', query.message.chat.id)

   
   elif query.data == 'pieces_classic' or query.data == 'pieces_royal' or query.data == 'pieces_Potter':
      del_mes(query.message.chat.id)
      load_prod('Hillel_online_course_PYTHON/chess_shop/pieces', query.message.chat.id)
   
   elif query.data == 'clock_mechanical' or query.data == 'clock_electronic' or query.data == 'clock_custom':
      del_mes(query.message.chat.id)
      load_prod('Hillel_online_course_PYTHON/chess_shop/clocks', query.message.chat.id)

   elif query.data == 'pay':
      id_code = '#'
      for i in range(7):
         id_code += f'{randint(0,9)}'
         
      bot.answer_callback_query(query.id, 'Product purchased')
      bot.send_message(query.message.chat.id,
                         f'''Your order number: {id_code}'''
                        )
      
bot.polling()

