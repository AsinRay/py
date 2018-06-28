# ! /usr/bin/pyton
# -*- coding: utf-8 -*-
import MySQLdb
from datetime import datetime, timedelta
import numpy as np
np.set_printoptions(suppress=True)

dis_addr_sql = 'SELECT distinct (address) FROM  symbol_position WHERE `time` > curdate()'
max_id_sql = "SELECT MAX(id) AS   id FROM symbol_position WHERE address = '%s'"
cur_data_sql = "SELECT `quantity`, `time`, `week_delta`  FROM symbol_position WHERE id = '%s'"
old_blc_dql = "select quantity from symbol_position where time <= '%10s' and address = '%s' and id < %d order by id asc limit 1"
update_sql = "update symbol_position set week_delta = '%s' where id = %d"

def exec_hold_exchange():
    db = MySQLdb.connect("47.98.56.206", "root", "123456", "blz", charset='utf8')
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    try:
        cursor.execute(dis_addr_sql)
        rs = cursor.fetchall()
        for r in rs:
            addr = r[0]
            cursor.execute(max_id_sql % addr)
            max_id = cursor.fetchone()[0]
            cursor.execute(cur_data_sql % max_id)
            one = cursor.fetchone()
            new_blc = one[0]
            tm = one[1]
            week_delta = one[2]

            if week_delta:
                continue
            d = tm - timedelta(days=7)
            cursor.execute(old_blc_dql % (d, addr, max_id))
            old_rst = cursor.fetchone()
            if old_rst:
                old_blc = old_rst[0]
                result = '%f' % (new_blc - old_blc)
            else:
                result = 'New'
            print(result)
            cursor.execute(update_sql % (result, max_id))
            db.commit()
    except:
        print('err')
        db.rollback()
    db.close()


if __name__ == '__main__':
    exec_hold_exchange()
    print "fname=%s,lname=%s,age=%d,sex=%s,income=%d, dt=%.10s" % \
          ('ss', 'dd', 13, 'x', 3.22, datetime.now())
