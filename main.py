# -*- coding: utf-8 -*-
# Python 3.8.6
import time
from pprint import pprint

from telebot import types, AsyncTeleBot
from settings import TOKEN
from models import create_user_in_db, change_photo, change_name, change_company, change_interests, change_usefulness, \
    subscribe, unsubscribe, subscribed, get_user_info, check_fields_filled, create_pairs, get_telegram_id, \
    create_meeting, get_name_by_meeting, update_meeting_status, update_meeting_opinion
import schedule
import re

bot = AsyncTeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def buttons_inline(message):
    """
    Функция инициирует бота и добавляет кнопки с выбором поля для заполнения информации.
    """
    if not check_fields_filled(telegram_id=message.from_user.id):
        markup = types.InlineKeyboardMarkup(row_width=1)
        get_photo = types.InlineKeyboardButton(text='Фото', callback_data='add_photo')
        get_name = types.InlineKeyboardButton(text='Имя и Фамилия', callback_data='add_name')
        get_company = types.InlineKeyboardButton(text='Компания и позиция', callback_data='add_company')
        get_interests = types.InlineKeyboardButton(text='Что я ищу', callback_data='add_interests')
        get_usefulness = types.InlineKeyboardButton(text='Чем могу быть полезен', callback_data='add_usefulness')
        markup.add(get_photo, get_name, get_company, get_interests, get_usefulness)
        start_message = 'Остались незаполненные поля'
        if message.text == '/start':
            start_message = 'Привет!\nДобавьте информацию о себе.\nМы рассылаем информацию каждую пятницу.'
            create_user_in_db(telegram_id=message.from_user.id)
        bot.send_message(message.chat.id, start_message, reply_markup=markup)

    else:
        markup = types.InlineKeyboardMarkup()
        participate_net = types.InlineKeyboardButton(text='Учавствовать в нетворкинге',
                                                     callback_data='participate_netw')
        markup.add(participate_net)
        bot.send_message(chat_id=message.chat.id, text='Учавствовать в нетворкинге', reply_markup=markup)


