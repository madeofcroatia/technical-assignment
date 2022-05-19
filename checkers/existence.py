import datetime


def room_exists(rooms, room_id):
    room = rooms.get_room(room_id)
    return room is not None


def user_exists(users, user_name):
    user = users.get_user(user_name)
    return user is not None


def date_exists(candidate):
    day, month, year = [int(i) for i in candidate.split('/')]
    try:
        datetime.date(day=day, month=month, year=year)
    except ValueError:
        return False
    else:
        return True


def time_exists(candidate):
    hour, minute = candidate.split(':')
    try:
        datetime.time(minute=int(minute), hour=int(hour))
    except ValueError:
        return False
    else:
        return True
