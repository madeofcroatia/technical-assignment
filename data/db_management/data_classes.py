from .dbms import DataBase


class Rooms(DataBase):
    def __init__(self, db_file, names=('Room 1', 'Room 2', 'Room 3', 'Room 4', 'Room 5')):
        DataBase.__init__(self, db_file)
        self.size = len(names)
        self.create_table('rooms', [('room_id', 'integer', 'PRIMARY KEY'),
                                    ('name', 'text', 'NOT NULL')])

        if self.get_new_id('rooms', 'room_id') == 1:
            for name in names:
                self.create_room(name)

    def create_room(self, name):
        new_room_id = self.get_new_id('rooms', 'room_id')
        self.add_entry('rooms', (new_room_id, name))

    def get_room(self, room_id):
        room = self.get_entry_by_id('rooms', 'room_id', room_id)
        return room


class Users(DataBase):
    def __init__(self, db_file, users=tuple()):
        DataBase.__init__(self, db_file)
        self.create_table('users', [('user_id', 'integer', 'PRIMARY KEY'),
                                    ('full_name', 'text', 'NOT NULL'),
                                    ('email', 'text', 'NOT NULL'),
                                    ('phone_number', 'text', 'NOT NULL')])

        for full_name, email, phone_number in users:
            self.add_user(full_name, email, phone_number)

    def add_user(self, full_name, email, phone_number):
        new_user_id = self.get_new_id('users', 'user_id')
        self.add_entry('users', (new_user_id, full_name, email, phone_number))

    def get_user(self, name):
        cursor = self.connection.cursor()
        sql_query = f"SELECT * FROM users WHERE full_name = '{name}';"
        cursor.execute(sql_query)
        user = cursor.fetchone()

        return user


class Reservations(DataBase):
    def __init__(self, db_file):
        DataBase.__init__(self, db_file)
        columns = [('reservation_id', 'integer', 'PRIMARY KEY'),
                   ('start_unixepoch', 'integer', 'NOT NULL'),
                   ('end_unixepoch', 'integer', 'NOT NULL'),
                   ('room_id', 'integer', 'NOT NULL'),
                   ('user_id', 'integer', 'NOT NULL')]

        rooms_foreign_key = ('rooms', 'room_id', 'room_id', 'CASCADE', 'CASCADE')
        users_foreign_key = ('users', 'user_id', 'user_id', 'CASCADE', 'CASCADE')

        self.create_table('reservations', columns, foreign_keys=[rooms_foreign_key,
                                                                 users_foreign_key])

    def make_reservation(self, start_unixepoch, end_unixepoch, room_id, user_id):
        new_key = self.get_new_id('reservations', 'reservation_id')

        self.add_entry('reservations', (new_key, start_unixepoch, end_unixepoch, room_id, user_id))

    def get_reservation_in_timeframe(self, reservation_start, reservation_end, room_id):
        cursor = self.connection.cursor()

        sql_query = f"SELECT room_id, start_unixepoch, end_unixepoch\n" \
                    f"FROM reservations\n" \
                    f"WHERE room_id = {room_id}\n" \
                    f"AND((start_unixepoch BETWEEN {reservation_start} and {reservation_end}) OR\n" \
                    f"(end_unixepoch BETWEEN {reservation_start} and {reservation_end})) OR \n" \
                    f"((start_unixepoch <= {reservation_start}) AND\n" \
                    f"(end_unixepoch >= {reservation_end}));"

        cursor.execute(sql_query)
        reservation = cursor.fetchone()
        return reservation
