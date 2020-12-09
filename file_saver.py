import datetime

def now_time_name(user_id):
    time_now = datetime.datetime.now()
    filename = str(user_id) + "_" + str(time_now.day) + "-" + str(time_now.month) + "-" + str(time_now.year) + "_" + str(time_now.hour) + "-" + str(time_now.minute) + "-" + str(time_now.second)
    return filename

def save_txt(user_id, text):
    filename = now_time_name(user_id)
    print(filename)
    path = fr"files/texts/{filename}.txt"
    file = open(path, "w")
    file.write(text)
    file.close()
    return path

def save_file(user_id, file):
    filename = now_time_name(user_id)
    print(filename)
    path = fr"files/texts/{filename}.???"

def save_image(user_id, image):
    filename = now_time_name(user_id)
    print(filename)
    path = fr"files/texts/{filename}.???"