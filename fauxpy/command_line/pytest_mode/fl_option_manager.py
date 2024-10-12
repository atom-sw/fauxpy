from pathlib import Path
from typing import List

import pytest

from fauxpy.fault_localization.collect_mbfl.session_lib import CollectMbflSession
from fauxpy.fault_localization.collect_ps_info.session_lib import CollectPsInfoSession
from fauxpy.fault_localization.collect_ps_run.session_lib import CollectPsRunSession
from fauxpy.fault_localization.mbfl.session_lib import MbflSession
from fauxpy.fault_localization.ps.session_lib import PsSession
from fauxpy.fault_localization.sbfl.session_lib import SbflSession
from fauxpy.fault_localization.st.session_lib import StSession
from fauxpy.session_lib.fl_file_manager import FlFileManager
from fauxpy.session_lib.fl_path_manager import FlPathManager
from fauxpy.session_lib.fl_session import FlSession
from fauxpy.session_lib.fl_type import FlFamily, FlGranularity
from fauxpy.session_lib.path_lib import PythonPath
from fauxpy.session_lib.ts_lib import TargetedFailingTst


class FlOptionManager:
    """
    Manages fault localization options and session creation.

    This class handles the parsing and validation of command-line options
    related to fault localization. It also creates and configures FauxPy
    session objects based on the provided options.
    """

    def __init__(
        self,
        project_working_directory,
        target_src_opt,
        exclude_list_opt,
        fl_family_opt,
        fl_granularity_opt,
        top_n_opt,
        failing_file_opt,
        failing_list_opt,
        file_or_dir,
    ):
        """
        Initializes the FlOptionManager with command-line options.

        Args:
            project_working_directory (str): The project working directory.
            target_src_opt (str): The source directory for fault localization.
            exclude_list_opt (str): Comma-separated list of paths to exclude.
            fl_family_opt (str): Fault localization family option (e.g., sbfl, mbfl).
            fl_granularity_opt (str): Fault localization granularity option (e.g., statement).
            top_n_opt (str): Top N results to consider, or -1 for all results.
            failing_file_opt (str): Path to the file containing targeted failing tests.
            failing_list_opt (str): Comma-separated list of targeted failing tests.
            file_or_dir (str): Additional file or directory option.
        """
        self._project_working_directory = Path(project_working_directory)
        self._target_src = self._get_validate_target_src(target_src_opt)
        self._exclude_list = self._get_validate_exclude_list(exclude_list_opt)
        self._fl_family = self._get_validate_fl_family(fl_family_opt)
        self._fl_granularity = self._get_validate_fl_granularity(fl_granularity_opt)
        self._top_n = self._get_validate_top_n(top_n_opt)
        self._targeted_failing_test_list = (
            self._get_validate_targeted_failing_test_list(
                failing_file_opt, failing_list_opt
            )
        )
        self._file_or_dir_opt = file_or_dir
        self._path_manager = FlPathManager(
            self._project_working_directory, self._fl_family, self._fl_granularity
        )
        self._fl_file_manager = None

    def get_fl_family(self) -> FlFamily:
        """
        Returns the fault localization family.

        Returns:
            FlFamily: The fault localization family option.
        """
        return self._fl_family

    def get_fl_granularity(self) -> FlGranularity:
        """
        Returns the fault localization granularity.

        Returns:
            FlGranularity: The fault localization granularity option.
        """
        return self._fl_granularity

    def get_targeted_failing_test_list(self) -> List[TargetedFailingTst]:
        """
        Returns the list of targeted failing tests.

        Returns:
            List[TargetedFailingTst]: The list of targeted failing tests.
        """
        return self._targeted_failing_test_list

    def get_session_file_manager(self):
        """
        Returns the file manager for the fault localization session.

        If the file manager is not yet created, it initializes it.

        Returns:
            FlFileManager: The fault localization file manager.
        """
        if self._fl_file_manager is None:
            report_directory_path = self._path_manager.get_report_directory_path()
            self._fl_file_manager = FlFileManager(report_directory_path)
        return self._fl_file_manager

    def get_fl_session(self) -> FlSession:
        """
        Creates and returns a fault localization session based on the family option.

        Returns:
            FlSession: The created fault localization session.
        """
        report_directory_path = self._path_manager.get_report_directory_path()

        fauxpy_session = None
        if self._fl_family == FlFamily.Sbfl:
            fauxpy_session = SbflSession(
                self._target_src,
                self._exclude_list,
                self._fl_granularity,
                self._top_n,
                self._targeted_failing_test_list,
                report_directory_path,
                self._project_working_directory,
            )
        elif self._fl_family == FlFamily.St:
            fauxpy_session = StSession(
                self._target_src,
                self._exclude_list,
                self._top_n,
                self._targeted_failing_test_list,
                report_directory_path,
                self._project_working_directory,
            )
        elif self._fl_family == FlFamily.Mbfl:
            fauxpy_session = MbflSession(
                self._target_src,
                self._exclude_list,
                self._fl_granularity,
                self._top_n,
                self._targeted_failing_test_list,
                self._file_or_dir_opt,
                report_directory_path,
                self._project_working_directory,
            )
        elif self._fl_family == FlFamily.Ps:
            fauxpy_session = PsSession(
                self._target_src,
                self._exclude_list,
                self._fl_granularity,
                self._top_n,
                self._targeted_failing_test_list,
                report_directory_path,
                self._project_working_directory,
            )
        elif self._fl_family == FlFamily.CollectMbfl:
            fauxpy_session = CollectMbflSession(
                report_directory_path, self._project_working_directory
            )
        elif self._fl_family == FlFamily.CollectPsInfo:
            fauxpy_session = CollectPsInfoSession(
                report_directory_path, self._project_working_directory
            )
        elif self._fl_family == FlFamily.CollectPsRun:
            fauxpy_session = CollectPsRunSession(
                report_directory_path, self._project_working_directory
            )

        assert fauxpy_session is not None

        return fauxpy_session

    def _get_validate_target_src(self, target_src_opt: str) -> PythonPath:
        """
        Validates the target source directory option.

        Args:
            target_src_opt (str): The path to validate.

        Returns:
            PythonPath: The validated target source directory.

        Raises:
            pytest.UsageError: If the path does not exist.
        """
        target_src_path_item = PythonPath(
            self._project_working_directory, target_src_opt
        )

        error_message = (
            f"{target_src_opt} is not a valid option. "
            f"Path {target_src_path_item} does not exist."
        )

        if not target_src_path_item.exists():
            raise pytest.UsageError(error_message)

        return target_src_path_item

    def _get_validate_exclude_list(self, exclude_list_opt: str) -> List[PythonPath]:
        """
        Validates the exclude list option.

        Args:
            exclude_list_opt (str): Comma-separated list of paths to exclude.

        Returns:
            List[PythonPath]: The validated list of excluded paths.

        Raises:
            pytest.UsageError: If any path does not exist.
        """
        exclude_str_list = self._comma_string_list_to_python_list(exclude_list_opt)

        exclude_path_item_list = []
        for exclude_str_item in exclude_str_list:
            exclude_path_item = PythonPath(
                self._project_working_directory, exclude_str_item
            )
            if not exclude_path_item.exists():
                error_message = (
                    f"{exclude_list_opt} is not a valid option. "
                    f"Path {exclude_path_item} does not exist."
                )
                raise pytest.UsageError(error_message)
            exclude_path_item_list.append(exclude_path_item)

        return exclude_path_item_list

    @staticmethod
    def _get_validate_fl_family(fl_family_opt: str) -> FlFamily:
        """
        Validates the fault localization family option.

        Args:
            fl_family_opt (str): The fault localization family option.

        Returns:
            FlFamily: The validated fault localization family.

        Raises:
            pytest.UsageError: If the option is not valid.
        """
        error_message = (
            f"{fl_family_opt} is not a valid option. "
            f"Correct options: sbfl, mbfl, ps, st."
        )

        if fl_family_opt not in [
            "sbfl",
            "st",
            "mbfl",
            "ps",
            "collectmbfl",
            "collectpsinfo",
            "collectpsrun",
        ]:
            raise pytest.UsageError(error_message)

        fl_family = FlFamily.Sbfl
        if fl_family_opt == "mbfl":
            fl_family = FlFamily.Mbfl
        elif fl_family_opt == "ps":
            fl_family = FlFamily.Ps
        elif fl_family_opt == "st":
            fl_family = FlFamily.St
        elif fl_family_opt == "collectmbfl":
            fl_family = FlFamily.CollectMbfl
        elif fl_family_opt == "collectpsinfo":
            fl_family = FlFamily.CollectPsInfo
        elif fl_family_opt == "collectpsrun":
            fl_family = FlFamily.CollectPsRun

        return fl_family

    @staticmethod
    def _get_validate_fl_granularity(fl_granularity_opt: str) -> FlGranularity:
        """
        Validates the fault localization granularity option.

        Args:
            fl_granularity_opt (str): The fault localization granularity option (e.g., statement).

        Returns:
            FlGranularity: The validated fault localization granularity.

        Raises:
            pytest.UsageError: If the option is not valid.
        """
        error_message = (
            f"{fl_granularity_opt} is not a valid option. "
            f"Correct options: statement and function."
        )

        if fl_granularity_opt not in ["statement", "function"]:
            raise pytest.UsageError(error_message)

        fl_granularity = FlGranularity.Statement
        if fl_granularity_opt == "function":
            fl_granularity = FlGranularity.Function

        return fl_granularity

    @staticmethod
    def _get_validate_top_n(top_n_opt: str) -> int:
        """
        Validates the top N results option.

        Args:
            top_n_opt (str): The top N option, which should be -1 or an integer >= 1.

        Returns:
            int: The validated top N value.

        Raises:
            pytest.UsageError: If the option is not a valid integer or is less than -1 or zero.
        """
        error_message = (
            f"{top_n_opt} is not a valid option. "
            f"Correct options: -1 or an integer x, where x >= 1."
        )
        try:
            int_value = int(top_n_opt)
        except:
            raise pytest.UsageError(error_message)

        if int_value < -1 or int_value == 0:
            raise pytest.UsageError(error_message)

        return int_value

    @staticmethod
    def _comma_string_list_to_python_list(comma_string_list: str) -> List[str]:
        """
        Converts a comma-separated string list to a Python list of strings.

        Args:
            comma_string_list (str): The comma-separated string list to convert.

        Returns:
            List[str]: The list of strings obtained from the input string.
        """
        stripped_string = comma_string_list.strip()
        brackets_removed = stripped_string[1:-1]
        if brackets_removed == "":
            return []
        else:
            items = brackets_removed.split(",")
            stripped_item_list = [x.strip() for x in items]

            return stripped_item_list

    @staticmethod
    def _multi_line_string_list_to_python_list(
        multi_line_string_list: str,
    ) -> List[str]:
        """
        Converts a multi-line string list to a Python list of strings.

        Args:
            multi_line_string_list (str): The multi-line string list to convert.

        Returns:
            List[str]: The list of strings obtained from the input string, excluding comments and empty lines.
        """
        list_content = multi_line_string_list.strip().split("\n")
        list_content_striped = [x.strip() for x in list_content]
        list_content_striped_no_comments = list(
            filter(lambda x: not x.startswith("#"), list_content_striped)
        )
        if len(list_content_striped_no_comments) == 0 or all(
            [x == "" for x in list_content_striped_no_comments]
        ):
            return []
        else:
            return list_content_striped_no_comments

    def _get_validate_targeted_failing_test_list(
        self, failing_file_opt: str, failing_list_opt: str
    ) -> List[TargetedFailingTst]:
        """
        Validates and returns the list of targeted failing tests based on the provided options.

        Args:
            failing_file_opt (str): Path to the file containing targeted failing tests (optional).
            failing_list_opt (str): Comma-separated list of targeted failing tests (optional).

        Returns:
            List[TargetedFailingTst]: The validated list of targeted failing tests.

        Raises:
            pytest.UsageError: If both file and list options are specified, or if any test item or path is invalid.
        """
        if failing_file_opt is not None and failing_list_opt is not None:
            error_message = (
                "You may specify either "
                "--failing-list or --failing-file,"
                " but not both."
            )
            raise pytest.UsageError(error_message)

        targeted_failing_test_string_list = []
        if failing_list_opt is not None:
            targeted_failing_test_string_list = self._comma_string_list_to_python_list(
                failing_list_opt
            )
        elif failing_file_opt is not None:
            failing_file_path = self._project_working_directory / failing_file_opt
            if not failing_file_path.exists():
                error_message = (
                    f"{failing_file_opt} is not a valid option. "
                    f"Path {failing_file_path} does not exist."
                )
                raise pytest.UsageError(error_message)
            failing_file_content = failing_file_path.read_text()
            targeted_failing_test_string_list = (
                self._multi_line_string_list_to_python_list(failing_file_content)
            )

        targeted_failing_test_item_list = []
        for targeted_failing_test_string_item in targeted_failing_test_string_list:
            target_failing_test_item = self._get_validate_targeted_failing_test_item(
                targeted_failing_test_string_item
            )
            targeted_failing_test_item_list.append(target_failing_test_item)
        return targeted_failing_test_item_list

    def _get_validate_targeted_failing_test_item(
        self, targeted_failing_test_string_item
    ) -> TargetedFailingTst:
        """
        Validates and returns a targeted failing test item based on the provided string.

        Args:
            targeted_failing_test_string_item (str): The string representing the targeted failing test.

        Returns:
            TargetedFailingTst: The validated targeted failing test item.

        Raises:
            pytest.UsageError: If the test item format is incorrect or the file containing the test does not exist.
        """
        content_parts = targeted_failing_test_string_item.split("::")
        if len(content_parts) == 2:
            module_path_item = PythonPath(
                self._project_working_directory, content_parts[0]
            )
            if not module_path_item.exists():
                error_message = (
                    f"{targeted_failing_test_string_item} is not a valid option. "
                    f"Path {module_path_item} does not exist."
                )
                raise pytest.UsageError(error_message)
            function_name = content_parts[1]
            targeted_failing_test_item = TargetedFailingTst(
                module_path_item, None, function_name
            )
        elif len(content_parts) == 3:
            module_path_item = PythonPath(
                self._project_working_directory, content_parts[0]
            )
            if not module_path_item.exists():
                error_message = (
                    f"{targeted_failing_test_string_item} is not a valid option. "
                    f"Path {module_path_item} does not exist."
                )
                raise pytest.UsageError(error_message)
            class_name = content_parts[1]
            function_name = content_parts[2]
            targeted_failing_test_item = TargetedFailingTst(
                module_path_item, class_name, function_name
            )
        else:
            error_message = (
                f"{targeted_failing_test_string_item} is not a valid option. "
                f"The format of the test is incorrect."
            )
            raise pytest.UsageError(error_message)

        return targeted_failing_test_item
