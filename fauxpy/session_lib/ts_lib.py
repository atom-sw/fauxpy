from typing import Optional

from fauxpy.session_lib.path_lib import PythonPath


class TargetedFailingTst:
    def __init__(
        self, module_path: PythonPath, class_name: Optional[str], function_name: str
    ):
        self._module_path = module_path
        self._class_name = class_name
        self._function_name = function_name

    def get_relative_test_name(self):
        relative_test_name = f"{self._module_path.get_relative_path()}::{self._class_name}::{self._function_name}"
        if self._class_name is None:
            relative_test_name = (
                f"{self._module_path.get_relative_path()}::{self._function_name}"
            )
        return relative_test_name

    def _pretty_representation(self):
        representation = (
            f"{self._module_path}::{self._class_name}::{self._function_name}"
        )
        if self._class_name is None:
            representation = f"{self._module_path}::{self._function_name}"
        return representation

    def __str__(self):
        return self._pretty_representation()

    def __repr__(self):
        return self._pretty_representation()
