from enum import Enum


class FauxpySessionType(Enum):
    """Represents the type of a FauxPy session.

    Attributes:
        FaultLocalization: A session where FauxPy is actively used for fault localization.
        FauxpyNotCalled: A session where FauxPy was not invoked during the test run.
    """
    FaultLocalization = 1
    FauxpyNotCalled = 2
