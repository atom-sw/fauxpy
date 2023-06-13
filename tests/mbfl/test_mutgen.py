from fauxpy.mbfl.mutgen import _main
from tests.common import getDataPath


def test__getAllMutants_for_error_Name_object_having_no_attribute_children_on_real_module():
    """Revealing a bug in CosmicRay using a module from pandas56.
    If an exception is in parentheses, CosmicRay throws an exception."""

    module_path = str(getDataPath("mbfl", "offsets.pyt").absolute())
    op_name = "core/ExceptionReplacer"
    operator_names = [op_name]

    mutants = _main._getAllMutants(module_path, operator_names)
    assert len(mutants) == 0


def test__getAllMutants_for_error_Name_object_having_no_attribute_children_on_minimal_module():
    """Revealing a bug in CosmicRay using a minimal example inspired by pandas56.
    If an exception is in parentheses, CosmicRay throws an exception."""

    module_path = str(getDataPath("mbfl", "minimal_exception_mutation.pyt").absolute())
    op_name = "core/ExceptionReplacer"
    operator_names = [op_name]

    mutants = _main._getAllMutants(module_path, operator_names)
    assert len(mutants) == 0


def test__getAllMutants_a_cosmic_ray_mutation_operator_on_real_module():
    module_path = str(getDataPath("mbfl", "offsets.pyt").absolute())
    op_name = "core/ReplaceBinaryOperator_Add_Mul"
    operator_names = [op_name]

    all_mutants = _main._getAllMutants(module_path, operator_names)
    assert len(all_mutants) == 84
    assert all_mutants[0].startPos == (130, 45) and all_mutants[0].endPos == (130, 46)
    assert all_mutants[-1].startPos == (2765, 20) and all_mutants[-1].endPos == (2765, 21)


def test__getAllMutants_a_cosmic_ray_mutation_operator_on_minimal_module():
    module_path = str(getDataPath("mbfl", "minimal_exception_mutation.pyt").absolute())
    op_name = "core/ReplaceBinaryOperator_Add_Sub"
    operator_names = [op_name]

    all_mutants = _main._getAllMutants(module_path, operator_names)
    assert len(all_mutants) == 1
    assert all_mutants[0].startPos == (6, 13) and all_mutants[0].endPos == (6, 14)
