# -*- coding: utf-8 -*-
# Python 3.8.6

import datetime
import logging
from collections import defaultdict
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, VARCHAR, String, LargeBinary, BOOLEAN, ForeignKey, DateTime
from settings import engine, debug_with_thread, error_with_thread
from bot_engine import create_pairs
# from threading import Thread


Session = scoped_session(sessionmaker(bind=engine))
# session = Session()
connection = engine.connect()
Base = declarative_base()


class User(Base):
    """
    Таблица с данными пользователя
    """
    __tablename__ = 'user'
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, nullable=False, unique=True)
    link = Column(VARCHAR(64))
    photo = Column(LargeBinary, nullable=True)
    name = Column(String(64), nullable=True)
    company = Column(VARCHAR, nullable=True)
    interests = Column(VARCHAR, nullable=True)
    usefulness = Column(VARCHAR, nullable=True)
    subscribed = Column(BOOLEAN, default=False)
    pass_meetings = Column(Integer, default=0)
    participate = Column(BOOLEAN, default=False)

    def __repr__(self):
        return f'<User(telegram_id="{self.telegram_id}">'


class Meeting(Base):
    """
    Таблица с данными о встречах пользователей
    """
    __tablename__ = 'meeting'
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    user_meeting_id = Column(Integer, ForeignKey('user.telegram_id', ondelete='CASCADE'), nullable=False)
    partner_meeting_id = Column(Integer, ForeignKey('user.telegram_id', ondelete='CASCADE'), nullable=False)
    message_date = Column(DateTime, nullable=True)
    status = Column(BOOLEAN, default=None)
    date = Column(DateTime, nullable=True, default=datetime.datetime.utcnow)
    opinion = Column(String(128), nullable=True)
    user = relationship('User', foreign_keys=[user_meeting_id])
    partner = relationship('User', foreign_keys=[partner_meeting_id])

    def __repr__(self):
        return f'<Meeting(user_tgid="{self.user_meeting_id}, partner_tgid={self.partner_meeting_id}">'


def user_in_db(telegram_id):
    """
    Проверка наличия пользователя в бд
    """
    try:
        session = Session()
        u = session.query(User).filter(User.telegram_id == telegram_id).first()
        return u
    except Exception as e:
        print(e)
        session.rollback()
        error_with_thread('Здесь ошибка')
    session.close()


def create_user_in_db(telegram_id, link):
    """
    Создание записи пользователя в бд user
    """
    try:
        session = Session()
        user = User(telegram_id=telegram_id, link=link)
        session.add(user)
        session.commit()
        debug_with_thread(f'Пользователь {telegram_id} добавлен')
    except Exception as e:
        session.rollback()
        print(e)
        error_with_thread('Здесь ошибка')
    session.close()


def check_photo(telegram_id):
    """
    Проверка заполнения поля "photo" в базе данных "user"
    """
    try:
        session = Session()
        u = session.query(User).filter(User.telegram_id == telegram_id).first().photo
        print(u)
        return u
    except Exception as e:
        session.rollback()
        print(e)
        error_with_thread('Здесь ошибка')
    session.close()


def check_name(telegram_id):
    """
    Проверка заполнения поля "name" в базе данных "user"
    """
    try:
        session = Session()
        u = session.query(User).filter(User.telegram_id == telegram_id).first().name
        print(u)
        return u
    except Exception as e:
        session.rollback()
        print(e)
        error_with_thread('Здесь ошибка')
    session.close()


def check_company(telegram_id):
    """
    Проверка заполнения поля "company" в базе данных "user"
    """
    try:
        session = Session()
        u = session.query(User).filter(User.telegram_id == telegram_id).first().company
        print(u)
        return u
    except Exception as e:
        session.rollback()
        print(e)
        error_with_thread('Здесь ошибка')
    session.close()


def check_interests(telegram_id):
    """
    Проверка заполнения поля "interests" в базе данных "user"
    """
    try:
        session = Session()
        u = session.query(User).filter(User.telegram_id == telegram_id).first().interests
        print(u)
        return u
    except Exception as e:
        session.rollback()
        print(e)
        error_with_thread('Здесь ошибка')
    session.close()


