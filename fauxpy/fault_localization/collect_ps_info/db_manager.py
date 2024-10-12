import sqlite3
from pathlib import Path


class CollectPsInfoDbManager:
    _File_name = "fauxpy.db"
    _Test_case_table = "TestCase"
    # _Covered_lines_for_test_table = "CoveredLinesForTest"
    # _Empty_test_case_table = "EmptyTest"
    # coveredLinesWithTestTypesView = "CoveredLinesWithTestTypes"
    _Test_predicate_sequence_table = "TestPredicateSequence"
    _Test_seen_exception_sequence_table = "TestSeenExceptionSequence"

    def __init__(self, report_directory_path: Path):
        db_file_path = report_directory_path / self._File_name
        db_file_path_str = str(db_file_path.absolute().resolve())
        self._connection = sqlite3.connect(db_file_path_str)
        commands = self._get_database_schema()
        for command in commands:
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

        # executed_line_for_test_table_create_command = (
        #     f"CREATE TABLE {self._Covered_lines_for_test_table} "
        #     f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
        #     f"TestName TEXT NOT NULL, "
        #     f"FilePath TEXT NOT NULL, "
        #     f"LineNumber INTEGER NOT NULL);"
        # )

        # empty_test_table_create_command = (
        #     f"CREATE TABLE {self._Empty_test_case_table} "
        #     f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
        #     f"TestName TEXT NOT NULL UNIQUE);"
        # )

        test_predicate_sequence_table_create_command = (
            f"CREATE TABLE {self._Test_predicate_sequence_table} "
            f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
            f"TestName TEXT NOT NULL UNIQUE, "
            f"PredicateSequence TEXT NOT NULL);"
        )

        test_seen_exceptions_sequence_table_create_command = (
            f"CREATE TABLE {self._Test_seen_exception_sequence_table} "
            f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
            f"TestName TEXT NOT NULL UNIQUE, "
            f"SeenExceptionSequence TEXT NOT NULL);"
        )

        # viewCreateCommand = f"CREATE VIEW {_Names.coveredLinesWithTestTypesView} AS " \
        #                     f"SELECT {_Names.coveredLinesForTestTable}.Rowid, " \
        #                     f"{_Names.coveredLinesForTestTable}.TestName, " \
        #                     f"{_Names.coveredLinesForTestTable}.FilePath, " \
        #                     f"{_Names.coveredLinesForTestTable}.LineNumber, " \
        #                     f"{_Names.testCaseTable}.Type " \
        #                     f"FROM {_Names.coveredLinesForTestTable} " \
        #                     f"INNER JOIN {_Names.testCaseTable} ON " \
        #                     f"{_Names.coveredLinesForTestTable}.TestName = {_Names.testCaseTable}.TestName"

        command_list = [
            test_case_table_create_command,
            # executed_line_for_test_table_create_command,
            # empty_test_table_create_command,
            test_predicate_sequence_table_create_command,
            # viewCreateCommand,
            test_seen_exceptions_sequence_table_create_command,
        ]

        return command_list

    def end(self):
        self._connection.close()

    # def insert_empty_test(self, test_name):
    #     cur = self._connection.cursor()
    #     cur.execute(
    #         f"INSERT INTO {self._Empty_test_case_table} VALUES (NULL, ?)", (test_name,)
    #     )
    #
    #     self._connection.commit()

    # def insert_covered_line_for_test(self, test_name: str, file_path: str, line_number: int):
    #     cur = self._connection.cursor()
    #     cur.execute(
    #         f"INSERT INTO {self._Covered_lines_for_test_table} VALUES (NULL, ?, ?, ?)",
    #         (test_name, file_path, line_number),
    #     )
    #
    #     self._connection.commit()

    # def insert_test_case(self, test_name: str, test_type: str, short_traceback: str, timeout_stat: int):
    #     cur = self._connection.cursor()
    #     cur.execute(
    #         f"INSERT INTO {self._Test_case_table} VALUES (NULL, ?, ?, ?, ?)",
    #         (test_name, test_type, short_traceback, timeout_stat),
    #     )
    #
    #     self._connection.commit()

    def select_all_test_cases(self):
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT TestName, Type, ShortTraceBack, Timeout FROM {self._Test_case_table}"
        )
        rows = cur.fetchall()

        return rows

    # def selectAllCoveredLinesForTest():
    #     global _Con
    #
    #     cur = _Con.cursor()
    #     cur.execute(f"SELECT TestName, FilePath, LineNumber FROM {_Names.coveredLinesForTestTable}")
    #     rows = cur.fetchall()
    #
    #     return rows

    def insert_predicate_sequence(self, test_name: str, predicate_sequence: str):
        cur = self._connection.cursor()
        cur.execute(
            f"INSERT INTO {self._Test_predicate_sequence_table} VALUES (NULL, ?, ?)",
            (test_name, predicate_sequence),
        )

        self._connection.commit()

    def select_all_predicate_sequences(self):
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT TestName, PredicateSequence FROM {self._Test_predicate_sequence_table}"
        )
        rows = cur.fetchall()

        return rows

    # def insert_seen_exception_sequence(self, test_name: str, seen_exceptions_sequence: str):
    #     cur = self._connection.cursor()
    #     cur.execute(
    #         f"INSERT INTO {self._Test_seen_exception_sequence_table} VALUES (NULL, ?, ?)",
    #         (test_name, seen_exceptions_sequence),
    #     )
    #
    #     self._connection.commit()

    def select_all_seen_exceptions(self):
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT TestName, SeenExceptionSequence FROM {self._Test_seen_exception_sequence_table}"
        )
        rows = cur.fetchall()

        return rows
