from typing import List, Tuple

from fauxpy.fault_localization.ps.db_manager import PsDbManager


class SeenExceptionManager:
    def __init__(self, db_manager: PsDbManager):
        self._db_manager = db_manager

    def _get_seen_exceptions_store_db(self, exceptions: List[Tuple[str, str, int]]):
        for i, exp in enumerate(exceptions):
            test_name, file_path, line_number = exp
            exception_name = f"Exception_{i}"

            self._db_manager.insert_seen_exceptions(
                test_name=test_name,
                file_path=file_path,
                line_number=line_number,
                exception_name=exception_name,
            )

    def get_seen_exceptions_store_db(self):
        """
        Stores in database the info about exception raises
        that happen while running the failing tests.
        """

        exceptions = self._db_manager.select_test_case_exceptions()
        self._get_seen_exceptions_store_db(exceptions)