def check_usefulness(telegram_id):
    """
    Проверка заполнения поля "usefulness" в базе данных "user"
    """
    try:
        session = Session()
        u = session.query(User).filter(User.telegram_id == telegram_id).first().usefulness
        print(u)
        return u
    except Exception as e:
        session.rollback()
        print(e)
        error_with_thread('Здесь ошибка')
    session.close()


def change_photo(telegram_id, photo):
    """
    Обновление поля "photo" в базе данных "user"
    """
    try:
        session = Session()
        u = session.query(User).filter(User.telegram_id == telegram_id).first()
        u.photo = photo
        session.commit()
        debug_with_thread(f'Пользователь {telegram_id} изменил фото')
    except Exception as e:
        session.rollback()
        print(e)
        error_with_thread('Здесь ошибка')
    session.close()


def change_name(telegram_id, name):
    """
    Обновление поля "name" в базе данных "user"
    """
    try:
        session = Session()
        u = session.query(User).filter(User.telegram_id == telegram_id).first()
        u.name = name
        session.commit()
        debug_with_thread(f'Пользователь {telegram_id} изменил имя')
    except Exception as e:
        session.rollback()
        print(e)
        error_with_thread('Здесь ошибка')
    session.close()


def change_company(telegram_id, company):
    """
    Обновление поля "company" в базе данных "user"
    """
    try:
        session = Session()
        u = session.query(User).filter(User.telegram_id == telegram_id).first()
        u.company = company
        session.commit()
        debug_with_thread(f'Пользователь {telegram_id} изменил информацию о месте работы')
    except Exception as e:
        session.rollback()
        print(e)
        error_with_thread('Здесь ошибка')
    session.close()


def change_interests(telegram_id, interests):
    """
    Обновление поля "interests" в базе данных "user"
    """
    try:
        session = Session()
        u = session.query(User).filter(User.telegram_id == telegram_id).first()
        u.interests = interests
        session.commit()
        debug_with_thread(f'Пользователь {telegram_id} изменил информацию о своих интересах')
    except Exception as e:
        session.rollback()
        print(e)
        error_with_thread('Здесь ошибка')
    session.close()


def change_usefulness(telegram_id, usefulness):
    """
    Обновление поля "usefulness" в базе данных "user"
    """
    try:
        session = Session()
        u = session.query(User).filter(User.telegram_id == telegram_id).first()
        u.usefulness = usefulness
        session.commit()
        debug_with_thread(f'Пользователь {telegram_id} изменил информацию о своей полезности')
    except Exception as e:
        session.rollback()
        print(e)
        error_with_thread('Здесь ошибка')
    session.close()


def subscribe(telegram_id):
    """
    Обновление поля "subscribe" на значение 1(True) в базе данных "user"
    """
    try:
        session = Session()
        u = session.query(User).filter(User.telegram_id == telegram_id).first()
        u.subscribed = True
        session.commit()
        debug_with_thread(f'Пользователь {telegram_id} подписался на участие в нетворкинге')
    except Exception as e:
        session.rollback()
        print(e)
        error_with_thread('Здесь ошибка')
    # session.close()


def unsubscribe(telegram_id):
    """
    Обновление поля "subscribe" на значение 0(False) в базе данных "user"
    """
    try:
        session = Session()
        u = session.query(User).filter(User.telegram_id == telegram_id).first()
        u.subscribed = False
        session.commit()
        debug_with_thread(f'Пользователь {telegram_id} отписался от участия в нетворкинге')
    except Exception as e:
        session.rollback()
        print(e)
        error_with_thread('Здесь ошибка')
    # session.close()


def subscribed(telegram_id):
    """
    Проверка значения поля "subscribe" в базе данных "user"
    """
    try:
        session = Session()
        u = session.query(User).filter(User.telegram_id == telegram_id).first().subscribed
        session.rollback()
        return u
    except Exception as e:
        session.rollback()
        print(e)
        error_with_thread('Здесь ошибка')
    session.close()


