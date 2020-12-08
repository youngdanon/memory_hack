from memo import Memo
from db_controller import DB
import datetime
import sqlite3

db = DB('./data/memos.db')

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
        db_line = [None, self.chat_id, new_memo.memo_type, new_memo.memo_name, new_memo.link, dt2str(new_memo.notify_time), new_memo.notify_count]
        db.add_row(db_line)
        print(f"New memo(user:{self.chat_id}) added at {null_time}")


    def get_memo(self, memo_id):
        raw_row = db.get_row(memo_id)
        recorded_memo = Memo(user_id=raw_row[1],
                            memo_type=raw_row[2],
                            memo_name=raw_row[3],
                            link=raw_row[4],
                            notify_time=str2dt(raw_row[5]),
                            notify_count=raw_row[6])
        return recorded_memo

    def get_memos_list(self):
        memos_list = []
        raw_data = db.get_rows_by_user_id(self.chat_id)
        for raw_row in raw_data:
            recorded_memo = Memo(user_id=raw_row[1],
                            memo_type=raw_row[2],
                            memo_name=raw_row[3],
                            link=raw_row[4],
                            notify_time=str2dt(raw_row[5]),
                            notify_count=raw_row[6])
            memos_list.append(recorded_memo)
        return memos_list


    def delete_memo(self, memo_id):
        try:
            db.delete_row(memo_id)
        except Exception as e:
            print("Deletion failed", e)