@bot.message_handler(commands=['edit'])
def edit_profile(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    get_photo = types.InlineKeyboardButton(text='Фото', callback_data='add_photo')
    get_name = types.InlineKeyboardButton(text='Имя и Фамилия', callback_data='add_name')
    get_company = types.InlineKeyboardButton(text='Компания и позиция', callback_data='add_company')
    get_interests = types.InlineKeyboardButton(text='Что я ищу', callback_data='add_interests')
    get_usefulness = types.InlineKeyboardButton(text='Чем могу быть полезен', callback_data='add_usefulness')
    markup.add(get_photo, get_name, get_company, get_interests, get_usefulness)
    start_message = 'Выберите поле для редактирования'
    bot.send_message(message.chat.id, start_message, reply_markup=markup)


@bot.message_handler(commands=['user_info'])
def user_info(message):
    model = get_user_info(telegram_id=message.from_user.id)
    print(model)
    bot.send_photo(chat_id=message.chat.id, photo=model.photo)
    bot.send_message(chat_id=message.chat.id, text='Информация о профиле:\n'
                                                   f'{model.name}, {model.company}\n'
                                                   f'Могу быть полезен: {model.usefulness}\n'
                                                   f'Я ищу: {model.interests}')


@bot.callback_query_handler(func=lambda call: call.data in ['add_photo', 'add_name', 'add_company',
                                                            'add_interests', 'add_usefulness'])
def handle(call):
    """
    Функция обрабатывает события в связи с нажатием на кнопку
    """
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    if call.data == 'add_photo':
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        profile_photos = bot.get_user_profile_photos(user_id=call.from_user.id, limit=1).wait().photos
        if profile_photos:
            markup = types.InlineKeyboardMarkup(row_width=2)
            take_from_profile = types.InlineKeyboardButton(text='Из профиля', callback_data='photo_from_profile')
            load_by_myself = types.InlineKeyboardButton(text='Загрузить фото', callback_data='load_photo')
            markup.add(take_from_profile, load_by_myself)
            text = 'В вашем профиле уже есть фото. Нажмите "Из профиля" и я возьму его.'
            bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)
        else:
            text = 'Загрузите свое фото, чтобы люди знали, как вы выглядите. ' \
                   'Можно прислать уже сделанное фото, но я рекомендую сделать селфи прямо сейчас. ' \
                   'Так вас легче будет узнать. ' \
                   'Отправьте свое фото прямо сюда.'
            msg = bot.send_message(call.message.chat.id, text).wait()
            bot.register_next_step_handler(msg, get_photo_from_user)
    elif call.data == 'add_name':
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        markup = types.InlineKeyboardMarkup(row_width=2)
        take_from_profile = types.InlineKeyboardButton(text='Оставить имя', callback_data='name_from_profile')
        load_by_myself = types.InlineKeyboardButton(text='Изменить', callback_data='edit_name')
        markup.add(take_from_profile, load_by_myself)
        print(call.from_user)
        text = 'Как вас представлять другим участникам? ' \
               f'В вашем профиле указано, что ваше имя - {call.from_user.first_name + call.from_user.last_name} ' \
               'Я могу использовать его. Или пришлите мне свое имя текстом. '
        msg = bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup).wait()
        bot.register_next_step_handler(msg, get_name_from_user)
    elif call.data == 'add_company':
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)

        text = 'Где и кем вы работаете? Это поможет людям понять, чем вы можете быть интересны. ' \
               'Пришлите мне, пожалуйста, название компании и вашу должность. ' \
               'Например, "Директор в "ООО Палехче".'
        msg = bot.send_message(call.message.chat.id, text).wait()
        bot.register_next_step_handler(msg, get_company_from_user)
    elif call.data == 'add_interests':
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)

        text = 'О каких темах вам было бы интересно поговорить? ' \
               'Например, "инвестиции, советы по воспитанию детей, ' \
               'возможна ли медицина в условиях невесомости".'
        msg = bot.send_message(call.message.chat.id, text).wait()
        bot.register_next_step_handler(msg, get_interests_from_user)
    elif call.data == 'add_usefulness':
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)

        text = 'В каких темах вы разбираетесь? Например, "умею пасти котов, инвестирую, развожу сурков".'
        msg = bot.send_message(call.message.chat.id, text).wait()
        bot.register_next_step_handler(msg, get_usefulness_from_user)
    bot.register_next_step_handler(message=call.message, callback=buttons_inline)


@bot.callback_query_handler(func=lambda call: call.data == 'photo_from_profile')
def from_profile(call):
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    profile_photos = bot.get_user_profile_photos(user_id=call.from_user.id).wait().photos
    avatar = bot.get_file(profile_photos[0][0].file_id).wait()
    downloaded = bot.download_file(avatar.file_path).wait()
    change_photo(telegram_id=call.from_user.id, photo=downloaded)
    bot.register_next_step_handler(message=call.message, callback=buttons_inline)


@bot.callback_query_handler(func=lambda call: call.data == 'load_photo')
def load_photo(call):
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    text = 'Загрузите свое фото, чтобы люди знали, как вы выглядите. ' \
           'Можно прислать уже сделанное фото, но я рекомендую сделать селфи прямо сейчас. ' \
           'Так вас легче будет узнать. ' \
           'Отправьте свое фото прямо сюда.'
    msg = bot.send_message(call.message.chat.id, text).wait()
    bot.register_next_step_handler(msg, get_photo_from_user)
    bot.register_next_step_handler(message=call.message, callback=buttons_inline)


@bot.callback_query_handler(func=lambda call: call.data == 'name_from_profile')
def name_from_profile(call):
    change_name(telegram_id=call.from_user.id, name=call.from_user.username)
    bot.register_next_step_handler(message=call.message, callback=buttons_inline)


@bot.callback_query_handler(func=lambda call: call.data == 'edit_name')
def edit_name(call):
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    text = 'Введите свое имя.'
    msg = bot.send_message(call.message.chat.id, text).wait()
    bot.register_next_step_handler(msg, get_name_from_user)
    bot.register_next_step_handler(message=call.message, callback=buttons_inline)


