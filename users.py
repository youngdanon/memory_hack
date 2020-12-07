from memo import Memo
from db_controller import DB

import sqlite3

def dt2str(raw_dt):
    str_dt = str(raw_dt)[:-7]
    return str_dt

def str2dt(str_dt):
    new_dt = datetime.datetime.strptime(str_dt, '%Y-%m-%d %H:%M:%S')
    return new_dt

class User:

    def __init__(self, chat_id):
        self.chat_id = chat_id

    def add_memo(self, new_memo, null_time=None):
        memo_id = 0
        db_line = [memo_id, new_memo.memo_type, new_memo.link, new_memo.notify_time, new_memo.notify_count]
        
        print(f"New memo(user:{self.chat_id}) added at {null_time}")


    def get_memo(self, memo_id):
        return self.list_of_memo[memo_id]


    def delete_memo(self, memo_id):
        try:
            self.list_of_memo.pop(memo_id)
            print("memo sucsessfuly deleted")
        except:
            print("Deletion failed")
