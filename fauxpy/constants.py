# Constants for PyLLMut
MUTANTS_PER_LINE_COUNT = 7  # Number of mutants generated per line
TIMEOUT_SECONDS_PER_LINE = 10  # Timeout in seconds per line during mutation generation

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

# Fl session constants
DB_FILE_NAME_FL_SESSION = "fauxpy.db"  # Database file name for FauxPy fault localization session
CONFIG_FILE_NAME_FL_SESSION = "config.json"  # Configuration file name for FauxPy fault localization session
TIME_FILE_NAME_FL_SESSION = "deltaTime.json"  # Time-related file for FauxPy fault localization session
LOG_FILE_NAME_FL_SESSION = "logging.log"  # Log file name for FauxPy fault localization session
REPORT_DIRECTORY_NAME_PREFIX_FL_SESSION = "FauxPyReport"  # Prefix for the directory name including FauxPy fault localization reports

# Fl results constants
SCORES_CSV_HEADER = ["Entity", "Score"]

class FileNames(object):
    CollectModeDirectoryName = "FauxPyCollectModeReport"
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


# Constants used to compute the timeout window for
# running mutants in MBFL and during predicate switching
# in PS
# TODO: Maybe finding better values for these two is a good idea.
TEST_TIMEOUT_SCALING_FACTOR = 2
TEST_TIMEOUT_OFFSET = 5
