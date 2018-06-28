# encoding=utf-8
from wxpy import *
import re
import MySQLdb


emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)


def exec_sql(sql):
    # Open database connection
    db = MySQLdb.connect("47.98.56.206", "root", "123456", "immsg", charset='utf8')
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print("rollback trigger!!!")
        db.rollback()
    db.close()


def gen_sql(data):
    try:
        d = [data.chat.nick_name, data.member.nick_name, data.text, data.voice_length,
             data.type, data.create_time, len(data.chat.members)]
        print(d)
        return "insert into wx_msg (grp,member,msg,duration,type,ctime,members) " \
               "values('%s','%s','%s','%d','%s','%s','%d')" \
           % (d[0], d[1], d[2], d[3], d[4], d[5], d[6])
    except:
        print("data error")



bot = Bot()


@bot.register(Group)
def print_others(msg):

    print(msg)
    sql = gen_sql(msg)
    print(sql)
    exec_sql(sql)


embed()