def get_photo_from_user(message):
    if message.content_type == 'photo':
        user_photo = bot.get_file(message.photo[0].file_id).wait()
        downloaded = bot.download_file(user_photo.file_path).wait()
        change_photo(telegram_id=message.from_user.id, photo=downloaded)
    else:
        bot.send_message(message.chat.id, 'Это не фото')


def get_name_from_user(message):
    print('user_name')
    if message.content_type == 'text':
        user_name = message.text

        change_name(telegram_id=message.from_user.id, name=user_name)
    else:
        bot.send_message(message.chat.id, 'Пришлите текст')


def get_company_from_user(message):
    if message.content_type == 'text':
        user_company = message.text
        change_company(telegram_id=message.from_user.id, company=user_company)
    else:
        bot.send_message(message.chat.id, 'Пришлите текст')


def get_interests_from_user(message):
    if message.content_type == 'text':
        user_interests = message.text
        change_interests(telegram_id=message.from_user.id, interests=user_interests)
    else:
        bot.send_message(message.chat.id, 'Пришлите текст')


def get_usefulness_from_user(message):
    if message.content_type == 'text':
        user_usefulness = message.text
        change_usefulness(telegram_id=message.from_user.id, usefulness=user_usefulness)
    else:
        bot.send_message(message.chat.id, 'Пришлите текст')


@bot.callback_query_handler(func=lambda call: call.data == 'participate_netw')
def clicked(call):
    bot.send_message(chat_id=call.from_user.id, text='Вы учавствуете')

    schedule.every().minute.at(':00').do(send_markup_yes_no, call)
    time.sleep(2)
    schedule.every().minute.at(':15').do(send)
    time.sleep(2)
    schedule.every().minute.at(':30').do(send_remind, call)
    time.sleep(2)
    schedule.every().minute.at(':45').do(after_meeting, call)

    while True:
        schedule.run_pending()
        time.sleep(1)


def send_markup_yes_no(call):
    bot.send_message(chat_id=call.from_user.id, text='Привет!\nНаступил день подбора новых собеседников.')
    markup = types.InlineKeyboardMarkup(row_width=2)
    yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    markup.add(yes, no)
    time.sleep(0.5)
    bot.send_message(chat_id=call.from_user.id, text='Вас включать в список подбора на завтра?', reply_markup=markup)
    time.sleep(0.5)
    bot.send_message(chat_id=call.from_user.id, text='Берегите себя и близких и поддерживайте общение онлайн!')


@bot.callback_query_handler(func=lambda call: call.data in ['yes', 'no'])
def subscribe_or_not(call):
    if call.data == 'yes':
        subscribe(call.from_user.id)
        bot.send_message(chat_id=call.from_user.id, text='Отлично!\nНапишу вам завтра')
    elif call.data == 'no':
        unsubscribe(call.from_user.id)
        bot.send_message(chat_id=call.from_user.id, text='На какое время ставить паузу? Укажите количество встреч.')


def send_remind(call):
    if subscribed(telegram_id=call.from_user.id):
        bot.send_message(chat_id=call.from_user.id,
                         text='Уже середина недели, напишите своему партнеру, если вдруг забыли')


def send():
    pairs = create_pairs()
    for pair in pairs:
        telegram_id_0, telegram_id_1 = get_telegram_id(pair[0]), get_telegram_id(pair[1])
        model_0, model_1 = get_user_info(telegram_id=telegram_id_0), get_user_info(telegram_id=telegram_id_1)
        try:
            bot.send_message(chat_id=telegram_id_0, text='Привет!\nВаша пара на эту неделю:')
            time.sleep(0.5)
            bot.send_photo(chat_id=telegram_id_0, photo=model_1.photo)
            time.sleep(0.5)
            bot.send_message(chat_id=telegram_id_0, text=f'{model_1.name}, {model_1.company}\n'
                                                         f'Могу быть полезен: {model_1.usefulness}\n'
                                                         f'Я ищу: {model_1.interests}')

            bot.send_message(chat_id=telegram_id_1, text='Привет!\nВаша пара на эту неделю:')
            time.sleep(0.5)
            bot.send_photo(chat_id=telegram_id_1, photo=model_0.photo)
            time.sleep(0.5)
            bot.send_message(chat_id=telegram_id_1, text=f'{model_0.name}, {model_0.company}\n'
                                                         f'Могу быть полезен: {model_0.usefulness}\n'
                                                         f'Я ищу: {model_0.interests}')
            create_meeting(user_telegram_id=telegram_id_0, partner_telegram_id=telegram_id_1)
            create_meeting(user_telegram_id=telegram_id_1, partner_telegram_id=telegram_id_0)
        except Exception as e:
            print('Не получилоь отправить сообщение', e)
        time.sleep(2)


