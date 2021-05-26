import time

import telebot
from steganography_in_text import Decrypter, Crypter

from settings import API_TOKEN
from additional_functions import *
from db_function import *

bot = telebot.TeleBot(API_TOKEN, parse_mode=None)
crypter = Crypter()
decrypter = Decrypter()

global_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
global_markup.row('Зашифровать', 'Расшифровать')
global_markup.row('Настройка паролей и их работы')


@bot.message_handler(commands=['start'])
def start_message(message):
    cid = message.chat.id
    try:
        create_user(message.from_user.id)
    except:
        pass
    bot.send_message(cid, 'Очень приятно видеть вас в рядах защищённых людей', reply_markup=global_markup)
    bot.send_message(cid, 'В ролике ниже вы можете увидеть работу telegram бота', reply_markup=global_markup)
    bot.send_message(cid, 'https://youtu.be/p7lEjWOUTUc', reply_markup=global_markup)


@bot.callback_query_handler(func=lambda call: True)
# setting: - 1 выбор настройки кнопок
# auto: - 2 выбор настройки кнопок
def log(call):
    id = call.from_user.id
    print(call.data)
    passwords = return_passwords(id, 0)
    auto_passwords = return_passwords(id, 1)
    if check_type(call.data, 'setting:'):
        if 'save' in call.data[len('setting:'):]:
            msg = bot.send_message(id, "Введите новый пароль")
            bot.register_next_step_handler(msg, add_password)
        elif 'setting' in call.data[len('setting:'):]:
            arr = [['изменить состояние авто расшифровки', 'flag'],
                   ['выбрать пароли, для авто расшифровки', 'passwords']]
            keyboard = create_keyboard(arr, 'auto:')
            bot.send_message(chat_id=id, text="Что именно вы хотите сделать?", reply_markup=keyboard)
        else:
            arr = deploy_arr(return_passwords(id, 0), 2)
            keyboard = create_keyboard(arr, 'del_key:')
            bot.send_message(chat_id=id, text="Какой пароль вы хотите удалить?", reply_markup=keyboard)
    elif check_type(call.data, 'auto:'):
        txt = call.data[5:]
        if txt == 'flag':
            sms = 'Вы включили авто расшифровку'
            if not change_aut_decryption(id):
                sms = 'Вы отключили авто расшифровку'
            bot.send_message(chat_id=id, text=sms)
        else:
            arr = [['добавить пароль', 'add'], ['удалить пароль', 'del']]
            # if len(auto_passwords) == 1:
            #     del arr[1]
            # if len(passwords) == len(auto_passwords):
            #     del arr[0]
            sms = 'Настройте пароли'
            if not arr:
                sms = 'сейчас вы не можите это сделать'
            keyboard = create_keyboard(arr, 'auto_password:')
            bot.send_message(chat_id=id, text=sms, reply_markup=keyboard)
    elif check_type(call.data, 'auto_password:'):
        txt = call.data[len('auto_password:'):]
        if txt == 'add':
            arr = deploy_arr(passwords, 2, auto_passwords)
            keyboard = create_keyboard(arr, 'auto_add:')
            bot.send_message(chat_id=id, text='Какой пароль вы хотите добавить', reply_markup=keyboard)
        elif txt == 'del':
            arr = deploy_arr(auto_passwords, 2)
            keyboard = create_keyboard(arr, 'auto_del:')
            bot.send_message(chat_id=id, text='Какой пароль вы хотите удалить', reply_markup=keyboard)
    elif check_type(call.data, 'auto_add:'):
        num = int(call.data[len('auto_add:'):])

        change_password_flag(id, passwords[num])
        arr = [['добавить пароль', 'add'], ['удалить пароль', 'del']]
        # if len(auto_passwords) == 1:
        #     del arr[1]
        # if len(passwords) == len(auto_passwords):
        #     del arr[0]
        keyboard = create_keyboard(arr, 'auto_password:')
        bot.send_message(chat_id=id, text='Вы успешно добавили пароль', reply_markup=keyboard)
    elif check_type(call.data, 'auto_del:'):
        num = int(call.data[len('auto_del:'):])
        change_password_flag(id, passwords[num])
        arr = [['добавить пароль', 'add'], ['удалить пароль', 'del']]
        # if len(auto_passwords) == 1:
        #     del arr[1]
        # if len(passwords) == len(auto_passwords):
        #     del arr[0]
        keyboard = create_keyboard(arr, 'auto_password:')
        bot.send_message(chat_id=id, text='Вы успешно удалили пароль', reply_markup=keyboard)

    elif check_type(call.data, 'del_key:'):
        menu = [['Сохранить новый пароль', 'save'], ['Удалить какой-то из паролей', 'delete']]
        keyboard = create_keyboard(menu, 'setting:')
        if len(passwords) == 1:
            bot.send_message(chat_id=id, text="Нельзя удалить пароль, если он последний в списке",
                             reply_markup=keyboard)
        else:
            num = int(call.data[len('del_key:'):])
            print(passwords[num])
            delete_password(id, passwords[num])
            bot.send_message(chat_id=id, text="вы успешно удалили этот пароль", reply_markup=keyboard)
    elif check_type(call.data, 'choice_key_0:'):
        sms = return_sms(id)
        password = passwords[int(call.data[len('choice_key_0:'):])]
        message = crypter.create_message(sms[0], password, sms[1])
        bot.send_message(id, message)
    elif check_type(call.data, 'choice_key_1:'):
        sms = return_sms(id)
        password = passwords[int(call.data[len('choice_key_1:'):])]
        try:
            message = decrypter.create_message(sms[2], password)
            bot.send_message(id, message)
        except ValueError:
            bot.send_message(id, 'не удалось расшифровать сообщение')


