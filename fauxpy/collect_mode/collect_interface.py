import glob
import os
import pathlib
from typing import List, Tuple, Optional

from .. import common, constants


class PSCollectModeRunResult:
    def __init__(self,
                 testCaseTable: List[Tuple[str, str, str]],
                 seenExceptionList: List[Tuple[str, str]]):
        self.testCaseTable = testCaseTable
        self.seenExceptionList = seenExceptionList

    def getTestResult(self, testName: str) -> Tuple[Optional[str], Optional[float]]:
        for currentTest, testType, stacktrace, timeoutStat in self.testCaseTable:
            if currentTest == testName:
                return testType, timeoutStat
        return None, None

    def getTestSeenExceptionList(self, testName: str) -> str:
        for item in self.seenExceptionList:
            if item[0] == testName:
                return item[1]
        return ""

    def isTestCaseTableEmptyOrNone(self):
        return self.testCaseTable is None or len(self.testCaseTable) == 0


def indexPredicateSequence(predicateSequence) -> str:
    predCountSet = dict()
    predSeqList = common.csvRowToList(predicateSequence)
    indexedPredSeq = []
    for pred in predSeqList:
        if pred in predCountSet.keys():
            predCountSet[pred] += 1
        else:
            predCountSet[pred] = 0
        indexedPredSeq.append(f"{pred}::{predCountSet[pred]}")

    indexedPredSeqStr = common.listToCsvRow(indexedPredSeq)

    return indexedPredSeqStr


def getIndexPredicateSequences(predicateSequenceTable) -> List[Tuple[str, str, str]]:
    indexedPredSequences = []
    for tableRow in predicateSequenceTable:
        testName, predicateSequence = tableRow
        indPredSeq = indexPredicateSequence(predicateSequence)
        indexedPredSequences.append((testName, predicateSequence, indPredSeq))
    return indexedPredSequences


def _cleanProject(tempDir):
    """
    Removed all .pyc files within the project directory.
    It is needed since after change the source code (e.g., mutating),
    the .pyc files remain the same and does not consider change.
    It also removed the file made by the instrumentation library (just in case,
    since it should not exist at the first run, and the mode generating this
    file is only executed ones during the predicate switching method).
    """

    # https://thispointer.com/python-how-to-remove-files-by-matching-pattern-wildcards-certain-extensions-only/
    pattern = f"{tempDir}/**/*.pyc"
    fileList = glob.glob(pattern, recursive=True)
    for filePath in fileList:
        if os.path.exists(filePath):
            os.remove(filePath)

    fileNamePredSequence = pathlib.Path(constants.getCollectModeExecutedPredicateSequenceFileName())
    if fileNamePredSequence.exists():
        fileNamePredSequence.unlink()

    fileNameEvaluationCounter = pathlib.Path(constants.getCollectModeEvaluationCounterFileName())
    if fileNameEvaluationCounter.exists():
        fileNameEvaluationCounter.unlink()

    fileNameExceptionSeen = pathlib.Path(constants.getExceptionSeenFileName())
    if fileNameExceptionSeen.exists():
        fileNameExceptionSeen.unlink()


def _runProject(src: str,
                exclude: List[str],
                projectPath: str,
                fileOrDir: List[str],
                timeout: Optional[float],
                processTimeout: float = None,
                mode: str = ""):
    _cleanProject(projectPath)
    command = ["python", "-m", "pytest"] + fileOrDir + ["--src", src, "--family", "collect" + mode,
                                                        "--exclude", common.convertListToString(exclude)
                                                        ]
    if timeout is not None:
        command += ["--timeout", str(timeout)]
        command += ["--timeout_method", "thread"]
    common.runCommand(command, projectPath, processTimeout)


def runMbflCollectMode(src: str, exclude: List[str],
                       projectPath: str, fileOrDir: List[str],
                       timeout: float,
                       processTimeout: float) -> Optional[List[Tuple[str, str, str]]]:
    _runProject(src, exclude, projectPath, fileOrDir, timeout, processTimeout, "mbfl")
    testCaseTable = common.loadAfterCollectModeTestCaseTable(projectPath)
    return testCaseTable


def runPSCollectModeInfo(src: str, exclude: List[str],
                         projectPath: str, fileOrDir: List[str],
                         timeout: Optional[float] = None) -> List[Tuple[str, str, str]]:
    _runProject(src, exclude, projectPath, fileOrDir, timeout, mode="psinfo")

    predicateSequenceTable = common.loadAfterCollectModePredicateSequenceTable(projectPath)
    indexedPredicateSequences = getIndexPredicateSequences(predicateSequenceTable)

    return indexedPredicateSequences


def runPSCollectModeRun(src: str,
                        exclude: List[str],
                        projectPath: str,
                        fileOrDir: List[str],
                        predicateName: str,
                        instanceNumber: int,
                        timeout: Optional[float] = None) -> PSCollectModeRunResult:
    common.saveBeforeCollectModeConfigFile(projectPath, predicateName, instanceNumber)
    _runProject(src, exclude, projectPath, fileOrDir, timeout, mode="psrun")

    testCaseTable = common.loadAfterCollectModeTestCaseTable(projectPath)
    seenExceptionList = common.loadAfterCollectModeSeenExceptionSequenceTable(projectPath)
    result = PSCollectModeRunResult(testCaseTable, seenExceptionList)

    return result
