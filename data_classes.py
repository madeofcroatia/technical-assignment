from dbms import DataBase


class Rooms(DataBase):
    def __init__(self, db_file, names):
        DataBase.__init__(self, db_file)
        self.size = len(names)
        self.create_table('rooms', [('room_id', 'integer', 'PRIMARY KEY'),
                                    ('name', 'text', 'NOT NULL')])

        for name in names:
            self.create_room(name)

    def create_room(self, name):
        key = self.get_last_id('rooms') + 1
        self.add_entry('rooms', (key, name))


class Users(DataBase):
    def __init__(self, db_file, users=tuple()):
        DataBase.__init__(self, db_file)
        self.create_table('users', [('user_id', 'integer', 'PRIMARY KEY'),
                                    ('full_name,', 'text', 'NOT NULL'),
                                    ('email', 'text', 'NOT NULL'),
                                    ('phone_number', 'text', 'NOT NULL')])

        for full_name, email, phone_number in users:
            self.add_user(full_name, email, phone_number)

    def add_user(self, full_name, email, phone_number):
        key = self.get_last_id('users') + 1
        self.add_entry('users', (key, full_name, email, phone_number))


class Reservations(DataBase):
    def __init__(self, db_file):
        DataBase.__init__(self, db_file)
        columns = [('reservation_id', 'integer', 'PRIMARY KEY'),
                   ('start_date', 'text', 'NOT NULL'),
                   ('end_date', 'text', 'NOT NULL'),
                   ('start_time', 'text', 'NOT NULL'),
                   ('end_time', 'text', 'NOT NULL'),
                   ('room_id', 'integer', 'NOT NULL'),
                   ('user_id', 'integer', 'NOT NULL')]

        rooms_foreign_key = ('rooms', 'room_id', 'room_id', 'CASCADE', 'CASCADE')
        users_foreign_key = ('users', 'user_id', 'user_id', 'CASCADE', 'CASCADE')

        self.create_table('reservations', columns, foreign_keys=[rooms_foreign_key,
                                                                 users_foreign_key])

    def make_reservation(self, start_date, end_date, start_time, end_time, room_id, user_id):
        self.add_entry('reservations', (start_date, end_date, start_time, end_time, room_id, user_id))
