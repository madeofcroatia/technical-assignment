import sqlite3


class DataBase:
    """
    The DataBase class for our SQL Database
    """
    def __init__(self, db_file, foreign_keys_allowed=True):
        self.db_file = db_file
        self.connection = self.make_connection()

        if foreign_keys_allowed:
            self.connection.execute("PRAGMA foreign_keys = 1;")
            self.connection.commit()

    def make_connection(self):
        try:
            connection = sqlite3.connect(self.db_file)
        except sqlite3.Error as e:
            raise ConnectionError(f"Connection could not be established at '{self.db_file}'\n" +
                                  f"{e} Error was raised.")
        else:
            return connection

    @staticmethod
    def sql_columns(columns):
        def to_sql(column):
            if len(column) == 3:
                col_name, col_type, col_spec = column
                return f"    {col_name} {col_type} {col_spec}"
            else:
                col_name, col_type = column
                return f"    {col_name} {col_type}"

        sql_cols = ',\n'.join(to_sql(col) for col in columns)
        return sql_cols

    @staticmethod
    def sql_foreign_keys(foreign_keys):
        def sql_foreignkey(ref_table, ref_col, col, on_update='CASCADE', on_delete='CASCADE'):
            sql = f"    FOREIGN KEY ({col})\n" \
                  f"    REFERENCES {ref_table}({ref_col})\n" \
                  f"        ON UPDATE {on_update}\n" \
                  f"        ON DELETE {on_delete}"

            return sql

        keys = []

        for table, col1, col2, update, delete in foreign_keys:
            keys.append(sql_foreignkey(table, col1, col2, update, delete))

        return ",\n" + ",\n".join(keys)

    def create_table(self, table_name, columns, foreign_keys=tuple(), commit=True):
        cursor = self.connection.cursor()

        sql_start = f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
        sql_contents = DataBase.sql_columns(columns)
        sql_refs = DataBase.sql_foreign_keys(foreign_keys) if len(foreign_keys) > 0 else ""
        sql_end = "\n);"
        print(sql_start + sql_contents + sql_refs + sql_end)
        cursor.execute(sql_start + sql_contents + sql_refs + sql_end)
        if commit:
            self.connection.commit()

    def get_last_id(self, table_name):
        cursor = self.connection.cursor()
        sql = f"SELECT MAX(Id) FROM {table_name};"
        max_id = cursor.execute(sql).fetchone()

        return max_id[0]

    def add_entry(self, table_name, entry, commit=True):
        cursor = self.connection.cursor()

        values = ', '.join(f'"{val}"'if isinstance(val, str) else str(val) for val in entry)
        insert_command = f"INSERT INTO {table_name} VALUES({values})"

        cursor.execute(insert_command)
        if commit:
            self.connection.commit()
