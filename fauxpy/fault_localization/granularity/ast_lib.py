import ast
from _ast import FunctionDef
from typing import Any


class FunctionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.function_range_list = []

    def visit_stmt(self, node):
        self.generic_visit(node)

    def visit_FunctionDef(self, node: FunctionDef) -> Any:
        function_name = node.name
        line_start = node.lineno
        line_end = self._get_ending_line(node)
        self.function_range_list.append((function_name, line_start, line_end))
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: FunctionDef) -> Any:
        function_name = node.name
        line_start = node.lineno
        line_end = self._get_ending_line(node)
        self.function_range_list.append((function_name, line_start, line_end))
        self.generic_visit(node)

    # TODO: This method is copied in other places. Combine them somehow.
    # TODO: if node.end_lineno exists, use it. Otherwise, the following one.

    def _get_ending_line(self, node):
        line_end_max = -1

        if hasattr(node, "__dict__"):
            all_att = node.__dict__
            for att in all_att:
                att_instance = node.__getattribute__(att)
                if isinstance(att_instance, list):
                    for sub_att in att_instance:
                        line_end_max = max(self._get_ending_line(sub_att), line_end_max)
                else:
                    line_end_max = max(
                        self._get_ending_line(att_instance), line_end_max
                    )
                if hasattr(att_instance, "lineno"):
                    line_end_max = max(att_instance.lineno, line_end_max)

        if hasattr(node, "lineno"):
            line_end_max = max(node.lineno, line_end_max)
        return line_end_max
