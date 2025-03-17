import sqlite3
from pathlib import Path
from typing import Tuple, List

from fauxpy import constants


class MbflDbManager:
    """
    Manages interactions with the database that stores information related to an MBFL fault localization session.
    """

    _File_name = constants.DB_FILE_NAME_FL_SESSION
    _Test_case_table = "TestCase"
    _Execution_trace_table = "ExecutionTrace"
    _Empty_test_case_table = "EmptyTest"
    _Execution_trace_with_test_type_view = "ExecutionTraceWithTestType"
    _Failing_line_number_table = "FailingLineNumber"
    _Mutant_info_table = "MutantInfo"
    _Mutant_score_term_table = "MutantScoreTerm"
    _Entity_score_table = "EntityScoreTable"
    _Test_time_table = "TestTime"

    _Pyllmut_mutant_info_table = "PyllmutMutantInfo"
    _Pyllmut_timeout_info_table = "PyllmutTimeoutInfo"
    _Pyllmut_bad_response_info_table = "PyllmutBadResponseInfo"

    def __init__(self, report_directory_path: Path):
        """
        Initializes the database manager by connecting to the specified SQLite database file.

        Args:
            report_directory_path (Path): The directory containing the database file.
        """
        db_file_path = report_directory_path / self._File_name
        db_file_path_str = str(db_file_path.absolute().resolve())
        self._connection = sqlite3.connect(db_file_path_str)
        command_list = self._get_database_schema()
        for command in command_list:
            self._connection.executescript(command)

    def _get_database_schema(self):
        """
        Constructs the SQL commands required to create the database schema.

        Returns:
            list: A list of SQL commands to create tables and views.
        """
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

        # PyLLMut tables

        pyllmut_mutant_info_table_create_command = (
            f"CREATE TABLE {self._Pyllmut_mutant_info_table} "
            f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
            f"PromptContent TEXT NOT NULL, "
            f"LineNumber INTEGER NOT NULL, "
            f"SentTokenCount INTEGER NOT NULL, "
            f"ResponseContent TEXT NOT NULL, "
            f"ReceivedTokenCount INTEGER NOT NULL, "
            f"DiffContent TEXT NOT NULL, "
            f"PreCodeModel TEXT NOT NULL, "
            f"AfterCodeModel TEXT NOT NULL, "
            f"PreCodeRefined TEXT NOT NULL, "
            f"AfterCodeRefined TEXT NOT NULL, "
            f"MutantType TEXT NOT NULL);"
        )

        pyllmut_response_info_table_create_command = (
            f"CREATE TABLE {self._Pyllmut_bad_response_info_table} "
            f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
            f"PromptContent TEXT NOT NULL, "
            f"LineNumber INTEGER NOT NULL, "
            f"SentTokenCount INTEGER NOT NULL, "
            f"ResponseContent TEXT NOT NULL, "
            f"ReceivedTokenCount INTEGER NOT NULL);"
        )

        pyllmut_timeout_info_table_create_command = (
            f"CREATE TABLE {self._Pyllmut_timeout_info_table} "
            f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, "
            f"PromptContent TEXT NOT NULL, "
            f"LineNumber INTEGER NOT NULL);"
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

            pyllmut_mutant_info_table_create_command,
            pyllmut_response_info_table_create_command,
            pyllmut_timeout_info_table_create_command
        ]

        return command_list

    def end(self):
        """Closes the database connection."""
        self._connection.close()

    def insert_execution_trace(self, test_name: str, covered_entity_list: List[str]):
        """
        Inserts an execution trace for a given test case into the database.

        Args:
            test_name (str): The name of the test case.
            covered_entity_list (List[str]): The list of covered entities by the test case.
        """
        for cov_entity in covered_entity_list:
            cur = self._connection.cursor()
            cur.execute(
                f"INSERT INTO {self._Execution_trace_table} VALUES (NULL, ?, ?)",
                (test_name, cov_entity),
            )

        self._connection.commit()

    def insert_empty_test(self, test_name):
        """
        Inserts an empty test case (a test case with no execution trace) into the empty test table.

        Args:
            test_name (str): The name of the empty test case.
        """
        cur = self._connection.cursor()
        cur.execute(
            f"INSERT INTO {self._Empty_test_case_table} VALUES (NULL, ?)", (test_name,)
        )

        self._connection.commit()

    def insert_test_case_run(
        self, test_name, test_type, test_trace_back, timeout_stat, target
    ):
        """
        Inserts a test case with its execution details into the test case table.

        Args:
            test_name (str): The name of the test case.
            test_type (str): The type of the test (e.g., 'failed' or 'passed').
            test_trace_back (str): The traceback of the test case.
            timeout_stat (int): Timeout status for the test case.
            target (bool): Whether the test case is a targeted failing test.
        """
        target_field = 1 if target else 0

        cur = self._connection.cursor()
        cur.execute(
            f"INSERT INTO {self._Test_case_table} VALUES (NULL, ?, ?, ?, ?, ?)",
            (test_name, test_type, test_trace_back, timeout_stat, target_field),
        )

        self._connection.commit()

    def select_distinct_line_numbers_covered_by_failing_tests(self):
        """
        Selects the distinct entities covered by failing tests.

        Returns:
            List[str]: The list of covered entities by failing tests.
        """
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT DISTINCT Entity FROM {self._Execution_trace_with_test_type_view} "
            f"WHERE Type = 'failed' and Target = 1"
        )

        entities = [x[0] for x in cur.fetchall()]
        return entities

    def insert_failing_line_number_components(self, module_path: str, line_number: int):
        """
        Inserts a failing line number (a line number covered by a failing test) along with its associated module path.

        Args:
            module_path (str): The path to the module.
            line_number (int): The line number covered by a failing test.
        """
        cur = self._connection.cursor()
        cur.execute(
            f"INSERT INTO {self._Failing_line_number_table} VALUES (NULL, ?, ?)",
            (module_path, line_number),
        )

        self._connection.commit()

    def select_distinct_failing_module_paths(self) -> List[str]:
        """
        Selects distinct module paths with failing lines.

        Returns:
            List[str]: List of distinct module paths with failing lines.
        """
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT DISTINCT ModulePath FROM {self._Failing_line_number_table}"
        )

        entities = [x[0] for x in cur.fetchall()]
        return entities

    def select_failing_line_numbers_for_module_path(
            self,
            module_path: str
    ) -> List[int]:
        """
        Selects the line numbers covered by failing tests, in the given module.

        Args:
            module_path (str): The path to the module.

        Returns:
            List[int]: List of line numbers covered by failing tests.
        """
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT LineNumber FROM {self._Failing_line_number_table} WHERE ModulePath = ?",
            (module_path,),
        )

        entities = [x[0] for x in cur.fetchall()]
        return entities

    def insert_mutant(
        self,
        mutant_id: str,
        module_path: str,
        line_number: int,
        operator_name: str,
        module_diff: str,
        start_pos: int,
        end_pos: int,
        timeout: int = -1,
        has_missing_tests: int = -1,
    ):
        """
        Inserts information about a mutant into the mutant info table.

        Args:
            mutant_id (str): The ID of the mutant.
            module_path (str): The path to the module containing the mutant.
            line_number (int): The line number of the mutant.
            operator_name (str): The name of the mutation operator.
            module_diff (str): The diff representation of the mutation.
            start_pos (int): The start position of the mutant in the module.
            end_pos (int): The end position of the mutant in the module.
            timeout (int, optional): Timeout value for the mutant. Defaults to -1.
            has_missing_tests (int, optional): Indicates whether the mutant has missing tests. Defaults to -1.
        """
        cur = self._connection.cursor()
        cur.execute(
            f"INSERT INTO {self._Mutant_info_table} VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                mutant_id,
                module_path,
                line_number,
                operator_name,
                module_diff,
                start_pos,
                end_pos,
                timeout,
                has_missing_tests,
            ),
        )

        self._connection.commit()

    def select_number_of_tests(self):
        """
        Selects the number of passed and failed test cases.

        Returns:
            Tuple[int, int]: The number of passed tests and failed tests.
        """
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
        """
        Selects a test case by its name.

        Args:
            test_name (str): The name of the test case.

        Returns:
            tuple: The details of the test case (TestName, Type, TestTraceBack, Timeout, Target).
        """
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
        """
        Inserts score terms for a mutant.

        Args:
            mutant_id (str): The ID of the mutant.
            entity (str): The associated entity.
            failed_to_passed (int): Number of failed-to-passed transitions.
            passed_to_failed (int): Number of passed-to-failed transitions.
            failed_changed (int): Number of changes in failed status.
        """
        cur = self._connection.cursor()
        cur.execute(
            f"INSERT INTO {self._Mutant_score_term_table} VALUES (NULL, ?, ?, ?, ?, ?, -1, -1)",
            (mutant_id, entity, failed_to_passed, passed_to_failed, failed_changed),
        )

        self._connection.commit()

    def select_total_failed_to_passed_and_passed_to_failed(self) -> Tuple[int, int]:
        """
        Selects the total counts of failed-to-passed and passed-to-failed transitions.

        Returns:
            Tuple[int, int]: The total counts for failed-to-passed and passed-to-failed.
        """
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
            self,
            mutant_id,
            mutant_muse_score,
            mutant_metallaxis_score
    ):
        """
        Selects all the mutant score terms.

        Returns:
            list: A list of tuples containing the mutant ID and its score terms.
        """
        cur = self._connection.cursor()
        cur.execute(
            f"UPDATE {self._Mutant_score_term_table} SET MutantMuseScore = ?, "
            f"MutantMetallaxisScore = ? WHERE MutantId = ?",
            (mutant_muse_score, mutant_metallaxis_score, mutant_id),
        )

        self._connection.commit()

    def select_distinct_all_mutant_score_terms_entities(self):
        """
        Selects all distinct entities from the mutant score term table.

        Returns:
            List[str]: A list of distinct entities from the mutant score term table.
        """
        cur = self._connection.cursor()
        cur.execute(f"SELECT DISTINCT Entity FROM {self._Mutant_score_term_table}")
        rows = cur.fetchall()

        entities = [x[0] for x in rows]
        return entities

    def select_mutant_score_terms_scores(self, entity):
        """
        Selects the Muse and Metallaxis scores for a given entity from the mutant score term table.

        Args:
            entity (str): The entity for which to retrieve the scores.

        Returns:
            dict: A dictionary containing the Muse and Metallaxis scores for the given entity.
                Example: {"Muse": [score1, score2], "Metallaxis": [score3, score4]}
        """
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
            self,
            entity: str,
            entity_muse_score: float,
            entity_metallaxis_score: float
    ):
        """
        Inserts a score for an entity into the entity score table.

        Args:
            entity (str): The name of the entity.
            entity_muse_score (float): The Muse score for the entity.
            entity_metallaxis_score (float): The Metallaxis score for the entity.
        """
        cur = self._connection.cursor()
        cur.execute(
            f"INSERT INTO {self._Entity_score_table} VALUES (NULL, ?, ?, ?)",
            (entity, entity_muse_score, entity_metallaxis_score),
        )

        self._connection.commit()

    def select_all_ranked_entities(self):
        """
        Selects all entities ranked by their Muse and Metallaxis scores.

        Returns:
            dict: A dictionary containing the ranked entities by Muse and Metallaxis scores.
                Example: {"Muse": [(entity1, score1), (entity2, score2)], "Metallaxis": [(entity3, score3)]}
        """
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

    def select_top_n_ranked_entities(self, top_n):
        """
        Selects the top N entities ranked by their Muse and Metallaxis scores.

        Args:
            top_n (int): The number of top-ranked entities to retrieve.

        Returns:
            dict: A dictionary containing the top N ranked entities by Muse and Metallaxis scores.
                Example: {"Muse": [(entity1, score1), (entity2, score2)], "Metallaxis": [(entity3, score3)]}
        """
        cur = self._connection.cursor()
        cur.execute(
            f"SELECT Entity, EntityMuseScore FROM {self._Entity_score_table} "
            f"ORDER BY EntityMuseScore DESC LIMIT ?",
            (top_n,),
        )
        scores_muse = cur.fetchall()

        cur = self._connection.cursor()
        cur.execute(
            f"SELECT Entity, EntityMetallaxisScore FROM {self._Entity_score_table} "
            f"ORDER BY EntityMetallaxisScore DESC LIMIT ?",
            (top_n,),
        )
        scores_metallaxis = cur.fetchall()

        return {"Muse": scores_muse, "Metallaxis": scores_metallaxis}

    def insert_test_time(self, test_name: str, test_time: int):
        """
        Inserts the execution time for a test case into the test time table.

        Args:
            test_name (str): The name of the test case.
            test_time (int): The execution time of the test case in milliseconds.
        """
        cur = self._connection.cursor()
        cur.execute(
            f"INSERT INTO {self._Test_time_table} VALUES (NULL, ?, ?)",
            (test_name, test_time),
        )

        self._connection.commit()

    def select_max_test_time(self):
        """
        Selects the maximum test execution time from the test time table.

        Returns:
            int: The maximum execution time of all test cases.
        """
        cur = self._connection.cursor()
        cur.execute(f"SELECT MAX(TestTime) FROM {self._Test_time_table}")
        row = cur.fetchone()
        max_time = row[0]

        return max_time

    def update_mutant_as_timeout(self, mutant_id):
        """
        Marks a mutant as having timed out in the mutant info table.

        Args:
            mutant_id (str): The ID of the mutant to update.
        """
        cur = self._connection.cursor()
        cur.execute(
            f"UPDATE {self._Mutant_info_table} SET Timeout = ? " f"WHERE MutantId = ?",
            (1, mutant_id),
        )

        self._connection.commit()

    def update_mutant_as_having_missing_tests(self, mutant_id):
        """
        Marks a mutant as having missing tests in the mutant info table.

        Args:
            mutant_id (str): The ID of the mutant to update.
        """
        cur = self._connection.cursor()
        cur.execute(
            f"UPDATE {self._Mutant_info_table} SET HasMissingTests = ? "
            f"WHERE MutantId = ?",
            (1, mutant_id),
        )

        self._connection.commit()

    def insert_pyllmut_mutant_info(
        self,
        prompt_content: str,
        line_number: int,
        sent_token_count: int,
        response_content: str,
        received_token_count: int,
        diff_content: str,
        pre_code_model: str,
        after_code_model: str,
        pre_code_refined: str,
        after_code_refined: str,
        mutant_type: str
    ):
        """
        Inserts a new PyLLMut mutant info object.

        Args:
            prompt_content (str): The content of the prompt.
            line_number (int): The line number where the mutation was applied.
            sent_token_count (int): The number of sent tokens when using the LLM.
            response_content (str): The response returned from the model.
            received_token_count (int): The number of tokens in the response.
            diff_content (str): A diff representation of the changes between the original and mutated code.
            pre_code_model (str): The content of the line before mutation, as returned by the model.
            after_code_model (str): The content of the line after mutation, as returned by the model.
            pre_code_refined (str): The actual content of the line before mutation, extracted from the original code.
            after_code_refined (str): The content of the line after mutation, with fixed indentation.
            mutant_type (str): The type of the mutant.
        """
        cur = self._connection.cursor()

        cur.execute(
            f"""
            INSERT INTO {self._Pyllmut_mutant_info_table} (
                PromptContent, LineNumber, SentTokenCount, ResponseContent, 
                ReceivedTokenCount, DiffContent, PreCodeModel, AfterCodeModel, 
                PreCodeRefined, AfterCodeRefined, MutantType
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                prompt_content, line_number, sent_token_count, response_content,
                received_token_count, diff_content, pre_code_model, after_code_model,
                pre_code_refined, after_code_refined, mutant_type
            ),
        )

        self._connection.commit()

    def insert_pyllmut_bad_response_info(
        self,
        prompt_content: str,
        line_number: int,
        sent_token_count: int,
        response_content: str,
        received_token_count: int
    ):
        """
        Inserts a new PyLLMut response info object representing an unparsable response (e.g., bad JSON) from the model.

        Args:
            prompt_content (str): The content of the prompt.
            line_number (int): The line number where the mutation was applied.
            sent_token_count (int): The number of sent tokens when using the LLM.
            response_content (str): The response returned from the model.
            received_token_count (int): The number of tokens in the response.
        """
        cur = self._connection.cursor()

        cur.execute(
            f"""
            INSERT INTO {self._Pyllmut_bad_response_info_table} (
                PromptContent, LineNumber, SentTokenCount, ResponseContent, 
                ReceivedTokenCount
            ) VALUES (?, ?, ?, ?, ?)
            """,
            (
                prompt_content, line_number, sent_token_count, response_content,
                received_token_count
            ),
        )

        self._connection.commit()

    def insert_pyllmut_timeout_info(
            self,
            prompt_content: str,
            line_number: int,
    ):
        """
        Inserts a new PyLLMut prompt info object representing a session timeout for a line number.

        Args:
            prompt_content (str): The content of the prompt.
            line_number (int): The line number where the mutation was applied.
        """
        cur = self._connection.cursor()

        cur.execute(
            f"""
            INSERT INTO {self._Pyllmut_timeout_info_table} (
                PromptContent, LineNumber
            ) VALUES (?, ?)
            """,
            (
                prompt_content, line_number
            ),
        )

        self._connection.commit()
