import os
import telebot
from telebot import types
from dotenv import load_dotenv
import logging
import transcriptbot
import re

load_dotenv()

TOKEN = os.getenv('TOKEN')    # token for the telegram API is located in .env
bot = telebot.TeleBot(TOKEN)

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def Theme_list(file):  #  Через эту функцию список тем будет загружаться в лист
    f = open (file, encoding='utf-8')
    theme_list = f.read()
    f.close()
    theme_list = theme_list.split('\n')
    theme_list.sort()
    return (theme_list)
#Сделать алфавитную сортировку DONE

class Parser:
    def __init__(self):
        pass
    def Parse_prof(self):
        return ('Okay')
    def Parse_wide(self):
        return ('Okay1')


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    name = message.chat.first_name if message.chat.first_name else 'No_name'
    logger.info(f"Chat {name} (ID: {message.chat.id}) started bot")
    welcome_mess = f'Добрый день,{name} \nВыберите сайты, откуда искать новости'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = [types.KeyboardButton("Новости с профильных сайтов"), types.KeyboardButton("Новости с общепрофильных сайтов")]
    for button in buttons:
        markup.add(button)
    bot.send_message(message.chat.id, welcome_mess, reply_markup=markup)
    # Баг с добавлением листа в маркап


@bot.message_handler(content_types=['text'])  #Будет выбор для парсера всех новостей с профильных сайтов или для выборочного парсера больших сайтов
def choice(message: types.Message):
    if message.text == 'Новости с профильных сайтов':
        bot.send_message(message.chat.id, text=Parser().Parse_prof())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        buttons = [types.KeyboardButton("Новости с профильных сайтов"),
                   types.KeyboardButton("Новости с общепрофильных сайтов")]
        for button in buttons:
            markup.add(button)
        bot.send_message(message.chat.id, text="Функция в разработке", reply_markup=markup)
    elif message.text == 'Новости с общепрофильных сайтов':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for button in Theme_list('Theme_list.txt'): # Каждый эдд это новый ряд
            markup.add(types.KeyboardButton(button[2:]))#,callback_data=f"{button[:][0]}")) # Здесь ебейшая загвоздка с размером колбэк даты, походу придется биндить через цифры
        bot.send_message(message.chat.id, text='Выберите тему',reply_markup=markup) #Темы надо сокращать, получается пиздец
# С реплай кнопками выглядит сочнее если честно, но надо спросить у всех что все думают
    elif message.text == 'Сооружение и эксплуатация АЭС и атомных реакторов':
        bot.send_message(message.chat.id, text=Parser().Parse_wide())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        buttons = [types.KeyboardButton("Новости с профильных сайтов"),
                   types.KeyboardButton("Новости с общепрофильных сайтов")]
        for button in buttons:
            markup.add(button)
        bot.send_message(message.chat.id, text="Функция в разработке", reply_markup=markup)


@bot.message_handler(content_types=['voice'])
def get_audio_messages(message: types.Message):
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_name = str(message.message_id) + '.ogg'
    name = message.chat.first_name if message.chat.first_name else 'No_name'
    logger.info(f"Chat {name} (ID: {message.chat.id}) download file {file_name}")

    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    converter = transcriptbot.Converter(file_name)
    os.remove(file_name)
    text = converter.audio_to_text()
    del converter
    pattern = text[:25]
    f = open('Theme_list.txt', encoding='utf-8')
    theme_list = f.read()
    result = re.findall(pattern,theme_list)
    f.close()
    bot.send_message(message.chat.id, text= result[0])
    Parser().Parse_wide()



@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    bot.send_message(call.message.chat.id, text="Okay")


if __name__ == '__main__':
    logger.info("Starting bot")
    bot.polling(none_stop=True)