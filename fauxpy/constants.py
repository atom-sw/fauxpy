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
    instrumentationCollectModeExecutedPredicateSequenceFileName = \
        "instrumentationCollectModeExecutedPredicateSequence.txt"
    instrumentationCollectModeConfigFileName = "instrumentationCollectModeConfig.txt"
    instrumentationCollectModeEvaluationCounterFileName = "instrumentationCollectModeEvaluationCounter.txt"
    instrumentationCollectModeExceptionSeenFileName = "instrumentationCollectModeExceptionSeen.txt"


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
