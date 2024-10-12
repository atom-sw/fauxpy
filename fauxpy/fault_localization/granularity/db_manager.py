import sqlite3
from pathlib import Path
from typing import List, Tuple


class FunctionLevelDbManager:
    _File_name = "common.db"
    _Function_info_table = "FunctionInformation"

    def __init__(self, report_directory_path: Path):
        db_file_path = report_directory_path / self._File_name
        db_file_path_str = str(db_file_path.absolute().resolve())
        self._connection = sqlite3.connect(db_file_path_str)
        commands = self._get_database_schema()
        for command in commands:
            self._connection.executescript(command)

    def _get_database_schema(self):
        function_info_table_create_command = (
            f"CREATE TABLE {self._Function_info_table} "
            f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
            f"FilePath	TEXT NOT NULL, "
            f"FunctionName	TEXT NOT NULL, "
            f"LineStart INTEGER NOT NULL, "
            f"LineEnd INTEGER NOT NULL);"
        )

        function_info_table_index_command = f"CREATE INDEX Index_OnThree ON {self._Function_info_table} (FilePath, LineStart, LineEnd);"

        commands = [
            function_info_table_create_command,
            function_info_table_index_command,
        ]

        return commands

    def end(self):
        self._connection.close()

    def select_function_ranges(
        self, file_path: str, line_number: int
    ) -> List[Tuple[str, int, int]]:
        cur = self._connection.cursor()

        cur.execute(
            f"SELECT FunctionName, LineStart, LineEnd FROM {self._Function_info_table} "
            f"WHERE FilePath = ? and LineStart <= ? and LineEnd >= ?",
            (file_path, line_number, line_number),
        )

        var = cur.fetchall()

        return var

    def insert_function_information(
        self, file_path: str, function_name: str, line_start: int, line_end: int
    ):
        cur = self._connection.cursor()

        cur.execute(
            f"INSERT INTO {self._Function_info_table} VALUES (NULL, ?, ?, ?, ?)",
            (file_path, function_name, line_start, line_end),
        )
        self._connection.commit()

    def is_file_path_covered(self, file_path: str) -> bool:
        cur = self._connection.cursor()

        cur.execute(
            f"SELECT COUNT(*) FROM {self._Function_info_table} WHERE FilePath = ?",
            (file_path,),
        )

        cnt = cur.fetchone()

        return cnt[0] > 0
