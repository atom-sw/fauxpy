from . import database, mutgen
from .. import common


def _setMutantIds(mutants):
    for i in range(len(mutants)):
        mutants[i].setId(f"M{i}")


def getAllMutantsForFailingLineNumbers(failingLineNumbers):
    mutants = []

    for statementName in failingLineNumbers:
        path, lineNumber = common.convertStatementNameToComponents(statementName)
        database.insertFailingLineNumberComponents(path, lineNumber)

    failingModulePaths = database.selectDistinctFailingModulePaths()
    for modulePath in failingModulePaths:
        lineNumbers = database.selectFailingLineNumbersForModulePath(modulePath)
        currentModuleMutants = mutgen.getMutantsForModuleAndLines(modulePath=modulePath,
                                                                  lineNumbers=lineNumbers,
                                                                  operatorMutationTargetUnique=True)
        mutants += currentModuleMutants

    _setMutantIds(mutants)

    return mutants
