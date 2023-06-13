from typing import List, Tuple

from . import database


def _getSeenExceptionsStoreDb(exceptions: List[Tuple[str, str, int]]):
    for i, exp in enumerate(exceptions):
        testName, filePath, lineNumber = exp
        exceptionName = f"Exception_{i}"

        database.insertSeenExceptions(testName=testName,
                                      filePath=filePath,
                                      lineNumber=lineNumber,
                                      exceptionName=exceptionName)


def getSeenExceptionsStoreDb():
    """
    Stores in database the info about exception raises
    that happen while running the failing tests.
    """

    exceptions = database.selectTestCaseExceptions()
    _getSeenExceptionsStoreDb(exceptions)
