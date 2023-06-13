import sqlite3
from typing import List, Optional, Tuple

from .. import common

_Con: sqlite3.Connection


class _Names(object):
    fileName = "fauxpy.db"
    testCaseTable = "TestCase"
    coveredLinesForTestTable = "CoveredLinesForTest"
    emptyTestCaseTable = "EmptyTest"
    shadowedCoveredPredicateTable = "ShadowedCoveredPredicate"
    coveredLinesWithTestTypesView = "CoveredLinesWithTestTypes"
    candidatePredicateTable = "CandidatePredicate"
    seenExceptionTable = "SeenException"
    predicateSequenceTable = "PredicateSequence"
    scoredEntityTable = "ScoredEntity"
    testTimeTable = "TestTime"
    timeoutPredicateInstanceTable = "TimeoutPredicateInstance"
    badExecutionPredicateInstanceTable = "BadExecutionPredicateInstance"
    astorAssertErrorInfoTable = "AstorAssertErrorInfo"


# TODO: Add indices.
def init():
    global _Con

    def getDatabaseSchema():
        testCaseTableCreateCommand = f"CREATE TABLE {_Names.testCaseTable} " \
                                     f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                                     f"TestName TEXT NOT NULL UNIQUE, " \
                                     f"Type TEXT NOT NULL, " \
                                     f"ExceptionFilePath TEXT NOT NULL, " \
                                     f"ExceptionLineNumber INTEGER NOT NULL, " \
                                     f"Target INTEGER NOT NULL);"

        executedLineForTestTableCreateCommand = f"CREATE TABLE {_Names.coveredLinesForTestTable} " \
                                                f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                                                f"TestName TEXT NOT NULL, " \
                                                f"FilePath TEXT NOT NULL, " \
                                                f"LineNumber INTEGER NOT NULL);"

        emptyTestTableCreateCommand = f"CREATE TABLE {_Names.emptyTestCaseTable} " \
                                      f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                                      f"TestName TEXT NOT NULL UNIQUE);"

        shadowedCoveredPredicateTableCreateCommand = f"CREATE TABLE {_Names.shadowedCoveredPredicateTable} " \
                                                     f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                                                     f"TestName TEXT NOT NULL, " \
                                                     f"FilePath TEXT NOT NULL, " \
                                                     f"ExeLineNumber INTEGER NOT NULL, " \
                                                     f"LineStart INTEGER NOT NULL, " \
                                                     f"LineEnd INTEGER NOT NULL );"

        candidatePredicateTableCreateCommand = f"CREATE TABLE {_Names.candidatePredicateTable} " \
                                               f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                                               f"FilePath TEXT NOT NULL, " \
                                               f"LineStart INTEGER NOT NULL, " \
                                               f"LineEnd INTEGER NOT NULL," \
                                               f"PredicateName TEXT NOT NULL);"

        # Todo: the combination (TestName, ExceptionFilePath, ExceptionLineNumber, ExceptionName) is unique.
        #  Add this constraint to this DB.
        seenExceptionTableCreateCommand = f"CREATE TABLE {_Names.seenExceptionTable} " \
                                          f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                                          f"TestName TEXT NOT NULL UNIQUE, " \
                                          f"ExceptionFilePath TEXT NOT NULL, " \
                                          f"ExceptionLineNumber INTEGER NOT NULL," \
                                          f"ExceptionName TEXT NOT NULL);"

        predicateSequenceTableCreateCommand = f"CREATE TABLE {_Names.predicateSequenceTable} " \
                                              f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                                              f"TestName TEXT NOT NULL UNIQUE, " \
                                              f"PredicateSequence TEXT NOT NULL," \
                                              f"IndexedPredicateSequence TEXT NOT NULL );"

        # ToDo: TestName has unique constraint.
        scoredEntityTableCreateCommand = f"CREATE TABLE {_Names.scoredEntityTable} " \
                                         f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                                         f"TestName TEXT NOT NULL, " \
                                         f"Entity TEXT NOT NULL, " \
                                         f"Score INTEGER NOT NULL);"

        testTimeTableCreateCommand = f"CREATE TABLE {_Names.testTimeTable} " \
                                     f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                                     f"TestName TEXT NOT NULL, " \
                                     f"TestTime REAL NOT NULL);"

        timeoutPredicateInstanceTableCreateCommand = f"CREATE TABLE {_Names.timeoutPredicateInstanceTable} " \
                                                     f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                                                     f"TestName TEXT NOT NULL, " \
                                                     f"PredicateName TEXT NOT NULL," \
                                                     f"PredicateInstanceNumber INTEGER NOT NULL);"

        badExecutionPredicateInstanceTableCreateCommand = f"CREATE TABLE {_Names.badExecutionPredicateInstanceTable} " \
                                                          f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                                                          f"TestName TEXT NOT NULL, " \
                                                          f"PredicateName TEXT NOT NULL," \
                                                          f"PredicateInstanceNumber INTEGER NOT NULL);"

        astorAssertErrorInfoTableTableCreateCommand = f"CREATE TABLE {_Names.astorAssertErrorInfoTable} " \
                                                      f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                                                      f"filePath TEXT NOT NULL, " \
                                                      f"lineStart INTEGER NOT NULL ," \
                                                      f"lineEnd INTEGER NOT NULL, " \
                                                      f"PredicateName TEXT NOT NULL);"
        # astorAssertErrorInfoTable
        viewCreateCommand = f"CREATE VIEW {_Names.coveredLinesWithTestTypesView} AS " \
                            f"SELECT {_Names.coveredLinesForTestTable}.Rowid, " \
                            f"{_Names.coveredLinesForTestTable}.TestName, " \
                            f"{_Names.coveredLinesForTestTable}.FilePath, " \
                            f"{_Names.coveredLinesForTestTable}.LineNumber, " \
                            f"{_Names.testCaseTable}.Type, " \
                            f"{_Names.testCaseTable}.Target " \
                            f"FROM {_Names.coveredLinesForTestTable} " \
                            f"INNER JOIN {_Names.testCaseTable} ON " \
                            f"{_Names.coveredLinesForTestTable}.TestName = {_Names.testCaseTable}.TestName"

        commands = [testCaseTableCreateCommand,
                    executedLineForTestTableCreateCommand,
                    emptyTestTableCreateCommand,
                    shadowedCoveredPredicateTableCreateCommand,
                    # realPredicateInstanceTableCreateCommand,
                    viewCreateCommand,
                    # finalPredicateTableCreateCommand,
                    candidatePredicateTableCreateCommand,
                    seenExceptionTableCreateCommand,
                    predicateSequenceTableCreateCommand,
                    scoredEntityTableCreateCommand,
                    testTimeTableCreateCommand,
                    timeoutPredicateInstanceTableCreateCommand,
                    badExecutionPredicateInstanceTableCreateCommand,
                    astorAssertErrorInfoTableTableCreateCommand
                    ]

        return commands

    dbFilePath = common.getDatabasePath(_Names.fileName)
    _Con = sqlite3.connect(dbFilePath)
    commands = getDatabaseSchema()
    for command in commands:
        _Con.executescript(command)


