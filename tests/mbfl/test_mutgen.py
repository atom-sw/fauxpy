from fauxpy.fault_localization.mbfl.cosmicray_mutant_generator.mutant_generator import (
    MutantGenerator,
)
from tests.common import getDataPath


def test__get_all_mutants_for_error_name_object_having_no_attribute_children_on_real_module():
    """Revealing a bug in CosmicRay using a module from pandas56.
    If an exception is in parentheses, CosmicRay throws an exception."""

    module_path = str(getDataPath("mbfl", "offsets.pyt").absolute())
    op_name = "core/ExceptionReplacer"
    operator_names = [op_name]

    mutant_generator = MutantGenerator()
    mutants = mutant_generator._get_all_mutant_list(module_path, operator_names)
    assert len(mutants) == 0


def test__get_all_mutants_for_error_name_object_having_no_attribute_children_on_minimal_module():
    """Revealing a bug in CosmicRay using a minimal example inspired by pandas56.
    If an exception is in parentheses, CosmicRay throws an exception."""

    module_path = str(getDataPath("mbfl", "minimal_exception_mutation.pyt").absolute())
    op_name = "core/ExceptionReplacer"
    operator_names = [op_name]

    mutant_generator = MutantGenerator()
    mutants = mutant_generator._get_all_mutant_list(module_path, operator_names)
    assert len(mutants) == 0


def test__get_all_mutants_a_cosmic_ray_mutation_operator_on_real_module():
    module_path = str(getDataPath("mbfl", "offsets.pyt").absolute())
    op_name = "core/ReplaceBinaryOperator_Add_Mul"
    operator_names = [op_name]

    mutant_generator = MutantGenerator()
    all_mutants = mutant_generator._get_all_mutant_list(module_path, operator_names)
    assert len(all_mutants) == 84
    assert all_mutants[0].start_pos == (130, 45) and all_mutants[0].end_pos == (130, 46)
    assert all_mutants[-1].start_pos == (2765, 20) and all_mutants[-1].end_pos == (
        2765,
        21,
    )


def test__get_all_mutants_a_cosmic_ray_mutation_operator_on_minimal_module():
    module_path = str(getDataPath("mbfl", "minimal_exception_mutation.pyt").absolute())
    op_name = "core/ReplaceBinaryOperator_Add_Sub"
    operator_names = [op_name]

    mutant_generator = MutantGenerator()
    all_mutants = mutant_generator._get_all_mutant_list(module_path, operator_names)
    assert len(all_mutants) == 1
    assert all_mutants[0].start_pos == (6, 13) and all_mutants[0].end_pos == (6, 14)
