import os
import telebot
from telebot import types
from dotenv import load_dotenv
import logging
import transcriptbot
import re
import stepbrother
import atomic_energy

load_dotenv()

TOKEN = os.getenv('TOKEN')    # token for the telegram API is located in .env
bot = telebot.TeleBot(TOKEN)

# webhook settings
#WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
#WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)

#bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def Theme_list(file,mode='parse'):  #  Через эту функцию список тем будет загружаться в лист
    f = open (file, encoding='utf-8')
    theme_list = f.read()
    f.close()
    if mode == 'recognition':
        return (theme_list)
    theme_list = theme_list.split('\n')
    theme_list.sort()
    return (theme_list)
#Сделать алфавитную сортировку DONE

class Parser:
    def __init__(self):
        pass
    def Parse_prof(self):
        return (atomic_energy.parse(stepbrother.parse()))
        #return (im.imp())
    def Parse_wide(self):
        return ('Okay1')


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    name = message.chat.first_name if message.chat.first_name else 'No_name'
    logger.info(f"Chat {name} (ID: {message.chat.id}) started bot")
    welcome_mess = f'Добрый день, Андрей Андреевич \nВыберите сайты, откуда искать новости'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = [types.KeyboardButton("Новости с профильных сайтов"), types.KeyboardButton("Новости с общепрофильных сайтов")]
    for button in buttons:
        markup.add(button)
    bot.send_message(message.chat.id, welcome_mess, reply_markup=markup)


@bot.message_handler(content_types=['text'])  #Будет выбор для парсера всех новостей с профильных сайтов или для выборочного парсера больших сайтов
def choice(message: types.Message):
    match message.text:
        case 'Новости с профильных сайтов':
            for news in Parser().Parse_prof():
                bot.send_message(message.chat.id, text=news)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            buttons = [types.KeyboardButton("Новости с профильных сайтов"),
                       types.KeyboardButton("Новости с общепрофильных сайтов")]
            for button in buttons:
                markup.add(button)
            bot.send_message(message.chat.id, "Что-то еще?", reply_markup=markup)
        case 'Новости с общепрофильных сайтов':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for button in Theme_list('Theme_list.txt'): # Каждый эдд это новый ряд
                markup.add(types.KeyboardButton(button))#,callback_data=f"{button[:][0]}"))
            bot.send_message(message.chat.id, text='Выберите тему',reply_markup=markup) #Темы надо сокращать
    # С реплай кнопками выглядит сочнее если честно, но надо спросить у всех что все думают
        case 'Сооружение и эксплуатация АЭС и атомных реакторов': #Дописать этот кусок по уму
            bot.send_message(message.chat.id, text=Parser().Parse_wide())
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            buttons = [types.KeyboardButton("Новости с профильных сайтов"),
                       types.KeyboardButton("Новости с общепрофильных сайтов")]
            for button in buttons:
                markup.add(button)
            bot.send_message(message.chat.id, text="Функция в разработке", reply_markup=markup)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = [types.KeyboardButton("Новости с профильных сайтов"),
               types.KeyboardButton("Новости с общепрофильных сайтов")]
    for button in buttons:
        markup.add(button)

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
    pattern = str(pattern)
    result = None
    theme_list =  Theme_list('Theme_list.txt','recognition')
    #for theme in theme_list:
    try:
        result = re.findall(pattern, theme_list)
        #logger.info(f"Chat {name} (ID: {message.chat.id}) {result}")
    except re.error:
        pass
    if result != []:                #Добавить обязательно вывод не распознанного а полной темы по ее куску
        bot.send_message(message.chat.id, text= result[0])
        Parser().Parse_wide()
    else:
    #if message.content_type == 'voice':
        bot.send_message(message.chat.id, text="Повторите название темы")


#@bot.callback_query_handler(func=lambda call: True)
#def callback_handler(call):
 #   bot.send_message(call.message.chat.id, text="Okay")


if __name__ == '__main__':
    logger.info("Starting bot")
    bot.polling(none_stop=True)