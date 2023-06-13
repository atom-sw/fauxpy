import ast
from typing import List, Tuple, Any, Optional

import astor


class InstrumentationTransformer(ast.NodeTransformer):
    def __init__(self,
                 tree,
                 candidatePredicates,
                 seenExceptions):
        self.tree = tree
        self.candidatePredicates = candidatePredicates
        self.seenExceptions = seenExceptions

    def isTestNode(self, node: ast.AST) -> bool:
        class TestVisitor(ast.NodeVisitor):
            def __init__(self, nd):
                self._node = nd
                self._isTestNode = False

            def visit(self, n: ast.AST) -> Any:
                if self._isTestNode:
                    return

                if hasattr(n, "test"):
                    if self._node == n.test:
                        self._isTestNode = True

                self.generic_visit(n)

            def isTestNode(self):
                return self._isTestNode

        testVisitor = TestVisitor(node)
        testVisitor.visit(self.tree)
        isTestNode = testVisitor.isTestNode()
        return isTestNode

    def visit(self, node: ast.AST) -> Any:
        candidateName = self._getCandidateName(node)
        seenExpName = self._getSeenExceptionName(node)

        if candidateName is not None and self.isTestNode(node):
            return InstrumentationTransformer._instrumentTestPredicate(node, candidateName)
        if seenExpName is not None:
            return InstrumentationTransformer._instrumentSeenException(node, seenExpName)

        return self.generic_visit(node)

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
                        lineEndMax = max(InstrumentationTransformer._getEndingLine(subAtt), lineEndMax)
                else:
                    lineEndMax = max(InstrumentationTransformer._getEndingLine(attInstance), lineEndMax)
                if hasattr(attInstance, "lineno"):
                    lineEndMax = max(attInstance.lineno, lineEndMax)

        if hasattr(node, "lineno"):
            lineEndMax = max(node.lineno, lineEndMax)
        return lineEndMax

    @staticmethod
    def _instrumentTestPredicate(node, candidateName):
        nodeAsText = astor.to_source(node).strip()
        newNodeAsText = f"fauxpy_inst.wrap_pred_to_switch({nodeAsText}, '{candidateName}')"
        newAst = ast.parse(newNodeAsText)
        newNodeAst = newAst.body[0].value
        return newNodeAst

    @staticmethod
    def _instrumentSeenException(node, seenExpName):
        # TODO: the solution is ad hoc. Find a better way for it.
        nodeAsText = astor.to_source(node).strip()
        visitExpStatementAsText = f"fauxpy_inst.exception_seen_at_next_line('{seenExpName}')"
        newNodeAsText = f"{visitExpStatementAsText}\n{nodeAsText}"
        newNodeAst = ast.parse(newNodeAsText)
        return newNodeAst

    def _getCandidateName(self, node):
        if hasattr(node, "lineno"):
            for predicate in self.candidatePredicates:
                lineStart, lineEnd, candidateName = predicate
                if lineStart == node.lineno and lineEnd == InstrumentationTransformer._getEndingLine(node):
                    return candidateName
        return None

    def _getSeenExceptionName(self, node):
        if hasattr(node, "lineno"):
            for seenException in self.seenExceptions:
                lineNumber, seenExpName = seenException
                if lineNumber == node.lineno:
                    return seenExpName
        return None


def _addInstrumentationImport(astTree):
    def isFromFuture(x) -> bool:
        if isinstance(x, ast.ImportFrom):
            return x.module == "__future__"
        return False

    # Probably it is OK for finding docstrings
    # at the beginning of a module.
    def isDocString(x) -> bool:
        if (isinstance(x, ast.Expr) and
                ((isinstance(x.value, ast.Str) and isinstance(x.value.s, str)) or  # for Python 3.6 and Python 3.7
                 (isinstance(x.value, ast.Constant) and isinstance(x.value.value, str)))):  # for Python 3.8 and Python 3.9
            return True
        return False

    index = 0
    for index, item in enumerate(astTree.body):
        if not isFromFuture(item) and not isDocString(item):
            break

    newImport = ast.ImportFrom(module='fauxpy', names=[ast.alias(name='fauxpy_inst', asname=None)], level=0)
    astTree.body.insert(index, newImport)


def instrumentCurrentFilePath(filePath: str,
                              candidatePredicates: List[Tuple[int, int, str]],
                              seenExceptions: List[Tuple[int, str]]) -> Optional[str]:
    with open(filePath, "r") as source:
        tree = ast.parse(source.read())

    astTransformer = InstrumentationTransformer(tree, candidatePredicates, seenExceptions)
    newAst = astTransformer.visit(tree)
    _addInstrumentationImport(newAst)
    ast.fix_missing_locations(newAst)
    try:
        newAstContentAsText = astor.to_source(newAst)
    except AssertionError:
        return None
    return newAstContentAsText
