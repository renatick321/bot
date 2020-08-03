import config
import smshub
import activate
import db
import telebot
import json
import requests
from time import sleep
from telebot import types
import qiwi

lib = globals()["smshub"]
bot = telebot.TeleBot(config.TOKEN)
global services
services = lib.smshub
global weblst
weblst = ['sms-hub', "sms-activate"]
country = ["Россия", "Украина", "Казахстан"]
ADMIN = 1198883635


@bot.message_handler(commands=['start'])  # Начало начал
def start_command(message):
    db.user_create(message.chat.id)
    bot.send_message(  
        message.chat.id,  
        'Здравствуй, Повелитель 👑,\n' +  
        'Я бот, созданный для экономии вашего времени🕞 ',
        reply_markup=menu() 
                    )

@bot.message_handler(commands=['cupon'])
def cupon(message):
    if message.chat.id == ADMIN:
        l = list(map(str, message.text.split()))
        if len(l) != 2:
            bot.send_message(message.chat.id, "Пожалуйста, отправьте команду по формату /cupon цена")
        else:
            bot.send_message(message.chat.id, "Купон генерируеться...")
            cupon = db.get_cupon(l[1])
            bot.send_message(message.chat.id, cupon)

@bot.message_handler(commands=['info'])
def info(message):
    if message.chat.id == ADMIN:
        bot.send_message(message.chat.id, db.info(), reply_markup=menu())

@bot.message_handler(commands=['send'])
def send(message):
    if message.chat.id == ADMIN:
        s = message.text[5:]
        users = db.get_users()
        print(users)
        came = 0
        notcame = 0
        for user in users:
            try:
                bot.send_message(user, s, reply_markup=tomenu())
                came += 1
                print(1)
            except:
                notcame += 1
            sleep(0.15)
        bot.send_message(message.chat.id, "Данная рассылка дошла до {came} пользователей\nНедошла до {notcame}пользователей".format(came, notcame))
        print(came, notcame)

@bot.message_handler(commands=['admin'])
def admin(message):
    if message.chat.id == ADMIN:
        bot.send_message(message.chat.id, "Команды\n/cupon цена - генерация купона\n/info - подробная информация о боте\n/send text - рассылка")

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    s = message.text
    if s == "🔥 Номера":
        bot.send_message(message.chat.id, "Пожалуйста, выберете для каких целей вы хотите арендовать номер", reply_markup=num())
    elif s == "🆘 Правила":
        bot.send_message(message.chat.id, "1. Главное:\n1.1 Мы продаем номера, без инструкций к их использованию. Вся ответственность после покупки номеров только на вас.\n1.2 Если комментарий при оплате был указан неверно, администрация имеет полное право не делать замену\n1.3 Администрация оставляет за собой право вносить любые изменения и дополнения в Правила, без предупреждения!\n1.4 Администрация вправе обнулить ваш лицевой счет.\n\nФОРМА ОБРАЩЕНИЯ\n1) Переписка с ботом + скрины переписки + скрин оплаты\n2) Предоставляйте видеозапись проверки номера с момента покупки в магазине и проверки на офф.сайте сервиса, который купили. Видео должно быть одно и цельное. ( ОБЯЗАТЕЛЬНО ) Отклонения от формы будут игнорироваться!!!", reply_markup=menu())
    elif s == "💰 Баланс":
        b = db.get_balance(message.chat.id)
        s = int(b) if int(b) == float(b) else float(b)
        bot.send_message(message.chat.id,  "Ваш баланс: " + str(s) + 'р.', reply_markup=balance())
        bot.register_next_step_handler(message, money)
    elif s == '💩 Помощь':
        bot.send_message(message.chat.id, 'Обратитесь к @freddy_support ', reply_markup=menu())
    elif s == "↪ В главное меню ↩":
        bot.send_message(message.chat.id, "Вы в главном меню", reply_markup=menu())
    elif s == "💼 Мой профиль":
        lst = db.get_info(message.chat.id)
        bot.send_message(message.chat.id, 'id: {}\nКоличество заказов: {}шт. \nСумма всех ваших покупок: {}р.'.format(message.chat.id, len(lst), sum(lst)))
    else:
        bot.send_message(message.chat.id, 'Воспользуйтесь клавиатурой', reply_markup=menu())


def money(message):
    s = message.text
    if s == '🎁 Купон 🎁':
        bot.send_message(message.chat.id, "Введите купон")
        bot.register_next_step_handler(message, cupon_activate)
    elif s == "💣 Пополнить 💣":
        bot.send_message(message.chat.id, "Выберете метод оплаты", reply_markup=method_payment())
        bot.register_next_step_handler(message, payment)
    elif s == "↪ В главное меню ↩":
        bot.send_message(message.chat.id, "Вы в главном меню", reply_markup=menu())
    else:
        bot.send_message(message.chat.id, 'Ошибка!', reply_markup=tomenu())

