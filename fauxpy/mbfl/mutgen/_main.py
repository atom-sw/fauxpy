# cosmic-ray==8.3.5
# https://github.com/sixty-north/cosmic-ray/tree/release/v8.3.5

import pathlib
from typing import List, Optional, Tuple

import cosmic_ray
import cosmic_ray.modules
from cosmic_ray.ast import get_ast, ast_nodes
from cosmic_ray.mutating import MutationVisitor
from cosmic_ray.plugins import get_operator
import difflib


class Mutant(object):
    def __init__(self,
                 modulePath: str,
                 operatorName: str,
                 startPos: Tuple[int],
                 endPos: Tuple[int],
                 occurrence: int,
                 moduleContent: str,
                 moduleDiff: List[str]):
        self.modulePath: str = modulePath
        self.operatorName: str = operatorName
        self.startPos: Tuple[int] = startPos
        self.endPos: Tuple[int] = endPos
        self.occurrence: int = occurrence
        self.moduleContent: str = moduleContent
        self.moduleDiff: List[str] = moduleDiff
        self.id = "-"

    def setId(self, val):
        self.id = val

    def getId(self):
        return self.id

    def getModulePath(self):
        return self.modulePath

    def getModuleOperator(self):
        return self.operatorName

    def getModuleContent(self):
        return self.moduleContent

    def getModuleDiffAsText(self):
        diffText = "\r\n".join(self.moduleDiff)
        return diffText

    def operatorMutationTargetEqualTo(self, mutant):
        result = self.operatorName == mutant.operatorName and \
                 self.startPos == mutant.startPos and \
                 self.endPos == mutant.endPos
        return result

    # TODO: Multiline predicates might cause problem.
    def getLineNumber(self):
        # A predicate can spread through multiple lines. In such cases,
        # we consider each line of the predicate a separate statement
        # while performing fault localization.
        # For instance, in the following predicate, we have two different lines
        # to mutate:
        # 12: if x > 10 and \
        # 13:   y < 24:
        # 14   ...
        # A mutation applied on line 12 or 13 (by for instance
        # changing the relational operators) are considered two
        # mutants with LineNumber == self.startPos[0].
        # However, putting a not operator after if affects the whole
        # predicate (i.e., both lines 12 and 13). In this case,
        # self.startPos[0] != self.endPos[0].
        # But even in this case, we consider LineNumber == self.startPos[0].
        # Thus, LineNumber is always self.startPos[0] (it is our assumption).

        return self.startPos[0]

    def getStartPos(self):
        return self.startPos[0]

    def getEndPos(self):
        return self.endPos[0]


# Comment it.
# This function is a modified version of the following function:
# https://github.com/sixty-north/cosmic-ray/blob/release/v8.3.5/src/cosmic_ray/mutating.py#L174
# Module: cosmic_ray/mutating.py
# Function: _make_diff
def _makeDiff(original_source, mutated_source, module_path):
    module_diff = ["--- mutation diff ---"]
    for line in difflib.unified_diff(
            original_source.split("\n"),
            mutated_source.split("\n"),
            fromfile="a" + str(module_path),
            tofile="b" + str(module_path),
            lineterm="",
    ):
        module_diff.append(line)
    return module_diff


# This function is a modified version of the following function:
# https://github.com/sixty-north/cosmic-ray/blob/release/v8.3.5/src/cosmic_ray/mutating.py#L113
# Module: cosmic_ray/mutating.py
# Function: apply_mutation
def produceMutation(module_path: str,
                    operator,
                    occurrence: int) -> Tuple[str, Optional[str]]:
    module_ast = get_ast(pathlib.Path(module_path))
    original_code = module_ast.get_code()
    visitor = MutationVisitor(occurrence, operator)

    mutated_ast = None
    cosmic_ray_bug_happened = False
    try:
        mutated_ast = visitor.walk(module_ast)
    except AttributeError:
        cosmic_ray_bug_happened = True

    mutated_code = None
    if visitor.mutation_applied and not cosmic_ray_bug_happened:
        mutated_code = mutated_ast.get_code()

    return original_code, mutated_code


# This function is a modified version of the following function:
# https://github.com/sixty-north/cosmic-ray/blob/release/v8.3.5/src/cosmic_ray/commands/init.py#L15
# Module: cosmic_ray/commands/init.py
# Function: _all_work_items
def _getAllMutants(module_path: str,
                   operator_names: List[str]) -> List[Mutant]:
    mutantList: List[Mutant] = []

    module_ast = get_ast(pathlib.Path(module_path))
    for op_name in operator_names:
        operator = get_operator(op_name)()

        # positions = (
        #     (start_pos, end_pos)
        #     for node in ast_nodes(module_ast)
        #     for start_pos, end_pos in operator.mutation_positions(node)
        # )

        positions = []
        for node in ast_nodes(module_ast):
            try:
                for start_pos, end_pos in operator.mutation_positions(node):
                    positions.append((start_pos, end_pos))
            except:
                positions = []
                continue

        for occurrence, (start_pos, end_pos) in enumerate(positions):
            original_code, mutated_code = produceMutation(module_path, operator, occurrence)
            if mutated_code is not None:
                moduleDiff = _makeDiff(original_code, mutated_code, pathlib.Path(module_path))
                mutant = Mutant(
                    modulePath=str(module_path),
                    operatorName=op_name,
                    occurrence=occurrence,
                    startPos=start_pos,
                    endPos=end_pos,
                    moduleContent=mutated_code,
                    moduleDiff=moduleDiff
                )

                mutantList.append(mutant)

    return mutantList


# The API written by me.
def getMutantsForModuleAndLines(modulePath: str,
                                lineNumbers: Optional[List[int]] = None,
                                operatorMutationTargetUnique: bool = True) -> List[Mutant]:
    """
    Given a module, it returns a list of mutants for every single
    mutable target that is in the lineNumbers list.
    :param operatorMutationTargetUnique: if set to true, for each mutable target
                and each mutation operator, only one mutation is returned.
                For instance, in a = a + 1, the mutation operator core/NumberReplacer
                can be applied multiple times to 1 and produce several mutants. But this
                function returns only one of them when this parameter is set to True.
    :param modulePath: the absolute path to the module for which mutants are generated.
    :param lineNumbers: the list of line numbers in the module in modulePath for which
                        mutants should be generated. For line numbers not in this
                        list, no mutants will be generated. If it is None, it generates mutants
                        for all line numbers.
    :return: a list of mutants.
    """

    operator_names = list(cosmic_ray.plugins.operator_names())
    mutantList = _getAllMutants(modulePath, operator_names)

    if lineNumbers is not None:
        mutantList = [x for x in mutantList if x.startPos[0] in lineNumbers or x.endPos[0] in lineNumbers]

    if operatorMutationTargetUnique:
        newMutantList = []
        while len(mutantList) > 0:
            tmp = mutantList.pop()
            if not any(tmp.operatorMutationTargetEqualTo(x) for x in mutantList):
                newMutantList.append(tmp)

        mutantList = newMutantList

    return mutantList
