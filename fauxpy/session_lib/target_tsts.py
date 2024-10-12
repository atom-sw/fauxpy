from typing import List

from fauxpy.session_lib import naming_lib


class TargetFailingTests(object):
    def __init__(self, target_failing_tests_list: List[str]):
        self._targetFailingTestsList = target_failing_tests_list

    def get_failing_tests(self):
        return self._targetFailingTestsList

    @classmethod
    def from_file(cls, file_path):
        try:
            with open(file_path, "r") as file:
                content = file.read()
            list_content = content.strip().split("\n")
            list_content_striped = [x.strip() for x in list_content]
            list_content_striped_no_comments = list(
                filter(lambda x: not x.startswith("#"), list_content_striped)
            )
            if len(list_content_striped_no_comments) == 0 or all(
                [x == "" for x in list_content_striped_no_comments]
            ):
                return None
            else:
                return TargetFailingTests(list_content_striped_no_comments)
        except FileNotFoundError:
            return None

    @classmethod
    def from_list_string(cls, failing_list):
        failing_list_striped = [x.strip() for x in failing_list]
        if len(failing_list_striped) == 0:
            return None
        else:
            return TargetFailingTests(failing_list_striped)

    def is_target_test(self, current_test_path, current_test_method_name):
        # currentTestFullPath = "::".join([currentTestPath, currentTestMethodName])
        current_test_full_path_generalized = naming_lib.get_generalized_test_name(
            current_test_path, current_test_method_name
        )
        for targetTest in self._targetFailingTestsList:
            # reformattedTargetFilePath = _reformatPytestTest(targetTest)
            if current_test_full_path_generalized == targetTest:
                return True
        return False
