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
        self.create_table('users', [('full_name', 'text', 'NOT NULL'),
                                    ('email', 'text', 'PRIMARY KEY')])

        for full_name, email in users:
            self.add_user(full_name, email)

    def add_user(self, full_name, email):
        self.add_entry('users', (full_name, email))

    def get_name(self, email):
        cursor = self.connection.cursor()
        sql_query = f"SELECT full_name FROM users WHERE email = '{email}';"
        cursor.execute(sql_query)

        full_name = cursor.fetchone()
        if isinstance(full_name, tuple):
            full_name = full_name[0]

        return full_name


class Reservations(DataBase):
    def __init__(self, db_file):
        DataBase.__init__(self, db_file)
        columns = [('reservation_id', 'integer', 'PRIMARY KEY'),
                   ('start_unixepoch', 'integer', 'NOT NULL'),
                   ('end_unixepoch', 'integer', 'NOT NULL'),
                   ('time_till_next', 'integer', 'NOT NULL'),
                   ('room_id', 'integer', 'NOT NULL'),
                   ('email', 'text', 'NOT NULL')]

        rooms_foreign_key = ('rooms', 'room_id', 'room_id', 'CASCADE', 'CASCADE')
        users_foreign_key = ('users', 'email', 'email', 'CASCADE', 'CASCADE')

        self.create_table('reservations', columns, foreign_keys=[rooms_foreign_key,
                                                                 users_foreign_key])

    def make_reservation(self, start_unixepoch, end_unixepoch, room_id, email):
        new_key = self.get_new_id('reservations', 'reservation_id')

        cursor = self.connection.cursor()
        left_reservation_query = f"SELECT reservation_id, MAX(end_unixepoch) FROM reservations " \
                                 f"WHERE room_id={room_id} AND end_unixepoch < {start_unixepoch}"
        right_reservation_query = f"SELECT MIN(start_unixepoch) FROM reservations " \
                                  f"WHERE room_id={room_id} AND start_unixepoch > {end_unixepoch}"
        cursor.execute(left_reservation_query)
        left_id, left_end_epoch = cursor.fetchone()
        cursor.execute(right_reservation_query)

        right_start_epoch = cursor.fetchone()
        if isinstance(right_start_epoch, tuple):
            right_start_epoch = right_start_epoch[0]

        if left_id is not None:
            new_time_left = start_unixepoch - left_end_epoch
            sql_update = f"UPDATE reservations SET time_till_next={new_time_left} " \
                         f"WHERE reservation_id={left_id};"
            cursor.execute(sql_update)
        if right_start_epoch is not None:
            time_till_next = right_start_epoch - end_unixepoch
        else:
            time_till_next = 100000000000

        self.add_entry('reservations', (new_key, start_unixepoch, end_unixepoch, time_till_next, room_id, email))

    def get_in_timeframe(self, reservation_start, reservation_end, room_id):
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

    def get_next(self, time_length, time_start, room_id):
        cursor = self.connection.cursor()

        sql_query = f"SELECT end_unixepoch FROM reservations " \
                    f"WHERE room_id={room_id} " \
                    f"AND time_till_next >= {time_length} " \
                    f"AND end_unixepoch > {time_start};"

        cursor.execute(sql_query)
        res = cursor.fetchone()
        if isinstance(res, tuple):
            res = res[0]
        return res
