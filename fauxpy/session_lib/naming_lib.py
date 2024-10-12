from typing import Tuple


def convert_test_name_to_components(test_name: str) -> Tuple[str, int, str]:
    components = test_name.split("::")
    return components[0], int(components[1]), components[2]


def get_statement_name(path: str, line_number: int):
    statement_name = path + "::" + str(line_number)
    return statement_name


def convert_statement_name_to_components(statement_name: str) -> Tuple[str, int]:
    components = statement_name.split("::")
    return components[0], int(components[1])


def get_covered_function_name(
    path: str, function_name: str, line_start: int, line_end: int
):
    cov_func_name = (
        path + "::" + function_name + "::" + str(line_start) + "::" + str(line_end)
    )
    return cov_func_name


def test_name_to_file_name(test_name: str):
    new_test_name = test_name.replace("/", "_").replace("/", "_").replace(":", "_")
    return new_test_name


def get_generalized_test_name(file_path: str, function_name: str) -> str:
    """
    For parametrized tests, this function removes the parameter values,
    leaving only the function name to represent all variations of the test.
    For non-parametrized tests, the original test name is returned as is.
    """
    # filePath, _, functionName = convertTestNameToComponents(testName)
    generalized_function_name = function_name.split("[")[0]

    # For CLASS_NAME.FUNCTION_NAME
    if "." in generalized_function_name:
        class_name, function_name = generalized_function_name.split(".")
        generalized_function_name = "::".join([class_name, function_name])

    generalized_test_func_path = "::".join([file_path, generalized_function_name])
    return generalized_test_func_path
