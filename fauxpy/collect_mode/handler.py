from enum import Enum
from typing import List

from . import database, report
from .. import common
from ..common.testcase import TestInformation


class CollectMode(Enum):
    MBFL = 1
    PSINFO = 2
    PSRUN = 3


_Src: str
_Exclude: List[str]
_Family: str
_CurrentTestName: str


def handlerConfigure(src, exclude, family):
    global _Src
    global _Exclude
    global _Family

    _Src = src
    _Exclude = exclude

    if family == "collectmbfl":
        _Family = CollectMode.MBFL
    elif family == "collectpsinfo":
        _Family = CollectMode.PSINFO
    elif family == "collectpsrun":
        _Family = CollectMode.PSRUN

    database.init()


def handlerRuntestCall(item):
    """
    Runs before the execution of the current test.
    """

    global _CurrentTestName

    if _Family in [CollectMode.PSINFO, CollectMode.PSRUN]:
        _CurrentTestName = TestInformation(item.location, item.nodeid).getTestName()


def handlerRuntestMakereport(item, call):
    """
    Runs after the execution of the current test.
    """

    if call.when == "call":
        if _Family in [CollectMode.PSINFO, CollectMode.PSRUN]:

            testName = TestInformation(item.location, item.nodeid).getTestName()
            if testName != _CurrentTestName:
                raise Exception(f"Starting coverage for {_CurrentTestName}. But closing coverage for {testName}.")

            if _Family == CollectMode.PSINFO:
                predicateSequence = common.loadInCollectModeExecutedPredicateSequenceAndRemoveFile()
                if predicateSequence is not None:
                    database.insertPredicateSequence(testName, predicateSequence)

            if _Family == CollectMode.PSRUN:
                seenExceptionsSequence = common.loadInCollectModeSeenExceptionSequenceAndRemoveFile()
                if seenExceptionsSequence is not None:
                    database.insertSeenExceptionSequence(testName, seenExceptionsSequence)

                common.inCollectModeRemoveEvaluationCounterFile()


def handlerTerminalSummary(terminalreporter):
    """
    Runs after the execution of all tests.
    """

    if _Family in [CollectMode.MBFL, CollectMode.PSRUN]:
        for key, value in terminalreporter.stats.items():
            if key in ["passed", "failed"]:
                for testReport in value:
                    testInformation = TestInformation(testReport.location, testReport.nodeid)
                    testName = testInformation.getTestName()

                    testTraceBack = ""
                    timeoutStat = -1
                    if key == "failed":
                        reprTraceback = testReport.longrepr.reprtraceback
                        testTraceBack = common.getShortTraceBackInfo(reprTraceback)
                        # TODO: probably not needed anymore as --timeout_method is set to thread
                        if common.hasTimeoutHappened(testReport.longreprtext):
                            timeoutStat = 1

                    database.insertTestCase(testName=testName,
                                            testType=key,
                                            shortTraceback=testTraceBack,
                                            timeoutStat=timeoutStat)

        report.saveTestCases()

    if _Family == CollectMode.PSINFO:
        report.saveTestPredicateSequenceTable()

    if _Family == CollectMode.PSRUN:
        report.saveSeenExceptionSequenceTable()

    database.end()

    return {"Default": []}
