# ! /usr/bin/pyton
# -*- coding: utf-8 -*-
import gc
import time
import MySQLdb
from datetime import timedelta

wc = ' FROM symbol_position WHERE `time` >= curdate() and name_eg is not null and week_delta is null'
dis_addr_sql = 'SELECT name_eg, address, id  %s and id in ' \
               '(select max(id) %s group by name_eg,address) order by id' % (wc, wc)
cur_data_sql = "SELECT `quantity`, `time`, `week_delta`  FROM symbol_position WHERE id = '%s'"
old_blc_dql = "SELECT quantity from symbol_position " \
              "WHERE time <= '%10s' and name_eg='%s' and address = '%s' and id < %d order by id desc limit 1"
update_sql = "update symbol_position set week_delta = '%s' where id = %d"


def exec_hold_exchange():
    print("Hold exchange started, working hard now ...")
    db = MySQLdb.connect("47.98.56.206", "root", "123456", "blz", charset='utf8')
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    try:
        cursor.execute(dis_addr_sql)
        rs = cursor.fetchall()
        print("fetch data records: %s " % len(rs))
        time.sleep(2)
        s = 0
        for r in rs:
            coin_name = r[0]
            addr = r[1]
            maxId = r[2]
            cursor.execute(cur_data_sql % maxId)
            one = cursor.fetchone()
            newBlc = one[0]
            tm = one[1]
            weekDelta = one[2]

            if weekDelta:
                print("skipped id %s " % maxId)
                continue
            d = tm - timedelta(days=7)
            cursor.execute(old_blc_dql % (d, coin_name, addr, maxId))
            oldRst = cursor.fetchone()
            if oldRst:
                oldBlc = oldRst[0]
                result = '%f' % (newBlc - oldBlc)
            else:
                result = 'New'
            cursor.execute(update_sql % (result, maxId))
            if s % 100 == 0:
                db.commit()
            s = s + 1
            f = "{0:<6}\tid:{1:<10}\taddr:{2:^10}\tcoin:{3:^10}\tresult:{4:>10}"
            print(f.format(s, maxId, addr, coin_name, result))

    except Exception, e:
        print(e)
        db.rollback()
    db.close()


if __name__ == '__main__':
    exec_hold_exchange()
