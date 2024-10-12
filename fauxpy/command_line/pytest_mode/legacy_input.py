from typing import List, Optional

from fauxpy.session_lib.fl_file_manager import FlFileManager
from fauxpy.session_lib.fl_type import FlGranularity, FlFamily
from fauxpy.session_lib.path_lib import PythonPath
from fauxpy.session_lib.target_tsts import TargetFailingTests
from fauxpy.session_lib.ts_lib import TargetedFailingTst


def get_granularity_legacy(fl_granularity: FlGranularity) -> str:
    legacy_granularity = "statement"
    if fl_granularity == FlGranularity.Function:
        legacy_granularity = "function"

    return legacy_granularity


def get_family_legacy(fl_family: FlFamily) -> str:
    legacy_family_name = "sbfl"
    if fl_family == FlFamily.Mbfl:
        legacy_family_name = "mbfl"
    elif fl_family == FlFamily.Ps:
        legacy_family_name = "ps"
    elif fl_family == FlFamily.St:
        legacy_family_name = "st"
    elif fl_family == FlFamily.CollectMbfl:
        legacy_family_name = "collectmbfl"
    elif fl_family == FlFamily.CollectPsInfo:
        legacy_family_name = "collectpsinfo"
    elif fl_family == FlFamily.CollectPsRun:
        legacy_family_name = "collectpsrun"

    return legacy_family_name


def get_src_legacy(target_src: PythonPath) -> str:
    return target_src.get_relative_path()


def get_exclude_legacy(exclude_list: List[PythonPath]) -> List[str]:
    legacy_exclude = [x.get_relative_path() for x in exclude_list]

    return legacy_exclude


def get_top_n_legacy(top_n: int) -> str:
    return str(top_n)


def get_targeted_failing_test_list_legacy(
    targeted_failing_test_list: List[TargetedFailingTst],
) -> Optional[TargetFailingTests]:
    if len(targeted_failing_test_list) == 0:
        return None
    legacy_targeted_failing_test_list = [
        x.get_relative_test_name() for x in targeted_failing_test_list
    ]

    return TargetFailingTests(legacy_targeted_failing_test_list)


def save_config_info_legacy(pytest_config, session_file_manager: FlFileManager):
    target_src_opt = pytest_config.getoption("--src")
    exclude_list = convert_argument_list_string_to_list(
        pytest_config.getoption("--exclude")
    )
    family_name_opt = pytest_config.getoption("--family")
    granularity_name_opt = pytest_config.getoption("--granularity")
    top_n_opt = pytest_config.getoption("--top-n")

    failing_file_opt = pytest_config.getoption("--failing-file")
    failing_list_opt = pytest_config.getoption("--failing-list")

    target_failing_tests = None
    if failing_file_opt is not None:
        target_failing_tests = TargetFailingTests.from_file(failing_file_opt)
    elif failing_list_opt is not None:
        failing_list = convert_argument_list_string_to_list(failing_list_opt)
        target_failing_tests = TargetFailingTests.from_list_string(failing_list)

    target_failing_tests_list = (
        target_failing_tests.get_failing_tests()
        if target_failing_tests is not None
        else ["No specific target failing tests"]
    )

    session_file_manager.save_config_to_file(
        src=target_src_opt,
        exclude=exclude_list,
        family=family_name_opt,
        granularity=granularity_name_opt,
        top_n=top_n_opt,
        target_failing_tests=target_failing_tests_list,
    )


def convert_argument_list_string_to_list(exclude_string: str) -> List[str]:
    stripped_string = exclude_string.strip()
    brackets_removed = stripped_string[1:-1]
    if brackets_removed == "":
        return []
    else:
        items = brackets_removed.split(",")
        items_stripped = [x.strip() for x in items]

        return items_stripped
