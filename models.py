# -*- coding: utf-8 -*-
# Python 3.8.6


from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, VARCHAR, String, LargeBinary
from settings import engine


Session = sessionmaker(bind=engine)
session = Session()

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


Base.metadata.create_all(engine)