def end():
    _Con.close()


def insertCoveredLineForTest(testName: str, filePath: str, lineNumber: int):
    cur = _Con.cursor()
    cur.execute(f"INSERT INTO {_Names.coveredLinesForTestTable} VALUES (NULL, ?, ?, ?)",
                (testName, filePath, lineNumber))

    _Con.commit()


def insertEmptyTest(testName):
    cur = _Con.cursor()
    cur.execute(f"INSERT INTO {_Names.emptyTestCaseTable} VALUES (NULL, ?)", (testName,))

    _Con.commit()


def insertTestCase(testName, testType, exceptionFilePath, exceptionLineNumber, target):
    targetField = 1 if target else 0

    cur = _Con.cursor()
    cur.execute(f"INSERT INTO {_Names.testCaseTable} VALUES (NULL, ?, ?, ?, ?, ?)",
                (testName, testType, exceptionFilePath, exceptionLineNumber, targetField))

    _Con.commit()


def selectCoveredLinesWithTestTypesForAllFailedTests():
    cur = _Con.cursor()
    cur.execute(f"SELECT TestName, FilePath, LineNumber, Type FROM {_Names.coveredLinesWithTestTypesView} "
                f"WHERE Type = 'failed' and Target = 1")

    return cur.fetchall()


def insertShadowedCoveredPredicate(testName: str, filePath: str, exeLineNumber: int, lineStart: int, lineEnd: int):
    cur = _Con.cursor()
    cur.execute(f"INSERT INTO {_Names.shadowedCoveredPredicateTable} VALUES (NULL, ?, ?, ?, ?, ?)",
                (testName, filePath, exeLineNumber, lineStart, lineEnd))

    _Con.commit()


