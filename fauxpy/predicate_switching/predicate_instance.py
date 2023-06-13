from typing import List, Tuple

from . import database, ast_manager


def _getShadowedCoveredPredicatesForCoveredLinesStoreDb(executedLines: List[Tuple[str, int]]):
    for testName, filePath, lineNumber, testType in executedLines:
        assert testType == "failed"
        lineStart, lineEnd = ast_manager.getPredicateInstanceRangeForProgramLine(filePath, lineNumber)
        if not lineStart == lineEnd == -1:
            database.insertShadowedCoveredPredicate(testName, filePath, lineNumber,
                                                    lineStart, lineEnd)


def _nameExecutedPredicatesStoreDb(executedPredicates):
    for i, exePred in enumerate(executedPredicates):
        filePath, lineStart, lineEnd = exePred
        predicateName = f"Pred_{i}"

        database.insertCandidatePredicate(filePath=filePath, lineStart=lineStart,
                                          lineEnd=lineEnd, predicateName=predicateName)


def getCandidatePredicatesStoreDb():
    coveredLines = database.selectCoveredLinesWithTestTypesForAllFailedTests()
    _getShadowedCoveredPredicatesForCoveredLinesStoreDb(coveredLines)
    distinctExecutedPredicates = database.selectDistinctExecutedSourceCodePredicates()
    _nameExecutedPredicatesStoreDb(distinctExecutedPredicates)