def number_of_pass_meetings(telegram_id):
    """
    Проверка значения поля "pass_meetings" в таблице "user"
    """
    try:
        session = Session()
        u = session.query(User).filter_by(telegram_id=telegram_id).first()
        session.rollback()
        return u.pass_meetings
    except Exception as e:
        print(e)
        error_with_thread('Здесь ошибка')
    session.close()


def reduce_pass_meetings_by_one(telegram_id):
    """
    Уменьшение значения значения поля "pass_meetings" в таблице "user" на единицу
    """
    try:
        session = Session()
        u = session.query(User).filter_by(telegram_id=telegram_id).first()
        u.pass_meetings -= 1
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
        error_with_thread('Здесь ошибка')
    session.close()


def increase_pass_meetings_by_user_input(telegram_id, meetings_quantity: int):
    """
    Увеличение значения значения поля "pass_meetings" в таблице "user" на значение пользовательского ввода
    """
    try:
        session = Session()
        u = session.query(User).filter_by(telegram_id=telegram_id).first()
        u.pass_meetings += meetings_quantity
        session.commit()
        debug_with_thread(f'Пользователь {telegram_id} решил пропустить {meetings_quantity} встречи')
    except Exception as e:
        session.rollback()
        print(e)
        error_with_thread('Здесь ошибка')
    session.close()


def get_user_info(telegram_id):
    """
    Получение всей информации по конкретному пользователю
    """
    try:
        session = Session()
        u = session.query(User).filter(User.telegram_id == telegram_id).first()
        return u
    except Exception as e:
        session.rollback()
        print(e)
        error_with_thread('Здесь ошибка')
    # session.close()


def check_fields_filled(telegram_id):
    """
    Проверка заполненности всех данных в таблице "user"
    """
    try:
        session = Session()
        u = session.query(User.photo, User.name, User.company, User.interests, User.usefulness).\
            filter(User.telegram_id == telegram_id).first()
        fields_filled = False if None in [i for i in u] else True
        return fields_filled
    except Exception as e:
        session.rollback()
        print(e)
        error_with_thread('Здесь ошибка')
    # session.close()


def get_all_users():
    """
    Получение всей информации из таблицы "user"
    """
    try:
        session = Session()
        u = session.query(User).all()
        return u
    except Exception as e:
        session.rollback()
        print(e)
        error_with_thread('Здесь ошибка')
    # session.close()


def get_all_subscribed_users():
    """
    Получение всей информации из таблицы "user"
    """
    try:
        session = Session()
        u = session.query(User).filter(User.subscribed == True).all()
        return u
    except Exception as e:
        session.rollback()
        print(e)
        error_with_thread('Здесь ошибка')
    session.close()


def participate(telegram_id):
    """
    Обновление поля "subscribe" на значение 1(True) в базе данных "user"
    """
    try:
        session = Session()
        u = session.query(User).filter(User.telegram_id == telegram_id).first()
        u.participate = True
        session.commit()
        debug_with_thread(f'Пользователь {telegram_id} подписался на участие в нетворкинге')
    except Exception as e:
        session.rollback()
        print(e)
        error_with_thread('Здесь ошибка')
    session.close()


def get_all_participated_users():
    try:
        session = Session()
        u = session.query(User).filter(User.participate == True).all()
        return u
    except Exception as e:
        session.rollback()
        print(e)
        error_with_thread('Здесь ошибка')
    session.close()


def get_pairs():
    """
    Составление пар для тех пользователей, у которых поле subscribed = 1(True) таблицы "user"
    """
    try:
        session = Session()
        u = session.query(User).filter(User.subscribed == True).all()
        users_and_partners = session.query(Meeting.user_meeting_id, Meeting.partner_meeting_id)\
            .order_by(Meeting.user_meeting_id).all()

        uids = [row.telegram_id for row in u]
        debug_with_thread(f'Пользователи, которые приняли участие в формировании пар {uids}')
        dict_with_previous_pairs = defaultdict(list)
        for user, partner in users_and_partners:
            user, partner = str(user), partner
            dict_with_previous_pairs[user].append(partner)
        print('dict_with_prev', dict_with_previous_pairs)
        debug_with_thread(f'Предыдущие пары пользователей {dict_with_previous_pairs}')
        pairs = create_pairs(dict_with_previous_meetings=dict_with_previous_pairs, taking_part_users=uids)
        debug_with_thread(f'Составленные пары {pairs}')
        print(pairs)
        return pairs
    except Exception as e:
        print(e)
        session.rollback()
        error_with_thread('Здесь ошибка')
    session.close()


