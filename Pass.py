import telebot
import gspread
import sqlite3
import os
from dotenv import load_dotenv, find_dotenv
from datetime import date


bot = telebot.TeleBot("TOKEN")
gc = gspread.service_account("credsdmk.json")
googlesheet_id = '1wo8rZBOcRGqHIvCYfp9wEEVK_fTbPKPZfZUlJidL5dI'



data_entry = {
    'num': '',
    'dept': '',
    'entry': '',
    'message': ''
}

today = date.today().strftime("%d.%m.%Y")


@bot.message_handler(commands=['start'])
def userexists(message):
    db = sqlite3.connect("dmkusers")
    cursor = db.cursor()
    user_id = message.from_user.id
    user = cursor.execute(f"SELECT * FROM users where user_id = {user_id}")

    if user.fetchone():
        global name
        msg = bot.send_message(message.chat.id, f'<b> Здравствуйте {message.from_user.first_name}'
                                                f' {message.from_user.last_name} </b> \nДля получения'
                                                f' пропуска введите гос.номер вашего авто', parse_mode='html')
        bot.register_next_step_handler(msg, dep)
        name = f'{message.from_user.first_name} {message.from_user.last_name}'
    else:
        bot.send_message(message.chat.id, f'<b>Вы не авторизованы!</b>\n Для получения доступа сообщите ID контакту https://t.me/aryadovoyy <b>Ваш ID:{message.from_user.id}</b>',
                         parse_mode='html')


def dep(message):
    data_entry['num'] = message.text
    msg = bot.send_message(message.chat.id, 'Введите названия отделения')
    bot.register_next_step_handler(msg, dt_ent)
    global dp
    dp = message.text


def dt_ent(message):
    data_entry['dept'] = message.text
    msg = bot.send_message(message.chat.id, 'Введите дату въезда')
    bot.register_next_step_handler(msg, getresults)
    global dt
    dt = message.text


def getresults(message):
    data_entry['message'] = message.text
    bot.send_message(message.chat.id,
                     f"<b>Ваш пропуск готов ✅ \nГос.номер авто: {data_entry['num']}"
                     f" \nОтделение: {data_entry['dept']} \nДата въезда: {data_entry['message']}</b>\n",
                     parse_mode='html')
    rr = message.text

    sh = gc.open_by_key(googlesheet_id)
    sh.sheet1.append_row([dp, dt, rr, today, name])


bot.polling(non_stop=True)
