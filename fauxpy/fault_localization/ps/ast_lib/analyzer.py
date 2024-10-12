# TODO: Consider adding assignment predicates such as x = 3 if p1 else 4.
import ast
from _ast import Expression, While
from typing import Any


class Analyzer(ast.NodeVisitor):
    def __init__(self, line_number: int):
        self._lineNumber = line_number
        self._lineStart = -1
        self._lineEnd = -1

    def get_line_start(self):
        return self._lineStart

    def get_line_end(self):
        return self._lineEnd

    def visit_If(self, node: Expression) -> Any:
        if node.test.lineno <= self._lineNumber:
            line_end = self._get_ending_line(node.test)
            if self._lineNumber <= line_end:
                self._lineStart = node.test.lineno
                self._lineEnd = line_end

        self.generic_visit(node)

    def visit_While(self, node: While) -> Any:
        if node.test.lineno <= self._lineNumber:
            line_end = self._get_ending_line(node.test)
            if self._lineNumber <= line_end:
                self._lineStart = node.test.lineno
                self._lineEnd = line_end

        self.generic_visit(node)

    # TODO: if node.end_lineno exists, use it. Otherwise, the following one.
    def _get_ending_line(self, node):
        line_end_max = -1

        if hasattr(node, "__dict__"):
            all_att = node.__dict__
            for att in all_att:
                att_instance = node.__getattribute__(att)
                if isinstance(att_instance, list):
                    for subAtt in att_instance:
                        line_end_max = max(self._get_ending_line(subAtt), line_end_max)
                else:
                    line_end_max = max(
                        self._get_ending_line(att_instance), line_end_max
                    )
                if hasattr(att_instance, "lineno"):
                    line_end_max = max(att_instance.lineno, line_end_max)

        if hasattr(node, "lineno"):
            line_end_max = max(node.lineno, line_end_max)
        return line_end_max
