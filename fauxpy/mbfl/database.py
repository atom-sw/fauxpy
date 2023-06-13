import sqlite3
from typing import List, Tuple

from .. import common

_Con: sqlite3.Connection


class _Names(object):
    fileName = "fauxpy.db"
    testCaseTable = "TestCase"
    executionTraceTable = "ExecutionTrace"
    emptyTestCaseTable = "EmptyTest"
    executionTraceWithTestTypeView = "ExecutionTraceWithTestType"
    failingLineNumberTable = "FailingLineNumber"
    mutantInfoTable = "MutantInfo"
    mutantScoreTermTable = "MutantScoreTerm"
    entityScoreTable = "EntityScoreTable"
    testTimeTable = "TestTime"


def init():
    global _Con

    def getDatabaseSchema():
        testCaseTableCreateCommand = f"CREATE TABLE {_Names.testCaseTable} " \
                                     f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                                     f"TestName TEXT NOT NULL UNIQUE, " \
                                     f"Type TEXT NOT NULL, " \
                                     f"TestTraceBack TEXT NOT NULL, " \
                                     f"Timeout INTEGER NOT NULL, " \
                                     f"Target INTEGER NOT NULL);"
        # ToDo: use the commented table which has unique command.
        # executionTraceTableCreateCommand = f"CREATE TABLE {_Names.executionTraceTable} " \
        #                                    f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
        #                                    f"TestName TEXT NOT NULL, " \
        #                                    f"Entity TEXT NOT NULL, " \
        #                                    f"UNIQUE(TestName, Entity));"
        executionTraceTableCreateCommand = f"CREATE TABLE {_Names.executionTraceTable} " \
                                           f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                                           f"TestName TEXT NOT NULL, " \
                                           f"Entity TEXT NOT NULL);"
        emptyTestTableCreateCommand = f"CREATE TABLE {_Names.emptyTestCaseTable} " \
                                      f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                                      f"TestName TEXT NOT NULL UNIQUE);"

        failingLineNumberTableCreateCommand = f"CREATE TABLE {_Names.failingLineNumberTable} " \
                                              f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                                              f"ModulePath TEXT NOT NULL, " \
                                              f"LineNumber INTEGER NOT NULL, " \
                                              f"UNIQUE(ModulePath, LineNumber));"

        mutantInfoTableCreateCommand = f"CREATE TABLE {_Names.mutantInfoTable} " \
                                       f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                                       f"MutantId TEXT NOT NULL, " \
                                       f"ModulePath TEXT NOT NULL, " \
                                       f"LineNumber INTEGER NOT NULL," \
                                       f"OperatorName TEXT NOT NULL, " \
                                       f"MutantDiff TEXT NOT NULL UNIQUE, " \
                                       f"StartPos INTEGER NOT NULL, " \
                                       f"EndPos INTEGER NOT NULL, " \
                                       f"Timeout INTEGER NOT NULL, " \
                                       f"HasMissingTests INTEGER NOT NULL);"

        mutantScoreTermTableCreateCommand = f"CREATE TABLE {_Names.mutantScoreTermTable} " \
                                            f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                                            f"MutantId TEXT NOT NULL, " \
                                            f"Entity TEXT NOT NULL,	" \
                                            f"FailedToPass INTEGER NOT NULL, " \
                                            f"PassedToFailed INTEGER NOT NULL, " \
                                            f"FailedChanged INTEGER NOT NULL, " \
                                            f"MutantMuseScore REAL NOT NULL, " \
                                            f"MutantMetallaxisScore REAL NOT NULL);"

        entityScoreTableCreateCommand = f"CREATE TABLE {_Names.entityScoreTable} " \
                                        f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                                        f"Entity TEXT NOT NULL, " \
                                        f"EntityMuseScore REAL NOT NULL, " \
                                        f"EntityMetallaxisScore REAL NOT NULL);"

        testTimeTableCreateCommand = f"CREATE TABLE {_Names.testTimeTable} " \
                                     f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                                     f"TestName TEXT NOT NULL, " \
                                     f"TestTime REAL NOT NULL);"

        testCaseTableTestNameIndexCommand = f"CREATE INDEX Index_TestCase_TestName ON {_Names.testCaseTable} (TestName);"

        testCaseTableTypeIndexCommand = f"CREATE INDEX Index_TestCase_Type ON {_Names.testCaseTable} (Type);"

        executionTraceTableTestNameIndexCommand = f"CREATE INDEX Index_ExecutionTrace_TestName ON {_Names.testCaseTable} (TestName);"

        failingLineNumberTableModulePathIndexCommand = f"CREATE INDEX Index_ModulePath ON " \
                                                       f"{_Names.failingLineNumberTable} (ModulePath);"

        # mutantInfoTableModulePathLineNumberIndexCommand = \
        #     f"CREATE INDEX Index_Mutant_ModulePath_LineNumber ON {_Names.mutantInfoTable} (ModulePath, LineNumber);"

        mutantScoreTermTableEntityIndexCommand = \
            f"CREATE INDEX Index_MutantScoreTerm ON {_Names.mutantScoreTermTable} (Entity);"

        EntityScoreTableEntityIndexCommand = f"CREATE INDEX Index_EntityScore ON {_Names.entityScoreTable} (Entity);"

        viewCreateCommand = f"CREATE VIEW {_Names.executionTraceWithTestTypeView} AS " \
                            f"SELECT {_Names.executionTraceTable}.Entity, " \
                            f"{_Names.executionTraceTable}.TestName, " \
                            f"{_Names.testCaseTable}.Type, " \
                            f"{_Names.testCaseTable}.Target " \
                            f"FROM {_Names.executionTraceTable} " \
                            f"INNER JOIN {_Names.testCaseTable} ON " \
                            f"{_Names.executionTraceTable}.TestName = {_Names.testCaseTable}.TestName"

        commands = [testCaseTableCreateCommand,
                    executionTraceTableCreateCommand,
                    emptyTestTableCreateCommand,
                    failingLineNumberTableCreateCommand,
                    mutantInfoTableCreateCommand,
                    mutantScoreTermTableCreateCommand,
                    entityScoreTableCreateCommand,
                    testTimeTableCreateCommand,
                    testCaseTableTestNameIndexCommand,
                    testCaseTableTypeIndexCommand,
                    executionTraceTableTestNameIndexCommand,
                    failingLineNumberTableModulePathIndexCommand,
                    # mutantInfoTableModulePathLineNumberIndexCommand,
                    mutantScoreTermTableEntityIndexCommand,
                    EntityScoreTableEntityIndexCommand,
                    viewCreateCommand]

        return commands

    dbFilePath = common.getDatabasePath(_Names.fileName)
    _Con = sqlite3.connect(dbFilePath)
    commands = getDatabaseSchema()
    for command in commands:
        _Con.executescript(command)


