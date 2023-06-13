from typing import Tuple


def convertTestNameToComponents(testName: str) -> Tuple[str, int, str]:
    components = testName.split("::")
    return components[0], int(components[1]), components[2]


def getStatementName(path: str, lineNumber: int):
    statementName = path + "::" + str(lineNumber)
    return statementName


def convertStatementNameToComponents(statementName: str) -> Tuple[str, int]:
    components = statementName.split("::")
    return components[0], int(components[1])


def getCoveredFunctionName(path: str, functionName: str, lineStart: int, lineEnd: int):
    covFuncName = path + "::" + functionName + "::" + str(lineStart) + "::" + str(lineEnd)
    return covFuncName


def testNameToFileName(testName: str):
    qftm = testName.replace("/", "_").replace("/", "_").replace(":", "_")
    return qftm


def getGeneralizedTestName(filePath: str,
                           functionName: str) -> str:
    """
    Returns the general test name if the test is a parametrized test.
    i.e., it removes the parameters and keeps only the function name.
    Thus, the general test name includes all instances of a parametrized test.
    For non parametrized tests, it does nothing and returns the received test.
    """

    # filePath, _, functionName = convertTestNameToComponents(testName)
    generalizedFunctionName = functionName.split("[")[0]

    # For CLASS_NAME.FUNCTION_NAME
    if "." in generalizedFunctionName:
        className, functionName = generalizedFunctionName.split(".")
        generalizedFunctionName = "::".join([className, functionName])

    generalizedTestFuncPath = "::".join([filePath, generalizedFunctionName])
    return generalizedTestFuncPath
