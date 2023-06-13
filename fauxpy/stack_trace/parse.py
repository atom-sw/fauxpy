from typing import List

from .. import common


def _is_python_module(path: str):
    return path.endswith(".py")


# TODO: Move to traceback_utils.py
def getOrderedTracebackFunctionNames(src, exclude, reprTraceback) -> List[str]:
    tracebackNames = []

    for reprEnt in reprTraceback.reprentries:
        path = reprEnt.reprfileloc.path
        lineNumber = reprEnt.reprfileloc.lineno
        absolutePath = common.relativePathToAbsPath(path)

        if not _is_python_module(path):
            continue

        if common.pathShouldBeLocalized(src, exclude, absolutePath):
            coveredFunction = common.getCoveredFunction(absolutePath, lineNumber)
            coveredFunctionName = common.getCoveredFunctionName(coveredFunction[0],
                                                                coveredFunction[1],
                                                                coveredFunction[2],
                                                                coveredFunction[3])
            tracebackNames.append(coveredFunctionName)
    tracebackNames.reverse()

    return tracebackNames
