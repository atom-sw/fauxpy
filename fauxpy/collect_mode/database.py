import sqlite3
from typing import List

from .. import common

_Con: sqlite3.Connection


class _Names(object):
    fileName = "fauxpy.db"
    testCaseTable = "TestCase"
    coveredLinesForTestTable = "CoveredLinesForTest"
    emptyTestCaseTable = "EmptyTest"
    # coveredLinesWithTestTypesView = "CoveredLinesWithTestTypes"
    testPredicateSequenceTable = "TestPredicateSequence"
    testSeenExceptionSequenceTable = "TestSeenExceptionSequence"


# TODO: Add indices.
def init():
    global _Con

    def getDatabaseSchema():
        testCaseTableCreateCommand = f"CREATE TABLE {_Names.testCaseTable} " \
                                     f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                                     f"TestName TEXT NOT NULL UNIQUE, " \
                                     f"Type TEXT NOT NULL, " \
                                     f"ShortTraceback TEXT NOT NULL," \
                                     f"Timeout INTEGER NOT NULL);"

        executedLineForTestTableCreateCommand = f"CREATE TABLE {_Names.coveredLinesForTestTable} " \
                                                f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                                                f"TestName TEXT NOT NULL, " \
                                                f"FilePath TEXT NOT NULL, " \
                                                f"LineNumber INTEGER NOT NULL);"

        emptyTestTableCreateCommand = f"CREATE TABLE {_Names.emptyTestCaseTable} " \
                                      f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                                      f"TestName TEXT NOT NULL UNIQUE);"

        testPredicateSequenceTableCreateCommand = f"CREATE TABLE {_Names.testPredicateSequenceTable} " \
                                                  f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                                                  f"TestName TEXT NOT NULL UNIQUE, " \
                                                  f"PredicateSequence TEXT NOT NULL);"

        testSeenExceptionsSequenceTableCreateCommand = f"CREATE TABLE {_Names.testSeenExceptionSequenceTable} " \
                                                       f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                                                       f"TestName TEXT NOT NULL UNIQUE, " \
                                                       f"SeenExceptionSequence TEXT NOT NULL);"

        # viewCreateCommand = f"CREATE VIEW {_Names.coveredLinesWithTestTypesView} AS " \
        #                     f"SELECT {_Names.coveredLinesForTestTable}.Rowid, " \
        #                     f"{_Names.coveredLinesForTestTable}.TestName, " \
        #                     f"{_Names.coveredLinesForTestTable}.FilePath, " \
        #                     f"{_Names.coveredLinesForTestTable}.LineNumber, " \
        #                     f"{_Names.testCaseTable}.Type " \
        #                     f"FROM {_Names.coveredLinesForTestTable} " \
        #                     f"INNER JOIN {_Names.testCaseTable} ON " \
        #                     f"{_Names.coveredLinesForTestTable}.TestName = {_Names.testCaseTable}.TestName"

        commands = [testCaseTableCreateCommand,
                    executedLineForTestTableCreateCommand,
                    emptyTestTableCreateCommand,
                    testPredicateSequenceTableCreateCommand,
                    # viewCreateCommand,
                    testSeenExceptionsSequenceTableCreateCommand
                    ]

        return commands

    dbFilePath = common.getDatabasePath(_Names.fileName)
    _Con = sqlite3.connect(dbFilePath)
    commands = getDatabaseSchema()
    for command in commands:
        _Con.executescript(command)


def end():
    _Con.close()


def insertEmptyTest(testName):
    global _Con

    cur = _Con.cursor()
    cur.execute(f"INSERT INTO {_Names.emptyTestCaseTable} VALUES (NULL, ?)", (testName,))

    _Con.commit()


def insertCoveredLineForTest(testName: str, filePath: str, lineNumber: int):
    global _Con

    cur = _Con.cursor()
    cur.execute(f"INSERT INTO {_Names.coveredLinesForTestTable} VALUES (NULL, ?, ?, ?)",
                (testName, filePath, lineNumber))

    _Con.commit()


def insertTestCase(testName: str, testType: str, shortTraceback: str, timeoutStat: int):
    global _Con

    cur = _Con.cursor()
    cur.execute(f"INSERT INTO {_Names.testCaseTable} VALUES (NULL, ?, ?, ?, ?)",
                (testName, testType, shortTraceback, timeoutStat))

    _Con.commit()


def selectAllTestCases():
    global _Con

    cur = _Con.cursor()
    cur.execute(f"SELECT TestName, Type, ShortTraceBack, Timeout FROM {_Names.testCaseTable}")
    rows = cur.fetchall()

    return rows


# def selectAllCoveredLinesForTest():
#     global _Con
#
#     cur = _Con.cursor()
#     cur.execute(f"SELECT TestName, FilePath, LineNumber FROM {_Names.coveredLinesForTestTable}")
#     rows = cur.fetchall()
#
#     return rows


def insertPredicateSequence(testName: str, predicateSequence: str):
    global _Con

    cur = _Con.cursor()
    cur.execute(f"INSERT INTO {_Names.testPredicateSequenceTable} VALUES (NULL, ?, ?)",
                (testName, predicateSequence))

    _Con.commit()


def selectAllPredicateSequences():
    global _Con

    cur = _Con.cursor()
    cur.execute(f"SELECT TestName, PredicateSequence FROM {_Names.testPredicateSequenceTable}")
    rows = cur.fetchall()

    return rows


def insertSeenExceptionSequence(testName: str, seenExceptionsSequence: str):
    global _Con

    cur = _Con.cursor()
    cur.execute(f"INSERT INTO {_Names.testSeenExceptionSequenceTable} VALUES (NULL, ?, ?)",
                (testName, seenExceptionsSequence))

    _Con.commit()


def selectAllSeenExceptions():
    global _Con

    cur = _Con.cursor()
    cur.execute(f"SELECT TestName, SeenExceptionSequence FROM {_Names.testSeenExceptionSequenceTable}")
    rows = cur.fetchall()

    return rows
