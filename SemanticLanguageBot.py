import telebot

import os

import semantic_handler

import json

import random

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
bot = telebot.TeleBot(input('Enter bot\' token: '), parse_mode=None)

bot_command_key = dict()

path = os.getcwd() + '/temp/'

bot_choose_pokemon_key = False


def get_dialogs():
    with open(os.getcwd() + '/data/dialog.json', 'r', encoding='utf-8') as file:
        data = file.read().strip()

    return json.loads(data)


def get_oak_answer():
    with open(os.getcwd() + '/data/oak_answers.txt', encoding='utf-8') as file:
        data = ''
        for line in file:
            if 'squirtle' in data.lower() and random.randint(0, 2) != 0:
                yield 'Congratulations! Squirtle are your Pokemon now'
            elif 'charmander' in data.lower() and random.randint(0, 2) != 0:
                yield 'Congratulations! Charmander are your Pokemon now'
            elif 'bulbasaur' in data.lower() and random.randint(0, 2) != 0:
                yield 'Congratulations! Bulbasaur are your Pokemon now'

            data = yield line


oak_answers = get_oak_answer()


@bot.message_handler(commands=['start'])
def start_message_handler(message):
    bot.send_message(message.chat.id, 'Hello, can I help you?', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def help_message_handler(message):
    bot.send_message(message.chat.id, help_message, reply_markup=keyboard)


@bot.message_handler(content_types=["document"])
def content_document(message):
    if bot_command_key[message.chat.id].lower() == 'wordcloud':
        try:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = path + message.document.file_name

            # открываем файл для записи
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)

            bot.send_photo(message.chat.id, semantic_handler.generate_wordcloud(src))
        except BaseException:
            bot.send_message(message.chat.id, 'Error document type...')
    else:
        bot.send_message(message.chat.id, 'Please choose a command.')

    bot_command_key[message.chat.id] = ''


@bot.message_handler(content_types=['text'])
def send_text(message):
    global bot_command_key
    global bot_choose_pokemon_key

    key = False

    if 'dictionary' in message.text.lower():
        key = True
        bot_command_key[message.chat.id] = 'dictionary'
        bot.send_message(message.chat.id, 'Enter a text and I will make dictionary.')
    elif 'tree' in message.text.lower():
        key = True
        bot_command_key[message.chat.id] = 'tree'
        bot.send_message(message.chat.id, 'Enter a text and I will make syntax tree.')
    elif 'analyse' in message.text.lower():
        key = True
        bot_command_key[message.chat.id] = 'analyse'
        bot.send_message(message.chat.id, 'Enter a text and I will do analyse of text.')
    elif 'wordcloud' in message.text.lower() or \
            'word cloud' in message.text.lower():
        key = True
        bot_command_key[message.chat.id] = 'wordcloud'
        bot.send_message(message.chat.id, 'Send the document (.docx) and I will make wordcloud.')

    if not key and message.chat.id in bot_command_key and len(bot_command_key[message.chat.id]) > 0:

        if bot_command_key[message.chat.id] == 'dictionary':
            answer = semantic_handler.tag_text(message.text)
            if len(answer) <= 512:
                bot.send_message(message.chat.id, answer)
            else:
                with open(path + 'dictionary.txt', 'w') as file:
                    file.write(answer)

                with open(path + 'dictionary.txt', 'rb') as file:
                    bot.send_document(message.chat.id, file)
        elif bot_command_key[message.chat.id] == 'tree':
            bot.send_photo(message.chat.id, semantic_handler.build_syntax_tree(message.text))
        elif bot_command_key[message.chat.id] == 'analyse':
            answer = semantic_handler.analyze(message.text)
            if len(answer) <= 512:
                bot.send_message(message.chat.id, answer)
            else:
                with open(path + 'syntax_analyse.txt', 'w') as file:
                    file.write(answer)

                with open(path + 'syntax_analyse.txt', 'rb') as file:
                    bot.send_document(message.chat.id, file)

        bot_command_key[message.chat.id] = ''
    elif bot_choose_pokemon_key is True:
        if message.text.lower() == 'no':
            bot_choose_pokemon_key = False
            bot.send_message(message.chat.id, 'I\'m sorry, I can\'t help you any more. All the skills and knowledge'
                                              ' you will get in your travel. Have a nice adventure!')
        else:
            answer = oak_answers.send(message.text.lower())
            if 'squirtle' in answer.lower():
                bot.send_message(message.chat.id, answer)
                bot.send_photo(message.chat.id, open(os.getcwd() + '/img/squirtle.png', 'rb'))
                bot_choose_pokemon_key = False
            elif 'charmander' in answer.lower():
                bot.send_message(message.chat.id, answer)
                bot.send_photo(message.chat.id, open(os.getcwd() + '/img/charmander.png', 'rb'))
                bot_choose_pokemon_key = False
            elif 'bulbasaur' in answer.lower():
                bot.send_message(message.chat.id, answer)
                bot.send_photo(message.chat.id, open(os.getcwd() + '/img/bulbasaur.png', 'rb'))
                bot_choose_pokemon_key = False
            elif 'pikachu' in answer.lower():
                bot.send_message(message.chat.id, answer)
                bot.send_photo(message.chat.id, open(os.getcwd() + '/img/pikachu.png', 'rb'))
                bot_choose_pokemon_key = False
            else:
                bot.send_message(message.chat.id, answer)

    elif 'choose' in message.text.lower() and 'pokemon' in message.text.lower():
        bot_choose_pokemon_key = True
        bot.send_message(message.chat.id, oak_answers.send(None))
    elif not key:
        dialogs = get_dialogs()
        answer_key = False
        for dialog in dialogs:
            if message.text.lower() in dialog['question'].lower():
                answer_key = True
                answers = list(dialog['answer'].split('|'))
                bot.send_message(message.chat.id, answers[random.randint(0, len(answers) - 1)])
                break

        if answer_key is False:
            bot.send_message(message.chat.id, 'I\'m sorry, I can\'t help you any more. All the skills and knowledge'
                                              ' you will get in your travel. Have a nice adventure!')


keyboard = telebot.types.ReplyKeyboardMarkup()

keyboard.row('Add text to the dictionary')
keyboard.row('Build semantic tree')
keyboard.row('Get semantic analyse of text')
keyboard.row('Build word cloud')
