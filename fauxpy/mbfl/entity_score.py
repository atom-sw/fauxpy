from . import database


def _muse(mutantScores):
    entityScore = float(sum(mutantScores)) / len(mutantScores)
    return entityScore


def _metallaxis(mutantScores):
    entityScore = max(mutantScores)
    return entityScore


def _computeEntityScores(mutantScores):
    museMutantScores = mutantScores["Muse"]
    metallaxisMutantScores = mutantScores["Metallaxis"]

    museEntityScore = _muse(museMutantScores)
    metallaxisEntityScore = _metallaxis(metallaxisMutantScores)

    return {"Muse": museEntityScore, "Metallaxis": metallaxisEntityScore}


def computeEntityScoresStoreDb(topN: int):
    entities = database.selectDistinctAllMutantScoreTermsEntities()

    for entity in entities:
        mutantScores = database.selectMutantScoreTermsScores(entity)
        entityScores = _computeEntityScores(mutantScores)

        entityMuseScore = entityScores["Muse"]
        entityMetallaxisScore = entityScores["Metallaxis"]

        database.insertEntityScore(entity, entityMuseScore, entityMetallaxisScore)

    if topN == -1:
        scoreEntities = database.selectAllRankedEntities()
    elif topN >= 1:
        pass
        scoreEntities = database.selectTopNRankedEntities(topN)
    else:
        raise Exception(f"TopN {topN} is not supported.")

    return scoreEntities
