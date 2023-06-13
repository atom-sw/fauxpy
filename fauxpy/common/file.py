import csv
import datetime
import json
import pathlib
import shutil
from typing import List, Tuple, Optional

from . import utils
from ..constants import FileNames
from .. import constants

_ReportDirectoryCreated = False
_ReportDirectory: pathlib.PosixPath

_CollectModeDirectoryCreated = False
_CollectModeDirectory: pathlib.PosixPath


def init(family: str, granularity: str):
    global _ReportDirectory, _CollectModeDirectory

    projectWd = pathlib.Path(utils.ProjectWorkingDirectory)
    projectName = projectWd.name
    projectParentDirectory = projectWd.parent
    ft = "%Y_%m_%d_%H_%M_%S_%f"
    dateTime = datetime.datetime.now().strftime(ft)
    reportDirectorName = f"{FileNames.ReportDirectoryNamePrefix}_{projectName}_{family}_{granularity}_{dateTime}"
    _ReportDirectory = projectParentDirectory / reportDirectorName

    if family in ["collectmbfl", "collectpsinfo", "collectpsrun"]:
        _ReportDirectory = projectWd / FileNames.CollectModeDirectoryName


def _getReportDirectory():
    global _ReportDirectoryCreated, _ReportDirectory
    if _ReportDirectory.exists() and not _ReportDirectoryCreated:
        shutil.rmtree(_ReportDirectory)  # Remove last reports
    if not _ReportDirectory.exists():
        _ReportDirectory.mkdir()  # Create report directory
        _ReportDirectoryCreated = True
    return _ReportDirectory


def getDatabasePath(filePath):
    databaseFilePath = _getReportDirectory() / filePath
    databaseFilePath = str(databaseFilePath)
    return databaseFilePath


def saveScoresToFile(technique: str, scores: List[Tuple[str, int]]):
    scoresFilePath = _getReportDirectory() / f"Scores_{technique}.csv"
    with open(scoresFilePath, "w") as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(FileNames.ScoresFileNameHeader)
        for score in scores:
            writer.writerow([score[0], score[1]])


def saveConfigToFile(src: str,
                     exclude: List[str],
                     family: str,
                     granularity: str,
                     topN: str,
                     targetFailingTests: List[str]):
    filePath = _getReportDirectory() / FileNames.ConfigFileName
    with open(filePath, "w") as file:
        file.write(f"Src = {src}\r\n")
        file.write(f"Exclude = {exclude}\r\n")
        file.write(f"Family = {family}\r\n")
        file.write(f"Granularity = {granularity}\r\n")
        file.write(f"TopN = {topN}\r\n")
        file.write(f"TargetFailingTests = {targetFailingTests}\r\n")


def saveDeltaTimeToFile(deltatime):
    filePath = _getReportDirectory() / FileNames.DeltaTimeFileName
    with open(filePath, "w") as file:
        file.write(f"DeltaTime = {deltatime}")


def getLogFilePath():
    filePath = _getReportDirectory() / FileNames.LogFilePath
    return str(filePath.absolute().resolve())


def saveInCollectModeTestCaseTable(jsonTable: str):
    temp = _getReportDirectory()
    filePath = temp / FileNames.collectModeTestCases
    with open(filePath, "w") as file:
        file.write(jsonTable)


def loadAfterCollectModeTestCaseTable(projectPath: str) -> Optional[List[Tuple[str, str, str]]]:
    filePath = pathlib.Path(projectPath) / FileNames.CollectModeDirectoryName / FileNames.collectModeTestCases
    if not filePath.exists():
        return None

    with open(filePath, "r") as file:
        jsonTable = file.read()
        table = json.loads(jsonTable)
    return table


def loadInCollectModeExecutedPredicateSequenceAndRemoveFile() -> Optional[str]:
    """
    This function is used while running in collect mode.
    It loads the predicate sequence file generated for the current
    execution by the instrumentation library, removes the file, and
    returns its content.
    @return: If the file exists, returns its content. If the file,
    does not exist or cannot be opened (for unknown reasons),
    returns None.
    """

    filePath = pathlib.Path(utils.ProjectWorkingDirectory) / pathlib.Path(
        FileNames.instrumentationCollectModeExecutedPredicateSequenceFileName)
    try:
        with open(filePath, "r") as file:
            predSequence = file.read()
            if predSequence[-1] == ",":
                predSequence = predSequence[0:-1]
            return predSequence
    except:
        return None
    finally:
        if filePath.exists():
            filePath.unlink()


def loadInCollectModeSeenExceptionSequenceAndRemoveFile() -> Optional[str]:
    """
    This function is used while running in collect mode.
    It loads the seen exceptions file generated for the current
    execution by the instrumentation library, removes the file, and
    returns its content.
    @return: If the file exists, returns its content. If the file,
    does not exist or cannot be opened (for unknown reasons),
    returns None.
    """

    filePath = pathlib.Path(utils.ProjectWorkingDirectory) / pathlib.Path(
        FileNames.instrumentationCollectModeExceptionSeenFileName)
    try:
        with open(filePath, "r") as file:
            seenExpSequence = file.read()
            if seenExpSequence[-1] == ",":
                seenExpSequence = seenExpSequence[0:-1]
            return seenExpSequence
    except:
        return None
    finally:
        if filePath.exists():
            filePath.unlink()


def inCollectModeRemoveEvaluationCounterFile():
    filePath = pathlib.Path(utils.ProjectWorkingDirectory) / pathlib.Path(
        FileNames.instrumentationCollectModeEvaluationCounterFileName)
    if filePath.exists():
        filePath.unlink()


def saveInCollectModePredicateSequenceTable(jsonTable: str):
    filePath = _getReportDirectory() / FileNames.collectModePredicateSequences
    with open(filePath, "w") as file:
        file.write(jsonTable)


def saveInCollectModeSeenExceptionSequenceTable(jsonTable: str):
    filePath = _getReportDirectory() / FileNames.collectModeSeenExceptions
    with open(filePath, "w") as file:
        file.write(jsonTable)


def loadAfterCollectModePredicateSequenceTable(projectPath):
    filePath = pathlib.Path(projectPath) / FileNames.CollectModeDirectoryName / FileNames.collectModePredicateSequences
    with open(filePath, "r") as file:
        jsonTable = file.read()
        table = json.loads(jsonTable)
    return table


def loadAfterCollectModeSeenExceptionSequenceTable(projectPath) -> Optional[List[Tuple[str, str]]]:
    filePath = pathlib.Path(projectPath) / FileNames.CollectModeDirectoryName / FileNames.collectModeSeenExceptions
    if not filePath.exists():
        return None

    with open(filePath, "r") as file:
        jsonTable = file.read()
        table = json.loads(jsonTable)
    return table


def saveBeforeCollectModeConfigFile(projectPath: str, predicateName: str, instanceNumber: int):
    configFileName = constants.getCollectModeConfigFileName()
    configFilePath = pathlib.Path(projectPath) / pathlib.Path(configFileName)
    contentDictionary = {"PredicateName": predicateName, "InstanceNumber": instanceNumber}
    jsonContent = json.dumps(contentDictionary)
    with open(configFilePath, "w") as file:
        file.write(jsonContent)


def getFileContentAsString(filePath: str) -> str:
    with open(filePath, "r") as file:
        content = file.read()
    return content
