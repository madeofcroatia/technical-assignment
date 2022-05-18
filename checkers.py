import datetime
from data_classes import Rooms


wrong_date = "Your date was entered in the incorrect format! You MUST use DD/MM/YYYY format."
wrong_time = "Your time was entered in the incorrect format! You MUST use HH:MM format."
non_existent_date = "The date {} does not exist!"
non_existent_time = "The time {} does not exist!"
non_existent_room = "The room {} does not exist!"
rooms = Rooms('db.sqlite3')


def check_input(parser):
    error_list = []

    try:
        c = rooms.connection.execute(f"SELECT room_id FROM rooms WHERE room_id = {parser.room};")
        assert c.fetchone() is not None
    except AssertionError:
        error_list.append(non_existent_room.format(parser.room))

    try:
        check_date_format(parser.date1)
        check_date_format(parser.date2)
    except (ValueError, AssertionError):
        error_list.append(wrong_date)

    try:
        check_time_format(parser.time1)
        check_time_format(parser.time2)
    except (ValueError, AssertionError):
        error_list.append(wrong_time)

    try:
        check_date(parser.date1)
    except ValueError:
        error_list.append(non_existent_date.format(parser.date1))

    try:
        check_date(parser.date2)
    except ValueError:
        error_list.append(non_existent_date.format(parser.date2))

    try:
        check_time(parser.time1)
    except ValueError:
        error_list.append(non_existent_time.format(parser.time1))

    try:
        check_time(parser.time2)
    except ValueError:
        error_list.append(non_existent_time.format(parser.time2))

    return error_list


def check_date_format(candidate):
    day, month, year = candidate.split('/')
    assert len(day) == len(month) == 2 and len(year) == 4
    assert day.isdecimal() and month.isdecimal() and year.isdecimal()


def check_date(candidate):
    day, month, year = [int(i) for i in candidate.split('/')]
    datetime.date(day=day, month=month, year=year)


def check_time_format(candidate):
    minutes, hours = candidate.split(':')
    assert len(minutes) == len(hours) == 2
    assert minutes.isdecimal() and hours.isdecimal()


def check_time(candidate):
    minute, hour = candidate.split(':')
    datetime.time(minute=minute, hour=hour)

def is_valid_name(candidate):
    return candidate.isalpha()


def is_valid_number(candidate):
    return len(candidate) == 9 and candidate.isdecimal()


def is_valid_address(candidate):
    if candidate.count('@') == 1:
        left, right = candidate.split('@')
        return len(left) != 0 and len(right) != 0
    return False

