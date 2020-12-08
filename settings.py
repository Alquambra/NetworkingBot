# -*- coding: utf-8 -*-
# Python 3.8.6

from sqlalchemy import create_engine


TOKEN = '1431183102:AAF95F0wUZovGBGsgg4tePQzbw69Fef0d6o'
engine = create_engine('sqlite:///bot.db', echo=False, connect_args={'check_same_thread': False})