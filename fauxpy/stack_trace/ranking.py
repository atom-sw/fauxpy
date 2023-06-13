from . import database


def computeScores(tracebackFunctionNames):
    scores = []
    for j in range(len(tracebackFunctionNames)):
        item = (tracebackFunctionNames[j], float(1)/(j+1))
        scores.append(item)

    return scores


def getSortedScores(topN):
    if topN == -1:
        scoredFucntions = database.selectAllRankedFunctions()
    elif topN >= 1:
        scoredFucntions = database.selectTopNRankedFunctions(topN)
    else:
        raise Exception(f"TopN {topN} is not supported.")

    return scoredFucntions
