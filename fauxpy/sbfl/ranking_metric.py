# eF: Number of failed tests that execute the program element.
# eP: Number of passed tests that execute the program element.
# nF: Number of failed tests that do not execute the program element.
# nP: Number of passed tests that do not execute the program element.
import math
from typing import List, Tuple

from . import database

EPSILON = 0.1


# ToDo: Find better ways to handle the division by zero issue.
def _tarantula(ef, ep, nf, np):
    numerator = float(ef) / (ef + nf + EPSILON)
    denominator = (float(ef) / (ef + nf + EPSILON)) + (float(ep) / (ep + np + EPSILON))
    score = numerator / denominator + EPSILON
    return score


def _ochiai(ef, ep, nf, np):
    score = float(ef) / (math.sqrt((ef + nf) * (ef + ep)) + EPSILON)
    return score


def _dstar(ef, ep, nf, np):
    score = float(math.pow(ef, 2)) / (ep + nf + EPSILON)
    return score


def _rankingMetric(ef, ep, nf, np):
    tarantulaScore = _tarantula(ef, ep, nf, np)
    ochiaiScore = _ochiai(ef, ep, nf, np)
    dstarScore = _dstar(ef, ep, nf, np)

    scores = {"Tarantula": tarantulaScore,
              "Ochiai": ochiaiScore,
              "Dstar": dstarScore}

    return scores


def computeSortedScores(topN: int) -> List[Tuple[str, int]]:
    entities = database.selectDistinctExecutedEntities()
    numAllPassed, numAllFailed = database.selectNumberOfTests()

    for entity in entities:
        numCovPassed, numCovFailed = database.selectNumberOfCoveringTests(entity)

        assert numAllPassed >= numCovPassed
        assert numAllFailed >= numCovFailed

        if numCovPassed + numCovFailed == 0:  # entities covered by xfail, xpass, and not targeted failing tests.
            continue

        ef = numCovFailed
        ep = numCovPassed
        nf = numAllFailed - ef
        np = numAllPassed - ep

        scores = _rankingMetric(ef, ep, nf, np)
        database.inertScores(entity, ef, ep, nf, np, scores)

    if topN == -1:
        scoreEntities = database.selectAllRankedEntities()
    elif topN >= 1:
        scoreEntities = database.selectTopNRankedEntities(topN)
    else:
        raise Exception(f"TopN {topN} is not supported.")

    return scoreEntities
