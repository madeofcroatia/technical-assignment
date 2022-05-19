import checkers.existence
import config
import datetime
from util import InputHandler, send_notification
from data.db_management.data_classes import Rooms, Users, Reservations


class ReservationsManager:
    def __init__(self):
        self.rooms = Rooms(config.database)
        self.users = Users(config.database)
        self.reservations = Reservations(config.database)
        self.input = InputHandler(self.rooms, self.users)
        self.app_loop()

    def app_loop(self):
        while True:
            room_number, utime1, utime2 = self.input.reservation_input()
            if self.is_available(room_number, utime1, utime2):
                if self.input.yes_no_input() == 'y':
                    name, email_address, phone_number = self.input.registration_input()

                    if not checkers.existence.user_exists(self.users, name):
                        self.users.add_user(name, email_address, phone_number)

                    user_id = self.users.get_new_id('users', 'user_id') - 1
                    self.reservations.make_reservation(utime1, utime2, room_number, user_id)

                    print("Reservation was successful! Sending email confirmation...")

                    message = ReservationsManager.format_notification(name, room_number, utime1, utime2)
                    send_notification(config.email, config.password, email_address, message)
                    print("Email confirmation was sent! If you are done, press Ctrl+C on your keyboard "
                          "and if you would like to check availability for another room or make another"
                          " reservation, stay with us!")
            else:
                reservations = self.reservations.get_reservations_in_timeframe(utime1, utime2, room_number)
                res_string_format = []
                for _, start_time, end_time, user_id in reservations:
                    _, _, name, _ = self.users.get_entry_by_id("users", user_id)
                    res_strng = f"{name} from {datetime.datetime.fromtimestamp(start_time)} till"
                                f" {datetime.datetime.fromtimestamp(start_time)}"
                    res_string_format.append(res_strng)


                print("Sorry, this room is unavailable in the given timeframe!"
                      f" It is taken by \n{',\n'.join(res_string_format)}.\n You can register another room now, or"
                      " if you are done press Ctrl+C on your keyboard!")

    def is_available(self, room_number, start_utime, end_utime):
        reservation = self.reservations.get_reservation_in_timeframe(start_utime, end_utime, room_number)
        # print(reservation)
        return reservation is None

    @staticmethod
    def format_notification(name, room_number, utime1, utime2):
        subject = "Subject: Reservation Confirmation\n"
        message = f"Hi {name},\n\nYour reservation for room number {room_number} was successful!\n\n" \
                  f"It starts on {datetime.datetime.fromtimestamp(utime1)} and lasts until " \
                  f"{datetime.datetime.fromtimestamp(utime2)}!\n\n" \
                  f"Best regards,\n\n" \
                  f"Reservations Manager"
        return subject + message

if __name__ == "__main__":
    ReservationsManager()