def after_meeting(call):
    if subscribed(telegram_id=call.from_user.id):
        markup = types.InlineKeyboardMarkup(row_width=2)
        meeting_took_place = types.InlineKeyboardButton(text='Встреча состоялась', callback_data='meeting_took_place')
        no_meeting = types.InlineKeyboardButton(text='Не получилось встретиться', callback_data='no_meeting')
        markup.add(meeting_took_place, no_meeting)
        partner_name = get_name_by_meeting(telegram_id=call.from_user.id)
        bot.send_message(chat_id=call.from_user.id, text=f'Состоялась встреча с {partner_name}?', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in ['meeting_took_place', 'no_meeting'])
def after_meeting_handler(call):
    if call.data == 'meeting_took_place':
        update_meeting_status(telegram_id=call.from_user.id, status=True)
        markup = types.InlineKeyboardMarkup(row_width=1)
        option1 = types.InlineKeyboardButton(text='Встреча состоялась, отличный собеседник',
                                             callback_data='yes_option1')
        option2 = types.InlineKeyboardButton(text='Встреча состоялась, не могу сформулировать мнение о собеседнике',
                                             callback_data='yes_option2')
        option3 = types.InlineKeyboardButton(text='Встреча состоялась, но, к сожалению, не сложилось общение',
                                             callback_data='yes_option3')
        markup.add(option1, option2, option3)
        bot.send_message(chat_id=call.from_user.id, text=call.message.text, reply_markup=markup)

    elif call.data == 'no_meeting':
        update_meeting_status(telegram_id=call.from_user.id, status=False)
        markup = types.InlineKeyboardMarkup(row_width=1)
        option1 = types.InlineKeyboardButton(text='Не было времени, чтобы написать', callback_data='no_option1')
        option2 = types.InlineKeyboardButton(text='Забыл написать', callback_data='no_option2')
        option3 = types.InlineKeyboardButton(text='Собеседник не ответил', callback_data='no_option3')
        option4 = types.InlineKeyboardButton(text='Собеседник не написал', callback_data='no_option4')
        option5 = types.InlineKeyboardButton(text='Другая причина', callback_data='other_reason')
        markup.add(option1, option2, option3, option4, option5)
        bot.send_message(chat_id=call.from_user.id, text=call.message.text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in ['yes_option1', 'yes_option2', 'yes_option3', 'no_option1',
                                                            'no_option2', 'no_option3', 'no_option4'])
def feedback(call):
    pattern = r'(yes|no)_option(\d+)'
    option = re.findall(pattern=pattern, string=call.data)[0][1]
    option = int(*option) - 1
    opinion = call.message.reply_markup.keyboard[option][0].text
    update_meeting_opinion(telegram_id=call.from_user.id, opinion=opinion)
    bot.send_message(chat_id=call.from_user.id, text='Ответ принят')


@bot.callback_query_handler(func=lambda call: call.data == 'other_reason')
def feedback_other_reason(call):
    bot.send_message(chat_id=call.from_user.id, text='Какая?\nРасскажите, почему не удалось встретиться, '
                                                     'или напишите "пропустить", если не хотите ничего указывать.')

    @bot.message_handler(content_types=['text'])
    def get_reason_from_user(message):

        if message.text.lower() == 'пропустить':
            bot.send_message(chat_id=call.from_user.id, text='Ответ принят')
            update_meeting_opinion(telegram_id=message.from_user.id, opinion='No data')
        else:
            update_meeting_opinion(telegram_id=message.from_user.id, opinion=message.text)
        bot.send_message(chat_id=message.from_user.id, text='Ответ принят')


if __name__ == '__main__':
    print('Running..')
    bot.polling(none_stop=True)