def cupon_activate(message):
    bot.send_message(message.chat.id, db.cupon_activate(message.chat.id,  message.text), reply_markup=menu())


def payment(message):
    if message.text == "🥝 Киви":
        print(1)
        comment = db.get_comment()
        print(2)
        bot.send_message(message.chat.id, "➖➖➖➖➖➖➖➖➖➖\nИнформация об оплате\n🥝 QIWI-кошелек: +{}\n📝 Комментарий к переводу: ```{}``` \n➖➖➖➖➖➖➖➖➖➖\n\nВнимание\nПереводите ту сумму, на которую хотите пополнить баланс!\nЗаполняйте номер телефона и комментарий при переводе внимательно!\nАдминистрация не несет ответственности за ошибочный перевод, возврата в данном случае не будет!\nПосле перевода нажмите кнопку 'Проверить оплату'!\n➖➖➖➖➖➖➖➖➖➖".format(qiwi.NUMBER, comment), parse_mode="Markdown", reply_markup=tomenu())
        bot.send_message(message.chat.id, "Нажмите для проверки оплаты", reply_markup=cash_check(comment))
    elif message.text == '↪ В главное меню ↩':
        bot.send_message(message.chat.id, "Вы в главном меню", reply_markup=menu())
    else:
        bot.send_message(message.chat.id, "Воспользуйтесь клавиатурой", reply_markup=menu())



@bot.callback_query_handler(func=lambda call: call.data.isdigit())
def check_button(call):
    comments = qiwi.get_comments()
    if call.data in list(comments.keys()):
        cash = comments[call.data]
        db.replenishment(call.message.chat.id, cash)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Оплата подтверждена")
        bot.send_message(ADMIN, "Пополнение на сумму {} руб.\nID: {}".format(cash, call.message.chat.id))
    else:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Оплата не пришла, попытайтесь снова", reply_markup=cash_check(call.data))



@bot.callback_query_handler(func=lambda call: call.data == "Закончить")
def end_number(call):
    number.edit_status(6)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, "Аренда номера была закончена", reply_markup=menu())

@bot.callback_query_handler(func=lambda call: call.data == "Ещё смс")
def end_number(call):
    number.edit_status(3)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, "Ожидайте прихода ещё одного смс", reply_markup=number_end())
    s = number.get_sms()
    print(s)
    if s == 'Аренда номера была отменена':
        cash = db.get_last_payment(call.message.chat.id)
        number.edit_status(6)
        bot.delete_message(call.message.chat.id, call.message.message_id + 1)
    else:
        bot.delete_message(call.message.chat.id, call.message.message_id + 1)
        bot.send_message(call.message.chat.id, "Ваш код: ```" + str(s) + '```\nПожалуйста, выберете одно из предложенных действий', reply_markup=number_sms(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "Отменить")
def cancel(call):
    number.edit_status(8)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, 'Вы в главном меню', reply_markup=menu())



@bot.callback_query_handler(func=lambda call: call.data == "В главное меню")
def gotomenu(call):
    bot.send_message(call.message.chat.id, 'Вы в главном меню', reply_markup=menu())


@bot.callback_query_handler(func=lambda call: call.data in services.keys())
def service_btn(call):
    bot.send_message(call.message.chat.id, 'Пожалуйста, выберете предпочитаемую подкатегорию', reply_markup=web())
    global choice
    print(call.data)
    choice = call.data


@bot.callback_query_handler(func=lambda call: call.data in weblst)
def get_sms(call):
    global lib
    if call.data == 'sms-activate':
        lib = globals()["activate"]
    elif call.data == 'sms-hub':
        lib = globals()["smshub"]
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, 'Выберете страну', reply_markup=country_btns())


