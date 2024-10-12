import ast

import pytest

from fauxpy.fault_localization.ps.ast_lib.instrumentation_manager import (
    InstrumentationManager,
)
from tests.common import getDataPath


def test_instrument_one_line_if_minimal():
    file_path = str(getDataPath("predicate_switching", "one_line_if.pyt").absolute())
    candidate_predicates = [(1, 1, "pred_1")]
    seen_exceptions = []
    instrumentation_manager = InstrumentationManager()
    inst_file_content = instrumentation_manager.instrument_current_file_path(
        file_path, candidate_predicates, seen_exceptions
    )
    expected_string = "from fauxpy import fauxpy_inst\nif fauxpy_inst.wrap_pred_to_switch(not line, 'pred_1'):\n    break\n"
    assert inst_file_content == expected_string


def test_instrument_normal_if_minimal():
    file_path = str(getDataPath("predicate_switching", "normal_if.pyt").absolute())
    candidate_predicates = [(1, 1, "pred_2")]
    seen_exceptions = []
    instrumentation_manager = InstrumentationManager()
    inst_file_content = instrumentation_manager.instrument_current_file_path(
        file_path, candidate_predicates, seen_exceptions
    )
    expected_string = "from fauxpy import fauxpy_inst\nif fauxpy_inst.wrap_pred_to_switch(not line, 'pred_2'):\n    raise TokenError('EOF in multi-line string', strstart)\n"
    assert inst_file_content == expected_string


def test_instrument_multiline_predicate_normal_if():
    file_path = str(
        getDataPath(
            "predicate_switching", "multiline_predicate_normal_if.pyt"
        ).absolute()
    )
    candidate_predicates = [(1, 3, "pred_3")]
    seen_exceptions = []
    instrumentation_manager = InstrumentationManager()
    inst_file_content = instrumentation_manager.instrument_current_file_path(
        file_path, candidate_predicates, seen_exceptions
    )
    expected_string = """from fauxpy import fauxpy_inst
if fauxpy_inst.wrap_pred_to_switch(not line or x > 12 and y <= z, 'pred_3'):
    raise TokenError('EOF in multi-line string', strstart)
"""
    assert inst_file_content == expected_string


def test_instrument_one_line_if_black14():
    file_path = str(getDataPath("predicate_switching", "tokenize.pyt").absolute())
    candidate_predicates = [(395, 395, "pred_20")]
    seen_exceptions = []
    instrumentation_manager = InstrumentationManager()
    inst_file_content = instrumentation_manager.instrument_current_file_path(
        file_path, candidate_predicates, seen_exceptions
    )
    instrumentation_string = "if fauxpy_inst.wrap_pred_to_switch(not line, 'pred_20'):"
    assert instrumentation_string in inst_file_content


def test_instrument_normal_if_black14():
    file_path = str(getDataPath("predicate_switching", "tokenize.pyt").absolute())
    candidate_predicates = [(374, 374, "pred_18")]
    seen_exceptions = []
    instrumentation_manager = InstrumentationManager()
    inst_file_content = instrumentation_manager.instrument_current_file_path(
        file_path, candidate_predicates, seen_exceptions
    )
    instrumentation_string = "if fauxpy_inst.wrap_pred_to_switch(not line, 'pred_18'):"
    assert instrumentation_string in inst_file_content


def test_instrument_astor_assertion_error():
    # Found in fastapi 11 running PS.
    # It is a bug in astor. It cannot
    # even transform back the untouched ast.
    # We fix the bug by simply ignoring
    # Python modules that cannot be instrumented.

    file_path = str(getDataPath("predicate_switching", "utils.pyt").absolute())
    candidate_predicates = [
        (131, 131, "Pred_1"),
        (134, 134, "Pred_2"),
        (137, 137, "Pred_3"),
        (149, 149, "Pred_4"),
        (157, 157, "Pred_5"),
        (159, 159, "Pred_6"),
        (80, 80, "Pred_7"),
        (242, 242, "Pred_8"),
        (117, 117, "Pred_9"),
        (124, 124, "Pred_10"),
        (253, 253, "Pred_11"),
    ]
    seen_exceptions = [(87, "Exception_0"), (87, "Exception_3")]
    instrumentation_manager = InstrumentationManager()
    instrumentation_manager.instrument_current_file_path(
        file_path, candidate_predicates, seen_exceptions
    )


@pytest.mark.parametrize(
    "file_name",
    [
        "future_import.pyt",
        "cookiecutter_4_utils.pyt",  # bug found in cookiecutter 4 running PS
        "spacy_2_compat.pyt",  # bug found in spacy 2 running PS
    ],
)
def test__add_instrumentation_import(file_name):
    file_path = str(getDataPath("predicate_switching", file_name).absolute())
    with open(file_path, "r") as source:
        tree_obj = ast.parse(source.read())

    instrumentation_manager = InstrumentationManager()
    instrumentation_manager._add_instrumentation_import(tree_obj)

    def is_from_future(x) -> bool:
        if isinstance(x, ast.ImportFrom):
            return x.module == "__future__"
        return False

    def is_doc_string(x) -> bool:
        if isinstance(x, ast.Expr) and (
            (isinstance(x.value, ast.Str) and isinstance(x.value.s, str))
            or (  # for Python 3.6 and Python 3.7
                isinstance(x.value, ast.Constant) and isinstance(x.value.value, str)
            )
        ):  # for Python 3.8 and Python 3.9
            return True
        return False

    for index, item in enumerate(tree_obj.body):
        if is_from_future(item):
            before_from_future = list(
                map(
                    lambda x: is_from_future(x) or is_doc_string(x),
                    tree_obj.body[0:index],
                )
            )
            assert len(before_from_future) == 0 or all(before_from_future)
