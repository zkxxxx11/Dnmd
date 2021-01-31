import datetime


def current_str_time(format='%Y-%m-%d %H:%M:%S'):
    current_time = datetime.datetime.now().strftime(format)
    return current_time
