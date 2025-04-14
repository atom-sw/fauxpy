from abc import abstractmethod
from typing import List

from .fl_type import FlGranularity, FlFamily
from .fl_session import FlSession
from .fauxpy_path import FauxpyPath
from .targeted_failing_tst import TargetedFailingTst


class FlFamilySession(FlSession):
    @abstractmethod
    def get_fl_granularity(self) -> FlGranularity:
        """
        Returns the fault localization granularity.

        Returns:
            FlGranularity: The fault localization granularity option.
        """
        pass

    @abstractmethod
    def get_fl_family(self) -> FlFamily:
        """
        Returns the fault localization family.

        Returns:
            FlFamily: The fault localization family option.
        """
        pass

    @abstractmethod
    def get_project_working_directory(self) -> FauxpyPath:
        """
        Returns the working directory for the project.

        Returns:
            FauxpyPath: The project working directory.
        """
        pass

    @abstractmethod
    def get_targeted_failing_test_list(self) -> List[TargetedFailingTst]:
        """
        Returns the list of targeted failing tests for fault localization.

        Returns:
            list: A list of targeted failing tests.
        """
        pass
