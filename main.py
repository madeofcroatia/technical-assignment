import config
from checkers import existence
from messages import responses
import util
from data.db_management.data_classes import Rooms, Users, Reservations


class ReservationsManager:
    def __init__(self):
        self.rooms = Rooms(config.database)
        self.users = Users(config.database)
        self.reservations = Reservations(config.database)
        self.input = util.InputHandler(self.rooms, self.users)
        self.app_loop()

    def app_loop(self):
        """
        The application loop for our Reservations Manager cmd app!
        Here, all the app logic happens, and it keeps running until
        the KeyboardInterrupt is used
        """
        while True:
            # Get the room, and datetime info in the form
            # of unix epoch time from the user
            room, ut1, ut2 = self.input.reservation_input()
            # Check if the room is available in the given timeframe
            if self.is_available(room, ut1, ut2):
                # Ask the user if they would want to book the room for
                # the given timeframe
                if self.input.yes_no_input() == 'y':
                    # Get the user info
                    name, email = self.register()
                    # Make a reservation of the requested room
                    # in the requested timeframe
                    self.make_reservation(ut1, ut2, room, email)
                    # Send email confirmation to the user that has just
                    # reserved the room
                    self.send_email(name, email, room, ut1, ut2,
                                    debug=config.debug)
            # If the room is unavailable, return the earliest time after
            # ut1 on which the room could be booked for the same duration
            else:
                # Get the next available time new_ut1 such that there are
                # no reservations for the room of interest between
                # new_ut1 and new_ut1 + ut2 - ut1, and new_ut1 > ut1
                new_ut1 = self.reservations.get_next(ut2 - ut1, ut1, room)
                # new_ut1 will be None if the next timeframe cannot be found
                if new_ut1 is None:
                    # No fitting timeframe has been found, meaning that
                    # the hardcoded time limit, which is 14:46:40 11/16/5138,
                    # has been reached
                    print(responses.room_always_busy)
                else:
                    # The next available timeframe has been found
                    new_ut1 += 1
                    new_ut2 = new_ut1 + ut2 - ut1
                    new_date = util.to_date(new_ut1)
                    new_time = util.to_time(new_ut1)
                    response = responses.room_busy.format(new_date, new_time)
                    # Ask the user if they would like to register for that
                    # timeframe
                    if self.input.yes_no_input(response) == 'y':
                        # If the user says yes, do the registration code
                        name, email = self.register()
                        self.make_reservation(new_ut1, new_ut2, room, email)
                        self.send_email(name, email, room, ut1, ut2,
                                        debug=config.debug)

    def is_available(self, room, ut1, ut2):
        """
        Find out if the room is available in the given timeframe

        Inputs:
            room (integer) --- the number of the room,
            ut1 (integer) --- the starting time, in unix epochs, for
                              the timeframe,
            ut2 (integer) --- the ending time, in unix epochs, for
                              the timeframe.
        Returns:
            True if and only if there is no reservation of the given room
            in the given timeframe. Otherwise, False.
        """
        res = self.reservations.get_in_timeframe(ut1, ut2, room)
        # print(res)
        return res is None

    def register(self):
        """
        Registration handler for our app
        This handles all the registration logic
        """
        # The primary key of the 'Users' table is email, so it is entered first
        email = self.input.email_input()
        # Check if the user with this email already exists
        if existence.user_exists(self.users, email):
            # If the user exists, get their full name from the 'Users' table
            name = self.users.get_name(email)
            print(f"Hello again {name}!")
        else:
            # If the user does not exist,
            name = self.input.name_input()
            self.users.add_user(name, email)
        return name, email

    def make_reservation(self, ut1, ut2, room, email):
        self.reservations.make_reservation(ut1, ut2, room, email)
        print(responses.res_success)

    @staticmethod
    def send_email(name, email, room, ut1, ut2, debug=False):
        if not debug:
            message = util.format_email(name, room, ut1, ut2)
            util.send_notification(config.email, config.password,
                                   email, message)

        print(responses.email_sent)



if __name__ == "__main__":
    ReservationsManager()
