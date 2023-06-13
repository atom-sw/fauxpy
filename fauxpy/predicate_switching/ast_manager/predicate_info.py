import ast
from _ast import Expression, While
from typing import Tuple, Any

from fauxpy import common


# TODO: Consider adding assignment predicates such as x = 3 if p1 else 4.
class Analyzer(ast.NodeVisitor):
    def __init__(self,
                 lineNumber: int):
        self._lineNumber = lineNumber
        self._lineStart = -1
        self._lineEnd = -1

    def getLineStart(self):
        return self._lineStart

    def getLineEnd(self):
        return self._lineEnd

    def visit_If(self, node: Expression) -> Any:
        if node.test.lineno <= self._lineNumber:
            lineEnd = Analyzer._getEndingLine(node.test)
            if self._lineNumber <= lineEnd:
                self._lineStart = node.test.lineno
                self._lineEnd = lineEnd

        self.generic_visit(node)

    def visit_While(self, node: While) -> Any:
        if node.test.lineno <= self._lineNumber:
            lineEnd = Analyzer._getEndingLine(node.test)
            if self._lineNumber <= lineEnd:
                self._lineStart = node.test.lineno
                self._lineEnd = lineEnd

        self.generic_visit(node)

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


def getPredicateInstanceRangeForProgramLine(filePath: str, lineNumber: int) -> Tuple[int, int]:
    with open(filePath, "r") as source:
        try:
            tree = ast.parse(source.read())
        except Exception as exp:
            common.Logger.warning(
                f"Due to the following error, the following module is removed form fault localization."
                f"To include it, fix the error, and run the tool again.\r\n"
                f"Error: {exp}.\r\n"
                f"Module: {filePath}")
            return -1, -1

    analyzer = Analyzer(lineNumber)
    analyzer.visit(tree)
    lineStart = analyzer.getLineStart()
    lineEnd = analyzer.getLineEnd()

    return lineStart, lineEnd
