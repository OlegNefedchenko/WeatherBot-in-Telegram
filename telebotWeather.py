#������ ��� ��������� ����.
import telebot
from telebot import types
import requests
import json

#����� �������� ���� ������ �� TelegramBotFather.
bot = telebot.TeleBot('5638832023:AAGRfOD7FBTPSQcxuP0aaL7MAJpbVL94yMQ')
#����� � ����� https://api.openweathermap.org/ ��� ������ ������.
api = 'b32541d02356e8f64558327951dad21b'

#³����� � ������������ ��� �������� ������� /start.
@bot.message_handler(commands= ['start'])
def start(chat):
    bot.send_message(chat.chat.id, f'³��� <b>{chat.chat.first_name} {chat.chat.last_name}</b>.\n ������ ����� ����:', parse_mode= 'html')

#��������� ���������� ��� ������.
@bot.message_handler(content_types=['text'])
def enter_city(chat):
    #city - ���������� ������� ����� ����, � ����� ���� ����������� ������.
    city = chat.text.strip().lower()
    website1 = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}&units=metric')
    #��������, �� ���� ����.
    #���� ���, �� �������� ���������� � ���������.
    if website1.status_code == 200:
        data = json.loads(website1.text)
        temp = round(data["main"]["temp"])
        weather = data ["weather"][0]["main"]
        wind_speed = data["wind"]["speed"]
        country = data["sys"]["country"]
        # button - ������ � ���������� �� ���� � �������.
        button = types.InlineKeyboardMarkup()
        button.add(types.InlineKeyboardButton("³������ ���� � �������", url="https://ua.sinoptik.ua/"))
        #����� � ��� ���� �����������, ������, �������� ����.
        if weather == "Rain":
            file =open('./'+'Rain.jpg','rb')
            bot.send_photo(chat.chat.id,file)
            bot.reply_to(chat, f' ����������� � ��� {city.upper()},{country} = {temp}��. ������ �� ������: ���. \n �������� ���� = {wind_speed}�/�.', reply_markup=button)
        elif weather == "Clouds":
            file = open('./' + 'Cloud.png', 'rb')
            bot.send_photo(chat.chat.id, file)
            bot.reply_to(chat, f' ����������� � ��� {city.upper()},{country} = {temp}��. ������ �� ������: ������. \n �������� ���� = {wind_speed}�/�.', reply_markup=button)
        elif weather == "Snow":
            file = open('./' + 'Cloud.png', 'rb')
            bot.send_photo(chat.chat.id, file)
            bot.reply_to(chat, f' ����������� � ��� {city.upper()},{country} = {temp}��. ������ �� ������: ���. \n �������� ���� = {wind_speed}�/�.', reply_markup=button)
        else:
            file = open('./' + 'Sun.png', 'rb')
            bot.send_photo(chat.chat.id, file)
            bot.reply_to(chat, f' ����������� � ��� {city.upper()},{country} = {temp}��. ������ �� ������: �������. \n �������� ���� = {wind_speed}�/�.', reply_markup=button)
    #���� �, ���������� ����������� �� ���� �� ����.
    else:
        bot.reply_to(chat,'̳���, ��� �� �����, �� ����. ��������� �� ���:')

#����� ��� ����������� ������ ����.
bot.polling(none_stop=True)
