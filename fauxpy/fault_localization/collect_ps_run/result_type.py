from typing import List, Tuple, Optional


class CollectPsRunResult:
    def __init__(
        self,
        test_case_table: List[Tuple[str, str, str]],
        seen_exception_list: List[Tuple[str, str]],
    ):
        self.testCaseTable = test_case_table
        self.seenExceptionList = seen_exception_list

    def get_test_result(self, test_name: str) -> Tuple[Optional[str], Optional[float]]:
        for currentTest, testType, stacktrace, timeoutStat in self.testCaseTable:
            if currentTest == test_name:
                return testType, timeoutStat
        return None, None

    def get_test_seen_exception_list(self, test_name: str) -> str:
        for item in self.seenExceptionList:
            if item[0] == test_name:
                return item[1]
        return ""

    def is_test_case_table_empty_or_none(self):
        return self.testCaseTable is None or len(self.testCaseTable) == 0