def end():
    _Con.close()


def insertExecutionTrace(testName: str, coveredEntity: List[str]):
    global _Con

    for covEntity in coveredEntity:
        cur = _Con.cursor()
        cur.execute(f"INSERT INTO {_Names.executionTraceTable} VALUES (NULL, ?, ?)", (testName, covEntity))

    _Con.commit()


def insertEmptyTest(testName):
    global _Con

    cur = _Con.cursor()
    cur.execute(f"INSERT INTO {_Names.emptyTestCaseTable} VALUES (NULL, ?)", (testName,))

    _Con.commit()


def insertTestCaseRun(testName, testType, testTraceBack, timeoutStat, target):
    global _Con

    targetField = 1 if target else 0

    cur = _Con.cursor()
    cur.execute(f"INSERT INTO {_Names.testCaseTable} VALUES (NULL, ?, ?, ?, ?, ?)",
                (testName, testType, testTraceBack, timeoutStat, targetField))

    _Con.commit()


def selectDistinctLineNumbersCoveredByFailingTests():
    global _Con

    cur = _Con.cursor()
    cur.execute(f"SELECT DISTINCT Entity FROM {_Names.executionTraceWithTestTypeView} "
                f"WHERE Type = 'failed' and Target = 1")

    entities = [x[0] for x in cur.fetchall()]
    return entities


