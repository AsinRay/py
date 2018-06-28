import MySQLdb

def exec_sql(sql):
    # Open database connection
    db = MySQLdb.connect("47.98.56.206", "root", "123456", "immsg",charset='utf8')
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()


a = "I'm %s. I'm %d year old" % ('Vamei', 99)
print(a)

sql = """ INSERT INTO `all_msg` (`content`, `duration`, `type`, `ctime`) 
VALUES ("asdf", '20', 'text', '2018-05-24 14:18:52')"""
exec_sql(sql)
