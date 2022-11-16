import requests
from telebot import types
from bs4 import BeautifulSoup as bs
import telebot
import random

URL = 'https://www.anekdot.ru/best/anekdot/'
API_KEY = ''


class Parse:

    def __init__(self, url):
        self.url = url

    def parser(self):
        r = requests.get(self.url)
        soup = bs(r.text, 'html.parser')
        anekdots = soup.find_all('div', class_='text')
        listed = [c.text for c in anekdots]
        return listed


bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Тык для анекдота".format(message.from_user))


@bot.message_handler(commands=['button'])
def button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Тык для анекдота")
    markup.add(button1)


@bot.message_handler(content_types=['text'])
def jokes(message):
    if message.text == "Тык для анекдота":
        list_of_jokes = Parse(URL + '0' + str(random.randrange(1, 9, 1)) + str(random.randrange(10, 29, 1))).parser()
        random.shuffle(list_of_jokes)
        bot.send_message(message.chat.id, list_of_jokes[0])
    else:
        bot.send_message(message.chat.id, text="Не выебывайся и нажми кнопку")


bot.polling()
