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

from fauxpy.fault_localization.mbfl.cosmicray_mutant_generator.mutant import Mutant


class MutantGenerator:
    @staticmethod
    def _make_diff(original_source, mutated_source, module_path):
        # Comment it.
        # This function is a modified version of the following function:
        # https://github.com/sixty-north/cosmic-ray/blob/release/v8.3.5/src/cosmic_ray/mutating.py#L174
        # Module: cosmic_ray/mutating.py
        # Function: _make_diff

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

    @staticmethod
    def produce_mutation(
        module_path: str, operator, occurrence: int
    ) -> Tuple[str, Optional[str]]:
        # This function is a modified version of the following function:
        # https://github.com/sixty-north/cosmic-ray/blob/release/v8.3.5/src/cosmic_ray/mutating.py#L113
        # Module: cosmic_ray/mutating.py
        # Function: apply_mutation
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

    def _get_all_mutant_list(
        self, module_path: str, operator_names: List[str]
    ) -> List[Mutant]:

        # This function is a modified version of the following function:
        # https://github.com/sixty-north/cosmic-ray/blob/release/v8.3.5/src/cosmic_ray/commands/init.py#L15
        # Module: cosmic_ray/commands/init.py
        # Function: _all_work_items

        mutant_list: List[Mutant] = []

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
                original_code, mutated_code = self.produce_mutation(
                    module_path, operator, occurrence
                )
                if mutated_code is not None:
                    module_diff = self._make_diff(
                        original_code, mutated_code, pathlib.Path(module_path)
                    )
                    mutant = Mutant(
                        module_path=str(module_path),
                        operator_name=op_name,
                        occurrence=occurrence,
                        start_pos=start_pos,
                        end_pos=end_pos,
                        module_content=mutated_code,
                        module_diff=module_diff,
                    )

                    mutant_list.append(mutant)

        return mutant_list

    def get_mutants_for_module_and_lines(
        self,
        module_path: str,
        line_numbers: Optional[List[int]] = None,
        operator_mutation_target_unique: bool = True,
    ) -> List[Mutant]:
        # The API written by me.
        """
        Given a module, it returns a list of mutants for every single
        mutable target that is in the lineNumbers list.
        :param operator_mutation_target_unique: if set to true, for each mutable target
                    and each mutation operator, only one mutation is returned.
                    For instance, in a = a + 1, the mutation operator core/NumberReplacer
                    can be applied multiple times to 1 and produce several mutants. But this
                    function returns only one of them when this parameter is set to True.
        :param module_path: the absolute path to the module for which mutants are generated.
        :param line_numbers: the list of line numbers in the module in modulePath for which
                            mutants should be generated. For line numbers not in this
                            list, no mutants will be generated. If it is None, it generates mutants
                            for all line numbers.
        :return: a list of mutants.
        """

        operator_names = list(cosmic_ray.plugins.operator_names())
        mutant_list = self._get_all_mutant_list(module_path, operator_names)

        if line_numbers is not None:
            mutant_list = [
                x
                for x in mutant_list
                if x.start_pos[0] in line_numbers or x.end_pos[0] in line_numbers
            ]

        if operator_mutation_target_unique:
            new_mutant_list = []
            while len(mutant_list) > 0:
                tmp = mutant_list.pop()
                if not any(
                    tmp.operator_mutation_target_equal_to(x) for x in mutant_list
                ):
                    new_mutant_list.append(tmp)

            mutant_list = new_mutant_list

        return mutant_list
