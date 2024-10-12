import ast
from typing import List, Tuple, Optional

import astor

from fauxpy.fault_localization.ps.ast_lib.instrumentation_transformer import (
    InstrumentationTransformer,
)


class InstrumentationManager:
    @staticmethod
    def _add_instrumentation_import(ast_tree):
        def is_from_future(x) -> bool:
            if isinstance(x, ast.ImportFrom):
                return x.module == "__future__"
            return False

        # Probably it is OK for finding docstrings
        # at the beginning of a module.
        def is_doc_string(x) -> bool:
            if isinstance(x, ast.Expr) and (
                (isinstance(x.value, ast.Str) and isinstance(x.value.s, str))
                or (  # for Python 3.6 and Python 3.7
                    isinstance(x.value, ast.Constant) and isinstance(x.value.value, str)
                )
            ):  # for Python 3.8 and Python 3.9
                return True
            return False

        index = 0
        for index, item in enumerate(ast_tree.body):
            if not is_from_future(item) and not is_doc_string(item):
                break

        new_import = ast.ImportFrom(
            module="fauxpy", names=[ast.alias(name="fauxpy_inst", asname=None)], level=0
        )
        ast_tree.body.insert(index, new_import)

    def instrument_current_file_path(
        self,
        file_path: str,
        candidate_predicates: List[Tuple[int, int, str]],
        seen_exceptions: List[Tuple[int, str]],
    ) -> Optional[str]:
        with open(file_path, "r") as source:
            tree = ast.parse(source.read())

        ast_transformer = InstrumentationTransformer(
            tree, candidate_predicates, seen_exceptions
        )
        new_ast = ast_transformer.visit(tree)
        self._add_instrumentation_import(new_ast)
        ast.fix_missing_locations(new_ast)
        try:
            new_ast_content_as_text = astor.to_source(new_ast)
        except AssertionError:
            return None
        return new_ast_content_as_text
