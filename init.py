from telebot import types 
import telebot
from pyqiwip2p import QiwiP2P
import json
import time
import threading


produc = {}
bills = []
BOT_TOKEN = "5572108825:AAFYNn_n2tSuoXMIvY7KaXW1_qqilRSn84A"
QIWI_PRIV_KEY = "eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6InBkOG5vci0wMCIsInVzZXJfaWQiOiI3OTYxNDg3Mzk0MyIsInNlY3JldCI6IjA2MzIzYzFlOWI2YTQ4ZGZjM2JjZTQ3NzI1MWMwNDFlOWRkYjk1YTNkZDZkNzJjNTZjMTEyNzNiNzNiNDU1ZDcifX0="




bot = telebot.TeleBot(token=BOT_TOKEN)
p2p = QiwiP2P(auth_key=QIWI_PRIV_KEY)

#SHOP#################################################################################################
##################################################################################################
def buy(message, List_):
    global produc
    if message.text == "✅":
        if List_['type'] == "Лайки":
            description = f"🔖 В течение времени для Вашего поста, который указан в заказе, будут накручены лайки. В любой момент с Вами смогут связаться, как через бота, так и в лс."
        else:
            description = f"🔖 В течение времени для Вашего аккаунта, который указан в заказе, будут накручены подписчики. В любой момент с Вами смогут связаться, как через бота, так и в лс."
        amount = int(int(List_['price'])*int(List_['count']))
        new_bill = p2p.bill(amount=amount, lifetime=1)
        bot.send_message(message.chat.id, f"ссылка для оплаты {new_bill.pay_url}")
        produc[message.chat.id] = List_
        bills.append([new_bill.bill_id, message.chat.id, message.from_user.username])
    else:
        bot.send_message(message.chat.id, "⚠️Отмена заказа")
def result(message, List_):
    OK = types.ReplyKeyboardMarkup(row_width=5, resize_keyboard=True, one_time_keyboard=True).add(
        types.KeyboardButton(text='✅'),types.KeyboardButton(text='🚫'))
    List_['info'] = message.text
    msg = bot.send_message(message.chat.id, f"📦📦📦 Заказ 📦📦📦\n\n📍 Мессенджер: {List_['msgr']}\n📍 Тип: {List_['type']}\n📍 Цена: {int(List_['price'])*int(List_['count'])} за {List_['count']}\n\nИнфо:\n{List_['info']}", reply_markup=OK)
    bot.register_next_step_handler(msg, buy, List_)
def info(message, List_, counts):
    try:
        List_['count'] = int(message.text)
        msg = bot.send_message(message.chat.id, "🗒 Данные к заказу (ссылки и Ваши пожелания)")
        bot.register_next_step_handler(msg, result, List_)
    except:
        msg = bot.send_message(message.chat.id, f"🖇Количество услуг за {List_['price']} x (шт)", reply_markup=counts)
        bot.register_next_step_handler(msg, info, List_, counts)
def count(message, List_, prices):
    counts = types.ReplyKeyboardMarkup(row_width=5, resize_keyboard=True, one_time_keyboard=True).add(
    types.KeyboardButton(text='1'),types.KeyboardButton(text='2'),types.KeyboardButton(text='4'), types.KeyboardButton(text='10'), types.KeyboardButton(text='20'))
    if (message.text == "1К подписчиков - 199р") or (message.text == "1K лайков - 99р"):
        if message.text == "1К подписчиков - 199р":
           List_['price'],List_['type'] = 199, 'Подписки'
        else:
            List_['price'],List_['type'] = 99, 'Лайки'
        msg = bot.send_message(message.chat.id, f"🖇Количество услуг за {List_['price']} x (шт)", reply_markup=counts)
        bot.register_next_step_handler(msg, info, List_, counts)
    else:
        msg = bot.send_message(message.chat.id, "💰 Выбор цены услуги (1 шт)", reply_markup=prices)
        bot.register_next_step_handler(msg, count, List_, prices)
