import sqlite3

from .. import common

_Con: sqlite3.Connection


class _Names(object):
    fileName = "fauxpy.db"
    tracebackScoreTable = "TracebackScore"


def init():
    global _Con

    def getDatabaseSchema():
        tracebackScoreTableCreateCommand = f"CREATE TABLE {_Names.tracebackScoreTable} " \
                                           f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                                           f"TestName TEXT NOT NULL, " \
                                           f"Function TEXT NOT NULL," \
                                           f"Score REAL NOT NULL);"

        tracebackScoreTableIndexCommand = f"CREATE INDEX Index_FunctionName ON {_Names.tracebackScoreTable} (Function);"

        commands = [tracebackScoreTableCreateCommand,
                    tracebackScoreTableIndexCommand]

        return commands

    dbFilePath = common.getDatabasePath(_Names.fileName)
    _Con = sqlite3.connect(dbFilePath)
    commands = getDatabaseSchema()
    for command in commands:
        _Con.executescript(command)


def end():
    _Con.close()


def insertTracebackScores(testName, testScores):
    for testScore in testScores:
        cur = _Con.cursor()
        cur.execute(f"INSERT INTO {_Names.tracebackScoreTable} VALUES (NULL, ?, ?, ?)", (testName,
                                                                                         testScore[0],
                                                                                         testScore[1]))

    _Con.commit()


def selectAllRankedFunctions():
    cur = _Con.cursor()
    cur.execute(f"SELECT Function, MAX(Score) FROM {_Names.tracebackScoreTable} "
                f"GROUP BY Function "
                f"ORDER BY Score DESC")

    return cur.fetchall()


def selectTopNRankedFunctions(topN):
    cur = _Con.cursor()
    cur.execute(f"SELECT Function, MAX(Score) FROM {_Names.tracebackScoreTable} "
                f"GROUP BY Function "
                f"ORDER BY Score DESC "
                f"LIMIT ?", (topN,))

    return cur.fetchall()
