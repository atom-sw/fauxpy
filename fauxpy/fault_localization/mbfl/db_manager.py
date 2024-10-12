import sqlite3
from pathlib import Path
from typing import Tuple, List


class MbflDbManager:
    _File_name = "fauxpy.db"
    _Test_case_table = "TestCase"
    _Execution_trace_table = "ExecutionTrace"
    _Empty_test_case_table = "EmptyTest"
    _Execution_trace_with_test_type_view = "ExecutionTraceWithTestType"
    _Failing_line_number_table = "FailingLineNumber"
    _Mutant_info_table = "MutantInfo"
    _Mutant_score_term_table = "MutantScoreTerm"
    _Entity_score_table = "EntityScoreTable"
    _Test_time_table = "TestTime"

    def __init__(self, report_directory_path: Path):
        db_file_path = report_directory_path / self._File_name
        db_file_path_str = str(db_file_path.absolute().resolve())
        self._connection = sqlite3.connect(db_file_path_str)
        command_list = self._get_database_schema()
        for command in command_list:
            self._connection.executescript(command)

    def _get_database_schema(self):
        test_case_table_create_command = (
            f"CREATE TABLE {self._Test_case_table} "
            f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
            f"TestName TEXT NOT NULL UNIQUE, "
            f"Type TEXT NOT NULL, "
            f"TestTraceBack TEXT NOT NULL, "
            f"Timeout INTEGER NOT NULL, "
            f"Target INTEGER NOT NULL);"
        )
        # ToDo: use the commented table which has unique command.
        # executionTraceTableCreateCommand = f"CREATE TABLE {_Names.executionTraceTable} " \
        #                                    f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
        #                                    f"TestName TEXT NOT NULL, " \
        #                                    f"Entity TEXT NOT NULL, " \
        #                                    f"UNIQUE(TestName, Entity));"
        execution_trace_table_create_command = (
            f"CREATE TABLE {self._Execution_trace_table} "
            f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
            f"TestName TEXT NOT NULL, "
            f"Entity TEXT NOT NULL);"
        )
        empty_test_table_create_command = (
            f"CREATE TABLE {self._Empty_test_case_table} "
            f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
            f"TestName TEXT NOT NULL UNIQUE);"
        )

        failing_line_number_table_create_command = (
            f"CREATE TABLE {self._Failing_line_number_table} "
            f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
            f"ModulePath TEXT NOT NULL, "
            f"LineNumber INTEGER NOT NULL, "
            f"UNIQUE(ModulePath, LineNumber));"
        )

        mutant_info_table_create_command = (
            f"CREATE TABLE {self._Mutant_info_table} "
            f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
            f"MutantId TEXT NOT NULL, "
            f"ModulePath TEXT NOT NULL, "
            f"LineNumber INTEGER NOT NULL,"
            f"OperatorName TEXT NOT NULL, "
            f"MutantDiff TEXT NOT NULL UNIQUE, "
            f"StartPos INTEGER NOT NULL, "
            f"EndPos INTEGER NOT NULL, "
            f"Timeout INTEGER NOT NULL, "
            f"HasMissingTests INTEGER NOT NULL);"
        )

        mutant_score_term_table_create_command = (
            f"CREATE TABLE {self._Mutant_score_term_table} "
            f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
            f"MutantId TEXT NOT NULL, "
            f"Entity TEXT NOT NULL,	"
            f"FailedToPass INTEGER NOT NULL, "
            f"PassedToFailed INTEGER NOT NULL, "
            f"FailedChanged INTEGER NOT NULL, "
            f"MutantMuseScore REAL NOT NULL, "
            f"MutantMetallaxisScore REAL NOT NULL);"
        )

        entity_score_table_create_command = (
            f"CREATE TABLE {self._Entity_score_table} "
            f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
            f"Entity TEXT NOT NULL, "
            f"EntityMuseScore REAL NOT NULL, "
            f"EntityMetallaxisScore REAL NOT NULL);"
        )

        test_time_table_create_command = (
            f"CREATE TABLE {self._Test_time_table} "
            f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
            f"TestName TEXT NOT NULL, "
            f"TestTime REAL NOT NULL);"
        )

        test_case_table_test_name_index_command = f"CREATE INDEX Index_TestCase_TestName ON {self._Test_case_table} (TestName);"

        test_case_table_type_index_command = (
            f"CREATE INDEX Index_TestCase_Type ON {self._Test_case_table} (Type);"
        )

        execution_trace_table_test_name_index_command = f"CREATE INDEX Index_ExecutionTrace_TestName ON {self._Test_case_table} (TestName);"

        failing_line_number_table_module_path_index_command = (
            f"CREATE INDEX Index_ModulePath ON "
            f"{self._Failing_line_number_table} (ModulePath);"
        )

        # mutantInfoTableModulePathLineNumberIndexCommand = \
        #     f"CREATE INDEX Index_Mutant_ModulePath_LineNumber ON {_Names.mutantInfoTable} (ModulePath, LineNumber);"

        mutant_score_term_table_entity_index_command = f"CREATE INDEX Index_MutantScoreTerm ON {self._Mutant_score_term_table} (Entity);"

        entity_score_table_entity_index_command = (
            f"CREATE INDEX Index_EntityScore ON {self._Entity_score_table} (Entity);"
        )

        view_create_command = (
            f"CREATE VIEW {self._Execution_trace_with_test_type_view} AS "
            f"SELECT {self._Execution_trace_table}.Entity, "
            f"{self._Execution_trace_table}.TestName, "
            f"{self._Test_case_table}.Type, "
            f"{self._Test_case_table}.Target "
            f"FROM {self._Execution_trace_table} "
            f"INNER JOIN {self._Test_case_table} ON "
            f"{self._Execution_trace_table}.TestName = {self._Test_case_table}.TestName"
        )

        command_list = [
            test_case_table_create_command,
            execution_trace_table_create_command,
            empty_test_table_create_command,
            failing_line_number_table_create_command,
            mutant_info_table_create_command,
            mutant_score_term_table_create_command,
            entity_score_table_create_command,
            test_time_table_create_command,
            test_case_table_test_name_index_command,
            test_case_table_type_index_command,
            execution_trace_table_test_name_index_command,
            failing_line_number_table_module_path_index_command,
            # mutantInfoTableModulePathLineNumberIndexCommand,
            mutant_score_term_table_entity_index_command,
            entity_score_table_entity_index_command,
            view_create_command,
        ]

        return command_list

    def end(self):
        self._connection.close()

    def insert_execution_trace(self, test_name: str, covered_entity_list: List[str]):
        for cov_entity in covered_entity_list:
            cur = self._connection.cursor()
            cur.execute(
                f"INSERT INTO {self._Execution_trace_table} VALUES (NULL, ?, ?)",
                (test_name, cov_entity),
            )

        self._connection.commit()

    def insert_empty_test(self, test_name):
        cur = self._connection.cursor()
        cur.execute(
            f"INSERT INTO {self._Empty_test_case_table} VALUES (NULL, ?)", (test_name,)
        )

        self._connection.commit()

    def insert_test_case_run(
        self, test_name, test_type, test_trace_back, timeout_stat, target
    ):
        target_field = 1 if target else 0

        cur = self._connection.cursor()
        cur.execute(
            f"INSERT INTO {self._Test_case_table} VALUES (NULL, ?, ?, ?, ?, ?)",
            (test_name, test_type, test_trace_back, timeout_stat, target_field),
        )

        self._connection.commit()

    def select_distinct_line_numbers_covered_by_failing_tests(self):
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT DISTINCT Entity FROM {self._Execution_trace_with_test_type_view} "
            f"WHERE Type = 'failed' and Target = 1"
        )

        entities = [x[0] for x in cur.fetchall()]
        return entities

    def insert_failing_line_number_components(self, module_path: str, line_number: int):
        cur = self._connection.cursor()
        cur.execute(
            f"INSERT INTO {self._Failing_line_number_table} VALUES (NULL, ?, ?)",
            (module_path, line_number),
        )

        self._connection.commit()

    def select_distinct_failing_module_paths(self) -> List[str]:
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT DISTINCT ModulePath FROM {self._Failing_line_number_table}"
        )

        entities = [x[0] for x in cur.fetchall()]
        return entities

    def select_failing_line_numbers_for_module_path(
        self, module_path: str
    ) -> List[int]:
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT LineNumber FROM {self._Failing_line_number_table} WHERE ModulePath = ?",
            (module_path,),
        )

        entities = [x[0] for x in cur.fetchall()]
        return entities

    def insert_mutant(
        self,
        mutantID: str,
        modulePath: str,
        lineNumber: int,
        operatorName: str,
        moduleDiff: str,
        startPos: int,
        endPos: int,
        timeout: int = -1,
        hasMissingTests: int = -1,
    ):
        cur = self._connection.cursor()
        cur.execute(
            f"INSERT INTO {self._Mutant_info_table} VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                mutantID,
                modulePath,
                lineNumber,
                operatorName,
                moduleDiff,
                startPos,
                endPos,
                timeout,
                hasMissingTests,
            ),
        )

        self._connection.commit()

    def select_number_of_tests(self):
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT COUNT(Type) FROM {self._Test_case_table} WHERE Type = 'passed'"
        )
        num_all_passed = cur.fetchone()[0]
        cur.execute(
            f"SELECT COUNT(Type) FROM {self._Test_case_table} WHERE Type = 'failed'"
        )
        num_all_failed = cur.fetchone()[0]
        # cur.execute(f"SELECT COUNT(*) FROM {_Names.testCaseTable}")
        # numAll = cur.fetchone()[0]
        # assert numAllPassed + num_all_failed == numAll  # Simple checking. Can be removed.

        return num_all_passed, num_all_failed

    def select_test_case(self, test_name: str):
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT TestName, Type, TestTraceBack, Timeout, Target FROM {self._Test_case_table} WHERE TestName = ?",
            (test_name,),
        )
        row = cur.fetchone()

        return row

    def insert_mutant_score_terms(
        self,
        mutant_id: str,
        entity: str,
        failed_to_passed: int,
        passed_to_failed: int,
        failed_changed: int,
    ):
        cur = self._connection.cursor()
        cur.execute(
            f"INSERT INTO {self._Mutant_score_term_table} VALUES (NULL, ?, ?, ?, ?, ?, -1, -1)",
            (mutant_id, entity, failed_to_passed, passed_to_failed, failed_changed),
        )

        self._connection.commit()

    def select_total_failed_to_passed_and_passed_to_failed(self) -> Tuple[int, int]:
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT SUM(FailedToPass), SUM(PassedToFailed) FROM {self._Mutant_score_term_table}"
        )
        row = cur.fetchone()

        return row

    def select_mutant_score_terms(self):
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT MutantId, FailedToPass, PassedToFailed, FailedChanged FROM {self._Mutant_score_term_table}"
        )
        rows = cur.fetchall()

        return rows

    def update_mutant_score_terms(
        self, mutant_id, mutant_muse_score, mutant_metallaxis_score
    ):
        cur = self._connection.cursor()
        cur.execute(
            f"UPDATE {self._Mutant_score_term_table} SET MutantMuseScore = ?, "
            f"MutantMetallaxisScore = ? WHERE MutantId = ?",
            (mutant_muse_score, mutant_metallaxis_score, mutant_id),
        )

        self._connection.commit()

    def select_distinct_all_mutant_score_terms_entities(self):
        cur = self._connection.cursor()
        cur.execute(f"SELECT DISTINCT Entity FROM {self._Mutant_score_term_table}")
        rows = cur.fetchall()

        entities = [x[0] for x in rows]
        return entities

    def select_mutant_score_terms_scores(self, entity):
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT MutantMuseScore FROM {self._Mutant_score_term_table} WHERE Entity = ?",
            (entity,),
        )
        rows = cur.fetchall()
        mutant_muse_scores = [x[0] for x in rows]

        cur.execute(
            f"SELECT MutantMetallaxisScore FROM {self._Mutant_score_term_table} WHERE Entity = ?",
            (entity,),
        )
        rows = cur.fetchall()
        mutant_metallaxis_scores = [x[0] for x in rows]

        return {"Muse": mutant_muse_scores, "Metallaxis": mutant_metallaxis_scores}

    def insert_entity_score(
        self, entity: str, entity_muse_score: float, entity_metallaxis_score: float
    ):
        cur = self._connection.cursor()
        cur.execute(
            f"INSERT INTO {self._Entity_score_table} VALUES (NULL, ?, ?, ?)",
            (entity, entity_muse_score, entity_metallaxis_score),
        )

        self._connection.commit()

    def select_all_ranked_entities(self):
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT Entity, EntityMuseScore FROM {self._Entity_score_table} "
            f"ORDER BY EntityMuseScore DESC"
        )
        scores_muse = cur.fetchall()

        cur = self._connection.cursor()
        cur.execute(
            f"SELECT Entity, EntityMetallaxisScore FROM {self._Entity_score_table} "
            f"ORDER BY EntityMetallaxisScore DESC"
        )
        scores_metallaxis = cur.fetchall()

        return {"Muse": scores_muse, "Metallaxis": scores_metallaxis}

    def select_top_n_ranked_entities(self, topN):
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT Entity, EntityMuseScore FROM {self._Entity_score_table} "
            f"ORDER BY EntityMuseScore DESC LIMIT ?",
            (topN,),
        )
        scores_muse = cur.fetchall()

        cur = self._connection.cursor()
        cur.execute(
            f"SELECT Entity, EntityMetallaxisScore FROM {self._Entity_score_table} "
            f"ORDER BY EntityMetallaxisScore DESC LIMIT ?",
            (topN,),
        )
        scores_metallaxis = cur.fetchall()

        return {"Muse": scores_muse, "Metallaxis": scores_metallaxis}

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

    def update_mutant_as_timeout(self, mutant_id):
        cur = self._connection.cursor()
        cur.execute(
            f"UPDATE {self._Mutant_info_table} SET Timeout = ? " f"WHERE MutantId = ?",
            (1, mutant_id),
        )

        self._connection.commit()

    def update_mutant_as_having_missing_tests(self, mutant_id):
        cur = self._connection.cursor()
        cur.execute(
            f"UPDATE {self._Mutant_info_table} SET HasMissingTests = ? "
            f"WHERE MutantId = ?",
            (1, mutant_id),
        )

        self._connection.commit()
