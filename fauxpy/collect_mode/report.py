import json

from . import database
from .. import common


def saveTestCases():
    testCasesTable = database.selectAllTestCases()
    jsonTestCasesTable = json.dumps(testCasesTable)
    common.saveInCollectModeTestCaseTable(jsonTestCasesTable)


def saveTestPredicateSequenceTable():
    table = database.selectAllPredicateSequences()
    jsonTable = json.dumps(table)
    common.saveInCollectModePredicateSequenceTable(jsonTable)


def saveSeenExceptionSequenceTable():
    table = database.selectAllSeenExceptions()
    jsonTable = json.dumps(table)
    common.saveInCollectModeSeenExceptionSequenceTable(jsonTable)


# def saveToFile():
#     saveTestCases()
#     saveTestPredicateSequenceTable()
#     saveSeenExceptionSequenceTable()

