import pytest
from unittest.mock import MagicMock

from fauxpy.session_lib.targeted_failing_tst import TargetedFailingTst


@pytest.fixture
def mock_fauxpy_path():
    """Creates a mock FauxpyPath that returns a relative module path."""
    mock = MagicMock()
    mock.get_relative.return_value = "tests/test_example.py"
    return mock


def test_relative_name_with_class(mock_fauxpy_path):
    """Should include class name in the relative test identifier."""
    test_case = TargetedFailingTst(
        module_path=mock_fauxpy_path,
        class_name="TestExample",
        function_name="test_function"
    )
    expected = "tests/test_example.py::TestExample::test_function"
    assert test_case.get_relative_test_name() == expected
    assert str(test_case) == expected


def test_relative_name_without_class(mock_fauxpy_path):
    """Should omit class name when it is None."""
    test_case = TargetedFailingTst(
        module_path=mock_fauxpy_path,
        class_name=None,
        function_name="test_function"
    )
    expected = "tests/test_example.py::test_function"
    assert test_case.get_relative_test_name() == expected
    assert str(test_case) == expected
