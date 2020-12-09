# -*- coding: utf-8 -*-
# Python 3.8.6
import datetime

from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, VARCHAR, String, LargeBinary, BOOLEAN, ForeignKey, DateTime
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
    user_id = Column(Integer, ForeignKey('user.telegram_id', ondelete='CASCADE'), nullable=False)
    partner_id = Column(Integer, ForeignKey('user.telegram_id', ondelete='CASCADE'), nullable=False)
    message_date = Column(DateTime, nullable=True)
    status = Column(BOOLEAN, default=None)
    date = Column(DateTime, nullable=True, default=datetime.datetime.utcnow)
    opinion = Column(String(128), nullable=True)
    user = relationship('User', foreign_keys=[user_id])
    partner = relationship('User', foreign_keys=[partner_id])

    def __repr__(self):
        return f'<Meeting(user_tgid="{self.user_id}, partner_tgid={self.partner_id}">'


def create_user_in_db(telegram_id):
    try:
        user = User(telegram_id=telegram_id)
        session.add(user)
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
    session.close()


def change_photo(telegram_id, photo):
    try:
        u = session.query(User).filter_by(telegram_id=telegram_id).first()
        u.photo = photo
        session.commit()
    except Exception as e:
        print(e)
    session.close()


def change_name(telegram_id, name):
    try:
        u = session.query(User).filter_by(telegram_id=telegram_id).first()
        print(u.id)
        u.name = name
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
    session.close()


def change_company(telegram_id, company):
    try:
        u = session.query(User).filter_by(telegram_id=telegram_id).first()
        print(u.id)
        u.company = company
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
    session.close()


def change_interests(telegram_id, interests):
    try:
        u = session.query(User).filter_by(telegram_id=telegram_id).first()
        print(u.id)
        u.interests = interests
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
    session.close()


def change_usefulness(telegram_id, usefulness):
    try:
        u = session.query(User).filter_by(telegram_id=telegram_id).first()
        print(u.id)
        u.usefulness = usefulness
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
    session.close()


def subscribe(telegram_id):
    try:
        u = session.query(User).filter_by(telegram_id=telegram_id).first()
        u.subscribed = True
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
    session.close()


def unsubscribe(telegram_id):
    try:
        u = session.query(User).filter_by(telegram_id=telegram_id).first()
        u.subscribed = False
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
    session.close()


def subscribed(telegram_id):
    try:
        u = session.query(User).filter_by(telegram_id=telegram_id).first().subscribed
        return u
    except Exception as e:
        print(e)
    session.close()


def get_user_info(telegram_id):
    try:
        u = session.query(User).filter_by(telegram_id=telegram_id).first()
        return u
    except Exception as e:
        session.rollback()
        print(e)
    session.close()


def check_fields_filled(telegram_id):
    try:
        u = session.query(User).filter_by(telegram_id=telegram_id).first()
        fields_filled = False if None in [i[1] for i in u.__dict__.items()] else True
        return fields_filled
    except Exception as e:
        session.rollback()
        print(e)
    session.close()


def get_all_users():
    try:
        u = session.query(User).all()
        return u
    except Exception as e:
        session.rollback()
        print(e)
    session.close()


def create_pairs():
    try:
        u = session.query(User).filter_by(subscribed=True).all()
        uids = [row.id for row in u]
        print('uids', uids)
        pairs = np.random.choice(a=uids, size=(len(uids)//2, 2), replace=False)
        return pairs
    except Exception as e:
        print(e)
        session.rollback()
    session.close()


def get_telegram_id(uid):
    try:
        u = session.query(User).filter_by(id=int(uid)).first().telegram_id
        return u
    except Exception as e:
        print(e)
        session.rollback()
    session.close()


def create_meeting(user_telegram_id, partner_telegram_id):
    try:
        u = Meeting(user_id=user_telegram_id, partner_id=partner_telegram_id)
        session.add(u)
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
    session.close()


def get_name_by_meeting(telegram_id):
    try:
        u = session.query(User, Meeting).join(Meeting, User.telegram_id == Meeting.partner_id).\
            filter_by(user_id=telegram_id).order_by(Meeting.date.desc()).first()
        name = u.User.name
        return name
    except Exception as e:
        print(e)
    session.close()


def update_meeting_status(telegram_id, status: bool):
    try:
        u = session.query(Meeting).filter_by(user_id=telegram_id).order_by(Meeting.date.desc()).first()
        u.status = status
        u.message_date = datetime.datetime.utcnow()
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
    session.close()


def update_meeting_opinion(telegram_id, opinion):
    try:
        u = session.query(Meeting).filter_by(user_id=telegram_id).order_by(Meeting.date.desc()).first()
        u.opinion = opinion
        session.commit()
    except Exception as e:
        print(e)
    session.close()


Base.metadata.create_all(bind=engine)
