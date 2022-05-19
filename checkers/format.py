import re


def check_date_format(candidate):
    try:
        day, month, year = candidate.split('/')
    except ValueError:
        return False
    else:
        return len(day) == len(month) == 2 and len(year) == 4 and \
               day.isdecimal() and month.isdecimal() and year.isdecimal()


def check_time_format(candidate):
    try:
        hour, minute = candidate.split(':')
    except ValueError:
        return False
    else:
        return len(hour) == len(minute) == 2 and \
               hour.isdecimal() and minute.isdecimal()


def check_user_format(candidate):
    names = candidate.split()
    return all(name.isalpha() for name in names)


def check_phone_format(candidate):
    phone_number = ''.join(candidate.split())
    return phone_number.isdecimal() and len(phone_number) == 9


def check_email_format(candidate):
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(email_regex, candidate)


def check_room_format(candidate):
    room_number = ''.join(candidate.split())
    if room_number.isdecimal():
        return room_number[0] != "0"