def selectDistinctExecutedSourceCodePredicates():
    cur = _Con.cursor()
    cur.execute(f"SELECT DISTINCT FilePath, LineStart, LineEnd FROM {_Names.shadowedCoveredPredicateTable} ")

    return cur.fetchall()


def insertCandidatePredicate(filePath: str, lineStart: int, lineEnd: int, predicateName: str):
    cur = _Con.cursor()
    cur.execute(f"INSERT INTO {_Names.candidatePredicateTable} VALUES (NULL, ?, ?, ?, ?)",
                (filePath, lineStart, lineEnd, predicateName))

    _Con.commit()


def selectDistinctCandidatePredicateFilePaths():
    cur = _Con.cursor()
    cur.execute(f"SELECT DISTINCT FilePath FROM {_Names.candidatePredicateTable} ")

    items = [x[0] for x in cur.fetchall()]

    return items


def selectCandidatePredicatesForFilePath(filepath):
    cur = _Con.cursor()
    cur.execute(f"SELECT LineStart, LineEnd, PredicateName FROM {_Names.candidatePredicateTable} WHERE FilePath = ?"
                , (filepath,))

    return cur.fetchall()


def selectTestCaseFailed():
    cur = _Con.cursor()
    # No need to check if they are target failing tests, but I added it anyway.
    cur.execute(f"SELECT TestName FROM {_Names.testCaseTable} WHERE "
                f"Type = 'failed' AND Target = 1")

    items = [x[0] for x in cur.fetchall()]

    return items


def selectTestCaseExceptions():
    cur = _Con.cursor()
    cur.execute(f"SELECT TestName, ExceptionFilePath, ExceptionLineNumber FROM {_Names.testCaseTable} "
                f"WHERE ExceptionLineNumber != -1 AND Target = 1")

    return cur.fetchall()


def insertSeenExceptions(testName: str, filePath: str, lineNumber: int, exceptionName: str):
    cur = _Con.cursor()
    cur.execute(f"INSERT INTO {_Names.seenExceptionTable} VALUES (NULL, ?, ?, ?, ?)",
                (testName, filePath, lineNumber, exceptionName))

    _Con.commit()


def selectDistinctSeenExceptionsFilePaths():
    cur = _Con.cursor()
    cur.execute(f"SELECT DISTINCT ExceptionFilePath FROM {_Names.seenExceptionTable} ")

    items = [x[0] for x in cur.fetchall()]

    return items


def selectSeenExceptionsForFilePath(filePath: str):
    cur = _Con.cursor()
    cur.execute(
        f"SELECT ExceptionLineNumber, ExceptionName FROM {_Names.seenExceptionTable} WHERE ExceptionFilePath = ?"
        , (filePath,))

    return cur.fetchall()


def insertPredicateSequenceForTest(testName: str, predicateSequence: str, indexedPredicateSequence: str):
    cur = _Con.cursor()
    cur.execute(f"INSERT INTO {_Names.predicateSequenceTable} VALUES (NULL, ?, ?, ?)",
                (testName, predicateSequence, indexedPredicateSequence))

    _Con.commit()


def selectTestType(testName: str) -> str:
    cur = _Con.cursor()
    cur.execute(f"SELECT Type FROM {_Names.testCaseTable} "
                f"WHERE TestName = ?", (testName,))

    return cur.fetchone()[0]


