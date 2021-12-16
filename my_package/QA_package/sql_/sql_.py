import MySQLdb

class db_setting():
    def __init__(self, host, user, password, table):
        db = MySQLdb.connect(host=host,
                             user=user,
                             password=password,
                             db=table,
                             charset='utf8')
        cursor = db.cursor()
        self.db = db
        self.cursor = cursor

    def db_select(self, sql):
        try:
            data_num = self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data_num, data
        except ValueError:
            raise ValueError("SQL(select) instruction have some error")

    def db_update(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return "Finish Update Work"
        except ValueError:
            raise ValueError("SQL(update) instruction have some error")

    def db_insert(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            raise ValueError("SQL(insert) instruction have some error")

    def db_delete(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            raise ValueError("SQL(delete) instruction have some error")

    def sql_shell(self, sql):
        try:
            self.cursor.execute(sql)
            print(self.cursor.execute(sql))
        except:
            raise ValueError("SQL(shell) instruction have some error")

