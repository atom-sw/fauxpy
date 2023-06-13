from typing import List
from .naming import getGeneralizedTestName


# def _reformatPytestTest(test: str):
#     reformatted = ""
#     testComponents = test.split("::")
#
#     # Target tests are functions in the forms
#     # FilePath::FunctionName or
#     # FilePath::ClassName::FunctionName
#     # So they must have two or three components
#     assert 2 <= len(testComponents) <= 3
#
#     if len(testComponents) == 2:
#         reformatted = "::".join([testComponents[0], testComponents[1]])  # FilePath::FunctionName
#     elif len(testComponents) == 3:
#         functionName = ".".join([testComponents[1], testComponents[2]])  # ClassName.FunctionName
#         reformatted = "::".join([testComponents[0], functionName])  # FilePath::ClassName.FunctionName
#
#     return reformatted


class TargetFailingTests(object):
    def __init__(self,
                 targetFailingTestsList: List[str]):
        self._targetFailingTestsList = targetFailingTestsList

    def getFailingTests(self):
        return self._targetFailingTestsList

    @classmethod
    def fromFile(cls, filePath):
        try:
            with open(filePath, "r") as file:
                content = file.read()
            listContent = content.strip().split("\n")
            listContentStriped = [x.strip() for x in listContent]
            listContentStripedNoComments = list(filter(lambda x: not x.startswith("#"), listContentStriped))
            if len(listContentStripedNoComments) == 0 or all([x == "" for x in listContentStripedNoComments]):
                return None
            else:
                return TargetFailingTests(listContentStripedNoComments)
        except FileNotFoundError:
            return None

    @classmethod
    def fromListString(cls, failingList):
        failingListStriped = [x.strip() for x in failingList]
        if len(failingListStriped) == 0:
            return None
        else:
            return TargetFailingTests(failingListStriped)

    def isTargetTest(self, currentTestPath, currentTestMethodName):
        # currentTestFullPath = "::".join([currentTestPath, currentTestMethodName])
        currentTestFullPathGeneralized = getGeneralizedTestName(currentTestPath, currentTestMethodName)
        for targetTest in self._targetFailingTestsList:
            # reformattedTargetFilePath = _reformatPytestTest(targetTest)
            if currentTestFullPathGeneralized == targetTest:
                return True
        return False


