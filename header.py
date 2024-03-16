import logging
import sqlite3
import random
import telebot
from telebot import types
from db import Database
import os
import shutil
import datetime


bot = telebot.TeleBot('6966549610:AAGkSZkDXIQ6oevh_fOHuoEPT2QPdFKwtFQ')
db = Database('C:/Users/DonZhidoMasson/PycharmProjects/WorkinBotTInka/bot_soft/Database.db')

def numbers_in_str(string):
    for x in string:
        if [str(s) == x for s in range(10)].count(True):
            return True
    return False

def forbidden_symbols(string):
    f = "<>?.,{}[]\\|/-=_+()*&^%$#!;:~`\'\""
    for x in string:
        if [str(s) == x for s in list(f)].count(True):
            return True
    return False



# @bot.message_handler(content_types=['voice', ])


@bot.message_handler(content_types=['text'], func=lambda message: True)
def all_message(add):
    #РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЕЙ В БД
    user_existst = db.user_exists(add.chat.id)
    if not user_existst:
        bot.send_message(add.chat.id, 'Введите ваше имя.')
        db.add_user(add.chat.id)
        db.set_lc(add.chat.id, 'reg_name')
        return
    else:
        l_c = db.get_lc(add.chat.id).split('.')
        if l_c[0].split('_')[0] != 'reg':
            db.set_lc(add.chat.id, 'home')

        #ПРАВИЛО ДЛЯ КОЛИЧЕСТВО СИМВОЛОВ В ДОБОВЛЯЕМОМ СОФТЕ
    match l_c[0]:
        #######
        case 'added_chapter':
            buttons = types.InlineKeyboardMarkup(row_width=1)
            db.set_lc(add.chat.id, 'home')
            chapter = add.text
            if len(chapter) > 120:
                return
            db.add_chapters(chapter, 'CAACAgIAAxkBAAELdLJl1Iv8iMINJWam0G2CmZqGO5RsUgACVjsAApP1wUs7KGkS3u8v8TQE')
            bot.send_message(add.chat.id, 'Раздел добавлен!')
            back = types.InlineKeyboardButton(text='Назад', callback_data='mainmenu')
            buttons.add(back)
            bot.send_message(add.chat.id, 'Нажми назад, чтобы перейти на главное меню', reply_markup=buttons)

        ########

        case 'add_soft':
            buttons = types.InlineKeyboardMarkup(row_width=1)
            db.set_lc(add.chat.id, 'home')
            soft = add.text
            if len(soft) >= 4096:
                return #Слишком длинное сообщение
            db.add_soft(l_c[1], soft, add.chat.id)
            bot.send_message(add.chat.id, 'Софт сохранён!')
            back = types.InlineKeyboardButton(text='Назад', callback_data='mainmenu')
            buttons.add(back)
            bot.send_message(add.chat.id, 'Нажми назад, чтобы перейти на главное меню', reply_markup=buttons)

        #Поля РЕГИСТРАЦИИ В БОТЕ + ПРОВЕРКИ
        case 'reg_name':
            answer = add.text
            if not 2 <= len(answer) <= 32 or numbers_in_str(answer) or forbidden_symbols(answer) or answer.count("@") > 0:
                bot.send_message(add.chat.id, 'Оло, оператор, введи имя(Состоит из буковок))')
                return
            db.update_user(add.chat.id, 'name', answer)
            db.set_lc(add.chat.id, 'reg_surname')

            bot.send_message(add.chat.id, 'Введите вашу Фамилию.')
            return
        case 'reg_surname':
            answer = add.text
            if not 2 <= len(answer) <= 32 or numbers_in_str(answer) or forbidden_symbols(answer) or answer.count("@") > 0:
                bot.send_message(add.chat.id, 'Фамилию, да-да)')
                return
            db.update_user(add.chat.id, 'surname', answer)
            db.set_lc(add.chat.id, 'reg_link')
            bot.send_message(add.chat.id, 'Введите вашу ссылку на телеграм.')
            return
        case 'reg_link':
            answer = add.text
            if not 6 <= len(answer) <= 33 or answer[0] != '@':
                bot.send_message(add.chat.id, 'Ссылка начинается с @, если что, держу в курсе))))0))')
                return
            db.update_user(add.chat.id, 'link', answer)
            db.set_lc(add.chat.id, 'home')
            bot.send_message(add.chat.id, 'Вы зарегистрированы, нажмите /start')
            return

    #МЕНЮ ДОБАВЛЕНИЕ СОФТА
    command = add.text.split()
    if add.text.lower() == 'добавить' or add.text == '/add':
        if db.get_level(add.chat.id) >= 1:
            meinmenu = types.InlineKeyboardMarkup(row_width=2)
            item = types.InlineKeyboardButton(text='Выбрать раздел', callback_data='add_soft')
            item2 = types.InlineKeyboardButton(text='Назад', callback_data='mainmenu')
            added_chapter = types.InlineKeyboardButton(text='Добавить раздел', callback_data='added_chapter')
            meinmenu.add(item, added_chapter, item2)
            bot.send_sticker(add.chat.id, 'CAACAgIAAxkBAAELa4Flz_icFD7SfPxMb5KuqCqXC1BHdwACmzgAAlBrwUuy7lEoMZ4wkTQE')
            bot.send_message(add.chat.id, 'Что выбираем ммм?', reply_markup=meinmenu)
        else:
            bot.send_message(add.chat.id, 'У тебя нет прав. До свидания')
            bot.send_message(add.chat.id, 'Напиши в чат "начать" или нажми на команду /start ')

    #ГЛАВНОЕ МЕНЮ
    elif add.text.lower() == "начать" or add.text == '/start':
        mainmenu = types.InlineKeyboardMarkup(row_width=2)
        item_1 = types.InlineKeyboardButton(text='Нужен софт?⌨️', callback_data='need_soft')
        item_3 = types.InlineKeyboardButton(text='Номер дежурного☎️', callback_data='key3')
        item_4 = types.InlineKeyboardButton(text='Связь с РГ📞', callback_data='key4')
        mainmenu.add(item_1, item_3, item_4)
        bot.send_sticker(add.chat.id, 'CAACAgIAAxkBAAELa4Nlz_kpEySgZ-FKZHW6e8IOsqmmoQACukIAAsG1GElddSfcSmr-rDQE')
        bot.send_message(add.chat.id, 'Привет, нулина! Я здесь чтобы помочь тебе!', reply_markup=mainmenu)

    #Резервное сохрание бд
    elif command[0] == '/backups':
        if int(db.get_level(add.chat.id)) == 2:
            shutil.copy('C:/Users/DonZhidoMasson/PycharmProjects/WorkinBotTInka/Database.db',
                        '/backups/')
            shutil.move('C:/Users/DonZhidoMasson/PycharmProjects/WorkinBotTInka/backups/Database.db',
                             f'C:/Users/DonZhidoMasson/PycharmProjects/WorkinBotTInka/backups/Database '
                                f'{str(datetime.datetime.now()).replace(":", "-")}.db')
    # Изменение имени
    elif command[0] == '/name':
        if len(command) == 2:
            answer = command[1]
            if not 2 <= len(answer) <= 32 or numbers_in_str(answer) or forbidden_symbols(answer) or answer.count(
                    "@") > 0:
                bot.send_message(add.chat.id, 'Введите новое имя)')
                return
            db.update_user(add.chat.id, 'name', answer)
            bot.send_message(add.chat.id, f'Имя изменено на: {answer}')
    # Изменение фамилии
    elif command[0] == '/surname':
        if len(command) == 2:
            answer = command[1]
            if not 2 <= len(answer) <= 32 or numbers_in_str(answer) or forbidden_symbols(answer) or answer.count("@") > 0:
                bot.send_message(add.chat.id, 'Фамилию, да-да)')
                return
            db.update_user(add.chat.id, 'surname', answer)
            bot.send_message(add.chat.id, f'Фамилия изменена на: {answer}')

    #Замена ссылки тг
    elif command[0] == '/link':
        if len(command) == 2:
            answer = command[1]
            if not 6 <= len(answer) <= 33 or answer[0] != '@':
                bot.send_message(add.chat.id, 'Ссылка начинается с @, если что, держу в курсе))))0))')
                return
            db.update_user(add.chat.id, 'link', answer)
            bot.send_message(add.chat.id, f'Ссылка изменена на: {answer}')


