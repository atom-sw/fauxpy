import sqlite3
from typing import List

from .. import common

_Con: sqlite3.Connection


class _Names(object):
    fileName = "fauxpy.db"
    testCaseTable = "TestCase"
    executionTraceTable = "ExecutionTrace"
    emptyTestCaseTable = "EmptyTest"
    scoreTable = "Score"
    executionTraceWithTestTypeView = "ExecutionTraceWithTestType"


def init():
    global _Con

    def getDatabaseSchema():
        testCaseTableCreateCommand = f"CREATE TABLE {_Names.testCaseTable} " \
                                     f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                                     f"TestName TEXT NOT NULL UNIQUE, " \
                                     f"Type TEXT NOT NULL," \
                                     f"Target INTEGER NOT NULL);"
        executionTraceTableCreateCommand = f"CREATE TABLE {_Names.executionTraceTable} " \
                                           f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                                           f"TestName TEXT NOT NULL, " \
                                           f"Entity TEXT NOT NULL, " \
                                           f"UNIQUE(TestName, Entity));"
        emptyTestTableCreateCommand = f"CREATE TABLE {_Names.emptyTestCaseTable} " \
                                      f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                                      f"TestName TEXT NOT NULL UNIQUE);"

        scoreTableCreateCommand = f"CREATE TABLE {_Names.scoreTable} " \
                                  f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                                  f"Entity TEXT NOT NULL UNIQUE, " \
                                  f"Ef REAL NOT NULL, " \
                                  f"Ep REAL NOT NULL, " \
                                  f"Nf REAL NOT NULL, " \
                                  f"Np REAL NOT NULL, " \
                                  f"Tarantula REAL NOT NULL, " \
                                  f"Ochiai REAL NOT NULL, " \
                                  f"Dstar REAL NOT NULL);"

        executionTraceTableIndexCommand = f"CREATE INDEX Index_Entity ON {_Names.executionTraceTable} (Entity);"

        testCaseTableIndexCommand = f"CREATE INDEX Index_Type ON {_Names.testCaseTable} (Type);"

        scoreTarantulaTableIndexCommand = f"CREATE INDEX index_Tarantula ON {_Names.scoreTable} (Tarantula);"

        scoreOchiaiTableIndexCommand = f"CREATE INDEX index_Ochiai ON {_Names.scoreTable} (Ochiai);"

        scoreDstarTableIndexCommand = f"CREATE INDEX index_Dstar ON {_Names.scoreTable} (Dstar);"

        viewCreateCommand = f"CREATE VIEW {_Names.executionTraceWithTestTypeView} AS " \
                            f"SELECT {_Names.executionTraceTable}.Entity, {_Names.executionTraceTable}.TestName, {_Names.testCaseTable}.Type, {_Names.testCaseTable}.Target " \
                            f"FROM {_Names.executionTraceTable} " \
                            f"INNER JOIN {_Names.testCaseTable} ON {_Names.executionTraceTable}.TestName = {_Names.testCaseTable}.TestName"

        commands = [testCaseTableCreateCommand,
                    executionTraceTableCreateCommand,
                    emptyTestTableCreateCommand,
                    scoreTableCreateCommand,
                    executionTraceTableIndexCommand,
                    testCaseTableIndexCommand,
                    scoreTarantulaTableIndexCommand,
                    scoreOchiaiTableIndexCommand,
                    scoreDstarTableIndexCommand,
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
    for covEntity in coveredEntity:
        cur = _Con.cursor()
        cur.execute(f"INSERT INTO {_Names.executionTraceTable} VALUES (NULL, ?, ?)", (testName, covEntity))

    _Con.commit()


def insertEmptyTest(testName):
    cur = _Con.cursor()
    cur.execute(f"INSERT INTO {_Names.emptyTestCaseTable} VALUES (NULL, ?)", (testName,))

    _Con.commit()


def insertTestCase(testName, testType, target: bool):
    targetField = 1 if target else 0

    cur = _Con.cursor()
    cur.execute(f"INSERT INTO {_Names.testCaseTable} VALUES (NULL, ?, ?, ?)", (testName, testType, targetField))

    _Con.commit()


def selectDistinctExecutedEntities():
    cur = _Con.cursor()
    cur.execute(f"SELECT DISTINCT Entity FROM {_Names.executionTraceTable}")

    entities = [x[0] for x in cur.fetchall()]
    return entities


def selectNumberOfTests():
    cur = _Con.cursor()
    cur.execute(f"SELECT COUNT(Type) FROM {_Names.testCaseTable} WHERE Type = 'passed'")
    numAllPassed = cur.fetchone()[0]
    cur.execute(f"SELECT COUNT(Type) FROM {_Names.testCaseTable} WHERE Type = 'failed' AND Target = 1")
    numAllFailed = cur.fetchone()[0]
    # cur.execute(f"SELECT COUNT(*) FROM {_Names.testCaseTable}")
    # numAll = cur.fetchone()[0]
    # assert numAllPassed + numAllFailed == numAll  # Simple checking. Can be removed.

    return numAllPassed, numAllFailed


def selectNumberOfCoveringTests(entity):
    cur = _Con.cursor()
    cur.execute(f"SELECT COUNT(*) FROM {_Names.executionTraceWithTestTypeView} "
                f"WHERE Type = 'passed' AND Entity = ?", (entity,))
    numCovPassed = cur.fetchone()[0]
    cur.execute(f"SELECT COUNT(*) FROM {_Names.executionTraceWithTestTypeView} "
                f"WHERE Type = 'failed' AND Target = 1 AND Entity = ?", (entity,))
    numCovFailed = cur.fetchone()[0]
    # cur.execute(f"SELECT COUNT(*) FROM {_Names.executionTraceWithTestTypeView} "
    #             f"WHERE Entity = ?", (entity,))
    # numCovAll = cur.fetchone()[0]
    # assert numCovPassed + numCovFailed == numCovAll  # Check if left join is causing any NULLs on test type of the view

    return numCovPassed, numCovFailed


def inertScores(entity, ef, ep, nf, np, scores):
    cur = _Con.cursor()
    cur.execute(f"INSERT INTO {_Names.scoreTable} "
                f"VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)", (entity, ef, ep, nf, np, scores["Tarantula"], scores["Ochiai"], scores["Dstar"]))

    _Con.commit()


def selectTopNRankedEntities(topN):
    cur = _Con.cursor()
    cur.execute(f"SELECT Entity, Tarantula FROM {_Names.scoreTable} ORDER BY Tarantula DESC LIMIT ?", (topN,))
    scoreTarantula = cur.fetchall()

    cur.execute(f"SELECT Entity, Ochiai FROM {_Names.scoreTable} ORDER BY Ochiai DESC LIMIT ?", (topN,))
    scoreOchiai = cur.fetchall()

    cur.execute(f"SELECT Entity, Dstar FROM {_Names.scoreTable} ORDER BY Dstar DESC LIMIT ?", (topN,))
    scoreDstar = cur.fetchall()

    rankedEntities = {"Tarantula": scoreTarantula,
                      "Ochiai": scoreOchiai,
                      "Dstar": scoreDstar}

    return rankedEntities


def selectAllRankedEntities():
    cur = _Con.cursor()
    cur.execute(f"SELECT Entity, Tarantula FROM {_Names.scoreTable} ORDER BY Tarantula DESC")
    scoreTarantula = cur.fetchall()

    cur.execute(f"SELECT Entity, Ochiai FROM {_Names.scoreTable} ORDER BY Ochiai DESC")
    scoreOchiai = cur.fetchall()

    cur.execute(f"SELECT Entity, Dstar FROM {_Names.scoreTable} ORDER BY Dstar DESC")
    scoreDstar = cur.fetchall()

    rankedEntities = {"Tarantula": scoreTarantula,
                      "Ochiai": scoreOchiai,
                      "Dstar": scoreDstar}

    return rankedEntities
