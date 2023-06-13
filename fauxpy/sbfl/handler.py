from typing import List

import coverage

from . import database, ranking_metric, covered_function
from .. import common
from ..common.testcase import TestInformation

_Granularity: str
_Src: str
_Exclude: List[str]
_TopN: int
_Cov: coverage.Coverage
_CurrentTestName: str
_TargetFailingTests: common.TargetFailingTests


def handlerConfigure(granularity, src, exclude, topN, targetFailingTests):
    global _Granularity, _Src, _Exclude, _TopN, _Cov, _TargetFailingTests

    _Granularity = granularity
    _Src = src
    _Exclude = exclude
    _TopN = int(topN)
    _TargetFailingTests = targetFailingTests
    # TODO: Good idea to change the data base file name
    #  like this _Cov = coverage.Coverage(data_suffix="fauxpy").
    #  Apply it to MBFL and PS as well.
    #  Test it for Python 3.6, 3.7, and 3.8.
    #  The API of Coverage.py changes in different version.
    _Cov = coverage.Coverage()
    database.init()


def handlerRuntestCall(item):
    """
    Runs before the execution of the current test.
    """

    global _Cov
    global _CurrentTestName

    _CurrentTestName = TestInformation(item.location, item.nodeid).getTestName()
    _Cov.start()


def handlerRuntestMakereport(item, call):
    """
    Runs after the execution of the current test.
    """

    global _Cov, _CurrentTestName

    if call.when == "call":
        testName = TestInformation(item.location, item.nodeid).getTestName()
        if testName != _CurrentTestName:
            raise Exception(f"Starting coverage for {_CurrentTestName}. But closing coverage for {testName}.")
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
            if _Granularity == "statement":
                coveredStatementNames = [common.getStatementName(x[0], x[1]) for x in coveredStatements]
                database.insertExecutionTrace(testName, coveredStatementNames)
            elif _Granularity == "function":
                coveredFunctionNames = covered_function.getCoveredFunctionNames(coveredStatements)
                database.insertExecutionTrace(testName, coveredFunctionNames)
            else:
                raise Exception(f"Granularity {_Granularity} is not supported.")

        _Cov.erase()


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

                target = False
                if _TargetFailingTests is not None and key == "failed":
                    target = _TargetFailingTests.isTargetTest(testPath, testMethodName)
                elif _TargetFailingTests is None and key == "failed":
                    target = True

                testName = testInformation.getTestName()
                database.insertTestCase(testName, key, target)

    scoreEntities = ranking_metric.computeSortedScores(_TopN)

    database.end()

    return scoreEntities
