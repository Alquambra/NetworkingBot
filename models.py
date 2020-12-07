# -*- coding: utf-8 -*-
# Python 3.8.6

from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, VARCHAR, String, LargeBinary, BOOLEAN, ForeignKey
from settings import engine
import numpy as np

Session = sessionmaker(bind=engine)
session = Session()
connection = engine.connect()
Base = declarative_base()


class User(Base):
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
    __tablename__ = 'meeting'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    user_tgid = Column(Integer, ForeignKey('user.telegram_id', ondelete='CASCADE'), nullable=False)
    partner_tgid = Column(Integer, ForeignKey('user.telegram_id', ondelete='CASCADE'), nullable=False)


def create_user_in_db(telegram_id):
    try:
        user = User(telegram_id=telegram_id)
        session.add(user)
        session.commit()
        session.close()
    except Exception as e:
        session.rollback()
        print(e)


def change_photo(telegram_id, photo):
    try:
        u = session.query(User).filter_by(telegram_id=telegram_id).first()
        u.photo = photo
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)


def change_name(telegram_id, name):
    try:
        u = session.query(User).filter_by(telegram_id=telegram_id).first()
        print(u.id)
        u.name = name
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)


def change_company(telegram_id, company):
    try:
        u = session.query(User).filter_by(telegram_id=telegram_id).first()
        print(u.id)
        u.company = company
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)


def change_interests(telegram_id, interests):
    try:
        u = session.query(User).filter_by(telegram_id=telegram_id).first()
        print(u.id)
        u.interests = interests
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)


def change_usefulness(telegram_id, usefulness):
    try:
        u = session.query(User).filter_by(telegram_id=telegram_id).first()
        print(u.id)
        u.usefulness = usefulness
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)


def subscribe(telegram_id):
    try:
        u = session.query(User).filter_by(telegram_id=telegram_id).first()
        u.subscribed = True
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)


def get_user_info(telegram_id):
    try:
        u = session.query(User).filter_by(telegram_id=telegram_id).first()
        session.rollback()
        return u
    except Exception as e:
        session.rollback()
        print(e)


def check_fields_filled(telegram_id):
    try:
        u = session.query(User).filter_by(telegram_id=telegram_id).first()
        fields_filled = False if None in [i[1] for i in u.__dict__.items()] else True
        session.rollback()
        return fields_filled
    except Exception as e:
        session.rollback()
        print(e)


def get_all_users():
    try:
        u = session.query(User).all()
        session.rollback()
        return u
    except Exception as e:
        session.rollback()
        print(e)


def create_pairs():
    try:
        u = session.query(User).all()
        uids = [row.id for row in u]
        pairs = np.random.choice(a=uids, size=(len(uids)//2, 2), replace=False)
        session.rollback()
        return pairs
    except Exception as e:
        print(e)
        session.rollback()


def get_telegram_id(uid):
    try:
        u = session.query(User).filter_by(id=int(uid)).first().telegram_id
        session.rollback()
        return u
    except Exception as e:
        print(e)
        session.rollback()


Base.metadata.create_all(bind=engine)
