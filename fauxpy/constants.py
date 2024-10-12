# https://medium.com/@zeid.zandi/how-to-manage-constants-in-python-best-practices-and-advanced-techniques-50fa1591d517

# Constants representing pytest phases and outcomes
PYTEST_CALL = "call"  # Represents the "call" phase of a test in pytest
PYTEST_PASSED = "passed"  # Indicates a test that has passed
PYTEST_FAILED = "failed"  # Indicates a test that has failed

# Constants for FauxPy fault localization granularity levels
FAUXPY_STATEMENT = (
    "statement"  # Specifies statement-level granularity in fault localization
)
FAUXPY_FUNCTION = (
    "function"  # Specifies function-level granularity in fault localization
)

# Database
DB_FILE_NAME = "fauxpy.db"


class FileNames(object):
    ReportDirectoryNamePrefix = "FauxPyReport"
    CollectModeDirectoryName = "FauxPyCollectModeReport"
    ConfigFileName = "config.txt"
    DeltaTimeFileName = "deltaTime.txt"
    ScoresFileNameHeader = ["Entity", "Score"]
    LogFilePath = "logging.log"
    collectModeTestCases = "collectModeTestCases.json"
    collectModeCoveredLinesForTest = "collectModeCoveredLinesForTest.json"
    collectModePredicateSequences = "collectModePredicateSequences.json"
    collectModeSeenExceptions = "collectModeSeenExceptions.json"
    instrumentationCollectModeExecutedPredicateSequenceFileName = (
        "instrumentationCollectModeExecutedPredicateSequence.txt"
    )
    instrumentationCollectModeConfigFileName = "instrumentationCollectModeConfig.txt"
    instrumentationCollectModeEvaluationCounterFileName = (
        "instrumentationCollectModeEvaluationCounter.txt"
    )
    instrumentationCollectModeExceptionSeenFileName = (
        "instrumentationCollectModeExceptionSeen.txt"
    )


def getCollectModeExecutedPredicateSequenceFileName():
    return FileNames.instrumentationCollectModeExecutedPredicateSequenceFileName


def getCollectModeConfigFileName():
    return FileNames.instrumentationCollectModeConfigFileName


def getCollectModeEvaluationCounterFileName():
    return FileNames.instrumentationCollectModeEvaluationCounterFileName


def getExceptionSeenFileName():
    return FileNames.instrumentationCollectModeExceptionSeenFileName


# TODO: Maybe finding better values for these two is a good idea.
testTimeoutFactor = 2
testTimeoutOffset = 5
