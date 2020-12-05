class Memo:
    def __init__(self, user_id=None, memo_type=None, link=None, notify_time=None, notify_count=None):
        self.user_id = user_id
        self.memo_type = memo_type
        self.link = link
        self.notify_time = notify_time
        self.notify_count = notify_count


    def show_memo(self):
        print("______________")
        print(self.user_id)
        print(self.memo_type)
        print(self.link)
        print(self.notify_time)
        print(self.notify_count)
        print("______________")