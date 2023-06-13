from fauxpy import collect_mode
from tests.common import getDataPath, deleteNoise


def setup_function():
    projectPaths = [
        getDataPath("predicate_switching", "no_exceptions"),
        getDataPath("predicate_switching", "no_predicate_sequence")
    ]
    for item in projectPaths:
        deleteNoise(item)


def teardown_function():
    projectPaths = [
        getDataPath("predicate_switching", "no_exceptions"),
        getDataPath("predicate_switching", "no_predicate_sequence")
    ]
    for item in projectPaths:
        deleteNoise(item)


def test_runPSCollectModeRun_no_exceptions():
    projectPath = getDataPath("predicate_switching", "no_exceptions")
    src = "src"
    exclude = []
    generalizedTestPath = "tests/test_main.py::test_mainFunction"
    predicateName = "Pred_1"
    instanceNumber = 0
    timeoutLimit = 1
    testName = "tests/data/predicate_switching/no_exceptions/tests/test_main.py::3::test_mainFunction"

    exeResultData = collect_mode.runPSCollectModeRun(src=src,
                                                     exclude=exclude,
                                                     projectPath=str(projectPath.absolute()),
                                                     fileOrDir=[generalizedTestPath],
                                                     predicateName=predicateName,
                                                     instanceNumber=instanceNumber,
                                                     timeout=timeoutLimit)

    testResult, timeoutStat = exeResultData.getTestResult(testName)
    seenExceptionListStr = exeResultData.getTestSeenExceptionList(testName)

    assert testResult == "passed"
    assert timeoutStat == -1
    assert seenExceptionListStr == ""


def test_runPSCollectModeInfo_no_predicate_sequence():
    projectPath = getDataPath("predicate_switching", "no_predicate_sequence")
    src = "src"
    exclude = []
    failedTestPaths = ["tests/test_main.py::test_mainFunction", "tests/test_main.py::test_addOne"]

    exeResultData = collect_mode.runPSCollectModeInfo(src=src,
                                                      exclude=exclude,
                                                      projectPath=str(projectPath.absolute()),
                                                      fileOrDir=failedTestPaths)
    assert exeResultData != ""
