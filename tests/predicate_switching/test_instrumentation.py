import ast

import pytest

from fauxpy.predicate_switching import ast_manager
from fauxpy.predicate_switching.ast_manager import instrumentation
from tests.common import getDataPath


def test_instrumentOneLineIfMinimal():
    filePath = str(getDataPath("predicate_switching", "one_line_if.pyt").absolute())
    candidatePredicates = [(1, 1, "pred_1")]
    seenExceptions = []
    instFileContent = ast_manager.instrumentCurrentFilePath(filePath,
                                                            candidatePredicates,
                                                            seenExceptions)
    expectedString = "from fauxpy import fauxpy_inst\nif fauxpy_inst.wrap_pred_to_switch(not line, 'pred_1'):\n    break\n"
    assert instFileContent == expectedString


def test_instrumentNormalIfMinimal():
    filePath = str(getDataPath("predicate_switching", "normal_if.pyt").absolute())
    candidatePredicates = [(1, 1, "pred_2")]
    seenExceptions = []
    instFileContent = ast_manager.instrumentCurrentFilePath(filePath,
                                                            candidatePredicates,
                                                            seenExceptions)
    expectedString = "from fauxpy import fauxpy_inst\nif fauxpy_inst.wrap_pred_to_switch(not line, 'pred_2'):\n    raise TokenError('EOF in multi-line string', strstart)\n"
    assert instFileContent == expectedString


def test_instrumentMultilinePredicateNormalIf():
    filePath = str(getDataPath("predicate_switching", "multiline_predicate_normal_if.pyt").absolute())
    candidatePredicates = [(1, 3, "pred_3")]
    seenExceptions = []
    instFileContent = ast_manager.instrumentCurrentFilePath(filePath,
                                                            candidatePredicates,
                                                            seenExceptions)
    expectedString = """from fauxpy import fauxpy_inst
if fauxpy_inst.wrap_pred_to_switch(not line or x > 12 and y <= z, 'pred_3'):
    raise TokenError('EOF in multi-line string', strstart)
"""
    assert instFileContent == expectedString


def test_instrumentOneLineIfBlack14():
    filePath = str(getDataPath("predicate_switching", "tokenize.pyt").absolute())
    candidatePredicates = [(395, 395, "pred_20")]
    seenExceptions = []
    instFileContent = ast_manager.instrumentCurrentFilePath(filePath,
                                                            candidatePredicates,
                                                            seenExceptions)
    instrumentationString = "if fauxpy_inst.wrap_pred_to_switch(not line, 'pred_20'):"
    assert instrumentationString in instFileContent


def test_instrumentNormalIfBlack14():
    filePath = str(getDataPath("predicate_switching", "tokenize.pyt").absolute())
    candidatePredicates = [(374, 374, "pred_18")]
    seenExceptions = []
    instFileContent = ast_manager.instrumentCurrentFilePath(filePath,
                                                            candidatePredicates,
                                                            seenExceptions)
    instrumentationString = "if fauxpy_inst.wrap_pred_to_switch(not line, 'pred_18'):"
    assert instrumentationString in instFileContent


def test_instrumentAstorAssertionError():
    # Found in fastapi 11 running PS.
    # It is a bug in astor. It cannot
    # even transform back the untouched ast.
    # We fix the bug by simply ignoring
    # Python modules that cannot be instrumented.

    filePath = str(getDataPath("predicate_switching", "utils.pyt").absolute())
    candidatePredicates = [(131, 131, 'Pred_1'), (134, 134, 'Pred_2'),
                           (137, 137, 'Pred_3'), (149, 149, 'Pred_4'),
                           (157, 157, 'Pred_5'), (159, 159, 'Pred_6'),
                           (80, 80, 'Pred_7'), (242, 242, 'Pred_8'),
                           (117, 117, 'Pred_9'), (124, 124, 'Pred_10'),
                           (253, 253, 'Pred_11')]
    seenExceptions = [(87, 'Exception_0'), (87, 'Exception_3')]
    instFileContent = ast_manager.instrumentCurrentFilePath(filePath,
                                                            candidatePredicates,
                                                            seenExceptions)


@pytest.mark.parametrize("fileName", [
    "future_import.pyt",
    "cookiecutter_4_utils.pyt",  # bug found in cookiecutter 4 running PS
    "spacy_2_compat.pyt"  # bug found in spacy 2 running PS
])
def test__addInstrumentationImport(fileName):
    filePath = str(getDataPath("predicate_switching", fileName).absolute())
    with open(filePath, "r") as source:
        treeObj = ast.parse(source.read())

    instrumentation._addInstrumentationImport(treeObj)

    def isFromFuture(x) -> bool:
        if isinstance(x, ast.ImportFrom):
            return x.module == "__future__"
        return False

    def isDocString(x) -> bool:
        if (isinstance(x, ast.Expr) and
                ((isinstance(x.value, ast.Str) and isinstance(x.value.s, str)) or  # for Python 3.6 and Python 3.7
                 (isinstance(x.value, ast.Constant) and isinstance(x.value.value, str)))):  # for Python 3.8 and Python 3.9
            return True
        return False

    for index, item in enumerate(treeObj.body):
        if isFromFuture(item):
            beforeFromFuture = list(map(lambda x: isFromFuture(x) or isDocString(x), treeObj.body[0:index]))
            assert len(beforeFromFuture) == 0 or all(beforeFromFuture)
