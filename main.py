from telebot import TeleBot, types
from settings import TOKEN
import peewee

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['none'])
def start(message):
    print(message.__dir__())
    print(message.chat)
    print(message.from_user)
    bot.send_message(message.chat.id, 'Привет!\nДобавьте информацию о себе.\nМы рассылаем информацию каждую пятницу.')


@bot.message_handler(commands=['start'])
def buttons_inline(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    get_photo = types.InlineKeyboardButton(text='Фото', callback_data='add_photo')
    get_name = types.InlineKeyboardButton(text='Имя и Фамилия', callback_data='add_name')
    get_company = types.InlineKeyboardButton(text='Компания и позиция', callback_data='add_company')
    get_interests = types.InlineKeyboardButton(text='Что я ищу', callback_data='add_interests')
    get_usefulness = types.InlineKeyboardButton(text='Чем могу быть полезен', callback_data='add_usefulness')

    markup.add(get_photo, get_name, get_company, get_interests, get_usefulness)

    start_message = 'Привет!\nДобавьте информацию о себе.\nМы рассылаем информацию каждую пятницу.'
    bot.send_message(message.chat.id, start_message, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    if call.data == 'add_photo':
        text = 'Загрузите свое фото, чтобы люди знали, как вы выглядите. ' \
               'Можно прислать уже сделанное фото, но я рекомендую сделать селфи прямо сейчас. ' \
               'Так вас легче будет узнать. ' \
               'Отправьте свое фото прямо сюда.'
        msg = bot.send_message(call.message.chat.id, text)
        bot.register_next_step_handler(msg, get_photo_from_user)


    elif call.data == 'add_name':
        text = 'Как вас представлять другим участникам? ' \
               f'В вашем профиле указано, что ваше имя - {call.from_user.username} ' \
               'Я могу использовать его. Или пришлите мне свое имя текстом. '
        msg = bot.send_message(call.message.chat.id, text)
        bot.register_next_step_handler(msg, get_name_from_user)


    elif call.data == 'add_company':
        text = 'Где и кем вы работаете? Это поможет людям понять, чем вы можете быть интересны. ' \
               'Пришлите мне, пожалуйста, название компании и вашу должность. ' \
               'Например, "Директор в "ООО Палехче".'
        msg = bot.send_message(call.message.chat.id, text)
        bot.register_next_step_handler(msg, get_company_from_user)


    elif call.data == 'add_interests':
        text = 'О каких темах вам было бы интересно поговорить? ' \
               'Например, "инвестиции, советы по воспитанию детей, ' \
               'возможна ли медицина в условиях невесомости".'
        msg = bot.send_message(call.message.chat.id, text)
        bot.register_next_step_handler(msg, get_interests_from_user)


    elif call.data == 'add_usefulness':
        text = 'В каких темах вы разбираетесь? Например, "умею пасти котов, инвестирую, развожу сурков".'
        msg = bot.send_message(call.message.chat.id, text)
        bot.register_next_step_handler(msg, get_usefulness_from_user)
    bot.clear_step_handler()


def get_photo_from_user(message):
    photo = ''


def get_name_from_user(message):
    name = message.text
    bot.clear_step_handler(name)
    print('name:', name)


def get_company_from_user(message):
    company = message.text
    bot.clear_step_handler(company)
    print('company:', company)


def get_interests_from_user(message):
    interests = message.text

    print('interests:', interests)


def get_usefulness_from_user(message):
    usefulness = message.text
    print('usefulness:', usefulness)


if __name__ == '__main__':
    print('Running..')
    bot.polling()
