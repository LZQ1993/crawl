import pymysql

class MysqlDao(object):
    def __init__(self):
        try:
            self.conn = pymysql.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                passwd='root',
                db='patent',
                charset='utf8'
            )
        except Exception as e:
            print(e)
        else:
            self.cur = self.conn.cursor()

    def create_table(self):
        sql = 'create table patent(id int, name varchar(10),age int)'
        res = self.cur.execute(sql)

    def close(self):
        self.cur.close()
        self.conn.close()

    def add(self,sql):  # 增
        res = self.cur.execute(sql)
        if res:
            self.conn.commit()
        else:
            self.conn.rollback()