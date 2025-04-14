from enum import Enum


class FlFamily(Enum):
    """Represents families of fault localization (FL) techniques.

    Attributes:
        Sbfl: Spectrum-Based Fault Localization.
        Mbfl: Mutation-Based Fault Localization.
        Ps: Predicate Switching.
        St: Stack Trace-based fault localization.
        CollectMbfl: Collecting data for mutation-based fault localization.
        CollectPsInfo: Collecting predicate switching information (e.g., conditionals).
        CollectPsRun: Collecting data by executing predicate switches during test runs.
    """
    Sbfl = 1
    Mbfl = 2
    Ps = 3
    St = 4
    CollectMbfl = 5
    CollectPsInfo = 6
    CollectPsRun = 7


class FlGranularity(Enum):
    """Represents the granularity level of fault localization.

    Attributes:
        Statement: Fault localization at the statement level.
        Function: Fault localization at the function level.
    """
    Statement = 1
    Function = 2


class MutationStrategy(Enum):
    """Represents strategies for generating mutants.

    Attributes:
        Traditional: Use only traditional mutation operators.
        TraditionalWithGPT4oMini: Combine traditional operators with GPT-4o Mini-generated mutants.
        GPT4oMini: Use only GPT-4o Mini to generate mutants.
        TraditionalWithGPT4o: Combine traditional operators with GPT-4o-generated mutants.
        GPT4o: Use only GPT-4o to generate mutants.
    """
    Traditional = 1
    TraditionalWithGPT4oMini = 2
    GPT4oMini = 3
    TraditionalWithGPT4o = 4
    GPT4o = 5