def get_telegram_id(uid):
    """
    Получение "telegram_id" пользователя по его "id" из таблицы "user"
    """
    try:
        session = Session()
        u = session.query(User).filter(User.id == int(uid)).first().telegram_id
        return u
    except Exception as e:
        print(e)
        session.rollback()
        error_with_thread('Здесь ошибка')
    session.close()


def create_meeting(user_telegram_id, partner_telegram_id):
    """
    Создание записи в таблице "meeting"
    """
    try:
        session = Session()
        u = Meeting(user_meeting_id=user_telegram_id, partner_meeting_id=partner_telegram_id)
        session.add(u)
        session.commit()
        debug_with_thread(f'Встреча пользователя {user_telegram_id} с {partner_telegram_id} добавлена')
    except Exception as e:
        print(e)
        session.rollback()
        error_with_thread('Здесь ошибка')
    session.close()


def get_name_by_meeting(telegram_id):
    """
    Получение "name" партнера пользователя из таблицы "meeting" с присоединением таблицы "user" по "partner_id"
    """
    try:
        session = Session()
        u = session.query(User, Meeting).join(Meeting, User.telegram_id == Meeting.partner_meeting_id).\
            filter(Meeting.user_meeting_id == telegram_id).order_by(Meeting.date.desc()).first()
        name = u.User.name
        return name
    except Exception as e:
        session.rollback()
        print(e)
        error_with_thread('Здесь ошибка')
    session.close()


def get_link_by_meeting(telegram_id):
    """
    Получение "link" партнера пользователя из таблицы "meeting" с присоединением таблицы "user" по "partner_id"
    """
    try:
        session = Session()
        u = session.query(User, Meeting).join(Meeting, User.telegram_id == Meeting.partner_meeting_id).\
            filter(Meeting.user_meeting_id == telegram_id).order_by(Meeting.date.desc()).first()
        name = u.User.link
        return name
    except Exception as e:
        session.rollback()
        print(e)
        error_with_thread('Здесь ошибка')
    session.close()


def update_meeting_status(telegram_id, status: bool):
    """
    Обновление поля "status" таблицы "meeting"
    """
    try:
        session = Session()
        u = session.query(Meeting).filter(Meeting.user_meeting_id == telegram_id).order_by(Meeting.date.desc()).first()
        u.status = status
        u.message_date = datetime.datetime.utcnow()
        session.commit()
        debug_with_thread(f'Пользователь {telegram_id} изменил статус встречи c {u.partner_meeting_id} на {status}')
    except Exception as e:
        print(e)
        session.rollback()
        error_with_thread('Здесь ошибка')
    session.close()


def update_meeting_opinion(telegram_id, opinion):
    """
    Обновление поля "opinion" таблицы "meeting"
    """
    try:
        session = Session()
        u = session.query(Meeting).filter(Meeting.user_meeting_id == telegram_id).order_by(Meeting.date.desc()).first()
        u.opinion = opinion
        session.commit()
        debug_with_thread(f'Пользователь {telegram_id} добавил обратную связь о встрече с {u.partner_meeting_id}:'
                          f' {opinion}')
    except Exception as e:
        session.rollback()
        print(e)
        error_with_thread('Здесь ошибка')
    session.close()


def get_last_time_of_message(telegram_id):
    try:
        session = Session()
        u = session.query(Meeting).filter_by(user_meeting_id=telegram_id).order_by(Meeting.date_desc()).first()
        return u.Meeting.date
    except Exception as e:
        session.rollback()
        error_with_thread(f'Здесь ошибка {e}')
    session.close()


Base.metadata.create_all(bind=engine)