@bot.callback_query_handler(func=lambda call: call.data in country)
def get_number(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    global number
    number = lib.Number(services[choice], call.data)
    price = lib.get_price(services[choice], call.data)
    if price == "Нет в наличии":
        bot.send_message(call.message.chat.id, "Просим прощения, но в наличие нету номеров с заданными параметрами, попробуйте позже, или поменяйте страну, подкатегорию")
    elif str(number) and float(price[::-1][2:][::-1]) <= db.get_balance(call.message.chat.id):
        s = 'Сервис: {}\nНомер:  {}\nОжидайте прихода смс\n\nЕсли в течении 4 минут смс не прийдёт, аренда будет отменена, после деньги, потраченные на аренду данного номера, будут зачислены к вам на счёт'.format(choice, str(number))
        bot.send_message(call.message.chat.id, s, reply_markup=end_sms())
        s = number.get_sms()
        print(s)
        if s == 'Аренда номера была отменена':
            cash = db.get_last_payment(call.message.chat.id)
            number.edit_status(8)
            bot.delete_message(call.message.chat.id, call.message.message_id + 1)
        else:
            bot.delete_message(call.message.chat.id, call.message.message_id + 1)
            db.buy(choice, str(number), call.message.chat.id, float(price[::-1][2:][::-1]))
            bot.send_message(call.message.chat.id, "Ваш код: ```" + str(s) + '```\nПожалуйста, выберете одно из предложенных действий', reply_markup=number_sms(), parse_mode="Markdown")

    else:
        try:
            number.edit_status(8)
        except:
            pass
        bot.send_message(call.message.chat.id, "На балансе недостаточно средств", reply_markup=menu())

def cash_check(comment):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(types.InlineKeyboardButton("Проверить оплату", callback_data=comment))
    return keyboard


def number_end():
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(types.InlineKeyboardButton("⛔ Закончить", callback_data='Закончить'))
    return keyboard

def number_sms():
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(types.InlineKeyboardButton("✉ Ещё смс", callback_data='Ещё смс'))
    keyboard.row(types.InlineKeyboardButton("⛔ Закончить", callback_data='Закончить'))
    return keyboard

def end_sms():
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(types.InlineKeyboardButton("❌ Отменить", callback_data='Отменить'))
    return keyboard


def country_btns():
    keyboard = telebot.types.InlineKeyboardMarkup()
    ru = lib.get_price(services[choice], "Россия")
    ua = lib.get_price(services[choice], "Украина")
    kz = lib.get_price(services[choice], "Казахстан")
    keyboard.row(types.InlineKeyboardButton("🇷🇺 Россия | {}".format(ru), callback_data='Россия'))
    keyboard.row(types.InlineKeyboardButton("🇺🇦 Украина | {}".format(ua), callback_data='Украина'))
    keyboard.row(types.InlineKeyboardButton("🇰🇿 Казахстан | {}".format(kz), callback_data='Казахстан'))
    return keyboard

def web():
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(types.InlineKeyboardButton("🔥 Дешёвые 🔥", callback_data='sms-hub'))
    keyboard.row(types.InlineKeyboardButton("✅ Проверенные ✅", callback_data='sms-activate'))
    #keyboard.row(types.InlineKeyboardButton("sms-online", callback_data='sms-online'))
    return keyboard

def num():
    keyboard = telebot.types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Telegram', callback_data='Telegram')
    btn2 = types.InlineKeyboardButton('Whatsapp', callback_data='Whatsapp')
    keyboard.add(btn1, btn2)
    btn1 = types.InlineKeyboardButton('Вконтакте', callback_data='Вконтакте')
    btn2 = types.InlineKeyboardButton('Avito', callback_data='Avito')
    keyboard.add(btn1, btn2)
    btn1 = types.InlineKeyboardButton('Qiwi', callback_data='Qiwi')
    btn2 = types.InlineKeyboardButton('Пятерочка', callback_data='Пятерочка')
    keyboard.add(btn1, btn2)
    btn1 = types.InlineKeyboardButton('McDonalds', callback_data='McDonalds')
    btn2 = types.InlineKeyboardButton('PayPal', callback_data='PayPal')
    keyboard.add(btn1, btn2)
    btn1 = types.InlineKeyboardButton('Burger King', callback_data='Burger King')
    btn2 = types.InlineKeyboardButton('Яндекс', callback_data='Яндекс')
    keyboard.add(btn1, btn2)
    btn1 = types.InlineKeyboardButton('BlaBlaCar', callback_data='BlaBlaCar')
    btn2 = types.InlineKeyboardButton('Instagram', callback_data='Instagram')
    keyboard.add(btn1, btn2)
    btn1 = types.InlineKeyboardButton('Google', callback_data='Google')
    btn2 = types.InlineKeyboardButton('Steam', callback_data='Steam')
    keyboard.add(btn1, btn2)
    keyboard.add(types.InlineKeyboardButton('↪ В главное меню ↩', callback_data='В главное меню'))
    return keyboard

def tomenu():
    keyboard = types.ReplyKeyboardMarkup(True, True)
    keyboard.row("↪ В главное меню ↩")
    return keyboard

def balance():
    keyboard = types.ReplyKeyboardMarkup(True, True)
    keyboard.row("🎁 Купон 🎁", "💣 Пополнить 💣")
    keyboard.row("↪ В главное меню ↩")
    return keyboard

def menu():
    keyboard = types.ReplyKeyboardMarkup(True, True)
    keyboard.row("🔥 Номера", "🆘 Правила", "💰 Баланс")
    keyboard.row('💩 Помощь', "💼 Мой профиль")
    return keyboard

def method_payment():
    keyboard = types.ReplyKeyboardMarkup(True, True)
    keyboard.row("🥝 Киви")
    keyboard.row("↪ В главное меню ↩")
    return keyboard


bot.polling(none_stop=True)