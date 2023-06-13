from typing import Tuple


class TestInformation:
    def __init__(self, location: Tuple[str, int, str], nodeId: str):
        self.location = location
        self.nodeId = nodeId

    def getPath(self):
        # Because of some weird test cases in Pandas 54
        # that are inherited in different test modules
        # (see pandas/tests/extension/test_period.py for example)
        # we need to have different ways of making test names
        # or there will be multiple executed test cases with
        # the same names.
        if self.isInheritedTestCase():
            testPath = self.getCallerPath()
        else:
            testPath = self.location[0]
        
        return testPath

    def getLineNumber(self):
        if self.isInheritedTestCase():
            testLineNumber = -1
        else:
            testLineNumber = self.location[1]

        return testLineNumber

    def getMethodName(self):
        testMethodName = self.location[2]
        return testMethodName

    def isInheritedTestCase(self):
        return self.location[0] != self.getCallerPath()

    def getCallerPath(self):
        return self.nodeId.split("::")[0]

    def getTestName(self):
        testName = self.getPath() + "::" + str(self.getLineNumber()) + "::" + _quoteFreeTestMethodName(self.getMethodName())
        return testName


def _quoteFreeTestMethodName(methodName: str):
    qftm = methodName.replace("'", "XquoteX").replace('"', "XdoubleQuoteX")
    return qftm
