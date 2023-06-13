import re
from typing import Tuple, List

from fauxpy.common import utils

from fauxpy import common


def _getRequiredLines(lines) -> str:
    linesList = []
    for line in lines:
        if line.startswith("> "):
            linesList.append(line)
        if line.startswith("E "):
            linesList.append(line)

    if len(linesList) == 0:
        linesList.append(lines[-1])

    information = "::".join(linesList)
    return information


def _getTraceBackEntryEssence(entry) -> str:
    filePath = entry.reprfileloc.path
    lineNumber = entry.reprfileloc.lineno
    message = entry.reprfileloc.message
    lines = _getRequiredLines(entry.lines)
    information = "::".join([filePath, str(lineNumber), message, lines])
    return information


def getShortTraceBackInfo(traceBack) -> str:
    information = []
    for item in traceBack.reprentries:
        itemInfo = _getTraceBackEntryEssence(item)
        information.append(itemInfo)

    infoString = "\n".join(information)
    return infoString


def hasTimeoutHappened(longreprtext) -> bool:
    # Pattern is "E       Failed: Timeout >"
    pattern = "E( +)Failed:( *)Timeout( *)>"
    mat = re.search(pattern, longreprtext)
    return mat is not None


def _is_python_module(path: str):
    return path.endswith(".py")


def getExceptionLocation(traceback, src: str, exclude: List[str]) -> Tuple[str, int]:
    exceptionFilePath = ""
    exceptionLineNumber = -1
    tbLen = len(traceback.reprentries)
    if tbLen > 1:
        for i in range(len(traceback.reprentries)):
            tmp = tbLen - i - 1
            cPath = traceback.reprentries[tbLen - i - 1].reprfileloc.path
            cLineNumber = traceback.reprentries[tbLen - i - 1].reprfileloc.lineno
            cPathAbs = utils.relativePathToAbsPath(cPath)
            if common.pathShouldBeLocalized(src, exclude, cPathAbs) and _is_python_module(cPathAbs):
                exceptionFilePath = cPath
                exceptionLineNumber = cLineNumber
                break

    return exceptionFilePath, exceptionLineNumber
