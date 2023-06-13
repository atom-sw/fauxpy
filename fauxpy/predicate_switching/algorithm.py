import pathlib
import shutil
from typing import List, Tuple, Optional

from . import ast_manager, database, predicate_instance, seen_exceptions
from .. import common, collect_mode


def _getInstrumentedModules() -> List[Tuple[str, str]]:
    """
    Returns a list of tuples of modules paths (having at least one candidate
    predicate or a seen exception) and their instrumented content.
    """
    instFilePathsContent: List[Tuple[str, str]] = []
    filePathsWithCandidatePredicate = database.selectDistinctCandidatePredicateFilePaths()
    filePathsWithSeenExceptions = database.selectDistinctSeenExceptionsFilePaths()
    instFilePaths = set(filePathsWithCandidatePredicate + filePathsWithSeenExceptions)
    for filePath in instFilePaths:
        candidatePredicates = database.selectCandidatePredicatesForFilePath(filePath)
        seenExceptions = database.selectSeenExceptionsForFilePath(filePath)
        instFileContent = ast_manager.instrumentCurrentFilePath(filePath, candidatePredicates, seenExceptions)
        if instFileContent is None:
            # For cases that astor cannot perform correctly
            for item in candidatePredicates:
                lineStart, lineEnd, predicateName = item
                database.insertAstorAssertErrorInfo(filePath, lineStart, lineEnd, predicateName)
        else:
            instFilePathsContent.append((filePath, instFileContent))

    return instFilePathsContent


def _injectInstrumentedContentInProject(tempProjectPath: str, instrumentedModules: List[Tuple[str, str]]):
    """
    Replaces modules to be instrumented with their instrumented versions.
    """
    for modulePath, moduleContent in instrumentedModules:
        relativeModulePath = common.absolutePathToRelativePath(modulePath)
        absoluteTempModulePath = pathlib.Path(tempProjectPath) / relativeModulePath
        with open(absoluteTempModulePath, "w") as file:
            file.write(moduleContent)


def _removeTempProject(tempProjectPath):
    shutil.rmtree(tempProjectPath)


def _instrumentProject() -> str:
    """
    Makes a copy of the project in a temporary directory, instruments it, and
     returns the path of the project copy.
    """
    instFilePathsContent = _getInstrumentedModules()
    tmpProjectPath = common.makeProjectCopyInTemp()
    _injectInstrumentedContentInProject(tmpProjectPath, instFilePathsContent)
    return tmpProjectPath


def _getPredicateSequences(projectPath: str,
                           src: str,
                           exclude: List[str],
                           failedTestPaths):
    """
    Runs the project in Collect mode and stores a list of tuples
    (testName, Predicate sequence).
    @param projectPath: path to the project subject to fault localization.
    """

    # TODO: Optimize the failing tests to run. Maybe running it on arg_min(failedTestPaths, fileOrDir).

    predicateSequences = []
    indexedPredicateSequences = collect_mode.runPSCollectModeInfo(src=src,
                                                                  exclude=exclude,
                                                                  projectPath=projectPath,
                                                                  fileOrDir=failedTestPaths)
    # exeResultData = collect_mode.getRunResult(projectPath)
    for r in indexedPredicateSequences:
        testName, predicateSequence, indPredSeq = r
        predicateSequences.append((testName, indPredSeq))

        # Not needed.
        database.insertPredicateSequenceForTest(testName, predicateSequence, indPredSeq)

    return predicateSequences


# def _getGeneralizedTestName(testName: str) -> str:
#     """
#     Returns the general test name if the test is a parametrized test.
#     i.e., it removes the parameters and keeps only the function name.
#     Thus, the general test name includes all instances of a parametrized test.
#     For non parametrized tests, it does nothing and returns the received test.
#     """
#
#     filePath, _, functionName = common.convertTestNameToComponents(testName)
#     generalizedFunctionName = functionName.split("[")[0]
#
#     # For CLASS_NAME.FUNCTION_NAME
#     if "." in generalizedFunctionName:
#         className, functionName = generalizedFunctionName.split(".")
#         generalizedFunctionName = "::".join([className, functionName])
#
#     generalizedTestFuncPath = "::".join([filePath, generalizedFunctionName])
#     return generalizedTestFuncPath


