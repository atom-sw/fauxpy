import sqlite3
from pathlib import Path


class StDbManager:
    _File_name = "fauxpy.db"
    _Traceback_score_table = "TracebackScore"

    def __init__(self, report_directory_path: Path):
        db_file_path = report_directory_path / self._File_name
        db_file_path_str = str(db_file_path.absolute().resolve())
        self._connection = sqlite3.connect(db_file_path_str)
        command_list = self._get_database_schema()
        for command in command_list:
            self._connection.executescript(command)

    def _get_database_schema(self):
        traceback_score_table_create_command = (
            f"CREATE TABLE {self._Traceback_score_table} "
            f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
            f"TestName TEXT NOT NULL, "
            f"Function TEXT NOT NULL,"
            f"Score REAL NOT NULL);"
        )

        traceback_score_table_index_command = f"CREATE INDEX Index_FunctionName ON {self._Traceback_score_table} (Function);"

        command_list = [
            traceback_score_table_create_command,
            traceback_score_table_index_command,
        ]

        return command_list

    def end(self):
        self._connection.close()

    def insert_traceback_scores(self, test_name, test_scores):
        for testScore in test_scores:
            cur = self._connection.cursor()
            cur.execute(
                f"INSERT INTO {self._Traceback_score_table} VALUES (NULL, ?, ?, ?)",
                (test_name, testScore[0], testScore[1]),
            )

        self._connection.commit()

    def select_all_ranked_functions(self):
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT Function, MAX(Score) FROM {self._Traceback_score_table} "
            f"GROUP BY Function "
            f"ORDER BY Score DESC"
        )

        return cur.fetchall()

    def select_top_n_ranked_functions(self, top_n):
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT Function, MAX(Score) FROM {self._Traceback_score_table} "
            f"GROUP BY Function "
            f"ORDER BY Score DESC "
            f"LIMIT ?",
            (top_n,),
        )

        return cur.fetchall()
