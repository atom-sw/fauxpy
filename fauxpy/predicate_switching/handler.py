from typing import List

import coverage

from . import database, algorithm
from .. import common
from ..common.testcase import TestInformation

# from .. import program_tracer


_Granularity: str
_Src: str
_Exclude: List[str]
_TopN: int
_TargetFailingTests: common.TargetFailingTests
_Cov: coverage.Coverage
_CurrentTestName: str

_CurrentTestTimer = common.Timer()


def handlerConfigure(granularity, src, exclude, topN, targetFailingTests):
    global _Granularity, _Src, _Exclude, _TopN, _Cov, _TargetFailingTests

    _Granularity = granularity
    _Src = src
    _Exclude = exclude
    _TopN = int(topN)
    _TargetFailingTests = targetFailingTests
    _Cov = coverage.Coverage()
    database.init()


def handlerRuntestCall(item):
    """
    Runs before the execution of the current test.
    """

    global _CurrentTestName, _Cov

    _CurrentTestTimer.startTimer()

    _CurrentTestName = TestInformation(item.location, item.nodeid).getTestName()
    # program_tracer.start(isWanted=lambda x: common.pathShouldBeLocalized(_Src, _Exclude, x))
    _Cov.start()


def handlerRuntestMakereport(item, call):
    """
    Runs after the execution of the current test.
    """

    global _CurrentTestName, _Cov

    # TODO: Replace custom tracer with coverage library (commented code).

    if call.when == "call":
        testName = TestInformation(item.location, item.nodeid).getTestName()
        if testName != _CurrentTestName:
            raise Exception(f"Starting coverage for {_CurrentTestName}. But closing coverage for {testName}.")

        # program_tracer.stop()
        # executionTrace = program_tracer.getExecutionTrace()
        # executedLines = executionTrace.getExecutedLinesInOrderOfExecution()
        # if len(executedLines) == 0:
        #     database.insertEmptyTest(testName)
        # else:
        #     for exeLine in executedLines:
        #         database.insertCoveredLineForTest(testName, exeLine[0], exeLine[1])

        _Cov.stop()
        covDat = _Cov.get_data()
        coveredStatements = []
        filesCov = covDat.measured_files()

        for file in filesCov:
            if common.pathShouldBeLocalized(_Src, _Exclude, file):
                lines = covDat.lines(file)
                for line in lines:
                    coveredStatements.append((file, line))
        if len(coveredStatements) == 0:
            database.insertEmptyTest(testName)
        else:
            for coveredStmt in coveredStatements:
                database.insertCoveredLineForTest(testName, coveredStmt[0], coveredStmt[1])

        _Cov.erase()

        # Lets give more time to mutants by putting these lines after
        currentTestTime = _CurrentTestTimer.endTimer()
        database.insertTestTime(testName, currentTestTime)


def handlerTerminalSummary(terminalreporter):
    """
    Runs after the execution of all tests.
    """

    global _TargetFailingTests

    for key, value in terminalreporter.stats.items():
        if key in ["passed", "failed"]:
            for testReport in value:
                testInformation = TestInformation(testReport.location, testReport.nodeid)
                testPath = testInformation.getPath()
                testMethodName = testInformation.getMethodName()

                testName = testInformation.getTestName()
                exceptionFilePath = ""
                exceptionLineNumber = -1
                target = False
                if key == "failed":

                    if _TargetFailingTests is not None:
                        target = _TargetFailingTests.isTargetTest(testPath, testMethodName)
                    elif _TargetFailingTests is None:
                        target = True

                    # TODO: Try not to use testReport.longrepr.reprtraceback. Does not work with {pytest-xdist,
                    #  --forked}. Same problem in collect mode and mbfl.
                    reprTraceback = testReport.longrepr.reprtraceback
                    exceptionFilePath, exceptionLineNumber = common.getExceptionLocation(reprTraceback, _Src, _Exclude)
                database.insertTestCase(testName=testName, testType=key,
                                        exceptionFilePath=common.relativePathToAbsPath(exceptionFilePath),
                                        exceptionLineNumber=exceptionLineNumber,
                                        target=target)

    # TODO: Get time from passing tests and target failing tests.
    maxTestTime = database.selectMaxTestTime()

    timeoutLimit = common.getTimeout(maxTestTime)
    resultsFL = algorithm.runPredicateSwitching(_Src, _Exclude, _Granularity, timeoutLimit, _TopN, _TargetFailingTests)

    database.end()

    return resultsFL