@bot.message_handler(func=lambda call: True)
def start(message):
    id = message.chat.id
    user_id = message.from_user.id
    if message.text == 'Зашифровать':
        msg = bot.send_message(id, "ваше сообщение в котором мы будем все хранить")
        bot.register_next_step_handler(msg, crypt_1)
    elif message.text == 'Настройка паролей и их работы':
        menu = [['Сохранить новый пароль', 'save'], ['Удалить какой-то из паролей', 'delete'],
                ['Настроить авто расшифровку', 'setting']]
        keyboard = create_keyboard(menu, 'setting:')
        bot.send_message(chat_id=id, text="Что вы хотите сделать?", reply_markup=keyboard)
    elif message.text == 'Расшифровать':
        msg = bot.send_message(id, "введите сообщение с шифровкой")
        bot.register_next_step_handler(msg, decrypt)
    else:
        if return_sms(id)[3]:
            n = 0
            for i in return_passwords(id, 1):
                sms = 'пароль ' + i + '\n'
                try:
                    message = decrypter.create_message(message.text, i)
                    bot.send_message(id, sms + message)
                    n += 1
                except ValueError:
                    pass
            if not n:
                bot.send_message(id, 'не удалось расшифровать сообщение')
        else:
            try:
                change_sms_2(id, message.text)
                arr = deploy_arr(return_passwords(id, 0), 2)
                keyboard = create_keyboard(arr, 'choice_key_1:')
                bot.send_message(chat_id=id, text="Какой пароль вы будите использовать для расшифровки",
                                 reply_markup=keyboard)
            except ValueError:
                bot.send_message(id, 'не удалось расшифровать сообщение')


def add_password(message):
    sms = "Этот пароль уже существует"
    if add_new_password(message.from_user.id, message.text):
        sms = "Вы удачно сохранили новый пароль"
    menu = [['Сохранить новый пароль', 'save'], ['Удалить какой-то из паролей', 'delete']]
    keyboard = create_keyboard(menu, 'setting:')
    bot.send_message(message.chat.id, sms, reply_markup=keyboard)


def setting_password(message):
    pass


def crypt_1(message):
    id = message.from_user.id
    change_sms_1(id, message.text)
    msg = bot.send_message(message.chat.id, "ваше секретное сообщение")
    bot.register_next_step_handler(msg, crypt_2)


def crypt_2(message):
    id = message.from_user.id
    change_secret(id, message.text)
    arr = deploy_arr(return_passwords(id, 0), 2)
    keyboard = create_keyboard(arr, 'choice_key_0:')
    bot.send_message(chat_id=id, text="Какой пароль вы будите использовать для шифровки", reply_markup=keyboard)


def decrypt(message):
    id = message.from_user.id
    change_sms_2(id, message.text)
    arr = deploy_arr(return_passwords(id, 0), 2)
    keyboard = create_keyboard(arr, 'choice_key_1:')
    bot.send_message(chat_id=id, text="Какой пароль вы будите использовать для расшифровки", reply_markup=keyboard)


def change_password(message):
    if add_new_password(message.from_user.id, message.text):
        bot.send_message(message.chat.id, 'пароль сохранён')
    else:
        bot.send_message(message.chat.id, 'вы уже сохранили этот пароль')



def running():
    try:
        bot.polling()
    except:
        time.sleep(5)
        running()

running()