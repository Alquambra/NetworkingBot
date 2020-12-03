from sqlalchemy import create_engine



TOKEN = '1431183102:AAF95F0wUZovGBGsgg4tePQzbw69Fef0d6o'
engine = create_engine('postgresql://postgres:root@localhost:5555/alchemy', echo=False)