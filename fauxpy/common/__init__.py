from .naming import convertTestNameToComponents, getStatementName, getCoveredFunctionName, \
    convertStatementNameToComponents, testNameToFileName, getGeneralizedTestName
from .file import saveScoresToFile, saveConfigToFile, saveDeltaTimeToFile, \
    getDatabasePath, saveInCollectModeTestCaseTable, loadInCollectModeExecutedPredicateSequenceAndRemoveFile,\
    loadInCollectModeSeenExceptionSequenceAndRemoveFile, loadAfterCollectModeTestCaseTable,\
    saveInCollectModePredicateSequenceTable, saveInCollectModeSeenExceptionSequenceTable, loadAfterCollectModeSeenExceptionSequenceTable,\
    loadAfterCollectModePredicateSequenceTable,\
    saveBeforeCollectModeConfigFile, inCollectModeRemoveEvaluationCounterFile, getFileContentAsString
# from .timer import startTimer, endTimer
from .timer import Timer, getTimeout, getProcessTimeout
from .ast_manager import getCoveredFunction, FunctionInformation
from .utils import pathShouldBeLocalized, relativePathToAbsPath, \
    convertArgumentListStringToList, convertListToString, absolutePathToRelativePath, \
    runCommand, makeProjectCopyInTemp, csvRowToList, listToCsvRow
from .log import Logger
from .traceback_utils import getShortTraceBackInfo, getExceptionLocation, hasTimeoutHappened
from . import database
from .failing_tests import TargetFailingTests


# TODO: Find a better design for using these libraries.
def init(family: str, granularity: str):
    # utils must be initialized before file
    # since file uses the ProjectWorkingDirectory variable
    # from utils
    utils.init()
    file.init(family, granularity)
    log.init()
    database.init()


def end():
    database.end()


