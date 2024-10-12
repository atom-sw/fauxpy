import sqlite3
from pathlib import Path


class CollectMbflDBManager:
    _File_name = "fauxpy.db"
    _Test_case_table = "TestCase"

    def __init__(self, report_directory_path: Path):
        db_file_path = report_directory_path / self._File_name
        db_file_path_str = str(db_file_path.absolute().resolve())
        self._connection = sqlite3.connect(db_file_path_str)
        command_list = self._get_database_schema()
        for command in command_list:
            self._connection.executescript(command)

    def _get_database_schema(self):
        # TODO: Add indices.
        test_case_table_create_command = (
            f"CREATE TABLE {self._Test_case_table} "
            f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
            f"TestName TEXT NOT NULL UNIQUE, "
            f"Type TEXT NOT NULL, "
            f"ShortTraceback TEXT NOT NULL,"
            f"Timeout INTEGER NOT NULL);"
        )

        command_list = [
            test_case_table_create_command,
        ]

        return command_list

    def end(self):
        self._connection.close()

    def insert_test_case(
        self, test_name: str, test_type: str, short_traceback: str, timeout_stat: int
    ):
        cur = self._connection.cursor()
        cur.execute(
            f"INSERT INTO {self._Test_case_table} VALUES (NULL, ?, ?, ?, ?)",
            (test_name, test_type, short_traceback, timeout_stat),
        )

        self._connection.commit()

    def select_all_test_cases(self):
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT TestName, Type, ShortTraceBack, Timeout FROM {self._Test_case_table}"
        )
        rows = cur.fetchall()

        return rows
