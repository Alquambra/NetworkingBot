# -*- coding: utf-8 -*-
# Python 3.8.6

import time
from telebot import types, AsyncTeleBot
from settings import TOKEN
from models import user_in_db, create_user_in_db, change_photo, change_name, change_company, change_interests, \
    change_usefulness, subscribe, unsubscribe, get_user_info, check_fields_filled, update_meeting_status,\
    update_meeting_opinion, increase_pass_meetings_by_user_input, participate
import re



# tok = os.environ['TOKEN']


bot = AsyncTeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def buttons_inline(message):
    """
    Функция инициирует бота и добавляет кнопки с выбором поля для заполнения информации.
    """
    if not user_in_db(telegram_id=message.from_user.id):
        create_user_in_db(telegram_id=message.from_user.id, link='@' + message.from_user.username)
    print(message.from_user.username)

    if not check_fields_filled(telegram_id=message.from_user.id):
        u = get_user_info(telegram_id=message.from_user.id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        photo_caption = 'Фото \u2705' if u.photo else 'Фото \u274c'
        name_caption = 'Имя и фамилия \u2705' if u.name else 'Имя и фамилия \u274c'
        company_caption = 'Компания и позиция \u2705' if u.company else 'Компани и позиция \u274c'
        interests_caption = 'Что я ищу \u2705' if u.interests else 'Что я ищу \u274c'
        usefulness_caption = 'Чем могу быть полезен \u2705' if u.usefulness else 'Чем могу быть полезен \u274c'
        get_photo = types.InlineKeyboardButton(text=photo_caption, callback_data='add_photo')
        get_name = types.InlineKeyboardButton(text=name_caption, callback_data='add_name')
        get_company = types.InlineKeyboardButton(text=company_caption, callback_data='add_company')
        get_interests = types.InlineKeyboardButton(text=interests_caption, callback_data='add_interests')
        get_usefulness = types.InlineKeyboardButton(text=usefulness_caption, callback_data='add_usefulness')
        markup.add(get_photo, get_name, get_company, get_interests, get_usefulness)

        start_message = 'Остались незаполненные поля'
        if message.text == '/start':
            start_message = 'Привет!\nДобавьте информацию о себе.\nМы рассылаем информацию каждую пятницу.'
        bot.send_message(message.chat.id, start_message, reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup()
        participate_net = types.InlineKeyboardButton(text='Учавствовать в нетворкинге',
                                                     callback_data='participate_netw')
        markup.add(participate_net)
        bot.send_message(chat_id=message.chat.id, text='Учавствовать в нетворкинге', reply_markup=markup)


@bot.message_handler(commands=['edit'])
def edit_profile(message):
    """
    Функция редактирования профиля. Отправляет пользовтелю кнопки с выбором поля для изменения.
    """
    u = get_user_info(telegram_id=message.from_user.id)
    markup = types.InlineKeyboardMarkup(row_width=1)
    photo_caption = 'Фото \u2705' if u.photo else 'Фото \u274c'
    name_caption = 'Имя и фамилия \u2705' if u.name else 'Имя и фамилия \u274c'
    company_caption = 'Компания и позиция \u2705' if u.company else 'Компани и позиция \u274c'
    interests_caption = 'Что я ищу \u2705' if u.interests else 'Что я ищу \u274c'
    usefulness_caption = 'Чем могу быть полезен \u2705' if u.usefulness else 'Чем могу быть полезен \u274c'

    get_photo = types.InlineKeyboardButton(text=photo_caption, callback_data='add_photo(edit)')
    get_name = types.InlineKeyboardButton(text=name_caption, callback_data='add_name(edit)')
    get_company = types.InlineKeyboardButton(text=company_caption, callback_data='add_company(edit)')
    get_interests = types.InlineKeyboardButton(text=interests_caption, callback_data='add_interests(edit)')
    get_usefulness = types.InlineKeyboardButton(text=usefulness_caption, callback_data='add_usefulness(edit)')
    markup.add(get_photo, get_name, get_company, get_interests, get_usefulness)
    start_message = 'Выберите поле для редактирования'
    bot.send_message(message.chat.id, start_message, reply_markup=markup)


@bot.message_handler(commands=['user_info'])
def user_info(message):
    """
    Функция отправляет пользователю информацию о его профиле.
    """
    model = get_user_info(telegram_id=message.from_user.id)
    bot.send_photo(chat_id=message.chat.id, photo=model.photo)
    bot.send_message(chat_id=message.chat.id, text='Информация о профиле:\n'
                                                   f'{model.name}, {model.company}\n'
                                                   f'Могу быть полезен: {model.usefulness}\n'
                                                   f'Я ищу: {model.interests}\n'
                                                   f'{model.link}')


@bot.callback_query_handler(func=lambda call: call.data in ['add_photo', 'add_name', 'add_company',
                                                            'add_interests', 'add_usefulness'])
def handle(call):
    """
    Функция обрабатывает события при редактировании профиля.
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
        firstlast_name = call.from_user.first_name
        if call.from_user.last_name:
            firstlast_name += f' {call.from_user.last_name}'
        text = 'Как вас представлять другим участникам? ' \
               f'В вашем профиле указано, что ваше имя - {firstlast_name} ' \
               'Я могу использовать его. Или пришлите мне свое имя текстом. '
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup).wait()
        # bot.register_next_step_handler(msg, get_name_from_user)

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


@bot.callback_query_handler(func=lambda call: call.data in ['add_photo(edit)', 'add_name(edit)', 'add_company(edit)',
                                                            'add_interests(edit)', 'add_usefulness(edit)'])
def handle_edit(call):
    """
    Функция обрабатывает события при редактировании профиля.
    """
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    if call.data == 'add_photo(edit)':
        text = 'Загрузите свое фото.'
        msg = bot.send_message(call.message.chat.id, text).wait()
        bot.register_next_step_handler(msg, get_photo_from_user)
    elif call.data == 'add_name(edit)':
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        msg = bot.send_message(chat_id=call.message.chat.id, text='Введите свое имя').wait()
        bot.register_next_step_handler(msg, get_name_from_user)
    elif call.data == 'add_company(edit)':
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        text = 'Где и кем вы работаете? Это поможет людям понять, чем вы можете быть интересны. ' \
               'Пришлите мне, пожалуйста, название компании и вашу должность. ' \
               'Например, "Директор в "ООО Палехче".'
        msg = bot.send_message(call.message.chat.id, text).wait()
        bot.register_next_step_handler(msg, get_company_from_user)
    elif call.data == 'add_interests(edit)':
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        text = 'О каких темах вам было бы интересно поговорить? ' \
               'Например, "инвестиции, советы по воспитанию детей, ' \
               'возможна ли медицина в условиях невесомости".'
        msg = bot.send_message(call.message.chat.id, text).wait()
        bot.register_next_step_handler(msg, get_interests_from_user)

    elif call.data == 'add_usefulness(edit)':
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        text = 'В каких темах вы разбираетесь? Например, "умею пасти котов, инвестирую, развожу сурков".'
        msg = bot.send_message(call.message.chat.id, text).wait()
        bot.register_next_step_handler(msg, get_usefulness_from_user)


@bot.callback_query_handler(func=lambda call: call.data == 'photo_from_profile')
def from_profile(call):
    """
    Функция загружает фотографию из аккаунта telegram пользователя
    """
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    profile_photos = bot.get_user_profile_photos(user_id=call.from_user.id).wait().photos
    avatar = bot.get_file(profile_photos[0][0].file_id).wait()
    downloaded = bot.download_file(avatar.file_path).wait()
    change_photo(telegram_id=call.from_user.id, photo=downloaded)
    bot.send_message(chat_id=call.from_user.id, text='Выбрана фотография из вашего профиля').wait()
    bot.send_photo(chat_id=call.from_user.id, photo=downloaded)
    time.sleep(0.5)
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    option1 = types.InlineKeyboardButton(text='Продолжить')
    markup.add(option1)
    bot.send_message(chat_id=call.from_user.id, text='Продолжить..', reply_markup=markup).wait()
    bot.register_next_step_handler(message=call.message, callback=buttons_inline)


@bot.callback_query_handler(func=lambda call: call.data == 'load_photo')
def load_photo(call):
    """
    Функция обрабатывает кнопку загрузки фото и перенаправляет в функцию загрузки
    """
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    text = 'Загрузите свое фото, чтобы люди знали, как вы выглядите. ' \
           'Можно прислать уже сделанное фото, но я рекомендую сделать селфи прямо сейчас. ' \
           'Так вас легче будет узнать. ' \
           'Отправьте свое фото прямо сюда.'
    msg = bot.send_message(call.message.chat.id, text).wait()
    bot.register_next_step_handler(msg, get_photo_from_user)


@bot.callback_query_handler(func=lambda call: call.data == 'name_from_profile')
def name_from_profile(call):
    """
    Функция загружает имя и фамилию (если есть) из аккаунта telegram пользователя
    """
    bot.clear_step_handler(message=call.message)
    firstlast_name = call.from_user.first_name
    if call.from_user.last_name:
        firstlast_name += f' {call.from_user.last_name}'

    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    option1 = types.InlineKeyboardButton(text='Продолжить')
    markup.add(option1)

    change_name(telegram_id=call.from_user.id, name=firstlast_name)
    text = f'Изменения приняты. Ваше имя {firstlast_name}. Продолжить..'
    bot.send_message(chat_id=call.from_user.id, text=text, reply_markup=markup).wait()
    bot.register_next_step_handler(message=call.message, callback=buttons_inline)


@bot.callback_query_handler(func=lambda call: call.data == 'edit_name')
def edit_name(call):
    """
    Функция принимает строку от пользователя и записывает ее в бд как имя
    """

    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    msg = bot.send_message(chat_id=call.message.chat.id, text='Введите свое имя').wait()
    bot.register_next_step_handler(msg, get_name_from_user)
    bot.register_next_step_handler(message=call.message, callback=buttons_inline)


def get_photo_from_user(message):
    """
    Функция принимает фото от пользователя и загружает его в бд
    """
    if message.content_type == 'photo':
        user_photo = bot.get_file(message.photo[0].file_id).wait()
        downloaded = bot.download_file(user_photo.file_path).wait()

        change_photo(telegram_id=message.from_user.id, photo=downloaded)
        bot.send_message(chat_id=message.from_user.id, text='Фотография загружена')
    else:
        bot.send_message(message.chat.id, 'Это не фото')


def get_name_from_user(message):
    """
    Функция принимает строку от пользователя и записывает ее как "Имя" в бд
    """
    if message.content_type == 'text':
        user_name = message.text
        print('Изменение имени', user_name)
        change_name(telegram_id=message.from_user.id, name=user_name)
        print('Изменение принято')
        bot.send_message(chat_id=message.chat.id, text='Изменения приняты')
    else:
        bot.send_message(message.chat.id, 'Пришлите текст')


def get_company_from_user(message):
    """
    Функция принимает строку от пользователя и записывает ее как "Компания и позиция" в бд
    """
    if message.content_type == 'text':
        user_company = message.text
        print('Изменение компании', user_company)
        change_company(telegram_id=message.from_user.id, company=user_company)
        print('Изменение принято')
        bot.send_message(chat_id=message.chat.id, text='Изменения приняты')
    else:
        bot.send_message(message.chat.id, 'Пришлите текст')


def get_interests_from_user(message):
    """
    Функция принимает строку от пользователя и записывает ее как "Что я ищу" в бд
    """
    if message.content_type == 'text':
        user_interests = message.text
        print('Изменение интересов', user_interests)
        change_interests(telegram_id=message.from_user.id, interests=user_interests)
        print('Изменение принято')
        bot.send_message(chat_id=message.chat.id, text='Изменения приняты')
    else:
        bot.send_message(message.chat.id, 'Пришлите текст')


def get_usefulness_from_user(message):
    """
    Функция принимает строку от пользователя и записывает ее как "Чем могу быть полезен" в бд
    """
    if message.content_type == 'text':
        user_usefulness = message.text
        change_usefulness(telegram_id=message.from_user.id, usefulness=user_usefulness)
        bot.send_message(chat_id=message.chat.id, text='Изменения приняты')
    else:
        bot.send_message(message.chat.id, 'Пришлите текст')


@bot.callback_query_handler(func=lambda call: call.data == 'participate_netw')
def clicked(call):
    """
    Функция обрабатывает кнопку "Участие в нетворкинге" и запускает цикл нетворкинга
    """
    subscribe(telegram_id=call.from_user.id)
    bot.send_message(chat_id=call.from_user.id, text='Участие подтверждено')
    participate(telegram_id=call.from_user.id)
#     schedule.every().minute.at(':00').do(send_markup_yes_no, call)
#     time.sleep(1)
#     schedule.every().minute.at(':15').do(send, call)
#     time.sleep(1)
#     schedule.every().minute.at(':30').do(send_remind, call)
#     time.sleep(1)
#     schedule.every().minute.at(':45').do(after_meeting, call)
#
#     while True:
#         schedule.run_pending()
#         time.sleep(1)


# def send_markup_yes_no(call):
#     """
#     Функция спрашивает пользователя будет ли он учавствовать в следующем подборе.
#     """
#     if number_of_pass_meetings(telegram_id=call.from_user.id) == 0:
#         unsubscribe(call.from_user.id)
#         bot.send_message(chat_id=call.from_user.id, text='Привет!\nНаступил день подбора новых собеседников.')
#         markup = types.InlineKeyboardMarkup(row_width=2)
#         yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
#         no = types.InlineKeyboardButton(text='Нет', callback_data='no')
#         markup.add(yes, no)
#         time.sleep(0.5)
#         bot.send_message(chat_id=call.from_user.id, text='Вас включать в список подбора на завтра?',
#                          reply_markup=markup)
#         time.sleep(0.5)
#         bot.send_message(chat_id=call.from_user.id, text='Берегите себя и близких и поддерживайте общение онлайн!')
#
#     else:
#         bot.send_message(chat_id=call.from_user.id, text='Ожидание')
#         reduce_pass_meetings_by_one(telegram_id=call.from_user.id)


@bot.callback_query_handler(func=lambda call: call.data in ['yes', 'no'])
def subscribe_or_not(call):
    """
    Функция обрабатывает результат предыдущей функции. Ответ пользователя записывается в бд.
    """
    if call.data == 'yes':
        subscribe(call.from_user.id)
        bot.send_message(chat_id=call.from_user.id, text='Отлично!\nНапишу вам завтра')
    elif call.data == 'no':
        unsubscribe(call.from_user.id)
        msg = bot.send_message(chat_id=call.from_user.id,
                               text='На какое время ставить паузу? Укажите количество встреч.').wait()
        bot.register_next_step_handler(message=msg, callback=increase_pass_meetings)


def increase_pass_meetings(message):
    try:
        number = int(message.text) - 1
        increase_pass_meetings_by_user_input(telegram_id=message.from_user.id, meetings_quantity=number)
    except Exception as e:
        bot.send_message(message.from_user.id, 'Необходимо ввести число')


# def send_remind(call):
#     """
#     Функция отправляет пользователю напоминание.
#     """
#     if subscribed(telegram_id=call.from_user.id):
#         bot.send_message(chat_id=call.from_user.id,
#                          text='Уже середина недели, напишите своему партнеру, если вдруг забыли')


# def send(call):
#     """
#     Функция составляет пары участников и отправляет каждому участнику сообщение с информацией о его паре.
#     """
#     pairs = get_pairs()
#     print(f'\n\nПАРЫ {pairs}\n\n')
#     for user_id, partner_id in pairs.items():
#         print('userid and partnerid', user_id, partner_id[0])
#         try:
#             if user_id and partner_id[0]:
#                 link = get_link_by_meeting(telegram_id=user_id)
#                 model = get_user_info(telegram_id=partner_id[0])
#                 bot.send_message(chat_id=user_id, text='Привет!\nВаша пара на эту неделю:')
#                 time.sleep(0.5)
#                 bot.send_photo(chat_id=user_id, photo=model.photo)
#                 time.sleep(0.5)
#                 bot.send_message(chat_id=user_id, text=f'{model.name}, {model.company}\n'
#                                                        f'Могу быть полезен: {model.usefulness}\n'
#                                                        f'Я ищу: {model.interests}\n'
#                                                        f'Ссылка {link}')
#                 create_meeting(user_telegram_id=user_id, partner_telegram_id=partner_id[0])
#             elif user_id and not partner_id[0]:
#                 # create_meeting(user_telegram_id=user_id, partner_telegram_id=None)
#                 bot.send_message(chat_id=user_id, text='К сожалению для вас не нашлось пары:(')
#             # else:
#             #     continue
#     # for pair in pairs:
#     #     telegram_id_0, telegram_id_1 = get_telegram_id(pair[0]), get_telegram_id(pair[1])
#     #     model_0, model_1 = get_user_info(telegram_id=telegram_id_0), get_user_info(telegram_id=telegram_id_1)
#     #     try:
#     #         bot.send_message(chat_id=telegram_id_0, text='Привет!\nВаша пара на эту неделю:')
#     #         time.sleep(0.5)
#     #         bot.send_photo(chat_id=telegram_id_0, photo=model_1.photo)
#     #         time.sleep(0.5)
#     #         bot.send_message(chat_id=telegram_id_0, text=f'{model_1.name}, {model_1.company}\n'
#     #                                                      f'Могу быть полезен: {model_1.usefulness}\n'
#     #                                                      f'Я ищу: {model_1.interests}')
#     #
#     #         bot.send_message(chat_id=telegram_id_1, text='Привет!\nВаша пара на эту неделю:')
#     #         time.sleep(0.5)
#     #         bot.send_photo(chat_id=telegram_id_1, photo=model_0.photo)
#     #         time.sleep(0.5)
#     #         bot.send_message(chat_id=telegram_id_1, text=f'{model_0.name}, {model_0.company}\n'
#     #                                                      f'Могу быть полезен: {model_0.usefulness}\n'
#     #                                                      f'Я ищу: {model_0.interests}')
#     #         create_meeting(user_telegram_id=telegram_id_0, partner_telegram_id=telegram_id_1)
#     #         create_meeting(user_telegram_id=telegram_id_1, partner_telegram_id=telegram_id_0)
#         except Exception as e:
#             print('Не получилоь отправить сообщение', e)
#
#
# def after_meeting(call):
#     """
#     Функция спрашивает пользователя о том, состоялась ли встреча.
#     """
#     if subscribed(telegram_id=call.from_user.id):
#         markup = types.InlineKeyboardMarkup(row_width=2)
#         meeting_took_place = types.InlineKeyboardButton(text='Встреча состоялась', callback_data='meeting_took_place')
#         no_meeting = types.InlineKeyboardButton(text='Не получилось встретиться', callback_data='no_meeting')
#         markup.add(meeting_took_place, no_meeting)
#         partner_name = get_name_by_meeting(telegram_id=call.from_user.id)
#         if partner_name is not None:
#             bot.send_message(chat_id=call.from_user.id, text=f'Состоялась встреча с {partner_name}?',
#                              reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in ['meeting_took_place', 'no_meeting'])
def after_meeting_handler(call):
    """
    Функция обрабатывает ответ пользователя на предыдущую функцию. Предлагает ему новые варианты ответов
    в зависимости от прошлого ответа
    """
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
    """
    Функция записывает в бд выбранный ответ пользователя
    """
    pattern = r'(yes|no)_option(\d+)'
    option = re.findall(pattern=pattern, string=call.data)[0][1]
    option = int(*option) - 1
    opinion = call.message.reply_markup.keyboard[option][0].text
    update_meeting_opinion(telegram_id=call.from_user.id, opinion=opinion)
    bot.send_message(chat_id=call.from_user.id, text='Ответ принят')


@bot.callback_query_handler(func=lambda call: call.data == 'other_reason')
def feedback_other_reason(call):
    """
    Функция обрабатывает вариант ответа "Другая причина".
    """
    bot.send_message(chat_id=call.from_user.id, text='Какая?\nРасскажите, почему не удалось встретиться, '
                                                     'или напишите "пропустить", если не хотите ничего указывать.')

    @bot.message_handler(content_types=['text'])
    def get_reason_from_user(message):
        """
        Функция записывает ответ пользователя в бд.
        """
        if message.text.lower() == 'пропустить':
            bot.send_message(chat_id=call.from_user.id, text='Ответ принят')
            update_meeting_opinion(telegram_id=message.from_user.id, opinion='No data')
        else:
            update_meeting_opinion(telegram_id=message.from_user.id, opinion=message.text)
            bot.send_message(chat_id=message.from_user.id, text='Ответ принят')


if __name__ == '__main__':
    print('Running..')
    bot.polling(none_stop=True)
