# -*- coding: utf-8 -*-
# Python 3.8.6
import datetime

from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, VARCHAR, String, LargeBinary, BOOLEAN, ForeignKey, DateTime
from settings import engine
import numpy as np


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
    photo = Column(LargeBinary, nullable=True)
    name = Column(String(64), nullable=True)
    company = Column(VARCHAR, nullable=True)
    interests = Column(VARCHAR, nullable=True)
    usefulness = Column(VARCHAR, nullable=True)
    subscribed = Column(BOOLEAN, default=False)

    def __repr__(self):
        return f'<User(telegram_id="{self.telegram_id}">'


class Meeting(Base):
    """
    Таблица с данными о встречах пользователей
    """
    __tablename__ = 'meeting'
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.telegram_id', ondelete='CASCADE'), nullable=False)
    partner_id = Column(Integer, ForeignKey('user.telegram_id', ondelete='CASCADE'), nullable=False)
    message_date = Column(DateTime, nullable=True)
    status = Column(BOOLEAN, default=None)
    date = Column(DateTime, nullable=True, default=datetime.datetime.utcnow)
    opinion = Column(String(128), nullable=True)
    user = relationship('User', foreign_keys=[user_id], )
    partner = relationship('User', foreign_keys=[partner_id])

    def __repr__(self):
        return f'<Meeting(user_tgid="{self.user_id}, partner_tgid={self.partner_id}">'


def user_in_db(telegram_id):
    """
    Проверка наличия пользователя в бд
    """
    try:
        session = Session()
        u = session.query(User).filter(User.telegram_id == telegram_id).first
        return u
    except Exception as e:
        print(e)
        session.rollback()


def create_user_in_db(telegram_id):
    """
    Создание записи пользователя в бд user
    """
    try:
        session = Session()
        user = User(telegram_id=telegram_id)
        session.add(user)
        session.flush()
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
    # session.close()


def check_photo(telegram_id):
    """
    Проверка заполнения поля "photo" в базе данных "user"
    """
    try:
        session = Session()
        u = session.query(User).filter(User.telegram_id == telegram_id).first().photo
        return u
    except Exception as e:
        session.rollback()
        print(e)
    # session.close()


def check_name(telegram_id):
    """
    Проверка заполнения поля "name" в базе данных "user"
    """
    try:
        session = Session()
        u = session.query(User).filter(User.telegram_id == telegram_id).first().name
        return u
    except Exception as e:
        session.rollback()
        print(e)
    # session.close()


def check_company(telegram_id):
    """
    Проверка заполнения поля "company" в базе данных "user"
    """
    try:
        session = Session()
        u = session.query(User).filter(User.telegram_id == telegram_id).first().company
        return u
    except Exception as e:
        session.rollback()
        print(e)
    # session.close()


def check_interests(telegram_id):
    """
    Проверка заполнения поля "interests" в базе данных "user"
    """
    try:
        session = Session()
        u = session.query(User).filter(User.telegram_id == telegram_id).first().interests
        return u
    except Exception as e:
        session.rollback()
        print(e)
    # session.close()


def check_usefulness(telegram_id):
    """
    Проверка заполнения поля "usefulness" в базе данных "user"
    """
    try:
        session = Session()
        u = session.query(User).filter(User.telegram_id == telegram_id).first().usefulness
        return u
    except Exception as e:
        session.rollback()
        print(e)
    # session.close()


def change_photo(telegram_id, photo):
    """
    Обновление поля "photo" в базе данных "user"
    """
    try:
        session = Session()
        u = session.query(User).filter(User.telegram_id == telegram_id).first()
        u.photo = photo
        session.flush()
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
    # session.close()


def change_name(telegram_id, name):
    """
    Обновление поля "name" в базе данных "user"
    """
    try:
        session = Session()
        u = session.query(User).filter(User.telegram_id == telegram_id).first()
        print(u.id)
        u.name = name
        session.flush()
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
    # session.close()


def change_company(telegram_id, company):
    """
    Обновление поля "company" в базе данных "user"
    """
    try:
        session = Session()
        u = session.query(User).filter(User.telegram_id == telegram_id).first()
        print(u.id)
        u.company = company
        session.add(u)
        print(u.company)
        print("ТОЧКА ОСТАНОВА")
        session.flush()
        session.commit()
        print('-----------')
    except Exception as e:
        session.rollback()
        print(e)
    # session.close()


