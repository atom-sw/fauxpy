import math

from . import database


def _computeMutantFuseScore(mutantFailedToPass: int,
                            mutantPassedToFailed: int,
                            totalFailedToPassed: int,
                            totalPassedToFailed: int) -> float:
    # ToDo: find a better way to solve the problem (i.e., totalPassedToFailed = 0).
    fraction = float(totalFailedToPassed) / (totalPassedToFailed + 0.01)
    score = mutantFailedToPass - fraction * mutantPassedToFailed

    return score


def _computeMutantMetallaxisScore(mutantFailedToPass: int,
                                  mutantFailedChanged: int,
                                  mutantPassedToFailed: int,
                                  numAllFailed):
    numerator = mutantFailedToPass + mutantFailedChanged
    tmpTerm = numAllFailed * (mutantFailedToPass + mutantFailedChanged + mutantPassedToFailed)
    if tmpTerm == 0:
        score = 0
    else:
        denominator = math.sqrt(tmpTerm)
        score = numerator / denominator

    return score


def computeMutantScoresStoreDb():
    totalFailedToPassed, totalPassedToFailed = database.selectTotalFailedToPassedAndPassedToFailed()

    _, numAllFailed = database.selectNumberOfTests()

    mutants = database.selectMutantScoreTerms()
    for mutant in mutants:
        mutantId, mutantFailedToPass, mutantPassedToFailed, mutantFailedChanged = mutant
        fuseScore = _computeMutantFuseScore(mutantFailedToPass,
                                            mutantPassedToFailed,
                                            totalFailedToPassed,
                                            totalPassedToFailed)

        metallaxisScore = _computeMutantMetallaxisScore(mutantFailedToPass,
                                                        mutantFailedChanged,
                                                        mutantPassedToFailed,
                                                        numAllFailed)

        database.updateMutantScoreTerms(mutantId, fuseScore, metallaxisScore)