def _getGeneralizedFailedTestFunctionPaths():
    """
    Returns failed test paths (i.e., TEST_FILE_PATH::TEST_FUNCTION_NAME).
    For parametrized tests, returns generalized path
     (i.e., parameters excluded).
    """
    generalizedTestNames = []
    failedTestCaseNames = database.selectTestCaseFailed()
    for testName in failedTestCaseNames:
        # generalizedTestName = _getGeneralizedTestName(testName)
        filePath, _, functionName = common.convertTestNameToComponents(testName)
        generalizedTestName = common.getGeneralizedTestName(filePath, functionName)
        generalizedTestNames.append(generalizedTestName)
    return generalizedTestNames


def _runSwitchedPredicateInstance(projectPath: str, testName: str, predicateName: str, instanceNumber: int, src: str,
                                  exclude: List[str], timeoutLimit: float) -> Tuple[Optional[str], Optional[List[str]], Optional[float], bool]:
    """
    Runs the instrumented project in temp directory on the given test name.
    In the execution, the given predicate instance is switched.
    Returns True if the given test passes, and False, if it does not.
    """

    # generalizedTestPath = _getGeneralizedTestName(testName)
    filePath, _, functionName = common.convertTestNameToComponents(testName)
    generalizedTestPath = common.getGeneralizedTestName(filePath, functionName)
    exeResultData = collect_mode.runPSCollectModeRun(src=src,
                                                     exclude=exclude,
                                                     projectPath=projectPath,
                                                     fileOrDir=[generalizedTestPath],
                                                     predicateName=predicateName,
                                                     instanceNumber=instanceNumber,
                                                     timeout=timeoutLimit)

    execStatError = exeResultData.isTestCaseTableEmptyOrNone()
    if execStatError:
        print("Bad execution")
        return None, None, None, execStatError

    testResult, timeoutStat = exeResultData.getTestResult(testName)
    if testResult is None and timeoutStat is None:
        # The parametrized tests might be executed with different parameters in the
        # main mode and the collect mode. In this situation, the test name from
        # main cannot be found in the tests executed in collect mode. Found by pandas 141.
        print("Non-deterministic execution")
        return None, None, None, False

    seenExceptionListStr = exeResultData.getTestSeenExceptionList(testName)
    seenExceptionList = common.csvRowToList(seenExceptionListStr)

    return testResult, seenExceptionList, timeoutStat, execStatError


def _runPredicateSequence(projectPath: str,
                          testName: str,
                          indexedPredSeqStr: str,
                          src: str,
                          exclude: List[str],
                          expectedExceptionSeenName: str,
                          timeoutLimit: float):
    """
    Runs the given ordered predicate instances for the given predicate test name.
    Returns an ordered sequence of predicate instances that can pass the given test if switched.
    """

    indPredSeq = common.csvRowToList(indexedPredSeqStr)
    indPredSeq.reverse()  # Predicate instances are executed from last to first

    numberOfPredicateInstancesForTest = len(indPredSeq)

    passingPredicateInstances = []
    for ind, predInst in enumerate(indPredSeq):
        predName, instNum = predInst.split("::")

        print(f"-----RUNNING Predicate Instance "
              f"{predName}::{instNum} - {ind} / {numberOfPredicateInstancesForTest} "
              f"----- on test {testName}-----")

        testResult, seenExceptionList, timeoutStat, execStatError = _runSwitchedPredicateInstance(
            projectPath=projectPath,
            testName=testName,
            predicateName=predName,
            instanceNumber=int(instNum),
            src=src,
            exclude=exclude,
            timeoutLimit=timeoutLimit)

        if execStatError:
            database.insertBadExecutionPredicateInstance(testName, predName, instNum)
            print("Execution error for: ", testName, predName, instNum)
            continue

        # Not needed. Just to collect info for further analysis.
        if timeoutStat == 1:
            database.insertTimeoutPredicateInstance(testName, predName, instNum)
            print("Timeout for: ", testName, predName, instNum)
            continue

        if testResult == "passed":
            # For crashing bugs, if switching prevents the program from crashing
            # but the crash location is not executed, the predicate is not critical.
            if (expectedExceptionSeenName is None) or (expectedExceptionSeenName in seenExceptionList):
                passingPredicateInstances.append(predInst)

    return passingPredicateInstances


