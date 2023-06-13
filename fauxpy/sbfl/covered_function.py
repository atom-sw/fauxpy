from typing import List, Tuple
from .. import common


def getCoveredFunctionNames(coveredStatements: List[Tuple[str, int]]) -> List[str]:
    coveredFunctionSet = set()
    for covStmt in coveredStatements:
        coveredFunction = common.getCoveredFunction(covStmt[0], covStmt[1])
        if coveredFunction is not None:
            coveredFunctionName = common.getCoveredFunctionName(coveredFunction[0],
                                                                coveredFunction[1],
                                                                coveredFunction[2],
                                                                coveredFunction[3])
            coveredFunctionSet.add(coveredFunctionName)

    return list(coveredFunctionSet)
