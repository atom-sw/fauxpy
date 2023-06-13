import sqlite3
from typing import List, Tuple

from .. import common

_Con: sqlite3.Connection


class _Names(object):
    fileName = "common.db"
    functionInfoTable = "FunctionInformation"


def init():
    global _Con

    def getDatabaseSchema():
        functionInfoTableCreateCommand = f"CREATE TABLE {_Names.functionInfoTable} " \
                                         f"(Rowid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, " \
                                         f"FilePath	TEXT NOT NULL, " \
                                         f"FunctionName	TEXT NOT NULL, " \
                                         f"LineStart INTEGER NOT NULL, " \
                                         f"LineEnd INTEGER NOT NULL);"

        functionInfoTableIndexCommand = f"CREATE INDEX Index_OnThree ON {_Names.functionInfoTable} (FilePath, LineStart, LineEnd);"

        commands = [functionInfoTableCreateCommand,
                    functionInfoTableIndexCommand]

        return commands

    dbFilePath = common.getDatabasePath(_Names.fileName)
    _Con = sqlite3.connect(dbFilePath)
    commands = getDatabaseSchema()
    for command in commands:
        _Con.executescript(command)


def end():
    _Con.close()


def selectFunctionRanges(filePath: str, lineNumber: int) -> List[Tuple[str, int, int]]:
    global _Con

    cur = _Con.cursor()

    cur.execute(f"SELECT FunctionName, LineStart, LineEnd FROM {_Names.functionInfoTable} "
                f"WHERE FilePath = ? and LineStart <= ? and LineEnd >= ?", (filePath, lineNumber, lineNumber))

    var = cur.fetchall()

    return var


def insertFunctionInformation(filePath: str,
                              functionName: str,
                              lineStart: int,
                              lineEnd: int):
    global _Con

    cur = _Con.cursor()

    cur.execute(f"INSERT INTO {_Names.functionInfoTable} VALUES (NULL, ?, ?, ?, ?)",
                (filePath, functionName, lineStart, lineEnd))
    _Con.commit()


def isFilePathCovered(filePath: str) -> bool:
    global _Con

    cur = _Con.cursor()

    cur.execute(f"SELECT COUNT(*) FROM {_Names.functionInfoTable} WHERE FilePath = ?", (filePath,))

    cnt = cur.fetchone()

    return cnt[0] > 0
