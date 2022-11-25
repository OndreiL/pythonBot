import os
import telebot
from telebot import types
from dotenv import load_dotenv
import logging
import datetime
import telegramcalendar, telegramjcalendar

load_dotenv()

TOKEN = os.getenv('TOKEN')    # token for the telegram API is located in .env
bot = telebot.TeleBot(TOKEN)

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

class Parser:
    pass

@bot.message_handler(commands=['start'])
def start(message: types.Message):
    pass

@bot.message_handler(commands=['calendar'])
def get_calendar(message):
    now = datetime.datetime.now()  # Текущая дата
    chat_id = message.chat.id
    date = (now.year, now.month)
    current_shown_dates[chat_id] = date  # Сохраним текущую дату в словарь
    markup = create_calendar(now.year, now.month)
    bot.send_message(message.chat.id, "Пожалйста, выберите дату", reply_markup=markup)

if __name__ == '__main__':
    logger.info("Starting bot")
    bot.polling(none_stop=True, timeout=123)