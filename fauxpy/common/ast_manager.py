import ast
from _ast import FunctionDef
from typing import Tuple, Any, Optional, List

from . import database
from .. import common


class FunctionInformation(object):
    def __init__(self,
                 filePath: str,
                 functionName: str,
                 lineStart: int,
                 lineEnd: int):
        self.filePath = filePath
        self.functionName = functionName
        self.lineStart = lineStart
        self.lineEnd = lineEnd


class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.functionRangeList = []

    def visit_stmt(self, node):
        self.generic_visit(node)

    def visit_FunctionDef(self, node: FunctionDef) -> Any:
        functionName = node.name
        lineStart = node.lineno
        lineEnd = Analyzer._getEndingLine(node)
        self.functionRangeList.append((functionName, lineStart, lineEnd))
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: FunctionDef) -> Any:
        functionName = node.name
        lineStart = node.lineno
        lineEnd = Analyzer._getEndingLine(node)
        self.functionRangeList.append((functionName, lineStart, lineEnd))
        self.generic_visit(node)

    # TODO: This method is copied in other places. Combine them somehow.
    # TODO: if node.end_lineno exists, use it. Otherwise, the following one.
    @staticmethod
    def _getEndingLine(node):
        lineEndMax = -1

        if hasattr(node, "__dict__"):
            allAtt = node.__dict__
            for att in allAtt:
                attInstance = node.__getattribute__(att)
                if isinstance(attInstance, list):
                    for subAtt in attInstance:
                        lineEndMax = max(Analyzer._getEndingLine(subAtt), lineEndMax)
                else:
                    lineEndMax = max(Analyzer._getEndingLine(attInstance), lineEndMax)
                if hasattr(attInstance, "lineno"):
                    lineEndMax = max(attInstance.lineno, lineEndMax)

        if hasattr(node, "lineno"):
            lineEndMax = max(node.lineno, lineEndMax)
        return lineEndMax


def _findAllFunctionRanges(filePath: str) -> List[Tuple[str, int, int]]:
    with open(filePath, "r") as source:
        try:
            tree = ast.parse(source.read())
        except Exception as exp:
            common.Logger.warning(
                f"Due to the following error, the following module is removed form fault localization."
                f"To include it, fix the error, and run the tool again.\r\n"
                f"Error: {exp}.\r\n"
                f"Module: {filePath}")
            return []

    analyzer = Analyzer()
    analyzer.visit(tree)

    return analyzer.functionRangeList


def getCoveredFunction(filePath: str, lineNumber: int) -> Optional[Tuple[str, str, int, int]]:
    functionRangeList = database.selectFunctionRanges(filePath, lineNumber)

    if len(functionRangeList) == 0:
        if database.isFilePathCovered(filePath):
            return None
        else:
            functionRangeList = _findAllFunctionRanges(filePath)
            for functionRange in functionRangeList:
                database.insertFunctionInformation(filePath, functionRange[0], functionRange[1], functionRange[2])

            if len(functionRangeList) == 0:
                return None
            else:
                functionRangeList = database.selectFunctionRanges(filePath, lineNumber)
                if len(functionRangeList) == 0:
                    return None

                functionRangeList.sort(key=lambda x: x[2] - x[1])
                return filePath, functionRangeList[0][0], functionRangeList[0][1], functionRangeList[0][2]
    else:
        functionRangeList.sort(key=lambda x: x[2] - x[1])
        return filePath, functionRangeList[0][0], functionRangeList[0][1], functionRangeList[0][2]

