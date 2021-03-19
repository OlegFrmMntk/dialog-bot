import telebot

import semantic_handler

help_message = """
1)Choose a command
2)Enter the text (Send the document for command "Build word cloud")

Dictionary:
S -- Start element(whole sentence)
P -- Preposition
N -- Noun
V -- Verbs and modals
JJP -- Adjective part(Adjectives, adverbs and cardinals)
NP -- Noun part
PP -- Prepositional part
VP -- Verbal part
"""

# You can set parse_mode by default. HTML or MARKDOWN
bot = telebot.TeleBot('1734276898:AAFzgB1ShRrZ_jd3AbrKls51QC4O8soK0_Y', parse_mode=None)
bot_command_key = dict()


@bot.message_handler(commands=['start'])
def start_message_handler(message):
    bot.send_message(message.chat.id, 'Hello, can I help you?', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def help_message_handler(message):
    bot.send_message(message.chat.id, help_message, reply_markup=keyboard)


@bot.message_handler(content_types=["document"])
def content_document(message):
    bot.send_photo(message.chat.id, open('squirtle.png', 'rb'))
    #bot.send_photo(message.chat.id, semantic_handler.generate_wordcloud(message))


@bot.message_handler(content_types=['text'])
def send_text(message):
    global bot_command_key
    key = False

    if message.text.lower() in ('add text to the dictionary', 'build semantic tree', 'get semantic analyse of text'):
        key = True
        bot_command_key[message.chat.id] = str(message.text.lower())
        bot.send_message(message.chat.id, 'Enter a text')
    elif message.text.lower() == 'build word cloud':
        key = True
        bot_command_key[message.chat.id] = str(message.text.lower())
        bot.send_message(message.chat.id, 'Send the document')

    if not key and message.chat.id in bot_command_key and len(bot_command_key[message.chat.id]) > 0:

        if bot_command_key[message.chat.id] == 'add text to the dictionary':
            bot.send_message(message.chat.id, semantic_handler.tag_text(message.text))
        elif bot_command_key[message.chat.id] == 'build semantic tree':
            bot.send_message(message.chat.id, 'TREEEEEEEEEEEEEEEEEEEEEE')
            semantic_handler.build_syntax_tree(message.text)
#           bot.send_photo(message.chat.id, semantic_handler.build_syntax_tree(message.text))
        elif bot_command_key[message.chat.id] == 'get semantic analyse of text':
            bot.send_message(message.chat.id, semantic_handler.analyze(message.text))

        bot_command_key[message.chat.id] = ''
    elif not key:
        bot.send_message(message.chat.id, 'Chatting')


keyboard = telebot.types.ReplyKeyboardMarkup()

keyboard.row('Add text to the dictionary')
keyboard.row('Build semantic tree')
keyboard.row('Get semantic analyse of text')
keyboard.row('Build word cloud')
