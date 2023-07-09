from typing import List, Tuple, Set


class ExecutionTrace(object):
    def __init__(
        self,
        executedLinesList: List[Tuple[str, int]],
        executedLinesSet: Set[Tuple[str, int]],
    ):
        self.executedLinesList = executedLinesList
        self.executedLinesSet = executedLinesSet

    def getExecutedFiles(self) -> List[str]:
        executedFiles = set()
        for execLine in self.executedLinesSet:
            executedFiles.add(execLine[0])

        return list(executedFiles)

    def getExecutedLineNumbersForFileInOrder(self, file: str) -> List[int]:
        """
        This function returns the lines in the order of their execution.
        Some lines might exist multiple times if they are executed more that once.
        """
        lineNumbers = []
        for execLine in self.executedLinesList:
            if execLine[0] == file:
                lineNumbers.append(execLine[1])

        return lineNumbers

    def getExecutedLinesInOrder(self) -> List[Tuple[str, int]]:
        return self.executedLinesList

    def getExecutedLinesNoOrder(self) -> List[Tuple[str, int]]:
        return list(self.executedLinesSet)
