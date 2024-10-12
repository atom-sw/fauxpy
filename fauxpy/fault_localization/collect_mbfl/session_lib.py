from pathlib import Path

from fauxpy.fault_localization.collect_mbfl.db_manager import CollectMbflDBManager
from fauxpy.fault_localization.collect_mbfl.reporter_lib import CollectMbflReporter
from fauxpy.fault_localization.collect_mbfl.session_file import (
    CollectMbflSessionFileManager,
)
from fauxpy.fault_localization.util.traceback_lib import TracebackParser
from fauxpy.session_lib.fl_session import FlSession
from fauxpy.session_lib.pytest_tst_item import PytestTstItem


class CollectMbflSession(FlSession):
    def __init__(self, report_directory_path: Path, project_working_directory: Path):
        self._db_manager = CollectMbflDBManager(report_directory_path)
        self._reporter = CollectMbflReporter(self._db_manager)
        self._session_file_manager = CollectMbflSessionFileManager(
            report_directory_path
        )
        self._traceback_parser = TracebackParser(project_working_directory)

    @staticmethod
    def __pretty_representation():
        return "Collect MBFL Mode"

    def __str__(self):
        return self.__pretty_representation()

    def __repr__(self):
        return self.__pretty_representation()

    def run_test_call(self, item):
        pass

    def run_test_make_report(self, item, call):
        pass

    def terminal_summary(self, terminal_reporter, exit_status):
        for key, value in terminal_reporter.stats.items():
            if key in ["passed", "failed"]:
                for test_report in value:
                    test_information = PytestTstItem(test_report)
                    test_name = test_information.get_test_name()

                    test_trace_back = ""
                    timeout_stat = -1
                    if key == "failed":
                        repr_traceback = test_report.longrepr.reprtraceback
                        test_trace_back = (
                            self._traceback_parser.get_short_trace_back_info(
                                repr_traceback
                            )
                        )
                        # TODO: probably not needed anymore as --timeout_method is set to thread
                        if self._traceback_parser.has_timeout_happened(
                            test_report.longreprtext
                        ):
                            timeout_stat = 1

                    self._db_manager.insert_test_case(
                        test_name=test_name,
                        test_type=key,
                        short_traceback=test_trace_back,
                        timeout_stat=timeout_stat,
                    )

        test_case_table = self._reporter.get_json_test_case_table()
        self._session_file_manager.save_in_collect_mode_test_case_table(test_case_table)
        self._db_manager.end()
        return {"Default": []}
