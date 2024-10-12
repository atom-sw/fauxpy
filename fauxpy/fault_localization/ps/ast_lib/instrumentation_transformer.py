import ast
from typing import Any

import astor


class InstrumentationTransformer(ast.NodeTransformer):
    def __init__(self, tree, candidate_predicates, seen_exceptions):
        self.tree = tree
        self.candidatePredicates = candidate_predicates
        self.seenExceptions = seen_exceptions

    def is_test_node(self, node: ast.AST) -> bool:
        class TestVisitor(ast.NodeVisitor):
            def __init__(self, nd):
                self._node = nd
                self._is_test_node = False

            def visit(self, n: ast.AST) -> Any:
                if self._is_test_node:
                    return

                if hasattr(n, "test"):
                    if self._node == n.test:
                        self._is_test_node = True

                self.generic_visit(n)

            def is_test_node(self):
                return self._is_test_node

        test_visitor = TestVisitor(node)
        test_visitor.visit(self.tree)
        is_test_node = test_visitor.is_test_node()
        return is_test_node

    def visit(self, node: ast.AST) -> Any:
        candidate_name = self._get_candidate_name(node)
        seen_exp_name = self._get_seen_exception_name(node)

        if candidate_name is not None and self.is_test_node(node):
            return self._instrument_test_predicate(node, candidate_name)
        if seen_exp_name is not None:
            return self._instrument_seen_exception(node, seen_exp_name)

        return self.generic_visit(node)

    # TODO: if node.end_lineno exists, use it. Otherwise, the following one.
    def _get_ending_line(self, node):
        line_end_max = -1

        if hasattr(node, "__dict__"):
            all_att = node.__dict__
            for att in all_att:
                att_instance = node.__getattribute__(att)
                if isinstance(att_instance, list):
                    for subAtt in att_instance:
                        line_end_max = max(
                            self._get_ending_line(subAtt),
                            line_end_max,
                        )
                else:
                    line_end_max = max(
                        self._get_ending_line(att_instance),
                        line_end_max,
                    )
                if hasattr(att_instance, "lineno"):
                    line_end_max = max(att_instance.lineno, line_end_max)

        if hasattr(node, "lineno"):
            line_end_max = max(node.lineno, line_end_max)
        return line_end_max

    @staticmethod
    def _instrument_test_predicate(node, candidate_name):
        node_as_text = astor.to_source(node).strip()
        new_node_as_text = (
            f"fauxpy_inst.wrap_pred_to_switch({node_as_text}, '{candidate_name}')"
        )
        new_ast = ast.parse(new_node_as_text)
        new_node_ast = new_ast.body[0].value
        return new_node_ast

    @staticmethod
    def _instrument_seen_exception(node, seen_exp_name):
        # TODO: the solution is ad hoc. Find a better way for it.
        node_as_text = astor.to_source(node).strip()
        visit_exp_statement_as_text = (
            f"fauxpy_inst.exception_seen_at_next_line('{seen_exp_name}')"
        )
        new_node_as_text = f"{visit_exp_statement_as_text}\n{node_as_text}"
        new_node_ast = ast.parse(new_node_as_text)
        return new_node_ast

    def _get_candidate_name(self, node):
        if hasattr(node, "lineno"):
            for predicate in self.candidatePredicates:
                line_start, line_end, candidate_name = predicate
                if line_start == node.lineno and line_end == self._get_ending_line(
                    node
                ):
                    return candidate_name
        return None

    def _get_seen_exception_name(self, node):
        if hasattr(node, "lineno"):
            for seenException in self.seenExceptions:
                line_number, seen_exp_name = seenException
                if line_number == node.lineno:
                    return seen_exp_name
        return None
