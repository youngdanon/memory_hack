import sqlite3

class DB:
    memos = "memos"
    def __init__(self, path):
        self.path = path

    
    def create_table(self):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS memos(Id INTEGER PRIMARY KEY AUTOINCREMENT, '
                                                    'User_id,'
                                                    'Type, '
                                                    'Memo_name, '
                                                    'Link, '
                                                    'Notify_time, '
                                                    'Notify_count) ')
        con.commit()
        cur.close()
        con.close()


    def add_row(self, row):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        cur.execute('INSERT INTO memos VALUES(?, ?, ?, ?, ?, ?, ?)', row)
        con.commit()
        cur.close()
        con.close()


    def get_row(self, row_id):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        cur.execute("""SELECT * FROM memos WHERE id = ?""", (row_id,))
        record = cur.fetchone()
        cur.close()
        con.close()
        return record

    def get_rows_by_user_id(self, user_id):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        cur.execute("""SELECT * FROM memos WHERE User_id = ?""", (user_id,))
        record = cur.fetchall()
        cur.close()
        con.close()
        return record

    def delete_row(self, row_id):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        # print(fr"DELETE FROM memos WHERE Id = {row_id}")
        # cur.execute(fr"DELETE FROM memos WHERE Id = {row_id}")
        cur.execute("DELETE FROM memos WHERE Id=?", (row_id,))
        con.commit()
        cur.close()
        con.close()


    def check_time(self, current_time):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        con.commit()
        cur.close()
        con.close()
