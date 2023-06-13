import pathlib
import shutil
from enum import Enum
from typing import List, Tuple

from . import mutgen, database
from .. import common, collect_mode


class TestComparisonState(Enum):
    Normal = 0
    BadTest = 1
    BadMutant = 2
    NotTarget = 3


def _backupFile(filePath: pathlib.Path):
    newPath = f"{str(filePath.resolve())}.bak"
    filePath.rename(newPath)


def _unbackupFile(filePath: pathlib.Path):
    assert filePath.exists()
    backupPathStr = f"{str(filePath.resolve())}.bak"
    backupPath = pathlib.Path(backupPathStr)
    assert backupPath.exists()
    filePath.unlink()
    assert not filePath.exists()
    filePathStr = str(filePath.resolve())
    backupPath.rename(filePathStr)
    assert filePath.exists()
    assert not backupPath.exists()


def _insertMutationModule(modulePath: str,
                          moduleContent: str):
    with open(modulePath, "w") as file:
        file.write(moduleContent)


def _mutateTempProject(tempProjectPath: str,
                       mutatingModulePath: str,
                       mutatingModuleContent: str):
    relativePathOfMutatingModule = common.absolutePathToRelativePath(mutatingModulePath)
    absoluteTempPathOfMutatingModule = pathlib.Path(tempProjectPath) / relativePathOfMutatingModule
    _backupFile(absoluteTempPathOfMutatingModule)
    _insertMutationModule(str(absoluteTempPathOfMutatingModule.resolve()),
                          mutatingModuleContent)


def _unmutateTempProject(tempProjectPath: str,
                         mutatingModulePath: str):
    relativePathOfMutatingModule = common.absolutePathToRelativePath(mutatingModulePath)
    absoluteTempPathOfMutatingModule = pathlib.Path(tempProjectPath) / relativePathOfMutatingModule
    _unbackupFile(absoluteTempPathOfMutatingModule)


# TODO: probably, the timeout computation is not need. If timeout happens,
#  the test cases jason file does not get generated, which is
#  something that needs to be checked to see if timeout happened or not.
def _compareTwoTestCaseResults(normalTestCase, mutantTestCase) -> Tuple[int, int, int, TestComparisonState]:
    failedToPassed = 0
    passedToFailed = 0
    failedChanged = 0

    mutantTestCaseTimeoutStat = mutantTestCase[3]

    normalTestType = normalTestCase[1]
    normalTestTimeoutStat = normalTestCase[3]
    normalTestTargetStat = normalTestCase[4]
    normalTestIncluded = (normalTestType == "passed") or (normalTestType == "failed" and normalTestTargetStat == 1)

    # ToDo: use the condition inside the if. Not as a boolean variable.
    if not normalTestIncluded:
        # The failing test is not a target failing test. Discard the current test.
        testComparisonState = TestComparisonState.NotTarget
    else:
        if normalTestTimeoutStat == -1 and mutantTestCaseTimeoutStat == -1:
            # Its OK! Compute the terms.
            testComparisonState = TestComparisonState.Normal
        elif normalTestTimeoutStat == -1 and mutantTestCaseTimeoutStat == 1:
            # Infinite loop. Do not compute the terms. Discard current mutant.
            testComparisonState = TestComparisonState.BadMutant
        elif normalTestTimeoutStat == 1 and mutantTestCaseTimeoutStat == -1:
            # Weired case. Do not compute the terms. Discard current test.
            testComparisonState = TestComparisonState.BadTest
        elif normalTestTimeoutStat == 1 and mutantTestCaseTimeoutStat == 1:
            # Bad initial test. Do not compute the terms. Discard current test.
            testComparisonState = TestComparisonState.BadTest
        else:
            raise Exception("This one must never happen.")

    if testComparisonState == TestComparisonState.Normal:
        if normalTestCase[1] == "passed" and mutantTestCase[1] == "failed":
            passedToFailed = 1
        elif normalTestCase[1] == "failed" and mutantTestCase[1] == "passed":
            failedToPassed = 1
        elif normalTestCase[1] == "failed" and mutantTestCase[1] == "failed":
            if normalTestCase[2] != mutantTestCase[2]:
                failedChanged = 1

    return failedToPassed, passedToFailed, failedChanged, testComparisonState


