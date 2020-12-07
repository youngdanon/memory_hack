import sqlite3

class DB:
    def __init__(self, path):
        self.path = path

    
    def create_table(self):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS memos(Id INTEGER PRIMARY KEY AUTOINCREMENT, '
                                                    'User_id,'
                                                    'Type, '
                                                    'Link,'
                                                    'Notify_time, '
                                                    'Notify_count) ')
        con.commit()
        cur.close()
        con.close()


    def get_new_id(self):
        pass

    def add_row(self, row):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        cur.execute('INSERT INTO memos VALUES(?, ?, ?, ?, ?, ?)', row)
        con.commit()
        cur.close()
        con.close()

    def get_row(self, row_id):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        con.commit()
        cur.close()
        con.close()


    def delete_row(self, row_id):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        con.commit()
        cur.close()
        con.close()


    def check_time(self, current_time):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        con.commit()
        cur.close()
        con.close()