def selectSeenExceptionForTestName(testName: str) -> Optional[str]:
    cur = _Con.cursor()
    cur.execute(f"SELECT ExceptionName FROM {_Names.seenExceptionTable} "
                f"WHERE TestName = ?", (testName,))

    itemsFound = cur.fetchone()
    if itemsFound is not None:
        return itemsFound[0]
    else:
        return None


def selectCandidatePredicate(predicateName: str):
    cur = _Con.cursor()
    cur.execute(f"SELECT FilePath, LineStart, LineEnd FROM {_Names.candidatePredicateTable} "
                f"WHERE PredicateName = ?", (predicateName,))

    itemsFound = cur.fetchone()
    return itemsFound


def insertScoredEntity(testName: str, entity: str, score: int):
    cur = _Con.cursor()
    cur.execute(f"INSERT INTO {_Names.scoredEntityTable} VALUES (NULL, ?, ?, ?)",
                (testName, entity, score))

    _Con.commit()


def scoredEntityExistsForTest(testName: str, entity: str):
    cur = _Con.cursor()
    cur.execute(f"SELECT DISTINCT TestName, Entity FROM {_Names.scoredEntityTable} "
                f"WHERE TestName = ? AND Entity = ?", (testName, entity))

    itemsFound = cur.fetchall()
    return len(itemsFound) > 0


def insertTestTime(testName: str, testTime: int):
    cur = _Con.cursor()
    cur.execute(f"INSERT INTO {_Names.testTimeTable} VALUES (NULL, ?, ?)",
                (testName, testTime))

    _Con.commit()


def selectMaxTestTime():
    cur = _Con.cursor()
    cur.execute(f"SELECT MAX(TestTime) FROM {_Names.testTimeTable}")
    row = cur.fetchone()
    maxTime = row[0]

    return maxTime


def insertTimeoutPredicateInstance(testName: str, predName: str, instNum: int):
    cur = _Con.cursor()
    cur.execute(f"INSERT INTO {_Names.timeoutPredicateInstanceTable} VALUES (NULL, ?, ?, ?)",
                (testName, predName, instNum))

    _Con.commit()


def selectScoredEntityTestNames():
    cur = _Con.cursor()
    cur.execute(f"SELECT DISTINCT TestName FROM {_Names.scoredEntityTable}")

    itemsFound = cur.fetchall()
    testNames = [x[0] for x in itemsFound]
    return testNames


def selectTestTopNScoredEntities(testName: str, topN: int) -> List[Tuple[str, float]]:
    cur = _Con.cursor()
    cur.execute(f"SELECT Entity, Score FROM {_Names.scoredEntityTable} "
                f"WHERE TestName = ? "
                f"ORDER BY Score DESC LIMIT ?", (testName, topN))

    itemsFound = cur.fetchall()
    return itemsFound


def selectTestAllScoredEntities(testName: str) -> List[Tuple[str, float]]:
    cur = _Con.cursor()
    cur.execute(f"SELECT Entity, Score FROM {_Names.scoredEntityTable} "
                f"WHERE TestName = ? "
                f"ORDER BY Score DESC ", (testName,))

    itemsFound = cur.fetchall()
    return itemsFound


def numberOfCandidatePredicates():
    cur = _Con.cursor()
    cur.execute(f"SELECT COUNT(*) FROM {_Names.candidatePredicateTable}")

    itemsFound = cur.fetchone()[0]
    return itemsFound


def insertBadExecutionPredicateInstance(testName, predName, instNum):
    cur = _Con.cursor()
    cur.execute(f"INSERT INTO {_Names.badExecutionPredicateInstanceTable} VALUES (NULL, ?, ?, ?)",
                (testName, predName, instNum))

    _Con.commit()


def insertAstorAssertErrorInfo(filePath: str, lineStart: int, lineEnd: int, predicateName: str):
    cur = _Con.cursor()
    cur.execute(f"INSERT INTO {_Names.astorAssertErrorInfoTable} VALUES (NULL, ?, ?, ?, ?)",
                (filePath, lineStart, lineEnd, predicateName))

    _Con.commit()
