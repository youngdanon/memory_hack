import datetime


def dt2str(raw_dt):
    str_dt = str(raw_dt)[:-7]
    return str_dt

def str2dt(str_dt):
    new_dt = datetime.datetime.strptime(str_dt, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(microseconds=1)
    return new_dt