def change_interests(telegram_id, interests):
    """
    Обновление поля "interests" в базе данных "user"
    """
    try:
        session = Session()
        u = session.query(User).filter(User.telegram_id == telegram_id).first()
        print(u.interests)
        u.interests = interests
        print(u.interests)
        session.flush()
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
        # session.close()
    print('111111', u.interests)


def change_usefulness(telegram_id, usefulness):
    """
    Обновление поля "usefulness" в базе данных "user"
    """
    try:
        session = Session()
        u = session.query(User).filter(User.telegram_id == telegram_id).first()
        print(u.id)
        u.usefulness = usefulness
        session.flush()
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
    # session.close()


def subscribe(telegram_id):
    """
    Обновление поля "subscribe" на значение 1(True) в базе данных "user"
    """
    try:
        session = Session()
        u = session.query(User).filter(User.telegram_id == telegram_id).first()
        u.subscribed = True
        session.flush()
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
    # session.close()


def unsubscribe(telegram_id):
    """
    Обновление поля "subscribe" на значение 0(False) в базе данных "user"
    """
    try:
        session = Session()
        u = session.query(User).filter(User.telegram_id == telegram_id).first()
        u.subscribed = False
        session.flush()
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
    # session.close()


def subscribed(telegram_id):
    """
    Проверка значения поля "subscribe" в базе данных "user"
    """
    try:
        session = Session()
        u = session.query(User).filter(User.telegram_id == telegram_id).first().subscribed
        return u
    except Exception as e:
        session.rollback()
        print(e)
    # session.close()


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
    # session.close()


def check_fields_filled(telegram_id):
    """
    Проверка заполненности всех данных в таблице "user"
    """
    try:
        session = Session()
        u = session.query(User).filter(User.telegram_id == telegram_id).first()
        fields_filled = False if None in [i[1] for i in u.__dict__.items()] else True
        return fields_filled
    except Exception as e:
        session.rollback()
        print(e)
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
    # session.close()


def create_pairs():
    """
    Составление пар для тех пользователей, у которых поле subscribed = 1(True) таблицы "user"
    """
    try:
        session = Session()
        u = session.query(User).filter(User.subscribed == True).all()
        uids = [row.id for row in u]
        print('uids', uids)
        pairs = np.random.choice(a=uids, size=(len(uids)//2, 2), replace=False)
        return pairs
    except Exception as e:
        print(e)
        session.rollback()
    # session.close()


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
    # session.close()


def create_meeting(user_telegram_id, partner_telegram_id):
    """
    Создание записи в таблице "meeting"
    """
    try:
        session = Session()
        u = Meeting(user_id=user_telegram_id, partner_id=partner_telegram_id)
        session.add(u)
        session.flush()
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
    # session.close()


def get_name_by_meeting(telegram_id):
    """
    Получение "name" партнера пользователя из таблицы "meeting" с присоединением таблицы "user" по "partner_id"
    """
    try:
        session = Session()
        u = session.query(User, Meeting).join(Meeting, User.telegram_id == Meeting.partner_id).\
            filter(Meeting.user_id == telegram_id).order_by(Meeting.date.desc()).first()
        name = u.User.name
        return name
    except Exception as e:
        session.rollback()
        print(e)
    # session.close()


def update_meeting_status(telegram_id, status: bool):
    """
    Обновление поля "status" таблицы "meeting"
    """
    try:
        session = Session()
        u = session.query(Meeting).filter(Meeting.user_id == telegram_id).order_by(Meeting.date.desc()).first()
        u.status = status
        u.message_date = datetime.datetime.utcnow()
        session.flush()
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
    # session.close()


def update_meeting_opinion(telegram_id, opinion):
    """
    Обновление поля "opinion" таблицы "meeting"
    """
    try:
        session = Session()
        u = session.query(Meeting).filter(Meeting.user_id == telegram_id).order_by(Meeting.date.desc()).first()
        u.opinion = opinion
        session.flush()
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
    # session.close()


Base.metadata.create_all(bind=engine)