#КОМАНДА КОТОРАЯ ПОКАЗЫВАЕТ ЮЗЕРУ ЕГО ID
    elif command[0] == '/id':
        bot.send_message(add.chat.id, str(add.chat.id))

    # проверка уровня доступа
    elif command[0] == '/level':
        if int(db.get_level(add.chat.id)) != 2:
            #не админ
            bot.send_message(add.chat.id, '-1 - Бан в боте\n0 - Пользователь\n1 - Модератор\n2 - Админ\n')
            return bot.send_message(add.chat.id, db.get_level(add.chat.id))


        else:
            if len(command) != 3:
                bot.send_message(add.chat.id, '-1 - Бан в боте\n0 - Пользователь\n1 - Модератор\n2 - Админ\n')
                bot.send_message(add.chat.id,  db.get_level(add.chat.id))
                bot.send_message(add.chat.id, '/level id level_up')  #НАЗНАЧЕНИЕ УРОВНЯ ДОСТУПА
                return
            db.set_level(command[1], command[2])


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # главное меню
    print(call.data)
    if call.data == "mainmenu":
        mainmenu = types.InlineKeyboardMarkup(row_width=2)
        need_soft_button = types.InlineKeyboardButton(text='Нужен софт?⌨️', callback_data='need_soft')
        call_button = types.InlineKeyboardButton(text='Номер дежурного☎️', callback_data='key3')
        connected__button = types.InlineKeyboardButton(text='Связь с РГ📞', callback_data='key4')
        mainmenu.add(need_soft_button, call_button, connected__button)
        bot.edit_message_text('Какой еще софт нужен ?', call.message.chat.id,
                              call.message.message_id, reply_markup=mainmenu)

        ###############################
    elif call.data == 'added_chapter':
        buttons = types.InlineKeyboardMarkup(row_width=1)
        if int(db.get_level(call.message.chat.id)) >= 1:
            bot.send_message(call.message.chat.id, 'Введите название раздела.', reply_markup=buttons)
            db.set_lc(call.message.chat.id, 'added_chapter')
        back = types.InlineKeyboardButton(text='Назад', callback_data='mainmenu')
        buttons.add(back)
        # bot.send_message(call.message.chat.id, 'Нажми назад, чтобы перейти на главное меню', reply_markup=buttons)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=buttons)



    #ИНФО СВЯЗИ С ДЕЖУРНЫМ
    elif call.data == 'key3':
        markup1 = types.InlineKeyboardMarkup()
        bot.send_message(call.message.chat.id, 'Держи номер дежурного 88005553535')
        back = types.InlineKeyboardButton(text='Назад в главное меню', callback_data='mainmenu')
        markup1.add(back)
        bot.send_message(call.message.chat.id, "Чтобы выйти обрато нажми 'Назад в меню' ", reply_markup=markup1)

    #КНОПКА СВЯЗИ С РГ
    elif call.data == 'key4':
        next_menu3 = types.InlineKeyboardMarkup()
        bot.send_message(call.message.chat.id,
                         'можешь позвонить РГ по этому номеру +98888888888, или найти его по этому номеру в ТГ')
        back = types.InlineKeyboardButton(text='Назад', callback_data='mainmenu')
        next_menu3.add(back)
        bot.send_message(call.message.chat.id, 'Нажми назад, чтобы перейти на главное меню', reply_markup=next_menu3)

    #МЕНЮ РАЗДЕЛОВ СОФТА
    if call.data == 'need_soft':
        buttons = types.InlineKeyboardMarkup(row_width=1)
        chapters = db.get_chapters()
        for c in chapters:
            buttons.add(types.InlineKeyboardButton(text=c[1], callback_data=f'soft_{c[0]}'))
            print(c[1], f'soft_{c[0]}')
        back = types.InlineKeyboardButton(text='Назад', callback_data='mainmenu')
        buttons.add(back)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=buttons)


    # РАЗДЕЛЫ СОФТА
    elif call.data == 'add_soft':
        buttons = types.InlineKeyboardMarkup(row_width=1)
        chapters = db.get_chapters()
        for c in chapters:
            buttons.add(types.InlineKeyboardButton(text=c[1], callback_data=f'add_{c[0]}'))
        back = types.InlineKeyboardButton(text='Назад', callback_data='mainmenu')
        buttons.add(back)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=buttons)

    #ПРОСМОТР СОФТА ПО РАЗДЕЛАМ/ДОБАВЛЕНИЕ НОВОГО СОФТА В РАЗДЕЛ
    else:
        buttons = types.InlineKeyboardMarkup(row_width=1)
        action = call.data.split('_')
        print(action)
        if action[0] == 'soft':
            softs = db.get_soft(action[1])
            back = types.InlineKeyboardButton(text='Назад', callback_data='mainmenu')
            bot.send_sticker(call.message.chat.id, db.get_chapter_sticker(action[1]))
            buttons.add(back)
            for i in range(len(softs)):
                if i == len(softs) - 1:
                    bot.send_message(call.message.chat.id, text=softs[i][0], reply_markup=buttons)
                else:
                    bot.send_message(call.message.chat.id, text=softs[i][0])
        elif action[0] == 'add':
            if int(db.get_level(call.message.chat.id)) >= 1:
                bot.send_message(call.message.chat.id, 'Введите новый софт!')
                db.set_lc(call.message.chat.id, f'add_soft.{action[1]}')
            back = types.InlineKeyboardButton(text='Назад', callback_data='mainmenu')
            buttons.add(back)
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=buttons)


bot.polling(none_stop=True)