import sqlite3
from pathlib import Path
from typing import List, Tuple, Optional


class PsDbManager:
    _File_name = "fauxpy.db"
    _Test_case_table = "TestCase"
    _Covered_lines_for_test_table = "CoveredLinesForTest"
    _Empty_test_case_table = "EmptyTest"
    _Shadowed_covered_predicate_table = "ShadowedCoveredPredicate"
    _Covered_lines_with_test_types_view = "CoveredLinesWithTestTypes"
    _Candidate_predicate_table = "CandidatePredicate"
    _Seen_exception_table = "SeenException"
    _Predicate_sequence_table = "PredicateSequence"
    _Scored_entity_table = "ScoredEntity"
    _Test_time_table = "TestTime"
    _Timeout_predicate_instance_table = "TimeoutPredicateInstance"
    _Bad_execution_predicate_instance_table = "BadExecutionPredicateInstance"
    _Astor_assert_error_info_table = "AstorAssertErrorInfo"

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
            f"ExceptionFilePath TEXT NOT NULL, "
            f"ExceptionLineNumber INTEGER NOT NULL, "
            f"Target INTEGER NOT NULL);"
        )

        executed_line_for_test_table_create_command = (
            f"CREATE TABLE {self._Covered_lines_for_test_table} "
            f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
            f"TestName TEXT NOT NULL, "
            f"FilePath TEXT NOT NULL, "
            f"LineNumber INTEGER NOT NULL);"
        )

        empty_test_table_create_command = (
            f"CREATE TABLE {self._Empty_test_case_table} "
            f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
            f"TestName TEXT NOT NULL UNIQUE);"
        )

        shadowed_covered_predicate_table_create_command = (
            f"CREATE TABLE {self._Shadowed_covered_predicate_table} "
            f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
            f"TestName TEXT NOT NULL, "
            f"FilePath TEXT NOT NULL, "
            f"ExeLineNumber INTEGER NOT NULL, "
            f"LineStart INTEGER NOT NULL, "
            f"LineEnd INTEGER NOT NULL );"
        )

        candidate_predicate_table_create_command = (
            f"CREATE TABLE {self._Candidate_predicate_table} "
            f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
            f"FilePath TEXT NOT NULL, "
            f"LineStart INTEGER NOT NULL, "
            f"LineEnd INTEGER NOT NULL,"
            f"PredicateName TEXT NOT NULL);"
        )

        # Todo: the combination (TestName, ExceptionFilePath, ExceptionLineNumber, ExceptionName) is unique.
        #  Add this constraint to this DB.
        seen_exception_table_create_command = (
            f"CREATE TABLE {self._Seen_exception_table} "
            f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
            f"TestName TEXT NOT NULL UNIQUE, "
            f"ExceptionFilePath TEXT NOT NULL, "
            f"ExceptionLineNumber INTEGER NOT NULL,"
            f"ExceptionName TEXT NOT NULL);"
        )

        predicate_sequence_table_create_command = (
            f"CREATE TABLE {self._Predicate_sequence_table} "
            f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
            f"TestName TEXT NOT NULL UNIQUE, "
            f"PredicateSequence TEXT NOT NULL,"
            f"IndexedPredicateSequence TEXT NOT NULL );"
        )

        # ToDo: TestName has unique constraint.
        scored_entity_table_create_command = (
            f"CREATE TABLE {self._Scored_entity_table} "
            f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
            f"TestName TEXT NOT NULL, "
            f"Entity TEXT NOT NULL, "
            f"Score INTEGER NOT NULL);"
        )

        test_time_table_create_command = (
            f"CREATE TABLE {self._Test_time_table} "
            f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
            f"TestName TEXT NOT NULL, "
            f"TestTime REAL NOT NULL);"
        )

        timeout_predicate_instance_table_create_command = (
            f"CREATE TABLE {self._Timeout_predicate_instance_table} "
            f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
            f"TestName TEXT NOT NULL, "
            f"PredicateName TEXT NOT NULL,"
            f"PredicateInstanceNumber INTEGER NOT NULL);"
        )

        bad_execution_predicate_instance_table_create_command = (
            f"CREATE TABLE {self._Bad_execution_predicate_instance_table} "
            f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
            f"TestName TEXT NOT NULL, "
            f"PredicateName TEXT NOT NULL,"
            f"PredicateInstanceNumber INTEGER NOT NULL);"
        )

        astor_assert_error_info_table_table_create_command = (
            f"CREATE TABLE {self._Astor_assert_error_info_table} "
            f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
            f"filePath TEXT NOT NULL, "
            f"lineStart INTEGER NOT NULL ,"
            f"lineEnd INTEGER NOT NULL, "
            f"PredicateName TEXT NOT NULL);"
        )
        # astorAssertErrorInfoTable
        view_create_command = (
            f"CREATE VIEW {self._Covered_lines_with_test_types_view} AS "
            f"SELECT {self._Covered_lines_for_test_table}.Rowid, "
            f"{self._Covered_lines_for_test_table}.TestName, "
            f"{self._Covered_lines_for_test_table}.FilePath, "
            f"{self._Covered_lines_for_test_table}.LineNumber, "
            f"{self._Test_case_table}.Type, "
            f"{self._Test_case_table}.Target "
            f"FROM {self._Covered_lines_for_test_table} "
            f"INNER JOIN {self._Test_case_table} ON "
            f"{self._Covered_lines_for_test_table}.TestName = {self._Test_case_table}.TestName"
        )

        command_list = [
            test_case_table_create_command,
            executed_line_for_test_table_create_command,
            empty_test_table_create_command,
            shadowed_covered_predicate_table_create_command,
            # realPredicateInstanceTableCreateCommand,
            view_create_command,
            # finalPredicateTableCreateCommand,
            candidate_predicate_table_create_command,
            seen_exception_table_create_command,
            predicate_sequence_table_create_command,
            scored_entity_table_create_command,
            test_time_table_create_command,
            timeout_predicate_instance_table_create_command,
            bad_execution_predicate_instance_table_create_command,
            astor_assert_error_info_table_table_create_command,
        ]

        return command_list

    def end(self):
        self._connection.close()

    def insert_covered_line_for_test(
        self, test_name: str, file_path: str, line_number: int
    ):
        cur = self._connection.cursor()
        cur.execute(
            f"INSERT INTO {self._Covered_lines_for_test_table} VALUES (NULL, ?, ?, ?)",
            (test_name, file_path, line_number),
        )

        self._connection.commit()

    def insert_empty_test(self, test_name):
        cur = self._connection.cursor()
        cur.execute(
            f"INSERT INTO {self._Empty_test_case_table} VALUES (NULL, ?)", (test_name,)
        )

        self._connection.commit()

    def insert_test_case(
        self, test_name, test_type, exception_file_path, exception_line_number, target
    ):
        target_field = 1 if target else 0

        cur = self._connection.cursor()
        cur.execute(
            f"INSERT INTO {self._Test_case_table} VALUES (NULL, ?, ?, ?, ?, ?)",
            (
                test_name,
                test_type,
                exception_file_path,
                exception_line_number,
                target_field,
            ),
        )

        self._connection.commit()

    def select_covered_lines_with_test_types_for_all_failed_tests(self):
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT TestName, FilePath, LineNumber, Type FROM {self._Covered_lines_with_test_types_view} "
            f"WHERE Type = 'failed' and Target = 1"
        )

        return cur.fetchall()

    def insert_shadowed_covered_predicate(
        self,
        test_name: str,
        file_path: str,
        exe_line_number: int,
        line_start: int,
        line_end: int,
    ):
        cur = self._connection.cursor()
        cur.execute(
            f"INSERT INTO {self._Shadowed_covered_predicate_table} VALUES (NULL, ?, ?, ?, ?, ?)",
            (test_name, file_path, exe_line_number, line_start, line_end),
        )

        self._connection.commit()

    def select_distinct_executed_source_code_predicates(self):
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT DISTINCT FilePath, LineStart, LineEnd FROM {self._Shadowed_covered_predicate_table} "
        )

        return cur.fetchall()

    def insert_candidate_predicate(
        self, file_path: str, line_start: int, line_end: int, predicate_name: str
    ):
        cur = self._connection.cursor()
        cur.execute(
            f"INSERT INTO {self._Candidate_predicate_table} VALUES (NULL, ?, ?, ?, ?)",
            (file_path, line_start, line_end, predicate_name),
        )

        self._connection.commit()

    def select_distinct_candidate_predicate_file_paths(self):
        cur = self._connection.cursor()
        cur.execute(f"SELECT DISTINCT FilePath FROM {self._Candidate_predicate_table} ")

        items = [x[0] for x in cur.fetchall()]

        return items

    def select_candidate_predicates_for_file_path(self, filepath):
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT LineStart, LineEnd, PredicateName FROM {self._Candidate_predicate_table} WHERE FilePath = ?",
            (filepath,),
        )

        return cur.fetchall()

    def select_test_case_failed(self):
        cur = self._connection.cursor()
        # No need to check if they are target failing tests, but I added it anyway.
        cur.execute(
            f"SELECT TestName FROM {self._Test_case_table} WHERE "
            f"Type = 'failed' AND Target = 1"
        )

        items = [x[0] for x in cur.fetchall()]

        return items

    def select_test_case_exceptions(self):
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT TestName, ExceptionFilePath, ExceptionLineNumber FROM {self._Test_case_table} "
            f"WHERE ExceptionLineNumber != -1 AND Target = 1"
        )

        return cur.fetchall()

    def insert_seen_exceptions(
        self, test_name: str, file_path: str, line_number: int, exception_name: str
    ):
        cur = self._connection.cursor()
        cur.execute(
            f"INSERT INTO {self._Seen_exception_table} VALUES (NULL, ?, ?, ?, ?)",
            (test_name, file_path, line_number, exception_name),
        )

        self._connection.commit()

    def select_distinct_seen_exceptions_file_paths(self):
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT DISTINCT ExceptionFilePath FROM {self._Seen_exception_table} "
        )

        items = [x[0] for x in cur.fetchall()]

        return items

    def select_seen_exceptions_for_file_path(self, filePath: str):
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT ExceptionLineNumber, ExceptionName FROM {self._Seen_exception_table} WHERE ExceptionFilePath = ?",
            (filePath,),
        )

        return cur.fetchall()

    def insert_predicate_sequence_for_test(
        self, test_name: str, predicate_sequence: str, indexed_predicate_sequence: str
    ):
        cur = self._connection.cursor()
        cur.execute(
            f"INSERT INTO {self._Predicate_sequence_table} VALUES (NULL, ?, ?, ?)",
            (test_name, predicate_sequence, indexed_predicate_sequence),
        )

        self._connection.commit()

    def select_test_type(self, testName: str) -> str:
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT Type FROM {self._Test_case_table} " f"WHERE TestName = ?",
            (testName,),
        )

        return cur.fetchone()[0]

    def select_seen_exception_for_test_name(self, testName: str) -> Optional[str]:
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT ExceptionName FROM {self._Seen_exception_table} "
            f"WHERE TestName = ?",
            (testName,),
        )

        items_found = cur.fetchone()
        if items_found is not None:
            return items_found[0]
        else:
            return None

    def select_candidate_predicate(self, predicate_name: str):
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT FilePath, LineStart, LineEnd FROM {self._Candidate_predicate_table} "
            f"WHERE PredicateName = ?",
            (predicate_name,),
        )

        items_found = cur.fetchone()
        return items_found

    def insert_scored_entity(self, test_name: str, entity: str, score: int):
        cur = self._connection.cursor()
        cur.execute(
            f"INSERT INTO {self._Scored_entity_table} VALUES (NULL, ?, ?, ?)",
            (test_name, entity, score),
        )

        self._connection.commit()

    def scored_entity_exists_for_test(self, test_name: str, entity: str):
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT DISTINCT TestName, Entity FROM {self._Scored_entity_table} "
            f"WHERE TestName = ? AND Entity = ?",
            (test_name, entity),
        )

        items_found = cur.fetchall()
        return len(items_found) > 0

    def insert_test_time(self, test_name: str, test_time: int):
        cur = self._connection.cursor()
        cur.execute(
            f"INSERT INTO {self._Test_time_table} VALUES (NULL, ?, ?)",
            (test_name, test_time),
        )

        self._connection.commit()

    def select_max_test_time(self):
        cur = self._connection.cursor()
        cur.execute(f"SELECT MAX(TestTime) FROM {self._Test_time_table}")
        row = cur.fetchone()
        max_time = row[0]

        return max_time

    def insert_timeout_predicate_instance(
        self, test_name: str, pred_name: str, inst_num: int
    ):
        cur = self._connection.cursor()
        cur.execute(
            f"INSERT INTO {self._Timeout_predicate_instance_table} VALUES (NULL, ?, ?, ?)",
            (test_name, pred_name, inst_num),
        )

        self._connection.commit()

    def select_scored_entity_test_names(self):
        cur = self._connection.cursor()
        cur.execute(f"SELECT DISTINCT TestName FROM {self._Scored_entity_table}")

        items_found = cur.fetchall()
        test_names = [x[0] for x in items_found]
        return test_names

    def select_test_top_n_scored_entities(
        self, test_name: str, top_n: int
    ) -> List[Tuple[str, float]]:
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT Entity, Score FROM {self._Scored_entity_table} "
            f"WHERE TestName = ? "
            f"ORDER BY Score DESC LIMIT ?",
            (test_name, top_n),
        )

        items_found = cur.fetchall()
        return items_found

    def select_test_all_scored_entities(
        self, test_name: str
    ) -> List[Tuple[str, float]]:
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT Entity, Score FROM {self._Scored_entity_table} "
            f"WHERE TestName = ? "
            f"ORDER BY Score DESC ",
            (test_name,),
        )

        items_found = cur.fetchall()
        return items_found

    def number_of_candidate_predicates(self):
        cur = self._connection.cursor()
        cur.execute(f"SELECT COUNT(*) FROM {self._Candidate_predicate_table}")

        items_found = cur.fetchone()[0]
        return items_found

    def insert_bad_execution_predicate_instance(self, test_name, pred_name, inst_num):
        cur = self._connection.cursor()
        cur.execute(
            f"INSERT INTO {self._Bad_execution_predicate_instance_table} VALUES (NULL, ?, ?, ?)",
            (test_name, pred_name, inst_num),
        )

        self._connection.commit()

    def insert_astor_assert_error_info(
        self, file_path: str, line_start: int, line_end: int, predicate_name: str
    ):
        cur = self._connection.cursor()
        cur.execute(
            f"INSERT INTO {self._Astor_assert_error_info_table} VALUES (NULL, ?, ?, ?, ?)",
            (file_path, line_start, line_end, predicate_name),
        )

        self._connection.commit()
