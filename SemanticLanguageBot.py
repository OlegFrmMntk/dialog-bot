import telebot

import os

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

token = '1734276898:AAFzgB1ShRrZ_jd3AbrKls51QC4O8soK0_Y'

# You can set parse_mode by default. HTML or MARKDOWN
bot = telebot.TeleBot(token, parse_mode=None)

bot_command_key = dict()

path = os.getcwd() + '/temp/'


@bot.message_handler(commands=['start'])
def start_message_handler(message):
    bot.send_message(message.chat.id, 'Hello, can I help you?', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def help_message_handler(message):
    bot.send_message(message.chat.id, help_message, reply_markup=keyboard)


@bot.message_handler(content_types=["document"])
def content_document(message):
    if bot_command_key[message.chat.id].lower() == 'build word cloud':
        try:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = path + message.document.file_name

            # открываем файл для записи
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)

            bot.send_photo(message.chat.id, semantic_handler.generate_wordcloud(src))
        except BaseException:
            bot.send_message(message.chat.id, 'Error document type')
    else:
        bot.send_message(message.chat.id, 'Please choose a command')

    bot_command_key[message.chat.id] = ''


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
        bot.send_message(message.chat.id, 'Send the document (.docx)')

    if not key and message.chat.id in bot_command_key and len(bot_command_key[message.chat.id]) > 0:

        if bot_command_key[message.chat.id] == 'add text to the dictionary':
            answer = semantic_handler.tag_text(message.text)
            if len(answer) <= 512:
                bot.send_message(message.chat.id, answer)
            else:
                with open(path + 'dictionary.txt', 'w') as file:
                    file.write(answer)

                with open(path + 'dictionary.txt', 'rb') as file:
                    bot.send_document(message.chat.id, file)
        elif bot_command_key[message.chat.id] == 'build semantic tree':
            bot.send_photo(message.chat.id, semantic_handler.build_syntax_tree(message.text))
        elif bot_command_key[message.chat.id] == 'get semantic analyse of text':
            answer = semantic_handler.analyze(message.text)
            if len(answer) <= 512:
                bot.send_message(message.chat.id, answer)
            else:
                with open(path + 'syntax_analyse.txt', 'w') as file:
                    file.write(answer)

                with open(path + 'syntax_analyse.txt', 'rb') as file:
                    bot.send_document(message.chat.id, file)

        bot_command_key[message.chat.id] = ''
    elif not key:
        bot.send_message(message.chat.id, 'Chatting')


keyboard = telebot.types.ReplyKeyboardMarkup()

keyboard.row('Add text to the dictionary')
keyboard.row('Build semantic tree')
keyboard.row('Get semantic analyse of text')
keyboard.row('Build word cloud')
