from unittest.mock import Mock

from fauxpy.session_lib.fauxpy_path import FauxpyPath
from fauxpy.session_lib.fl_session_report import FlSessionReport
from fauxpy.session_lib.fl_type import FlGranularity


def test_generate_report_statement_level():
    project_path = FauxpyPath.from_relative_path(
        "/project",
        "."
    )
    scored_dict = {
        "technique1": [
            ("/project/path/to/file1.py::10", 0.75678),
            ("/project/path/to/file2.py::15", 0.23456)
        ]
    }
    report = FlSessionReport(
        scored_entity_dict=scored_dict,
        execution_time=1.23456,
        granularity=FlGranularity.Statement,
        project_working_directory=project_path
    )

    output = report.generate_report()

    assert "Fault Localization Results" in output
    assert "Execution Time: 1.2346" in output
    assert "Scores for technique1" in output
    assert "path/to/file1.py" in output
    assert "+0.7568" not in output  # Should not have sign for positive score if all scores are non-negative
    assert "0.7568" in output


def test_generate_report_function_level():
    project_path = FauxpyPath.from_relative_path(
        "/project",
        "."
    )
    scored_dict = {
        "technique2": [
            ("project/path/to/file1.py::my_func::5::20", -0.3),
            ("project/path/to/file2.py::another_func::21::35", 0.8)
        ]
    }
    report = FlSessionReport(
        scored_entity_dict=scored_dict,
        execution_time=2.98765,
        granularity=FlGranularity.Function,
        project_working_directory=project_path
    )

    output = report.generate_report()

    assert "Scores for technique2" in output
    assert "+0.8000" in output
    assert "-0.3000" in output


def test_get_rounded_scores():
    scored_dict = {
        "tech": [("file::10", 0.123456), ("file::20", 0.987654)]
    }

    report = FlSessionReport(
        scored_entity_dict=scored_dict,
        execution_time=0.0,
        granularity=FlGranularity.Statement,
        project_working_directory=Mock()
    )

    assert report._scored_entity_dict["tech"][0][1] == 0.1235
    assert report._scored_entity_dict["tech"][1][1] == 0.9877
