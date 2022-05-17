import sqlite3


class DataBase:
    """
    The DataBase class for our SQL Database
    """
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = self.make_connection()

    def make_connection(self):
        try:
            connection = sqlite3.connect(self.db_file)
        except sqlite3.Error as e:
            raise ConnectionError(f"Connection could not be established at '{self.db_file}'\n" +
                                  f"{e} Error was raised.")
        else:
            return connection

    def create_table(self, table_name, columns):
        cursor = self.connection.cursor()

        sql_start = f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
        sql_end = "\n);"
        indent = "    "
        sql_contents = ""

        def to_sql(column):
            if len(column) == 3:
                col_name, col_type, col_spec = column
                return indent + f"{col_name} {col_type} {col_spec}"
            else:
                col_name, col_type = column
                return indent + f"{col_name} {col_type}"

        sql_contents += ',\n'.join(to_sql(col) for col in columns)
        cursor.execute(sql_start + sql_contents + sql_end)

    def add_entry(self, table_name, entry):
        cursor = self.connection.cursor()

        values = ', '.join(f'"{val}"'if isinstance(val, str) else str(val) for val in entry)
        insert_command = f"INSERT INTO {table_name} VALUES({values})"

        cursor.execute(insert_command)