def price(message, messagers):
    if (message.text == "Telegram") or (message.text == "Instagram") or (message.text == "Вконтакте"):
        prices = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True).add(
            types.KeyboardButton(text='1К подписчиков - 199р'))
        if message.text != "Telegram":
            prices.add(types.KeyboardButton(text='1K лайков - 99р'))
        msg = bot.send_message(message.chat.id, f"💰 Мессенджер: {message.text}\n Выбор услуги (1 шт)", reply_markup=prices)
        bot.register_next_step_handler(msg , count, {"msgr": message.text}, prices)
    else:
        msg = bot.send_message(message.chat.id, "🔎 Выберите мессенджер", reply_markup=messagers)
        bot.register_next_step_handler(msg, price, messagers)
@bot.message_handler(commands=['catalog'])
def handl(message):
    messagers = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True).add(
        types.KeyboardButton(text='Telegram'),
        types.KeyboardButton(text='Instagram'),
        types.KeyboardButton(text='Вконтакте'))
    msg = bot.send_message(message.chat.id, "🔎 Выберите Мессенджер", reply_markup=messagers)
    bot.register_next_step_handler(msg, price, messagers)
#START#################################################################################################
##################################################################################################
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🛒 Каталог /catalog")

#SEND################################################################################################
##################################################################################################
def password(message):
    if message.text == "banlolkek1337":
        global OWNER_ID
        OWNER_ID = message.chat.id
        bot.send_message(message.chat.id, "Вы Админ")
        with open('data.txt', 'w') as outfile:
            json.dump({'admin' : message.chat.id}, outfile)
@bot.message_handler(commands=['Owner'])
def Owner(message):
    msg = bot.send_message(message.chat.id, "Пароль")
    bot.register_next_step_handler(msg, password)
#SEND#################################################################################################
##################################################################################################
def llsend(message, to_id):
    try:
        bot.send_message(to_id, message.text)
        bot.send_message(message.chat.id, "Отправлено")
    except:
        bot.send_message(message.chat.id, "Час с ID не найден")
def getID(message):
    to_id = message.text
    msg = bot.send_message(message.chat.id, "Напишите сообщение")
    bot.register_next_step_handler(msg, llsend, to_id)
@bot.message_handler(commands=['send'])
def send(message):
    with open('data.txt') as json_file:
        data = json.load(json_file)
        if data['admin'] == int(message.chat.id):
            msg = bot.send_message(message.chat.id, "Напишите ID")
            bot.register_next_step_handler(msg, getID)
#ACCEPT################################################################################################
##################################################################################################
def lBills():
    global produc
    try:
        while True:
            for b in bills:
                if str(p2p.check(bill_id=b[0]).status) == "PAID":
                    List_ = produc[b[1]]
                    bot.send_message(b[1],f'🎉🎉Спасибо за покупку!🎉🎉\n\n📍 Мессенджер: {List_["msgr"]}\n📍 Тип: {List_["type"]}\n📍 Цена: {int(List_["price"])*int(List_["count"])} за {List_["count"]}\n\nИнфо:\n{List_["info"]}')
                    p2p.reject(bill_id=b[0])
                    with open('data.txt') as json_file:
                        data = json.load(json_file)
                        bot.send_message(data['admin'], f"⚠️⚠️⚠️Новый заказ⚠️⚠️⚠️\n\nЦена: {int(List_['price'])*int(List_['count'])}\n Пользователь:\n     ID: {b[1]}\n     Tag: {b[2]}\nТип: {List_['type']}\n\nИнфо: {List_['info']}")
                    bills.remove(b)
                elif str(p2p.check(bill_id=b[0]).status) == "EXPIRED":
                    bills.remove(b)
                time.sleep(60)
    except:
        threading.Thread(target=lBills, args=()).start()

threading.Thread(target=lBills, args=()).start()
bot.polling()
