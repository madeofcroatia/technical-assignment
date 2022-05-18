import argparse
import checkers
import datetime
import os
import sys

from data_classes import Rooms, Users, Reservations

rooms = Rooms('db.sqlite3')
users = Users('db.sqlite3')
reservations = Reservations('db.sqlite3')

parser = argparse.ArgumentParser()

parser.add_argument("room", help="the room number that you would like to know the availability for",
                    type=int)
parser.add_argument("date1", help="the start date of the timeframe you are interested in")
parser.add_argument("time1", help="the start time of the timeframe you are interested in (starting "
                                  "on 'date1' provided)")
parser.add_argument("date2", help="the end date of the timeframe you are interested in (MUST be on "
                                  "or after the date provided in 'date1' argument")
parser.add_argument("time2", help="the end time of the timeframe in which you are interested in the"
                                  " room (MUST be after 'time1' if date1=date2")

parser.parse_args()

error_messages = checkers.check_input(parser)

if len(error_messages) > 0:
    print('\n'.join(error_messages))
    sys.exit()


def to_timestamp(date, time):
    day, month, year = [int(i) for i in date.split('/')]
    hour, minute = [int(i) for i in time.split(':')]
    dt = datetime.datetime(day=day, month=month, year=year, hour=hour, minute=minute)

    unix_time = datetime.datetime.timestamp(dt)

    return unix_time


def is_room_available(room_id, unix_time1, unix_time2):

    reservation = reservations.get_reservation(unix_time1, unix_time2, room_id)

    return reservation is None


ut1 = to_timestamp(parser.date1, parser.time1)
ut2 = to_timestamp(parser.date2, parser.time2)

if not is_room_available(parser.room, ut1, ut2):
    print("This room is not available within the given timeframe!")
    sys.exit()

print("The room is available! To book it, please provide us with the following information:")
first_name = input("first name: ")
last_name = input("last name: ")
email = input("email: ")
phone_number = input("phone number: ")

print("/n/nProcessing the reservation...")
name = first_name + " " + last_name
users_cursor = users.connection.cursor()


if users_cursor.execute(f"SELECT * FROM users WHERE full_name = {name};").fetchone()[0] is None:
    users.add_user(name, email, phone_number)

user_id = users_cursor.execute(f"SELECT user_id FROM users WHERE full_name = {name};").fetchone()[0]

reservations.make_reservation(ut1, ut2, room_id=parser.room, user_id=user_id)

res_id = reservations.get_new_id("reservations", 'reservation_id') - 1
print(f"Your reservation was processed, and your reservation id is {res_id}")
print("Sending confirmation email...")

