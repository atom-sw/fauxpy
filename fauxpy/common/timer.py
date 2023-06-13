import time

from fauxpy import constants


class Timer(object):
    def __init__(self):
        self._startingTime = 0

    def startTimer(self):
        self._startingTime = time.time()

    def endTimer(self):
        endingTime = time.time()
        return endingTime - self._startingTime


# _StartingTime = 0
#
#
# def startTimer():
#     global _StartingTime
#     _StartingTime = time.time()
#
#
# def endTimer():
#     global _StartingTime
#     endingTime = time.time()
#     return endingTime - _StartingTime


def getTimeout(maxTestTime: float) -> float:
    if maxTestTime is None:
        maxTestTime = 0
    timeout = constants.testTimeoutFactor * maxTestTime + constants.testTimeoutOffset
    return timeout


def getProcessTimeout(numAllTests, timeoutLimit):
    return (numAllTests + 1) * timeoutLimit
