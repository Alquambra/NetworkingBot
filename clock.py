import time
from telebot import types
import schedule
from models import number_of_pass_meetings, reduce_pass_meetings_by_one, get_pairs, get_user_info, get_link_by_meeting, \
    create_meeting, subscribed, get_name_by_meeting, get_all_subscribed_users
from telebot import AsyncTeleBot
from settings import TOKEN


bot = AsyncTeleBot(TOKEN)


def func1(bot):
    for uid in uids:
        try:
            if number_of_pass_meetings(uid) == 0:
                bot.send_message(chat_id=uid, text='Привет!\nНаступил день подбора новых собеседников.')
                markup = types.InlineKeyboardMarkup(row_width=2)
                yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
                no = types.InlineKeyboardButton(text='Нет', callback_data='no')
                markup.add(yes, no)
                time.sleep(0.5)
                bot.send_message(chat_id=uid,
                                 text='Вас включать в список подбора на завтра?',
                                 reply_markup=markup)
                time.sleep(0.5)
                bot.send_message(chat_id=uid, text='Берегите себя и близких и поддерживайте общение онлайн!')

            else:
                bot.send_message(chat_id=uid, text='Ожидание')
                reduce_pass_meetings_by_one(telegram_id=uid)
        except Exception as e:
            print(e)


def func2(bot):
    pairs = get_pairs()
    for user_id, partner_id in pairs.items():
        try:
            if user_id and partner_id[0]:
                link = get_link_by_meeting(telegram_id=user_id)
                model = get_user_info(telegram_id=partner_id[0])
                bot.send_message(chat_id=user_id, text='Привет!\nВаша пара на эту неделю:')
                time.sleep(0.5)
                bot.send_photo(chat_id=user_id, photo=model.photo)
                time.sleep(0.5)
                bot.send_message(chat_id=user_id, text=f'{model.name}, {model.company}\n'
                                                       f'Могу быть полезен: {model.usefulness}\n'
                                                       f'Я ищу: {model.interests}\n'
                                                       f'Ссылка {link}')
                create_meeting(user_telegram_id=user_id, partner_telegram_id=partner_id[0])
            elif user_id and not partner_id[0]:
                # create_meeting(user_telegram_id=user_id, partner_telegram_id=None)
                bot.send_message(chat_id=user_id, text='К сожалению для вас не нашлось пары:(')

        except Exception as e:
            print('Не получилоь отправить сообщение', e)


def func3(bot):
    for uid in uids:
        try:
            if subscribed(telegram_id=uid):
                bot.send_message(chat_id=uid,
                                 text='Уже середина недели, напишите своему партнеру, если вдруг забыли')
        except Exception as e:
            print(e)


def check_meeting_status(bot):
    for uid in uids:
        try:
            if subscribed(telegram_id=uid):
                markup = types.InlineKeyboardMarkup(row_width=2)
                meeting_took_place = types.InlineKeyboardButton(
                    text='Встреча состоялась',
                    callback_data='meeting_took_place'
                )
                no_meeting = types.InlineKeyboardButton(
                    text='Не получилось встретиться',
                    callback_data='no_meeting')
                markup.add(meeting_took_place, no_meeting
                           )
                partner_name = get_name_by_meeting(telegram_id=uid)
                if partner_name is not None:
                    bot.send_message(chat_id=uid, text=f'Состоялась встреча с {partner_name}?', reply_markup=markup)
        except Exception as e:
            print(e)


users = get_all_subscribed_users()
uids = [user.telegram_id for user in users]
print(uids)


print('Run')
schedule.every().minute.at(':00').do(func1, bot)
schedule.every().minute.at(':15').do(func2, bot)
schedule.every().minute.at(':30').do(func3, bot)
schedule.every().minute.at(':45').do(check_meeting_status, bot)


while True:
    schedule.run_pending()
    time.sleep(1)