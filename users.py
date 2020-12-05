from memo import Memo

class User:

    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.memo_ids = []

    def add_memo(self, new_info, null_time=None):
        print(f"New information(user:{self.name}) added at {null_time}")
        self.list_of_info.append(new_info)
        self.info_amount += 1


    def get_info(self, info_id):
        return self.list_of_info[info_id]


    def delete_info(self, info_id):
        try:
            self.list_of_info.pop(info_id)
            print("Info sucsessfuly deleted")
        except:
            print("Deletion failed")
