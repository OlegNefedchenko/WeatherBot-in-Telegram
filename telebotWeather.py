#Модулу для написання боту.
import telebot
from telebot import types
import requests
import json

#Токен телеграм боту взятий від TelegramBotFather.
bot = telebot.TeleBot('5638832023:AAGRfOD7FBTPSQcxuP0aaL7MAJpbVL94yMQ')
#Токен з сайту https://api.openweathermap.org/ для показу погоди.
api = 'b32541d02356e8f64558327951dad21b'

#Вітання з користувачем при написанні команди /start.
@bot.message_handler(commands= ['start'])
def start(chat):
    bot.send_message(chat.chat.id, f'Вітаю <b>{chat.chat.first_name} {chat.chat.last_name}</b>.\n Введіть назву міста:', parse_mode= 'html')

#Отримання інформації про погоду.
@bot.message_handler(content_types=['text'])
def enter_city(chat):
    #city - користувач вводить назву міста, в якому хоче переглянути погоду.
    city = chat.text.strip().lower()
    website1 = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}&units=metric')
    #Перевірка, чи існує місто.
    #Якщо так, то вивидить інформацію в месенджер.
    if website1.status_code == 200:
        data = json.loads(website1.text)
        temp = round(data["main"]["temp"])
        weather = data ["weather"][0]["main"]
        wind_speed = data["wind"]["speed"]
        country = data["sys"]["country"]
        # button - кнопка з посиланням на сайт з погодою.
        button = types.InlineKeyboardMarkup()
        button.add(types.InlineKeyboardButton("Відвідати сайт з погодою", url="https://ua.sinoptik.ua/"))
        #Вивод у чат боту температури, погоди, швидкості вітру.
        if weather == "Rain":
            file =open('./'+'Rain.jpg','rb')
            bot.send_photo(chat.chat.id,file)
            bot.reply_to(chat, f' Температура в місті {city.upper()},{country} = {temp}°С. Погода на вулиці: Дощ. \n Швидкість вітру = {wind_speed}м/с.', reply_markup=button)
        elif weather == "Clouds":
            file = open('./' + 'Cloud.png', 'rb')
            bot.send_photo(chat.chat.id, file)
            bot.reply_to(chat, f' Температура в місті {city.upper()},{country} = {temp}°С. Погода на вулиці: Хмарно. \n Швидкість вітру = {wind_speed}м/с.', reply_markup=button)
        elif weather == "Snow":
            file = open('./' + 'Cloud.png', 'rb')
            bot.send_photo(chat.chat.id, file)
            bot.reply_to(chat, f' Температура в місті {city.upper()},{country} = {temp}°С. Погода на вулиці: Сніг. \n Швидкість вітру = {wind_speed}м/с.', reply_markup=button)
        else:
            file = open('./' + 'Sun.png', 'rb')
            bot.send_photo(chat.chat.id, file)
            bot.reply_to(chat, f' Температура в місті {city.upper()},{country} = {temp}°С. Погода на вулиці: Сонячно. \n Швидкість вітру = {wind_speed}м/с.', reply_markup=button)
    #Якщо ні, виводиться повідомлення що міста не існує.
    else:
        bot.reply_to(chat,'Місто, яке ви ввели, не існує. Спробуйте ще раз:')

#Метод для безпреривної роботи боту.
bot.polling(none_stop=True)
