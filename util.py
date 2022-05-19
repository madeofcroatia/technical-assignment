import datetime
from checkers import emsg, format, existence
import smtplib
import ssl


def send_notification(host_email, host_password, receiver_email, notification):
    port = 445
    context = ssl.create_default_context()
    print(context)
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        print(server)
        server.login(host_email, host_password)
        print(1)
        server.sendmail(host_email, receiver_email, notification)
        print(2)


def to_timestamp(date, time):
    day, month, year = [int(i) for i in date.split('/')]
    hour, minute = [int(i) for i in time.split(':')]
    dt = datetime.datetime(day=day, month=month, year=year, hour=hour, minute=minute)

    unix_time = datetime.datetime.timestamp(dt)

    return unix_time


class InputHandler:
    def __init__(self, rooms, users):
        self.rooms = rooms
        self.users = users

    def reservation_input(self):
        room = self.room_input_handler()
        utime1 = 0
        utime2 = 0
        message = ""
        while utime1 >= utime2:
            print(message)
            message = "The start of your reservation cannot come AFTER the end of it!"
            date1 = InputHandler.datetime_input_handler('date', 'Enter the date on which you would want '
                                                                'to start the reservation: ')
            time1 = InputHandler.datetime_input_handler('time', 'Enter the time when you would want to '
                                                                'start the reservation: ')
            date2 = InputHandler.datetime_input_handler('date', 'Enter the date on which you would want '
                                                                'to end the reservation: ')
            time2 = InputHandler.datetime_input_handler('time', 'Enter the time when you would want to '
                                                                'end the reservation: ')
            utime1 = to_timestamp(date1, time1)
            utime2 = to_timestamp(date2, time2)

        return int(room), utime1, utime2

    @staticmethod
    def registration_input():
        name = InputHandler.format_only('user', 'Enter your full name: ')
        email_address = InputHandler.format_only('email', 'Enter your email address: ')
        phone = InputHandler.format_only('phone', 'Enter your phone number: ')
        return name, email_address, phone

    @staticmethod
    def yes_no_input():
        msg = "The room is available! Would you like to book it?(y/n) "
        while True:
            yes_no = input(msg)
            if yes_no in ('y', 'n'):
                return yes_no
            msg = "You can only enter 'y' or 'n', 'y' meaning 'yes', and 'n' meaning no! "

    def room_input_handler(self):
        msg = "Please, enter the room number: "
        while True:
            room = input(msg)
            if format.check_room_format(room):
                if existence.room_exists(self.rooms, int(room)):
                    break
                msg = emsg.room_exist_emsg.format(room)
            else:
                msg = emsg.room_format_emsg
        return room

    @staticmethod
    def datetime_input_handler(kind, first_msg):
        msg = first_msg
        while True:
            info = input(msg)
            if eval(f"format.check_{kind}_format(info)"):
                if eval(f"existence.{kind}_exists(info)"):
                    break
                msg = eval(f"emsg.{kind}_exist_emsg").format(info)
            else:
                msg = eval(f"emsg.{kind}_format_emsg")
        return info

    @staticmethod
    def format_only(kind, start_msg):
        msg = start_msg
        while True:
            info = input(msg)
            if eval(f"format.check_{kind}_format(info)"):
                break
            else:
                msg = eval(f"emsg.{kind}_format_emsg")
        return info
