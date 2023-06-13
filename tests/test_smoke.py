import pytest

from tests.common import getDataPath, runCommand, deleteNoise

MINIMAL_PROJECT = "minimal_project"


def setup_function():
    projectPath = getDataPath("common", MINIMAL_PROJECT)
    deleteNoise(projectPath)


def teardown_function():
    projectPath = getDataPath("common", MINIMAL_PROJECT)
    deleteNoise(projectPath)


testdata = [
    ("sbfl", "statement"),
    # ("mbfl", "statement"),
    ("ps", "statement"),
    ("st", "statement"),
    ("sbfl", "function"),
    # ("mbfl", "function"),
    ("ps", "function"),
    ("st", "function")
]


@pytest.mark.parametrize("family,granularity", testdata)
def test_family(family, granularity):
    projectName = MINIMAL_PROJECT
    workingDirectoryPath = getDataPath("common", projectName)
    workingDirectory = str(workingDirectoryPath.absolute())
    command = ["python", "-m", "pytest",
               "tests",
               "--src", "src",
               "--family", family,
               "--granularity", granularity]
    runCommand(command, workingDirectory)

    reportDirs = list(workingDirectoryPath.parent.rglob(f"FauxPyReport_{MINIMAL_PROJECT}*"))
    assert len(reportDirs) != 0
    scoreFiles = list(reportDirs[-1].rglob("Scores_*"))
    assert len(scoreFiles) != 0
