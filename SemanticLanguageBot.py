import telebot

import semantic_handler

# You can set parse_mode by default. HTML or MARKDOWN
bot = telebot.TeleBot('1734276898:AAFzgB1ShRrZ_jd3AbrKls51QC4O8soK0_Y', parse_mode=None)
bot_command_key = ''


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Hello, can I help you?', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def send_text(message):
    global bot_command_key
    key = False

    if message.text.lower() in ('add text to the dictionary', 'build semantic tree', 'get semantic analyse of text'):
        key = True
        bot_command_key = str(message.text.lower())
        bot.send_message(message.chat.id, 'Enter a text')

    if not key and len(bot_command_key) > 0:

        if bot_command_key == 'add text to the dictionary':
            bot.send_message(message.chat.id, semantic_handler.tag_text(message.text))
        elif bot_command_key == 'build semantic tree':
            # Need semantic tree picture
            bot.send_photo(message.chat.id, semantic_handler.build_syntax_tree(message.text))
        elif bot_command_key == 'get semantic analyse of text':
            bot.send_message(message.chat.id, 'Semantic analyse')

        bot_command_key = ''
    elif not key:
        bot.send_message(message.chat.id, 'Chatting')


keyboard = telebot.types.ReplyKeyboardMarkup()

keyboard.row('Add text to the dictionary')
keyboard.row('Build semantic tree')
keyboard.row('Get semantic analyse of text')
keyboard.row('Help')
