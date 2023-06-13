from typing import List

from . import parse, ranking, database
from .. import common
from ..common.testcase import TestInformation

_Src: str
_Exclude: List[str]
_TopN: int
_CurrentTestName: str
_TargetFailingTests: common.TargetFailingTests


def handlerConfigure(src, exclude, topN, targetFailingTests):
    global _Src, _Exclude, _TopN, _TargetFailingTests

    _Src = src
    _Exclude = exclude
    _TopN = int(topN)
    _TargetFailingTests = targetFailingTests
    database.init()


def handlerRuntestCall(item):
    """
    Runs before the execution of the current test.
    """

    global _CurrentTestName
    _CurrentTestName = TestInformation(item.location, item.nodeid).getTestName()


def handlerRuntestMakereport(item, call):
    """
    Runs after the execution of the current test.
    """

    global _CurrentTestName

    if call.when == "call":
        testName = TestInformation(item.location, item.nodeid).getTestName()
        if testName != _CurrentTestName:
            raise Exception(f"Starting coverage for {_CurrentTestName}. But closing coverage for {testName}.")


def handlerTerminalSummary(terminalreporter):
    """
    Runs after the execution of all tests.
    """
    global _Src, _Exclude, _TargetFailingTests

    for key, value in terminalreporter.stats.items():
        if key in ["failed"]:
            for testReport in value:
                testInformation = TestInformation(testReport.location, testReport.nodeid)
                testPath = testInformation.getPath()
                testMethodName = testInformation.getMethodName()

                if ((_TargetFailingTests is not None and _TargetFailingTests.isTargetTest(testPath, testMethodName))
                        or _TargetFailingTests is None):
                    currentTest = testInformation.getTestName()
                    reprTraceback = testReport.longrepr.reprtraceback
                    tracebackFunctionNames = parse.getOrderedTracebackFunctionNames(_Src, _Exclude, reprTraceback)
                    currentTestScores = ranking.computeScores(tracebackFunctionNames)
                    database.insertTracebackScores(currentTest, currentTestScores)

    scores = ranking.getSortedScores(_TopN)

    database.end()

    return {"default": scores}