def _getTestScoredEntityStoreDb(testName: str,
                                passingPredicateInstanceSequence: List[str],
                                granularity: str):
    score = 1
    for predicateInstance in passingPredicateInstanceSequence:
        predicateName, instanceNumber = predicateInstance.split("::")
        filePath, lineStart, lineEnd = database.selectCandidatePredicate(predicateName)

        if granularity == "statement":
            entity = f"{filePath}::{lineStart}::{lineEnd}"
        elif granularity == "function":
            cfi = common.getCoveredFunction(filePath, lineStart)
            if cfi is None:
                entity = f"{filePath}::GLOBAL"
            else:
                functionFilePath, functionName, functionLineStart, functionLineEnd = cfi
                entity = common.getCoveredFunctionName(functionFilePath, functionName, functionLineStart,
                                                       functionLineEnd)
        else:
            raise Exception(f"The granularity {granularity} is not supported.")

        # For function granularity it can happen.
        # In this case, only one should be stored.
        # Found in youtube_dl13
        if database.scoredEntityExistsForTest(testName, entity):
            continue

        database.insertScoredEntity(testName, entity, score)

        # Critical predicate closer to the failure location is more suspicious to be buggy.
        # Predicate instance closer to the failure locations is more suspicious to be buggy.
        score = score / 1.1


def _getAllTestsTopNScoredEntities(topN):
    allTestsTopNScoredEntities = {}

    finalFailingTestNames = database.selectScoredEntityTestNames()

    for testName in finalFailingTestNames:
        testNameAsFilePath = common.testNameToFileName(testName)

        if topN == -1:
            testTopNScoredEntities = database.selectTestAllScoredEntities(testName)
        elif topN >= 0:
            testTopNScoredEntities = database.selectTestTopNScoredEntities(testName, topN)
        else:
            raise Exception(f"TopN {topN} is not supported.")

        allTestsTopNScoredEntities[testNameAsFilePath] = testTopNScoredEntities

    if len(allTestsTopNScoredEntities) == 0:
        allTestsTopNScoredEntities = {"fauxpy_no_swapped_instances": []}

    return allTestsTopNScoredEntities


def runPredicateSwitching(src: str, exclude: List[str], granularity: str,
                          timeoutLimit: float,
                          topN: int,
                          targetFailingTests: common.TargetFailingTests):
    """
    Runs the whole predicate switching algorithm.
    """

    predicate_instance.getCandidatePredicatesStoreDb()

    if database.numberOfCandidatePredicates() == 0:
        return {"fauxpy_no_candidate_predicates": []}

    seen_exceptions.getSeenExceptionsStoreDb()
    tempProjectPath = _instrumentProject()

    if targetFailingTests is None:
        failingTests = _getGeneralizedFailedTestFunctionPaths()
    else:
        failingTests = targetFailingTests.getFailingTests()

    predicateSequences = _getPredicateSequences(tempProjectPath, src, exclude, failingTests)

    for predSeqItem in predicateSequences:
        testName, indexedPredSeqStr = predSeqItem
        originalTestType = database.selectTestType(testName)
        if originalTestType == "passed":
            continue

        seenExceptionName = database.selectSeenExceptionForTestName(testName)
        passingPredicateInstanceSequence = _runPredicateSequence(tempProjectPath,
                                                                 testName,
                                                                 indexedPredSeqStr,
                                                                 src,
                                                                 exclude,
                                                                 seenExceptionName,
                                                                 timeoutLimit)

        _getTestScoredEntityStoreDb(testName, passingPredicateInstanceSequence, granularity)

    _removeTempProject(tempProjectPath)

    allTestsScoredEntities = _getAllTestsTopNScoredEntities(topN)

    return allTestsScoredEntities
