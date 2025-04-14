"""
Module for representing a targeted failing test case in a fault localization session.

A targeted failing test is a failing test that a fault localization technique focuses on
to isolate and locate a specific bug in the presence of multiple bugs.
"""

from typing import Optional

from fauxpy.session_lib.fauxpy_path import FauxpyPath


class TargetedFailingTst:
    """Represents a failing test case targeted for fault localization.

    This class identifies a specific test case
    that triggers a bug, enabling fault localization to isolate it from other failures.
    """

    def __init__(
            self,
            module_path: FauxpyPath,
            class_name: Optional[str],
            function_name: str
    ):
        """Initializes a TargetedFailingTst.

        Args:
            module_path (FauxpyPath): Path to the test module.
            class_name (Optional[str]): Name of the test class, if any.
            function_name (str): Name of the test function.
        """

        self._module_path = module_path
        self._class_name = class_name
        self._function_name = function_name

    def get_relative_test_name(self) -> str:
        """Returns the test's relative name in Pytest-compatible format.

        Returns:
            str: Relative test name in the format
                'module_path::class_name::function_name' or
                'module_path::function_name' if the test is not part of a class.
        """
        if self._class_name is None:
            return f"{self._module_path.get_relative()}::{self._function_name}"
        return f"{self._module_path.get_relative()}::{self._class_name}::{self._function_name}"

    def __str__(self) -> str:
        """Returns the string representation of the targeted test.

        Returns:
            str: Human-readable identifier of the test.
        """
        return self.get_relative_test_name()
