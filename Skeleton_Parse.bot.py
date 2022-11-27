import os
import telebot
from telebot import types
from dotenv import load_dotenv
import logging

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
    return (theme_list.split('\n'))

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
    welcome_mess = f'Добрый день,{message.chat.first_name}! \nВыберите сайты, откуда искать новости'
    bot.send_message(message.chat.id, welcome_mess)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [types.KeyboardButton("Новости с профильных сайтов"), types.KeyboardButton("Новости с общепрофильных сайтов")]
    for button in buttons:
        markup.add(button)
    # Баг с добавлением листа в маркап


@bot.message_handler(content_types=['text'])  #Будет выбор для парсера всех новостей с профильных сайтов или для выборочного парсера больших сайтов
def choice(message: types.Message):
    if message.text == 'Новости с профильных сайтов':
        bot.send_message(message.chat.id, text=Parser().Parse_prof())
    elif message.text == 'Новости с общепрофильных сайтов':
        markup = types.InlineKeyboardMarkup(row_width=2)
        for button in Theme_list('Theme_list.txt'): # Каждый эдд это новый ряд
            markup.add(types.InlineKeyboardButton(button[2:],callback_data=f"{button[:][0]}")) # Здесь ебейшая загвоздка с размером колбэк даты, походу придется биндить через цифры
        bot.send_message(message.chat.id, text='Выберите тему', reply_markup=markup) #Темы надо сокращать, получается пиздец
# С реплай кнопками выглядит сочнее если честно, но надо спросить у всех что все думают

#@bot.callback_query_handler(func=lambda call: True)
#def callback_handler(call):
#    bot.send_message(chat_id=)


if __name__ == '__main__':
    logger.info("Starting bot")
    bot.polling(none_stop=True, timeout=123)