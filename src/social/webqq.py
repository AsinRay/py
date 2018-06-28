#!/usr/bin/python
# encoding=utf-8
import MySQLdb
from subprocess import Popen, PIPE
import sys


logFile = '~/webqq.log'


def format_data(data):
    try:
        idx = data.find('[info]')
        if idx == -1:
            dt = data[1:18]
            msg = data[20:]
            msg = msg.replace('[36m', '').replace('[0m', '').strip()
            if msg.find('群消息') == 2:
                msg = msg[14:]
                grp_person = msg.split('|')
                person = grp_person[0]
                if grp_person[1]:
                    gp = grp_person[1].split(':')
                    if gp:
                        grp = gp[0]
                        if gp[1]:
                            msg = gp[1]
                        else:
                            msg = ''
                        return [dt, grp, person, msg]
                    else:
                        return []
                else:
                    return []

            else:
                return []
        else:
            return []
    except:
        print(">>>> %s " % data)
        return []


def gen_sql(data):
    if data:
        d = data
        return "insert into qqmsg (msg_dt,grp,member, msg) values('{0}','{1}','{2}','{3}')".format(d[0], d[1], d[2], d[3])
    else:
        return None

def exec_sql(sql):
    # Open database connection
    db = MySQLdb.connect("47.98.56.206", "root", "123456", "immsg", charset='utf8')
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print('Err on commit to database !!')
        db.rollback()
    db.close()


def monitor_log(log):
    reload(sys)
    sys.setdefaultencoding('utf8')
    p = Popen('tail -3f ' + log, stdout=PIPE, stderr=PIPE, shell=True)
    pid = p.pid
    print("Popen pid: %s" % str(pid))
    while True:
        line = p.stdout.readline()
        if line:
            data = format_data(line)
            if data:
                # print(data)
                sql = gen_sql(data)
                if sql:
                    exec_sql(sql)
        else:
            print('No data is received!!')


if __name__ == '__main__':
    monitor_log(logFile)
