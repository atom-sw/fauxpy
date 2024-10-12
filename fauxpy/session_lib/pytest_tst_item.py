"""
This module provides functionality to extract information
from Pytest test items returned by various Pytest hooks.
"""


class PytestTstItem:
    def __init__(self, pytest_tst_item):
        self.location = pytest_tst_item.location
        self.node_id = pytest_tst_item.nodeid

    def _is_inherited_test_case(self):
        return self.location[0] != self._get_caller_path()

    def _get_caller_path(self):
        return self.node_id.split("::")[0]

    def _get_line_number(self):
        if self._is_inherited_test_case():
            test_line_number = -1
        else:
            test_line_number = self.location[1]
        return test_line_number

    def get_path(self):
        # Due to some unusual test cases in Pandas 54,
        # which are inherited across different test modules
        # (e.g., pandas/tests/extension/test_period.py),
        # we need to generate unique test names.
        # Without this, multiple executed test cases
        # may end up having the same names, causing conflicts.
        if self._is_inherited_test_case():
            test_path = self._get_caller_path()
        else:
            test_path = self.location[0]

        return test_path

    def get_method_name(self):
        test_method_name = self.location[2]
        return test_method_name

    @staticmethod
    def _quote_free_test_method_name(method_name: str):
        new_test_name = method_name.replace("'", "XquoteX").replace(
            '"', "XdoubleQuoteX"
        )
        return new_test_name

    def get_test_name(self):
        test_name = (
            self.get_path()
            + "::"
            + str(self._get_line_number())
            + "::"
            + self._quote_free_test_method_name(self.get_method_name())
        )
        return test_name
