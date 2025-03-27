from enum import Enum


class FlFamily(Enum):
    Sbfl = 1
    Mbfl = 2
    Ps = 3
    St = 4
    CollectMbfl = 5
    CollectPsInfo = 6
    CollectPsRun = 7


class FlGranularity(Enum):
    Statement = 1
    Function = 2


class MutationStrategy(Enum):
    Traditional = 1
    TraditionalWithGPT4oMini = 2
    GPT4oMini = 3
    TraditionalWithGPT4o = 4
    GPT4o = 5