def insertFailingLineNumberComponents(modulePath: str, lineNumber: int):
    global _Con

    cur = _Con.cursor()
    cur.execute(f"INSERT INTO {_Names.failingLineNumberTable} VALUES (NULL, ?, ?)", (modulePath, lineNumber))

    _Con.commit()


def selectDistinctFailingModulePaths() -> List[str]:
    global _Con

    cur = _Con.cursor()
    cur.execute(f"SELECT DISTINCT ModulePath FROM {_Names.failingLineNumberTable}")

    entities = [x[0] for x in cur.fetchall()]
    return entities


def selectFailingLineNumbersForModulePath(modulePath: str) -> List[int]:
    global _Con

    cur = _Con.cursor()
    cur.execute(f"SELECT LineNumber FROM {_Names.failingLineNumberTable} WHERE ModulePath = ?", (modulePath,))

    entities = [x[0] for x in cur.fetchall()]
    return entities


def insertMutant(mutantID: str, modulePath: str, lineNumber: int,
                 operatorName: str, moduleDiff: str, startPos: int,
                 endPos: int,
                 timeout: int = -1,
                 hasMissingTests: int = -1):
    global _Con

    cur = _Con.cursor()
    cur.execute(f"INSERT INTO {_Names.mutantInfoTable} VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (mutantID, modulePath, lineNumber, operatorName, moduleDiff, startPos, endPos, timeout, hasMissingTests))

    _Con.commit()


def selectNumberOfTests():
    global _Con

    cur = _Con.cursor()
    cur.execute(f"SELECT COUNT(Type) FROM {_Names.testCaseTable} WHERE Type = 'passed'")
    numAllPassed = cur.fetchone()[0]
    cur.execute(f"SELECT COUNT(Type) FROM {_Names.testCaseTable} WHERE Type = 'failed'")
    numAllFailed = cur.fetchone()[0]
    # cur.execute(f"SELECT COUNT(*) FROM {_Names.testCaseTable}")
    # numAll = cur.fetchone()[0]
    # assert numAllPassed + numAllFailed == numAll  # Simple checking. Can be removed.

    return numAllPassed, numAllFailed


def selectTestCase(testName: str):
    global _Con

    cur = _Con.cursor()
    cur.execute(f"SELECT TestName, Type, TestTraceBack, Timeout, Target FROM {_Names.testCaseTable} WHERE TestName = ?", (testName,))
    row = cur.fetchone()

    return row


def insertMutantScoreTerms(mutantId: str,
                           entity: str,
                           failedToPassed: int,
                           passedToFailed: int,
                           failedChanged: int):
    global _Con

    cur = _Con.cursor()
    cur.execute(f"INSERT INTO {_Names.mutantScoreTermTable} VALUES (NULL, ?, ?, ?, ?, ?, -1, -1)",
                (mutantId, entity, failedToPassed, passedToFailed, failedChanged))

    _Con.commit()


def selectTotalFailedToPassedAndPassedToFailed() -> Tuple[int, int]:
    global _Con

    cur = _Con.cursor()
    cur.execute(f"SELECT SUM(FailedToPass), SUM(PassedToFailed) FROM {_Names.mutantScoreTermTable}")
    row = cur.fetchone()

    return row


def selectMutantScoreTerms():
    global _Con

    cur = _Con.cursor()
    cur.execute(f"SELECT MutantId, FailedToPass, PassedToFailed, FailedChanged FROM {_Names.mutantScoreTermTable}")
    rows = cur.fetchall()

    return rows


def updateMutantScoreTerms(mutantId, mutantMuseScore, mutantMetallaxisScore):
    global _Con

    cur = _Con.cursor()
    cur.execute(f"UPDATE {_Names.mutantScoreTermTable} SET MutantMuseScore = ?, "
                f"MutantMetallaxisScore = ? WHERE MutantId = ?",
                (mutantMuseScore, mutantMetallaxisScore, mutantId))

    _Con.commit()


def selectDistinctAllMutantScoreTermsEntities():
    global _Con

    cur = _Con.cursor()
    cur.execute(f"SELECT DISTINCT Entity FROM {_Names.mutantScoreTermTable}")
    rows = cur.fetchall()

    entities = [x[0] for x in rows]
    return entities


def selectMutantScoreTermsScores(entity):
    global _Con

    cur = _Con.cursor()
    cur.execute(f"SELECT MutantMuseScore FROM {_Names.mutantScoreTermTable} WHERE Entity = ?", (entity,))
    rows = cur.fetchall()
    mutantMuseScores = [x[0] for x in rows]

    cur.execute(f"SELECT MutantMetallaxisScore FROM {_Names.mutantScoreTermTable} WHERE Entity = ?", (entity,))
    rows = cur.fetchall()
    mutantMetallaxisScores = [x[0] for x in rows]

    return {"Muse": mutantMuseScores, "Metallaxis": mutantMetallaxisScores}


def insertEntityScore(entity: str,
                      entityMuseScore: float,
                      entityMetallaxisScore: float):
    global _Con

    cur = _Con.cursor()
    cur.execute(f"INSERT INTO {_Names.entityScoreTable} VALUES (NULL, ?, ?, ?)",
                (entity, entityMuseScore, entityMetallaxisScore))

    _Con.commit()


def selectAllRankedEntities():
    global _Con

    cur = _Con.cursor()
    cur.execute(f"SELECT Entity, EntityMuseScore FROM {_Names.entityScoreTable} "
                f"ORDER BY EntityMuseScore DESC")
    scoresMuse = cur.fetchall()

    cur = _Con.cursor()
    cur.execute(f"SELECT Entity, EntityMetallaxisScore FROM {_Names.entityScoreTable} "
                f"ORDER BY EntityMetallaxisScore DESC")
    scoresMetallaxis = cur.fetchall()

    return {"Muse": scoresMuse,
            "Metallaxis": scoresMetallaxis}


def selectTopNRankedEntities(topN):
    global _Con

    cur = _Con.cursor()
    cur.execute(f"SELECT Entity, EntityMuseScore FROM {_Names.entityScoreTable} "
                f"ORDER BY EntityMuseScore DESC LIMIT ?", (topN,))
    scoresMuse = cur.fetchall()

    cur = _Con.cursor()
    cur.execute(f"SELECT Entity, EntityMetallaxisScore FROM {_Names.entityScoreTable} "
                f"ORDER BY EntityMetallaxisScore DESC LIMIT ?", (topN,))
    scoresMetallaxis = cur.fetchall()

    return {"Muse": scoresMuse,
            "Metallaxis": scoresMetallaxis}


def insertTestTime(testName: str, testTime: int):
    global _Con

    cur = _Con.cursor()
    cur.execute(f"INSERT INTO {_Names.testTimeTable} VALUES (NULL, ?, ?)",
                (testName, testTime))

    _Con.commit()


def selectMaxTestTime():
    global _Con

    cur = _Con.cursor()
    cur.execute(f"SELECT MAX(TestTime) FROM {_Names.testTimeTable}")
    row = cur.fetchone()
    maxTime = row[0]

    return maxTime


def updateMutantAsTimeout(mutantId):
    global _Con

    cur = _Con.cursor()
    cur.execute(f"UPDATE {_Names.mutantInfoTable} SET Timeout = ? "
                f"WHERE MutantId = ?",
                (1, mutantId))

    _Con.commit()


def updateMutantAsHavingMissingTests(mutantId):
    cur = _Con.cursor()
    cur.execute(f"UPDATE {_Names.mutantInfoTable} SET HasMissingTests = ? "
                f"WHERE MutantId = ?",
                (1, mutantId))

    _Con.commit()
