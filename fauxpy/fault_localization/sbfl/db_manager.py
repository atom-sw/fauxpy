import sqlite3
from pathlib import Path
from typing import List, Tuple


class SbflDbManager:
    _File_name = "fauxpy.db"
    _Test_case_table = "TestCase"
    _Execution_trace_table = "ExecutionTrace"
    _Empty_test_case_table = "EmptyTest"
    _Score_table = "Score"
    _Execution_trace_with_test_type_view = "ExecutionTraceWithTestType"

    def __init__(self, report_directory_path: Path):
        db_file_path = report_directory_path / self._File_name
        db_file_path_str = str(db_file_path.absolute().resolve())
        self._connection = sqlite3.connect(db_file_path_str)
        command_list = self._get_database_schema()
        for command in command_list:
            self._connection.executescript(command)

    def end(self):
        self._connection.close()

    def _get_database_schema(self):
        test_case_table_create_command = (
            f"CREATE TABLE {self._Test_case_table} "
            f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
            f"TestName TEXT NOT NULL UNIQUE, "
            f"Type TEXT NOT NULL,"
            f"Target INTEGER NOT NULL);"
        )
        execution_trace_table_create_command = (
            f"CREATE TABLE {self._Execution_trace_table} "
            f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
            f"TestName TEXT NOT NULL, "
            f"Entity TEXT NOT NULL, "
            f"UNIQUE(TestName, Entity));"
        )
        empty_test_table_create_command = (
            f"CREATE TABLE {self._Empty_test_case_table} "
            f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
            f"TestName TEXT NOT NULL UNIQUE);"
        )

        score_table_create_command = (
            f"CREATE TABLE {self._Score_table} "
            f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
            f"Entity TEXT NOT NULL UNIQUE, "
            f"Ef REAL NOT NULL, "
            f"Ep REAL NOT NULL, "
            f"Nf REAL NOT NULL, "
            f"Np REAL NOT NULL, "
            f"Tarantula REAL NOT NULL, "
            f"Ochiai REAL NOT NULL, "
            f"Dstar REAL NOT NULL);"
        )

        execution_trace_table_index_command = (
            f"CREATE INDEX Index_Entity ON {self._Execution_trace_table} (Entity);"
        )

        test_case_table_index_command = (
            f"CREATE INDEX Index_Type ON {self._Test_case_table} (Type);"
        )

        score_tarantula_table_index_command = (
            f"CREATE INDEX index_Tarantula ON {self._Score_table} (Tarantula);"
        )

        score_ochiai_table_index_command = (
            f"CREATE INDEX index_Ochiai ON {self._Score_table} (Ochiai);"
        )

        score_dstar_table_index_command = (
            f"CREATE INDEX index_Dstar ON {self._Score_table} (Dstar);"
        )

        view_create_command = (
            f"CREATE VIEW {self._Execution_trace_with_test_type_view} AS "
            f"SELECT {self._Execution_trace_table}.Entity, {self._Execution_trace_table}.TestName, {self._Test_case_table}.Type, {self._Test_case_table}.Target "
            f"FROM {self._Execution_trace_table} "
            f"INNER JOIN {self._Test_case_table} ON {self._Execution_trace_table}.TestName = {self._Test_case_table}.TestName"
        )

        command_list = [
            test_case_table_create_command,
            execution_trace_table_create_command,
            empty_test_table_create_command,
            score_table_create_command,
            execution_trace_table_index_command,
            test_case_table_index_command,
            score_tarantula_table_index_command,
            score_ochiai_table_index_command,
            score_dstar_table_index_command,
            view_create_command,
        ]

        return command_list

    def insert_execution_trace(self, test_name: str, covered_entity: List[str]):
        for covEntity in covered_entity:
            cur = self._connection.cursor()
            cur.execute(
                f"INSERT INTO {self._Execution_trace_table} VALUES (NULL, ?, ?)",
                (test_name, covEntity),
            )

        self._connection.commit()

    def insert_empty_test(self, test_name):
        cur = self._connection.cursor()
        cur.execute(
            f"INSERT INTO {self._Empty_test_case_table} VALUES (NULL, ?)", (test_name,)
        )

        self._connection.commit()

    def insert_test_case(self, test_name, test_type, target: bool):
        target_field = 1 if target else 0

        cur = self._connection.cursor()
        cur.execute(
            f"INSERT INTO {self._Test_case_table} VALUES (NULL, ?, ?, ?)",
            (test_name, test_type, target_field),
        )

        self._connection.commit()

    def select_distinct_executed_entity_list(self):
        cur = self._connection.cursor()
        cur.execute(f"SELECT DISTINCT Entity FROM {self._Execution_trace_table}")

        entity_list = [x[0] for x in cur.fetchall()]
        return entity_list

    def select_number_of_tests(self) -> Tuple[int, int]:
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT COUNT(Type) FROM {self._Test_case_table} WHERE Type = 'passed'"
        )
        num_all_passed = cur.fetchone()[0]
        cur.execute(
            f"SELECT COUNT(Type) FROM {self._Test_case_table} WHERE Type = 'failed' AND Target = 1"
        )
        num_all_failed = cur.fetchone()[0]
        # cur.execute(f"SELECT COUNT(*) FROM {_Names.testCaseTable}")
        # numAll = cur.fetchone()[0]
        # assert num_all_passed + num_all_failed == numAll  # Simple checking. Can be removed.

        return num_all_passed, num_all_failed

    def select_number_of_covering_tests(self, entity):
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT COUNT(*) FROM {self._Execution_trace_with_test_type_view} "
            f"WHERE Type = 'passed' AND Entity = ?",
            (entity,),
        )
        num_cov_passed = cur.fetchone()[0]
        cur.execute(
            f"SELECT COUNT(*) FROM {self._Execution_trace_with_test_type_view} "
            f"WHERE Type = 'failed' AND Target = 1 AND Entity = ?",
            (entity,),
        )
        num_cov_failed = cur.fetchone()[0]
        # cur.execute(f"SELECT COUNT(*) FROM {_Names.executionTraceWithTestTypeView} "
        #             f"WHERE Entity = ?", (entity,))
        # numCovAll = cur.fetchone()[0]
        # assert num_cov_passed + num_cov_failed == numCovAll  # Check if left join is causing any NULLs on test type of the view

        return num_cov_passed, num_cov_failed

    def inert_scores(self, entity, ef, ep, nf, np, scores):
        cur = self._connection.cursor()
        cur.execute(
            f"INSERT INTO {self._Score_table} "
            f"VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                entity,
                ef,
                ep,
                nf,
                np,
                scores["Tarantula"],
                scores["Ochiai"],
                scores["Dstar"],
            ),
        )

        self._connection.commit()

    def select_top_n_ranked_entities(self, top_n):
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT Entity, Tarantula FROM {self._Score_table} ORDER BY Tarantula DESC LIMIT ?",
            (top_n,),
        )
        score_tarantula = cur.fetchall()

        cur.execute(
            f"SELECT Entity, Ochiai FROM {self._Score_table} ORDER BY Ochiai DESC LIMIT ?",
            (top_n,),
        )
        score_ochiai = cur.fetchall()

        cur.execute(
            f"SELECT Entity, Dstar FROM {self._Score_table} ORDER BY Dstar DESC LIMIT ?",
            (top_n,),
        )
        score_dstar = cur.fetchall()

        ranked_entities = {
            "Tarantula": score_tarantula,
            "Ochiai": score_ochiai,
            "Dstar": score_dstar,
        }

        return ranked_entities

    def select_all_ranked_entities(self):
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT Entity, Tarantula FROM {self._Score_table} ORDER BY Tarantula DESC"
        )
        score_tarantula = cur.fetchall()

        cur.execute(
            f"SELECT Entity, Ochiai FROM {self._Score_table} ORDER BY Ochiai DESC"
        )
        score_ochiai = cur.fetchall()

        cur.execute(
            f"SELECT Entity, Dstar FROM {self._Score_table} ORDER BY Dstar DESC"
        )
        score_dstar = cur.fetchall()

        ranked_entities = {
            "Tarantula": score_tarantula,
            "Ochiai": score_ochiai,
            "Dstar": score_dstar,
        }

        return ranked_entities