def _removeTempProject(tempProjectPath):
    shutil.rmtree(tempProjectPath)


def _getMutantScoreTerms(mutantTestCaseRunResultTable):
    """
    Bad tests are removed from computation.
    In case of timeoutHappened = True, the terms failedToPassed, passedToFailed, failedChanged are not valid.
    """
    failedToPassed = 0
    passedToFailed = 0
    failedChanged = 0
    timeoutHappened = False

    for mutantTestCaseResult in mutantTestCaseRunResultTable:
        normalTestCaseResult = database.selectTestCase(mutantTestCaseResult[0])

        if normalTestCaseResult is None:
            # In pandas 47, one of the parametrized tests can have names
            # generated randomly (a very rare case). Thus, the collect mode
            # can return test names that do not exist in the main execution of the
            # MBFL method. In these cases, let's just ignore that test
            # and continue the score terms computation using the remaining tests.
            continue

        f2p, p2f, fc, testCompState = _compareTwoTestCaseResults(normalTestCaseResult, mutantTestCaseResult)
        if testCompState == TestComparisonState.Normal:
            failedToPassed += f2p
            passedToFailed += p2f
            failedChanged += fc
        elif testCompState == TestComparisonState.BadTest or TestComparisonState.NotTarget:
            continue
        elif testCompState == TestComparisonState.BadMutant:
            timeoutHappened = True
            break

    return failedToPassed, passedToFailed, failedChanged, timeoutHappened


def runAllMutantsStoreDb(mutants: List[mutgen.Mutant],
                         fileOrDir: List[str],
                         granularity: str,
                         src: str,
                         exclude: List[str],
                         timeoutLimit: float,
                         targetFailingTests: common.TargetFailingTests,
                         numberAllTests,
                         processTimeout):
    tempProjectPath = common.makeProjectCopyInTemp()

    numberOfAllMutants = len(mutants)

    print(f"-------------- Running {numberOfAllMutants} Mutants --------------")
    for mutant in mutants:
        print(f"------------ Running Mutant ID ----->>>>> {mutant.getId()} / {numberOfAllMutants} ------------")

        _mutateTempProject(tempProjectPath, mutant.getModulePath(), mutant.getModuleContent())
        mutantTestCaseRunResultTable = collect_mode.runMbflCollectMode(src,
                                                                       exclude,
                                                                       tempProjectPath,
                                                                       fileOrDir,
                                                                       timeout=timeoutLimit,
                                                                       processTimeout=processTimeout)

        if (mutantTestCaseRunResultTable is None or
                len(mutantTestCaseRunResultTable) == 0):
            # Timeout happened
            print("Timeout or bad mutant")
            database.updateMutantAsTimeout(mutant.getId())
            _unmutateTempProject(tempProjectPath, mutant.getModulePath())
            continue

        # For some reason, some mutant executions might return fewer
        # number of test cases. For now I remove them.
        # TODO: Find the reason. Found in sonic3. Takes around three hours.
        if numberAllTests != len(mutantTestCaseRunResultTable):
            print("Missing tests mutant")
            database.updateMutantAsHavingMissingTests(mutant.getId())
            _unmutateTempProject(tempProjectPath, mutant.getModulePath())
            continue

        failedToPassed, passedToFailed, failedChanged, timeoutHappened = _getMutantScoreTerms(
            mutantTestCaseRunResultTable)

        # In case of timeout, the mutant is thrown away and
        # its status is updated in the database
        # TODO: most probably this part is not needed
        if timeoutHappened:
            database.updateMutantAsTimeout(mutant.getId())
        else:
            if granularity == "statement":
                entityName = common.getStatementName(mutant.getModulePath(), mutant.getLineNumber())
            elif granularity == "function":
                coveredFunction = common.getCoveredFunction(mutant.getModulePath(), mutant.getLineNumber())
                entityName = common.getCoveredFunctionName(coveredFunction[0],
                                                           coveredFunction[1],
                                                           coveredFunction[2],
                                                           coveredFunction[3])
            else:
                raise Exception(f"Granularity {granularity} is not supported.")

            database.insertMutantScoreTerms(mutant.getId(),
                                            entityName,
                                            failedToPassed,
                                            passedToFailed,
                                            failedChanged)

        _unmutateTempProject(tempProjectPath, mutant.getModulePath())
    _removeTempProject(tempProjectPath)
