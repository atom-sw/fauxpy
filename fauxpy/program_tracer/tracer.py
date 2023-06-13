import sys
from types import FrameType
from typing import Any, Optional, Callable

from .execution_trace import ExecutionTrace

_ExecutedLinesList = []
_ExecutedLinesSet = set()
_OriginalTracer: Callable
_IsWanted: Callable


def _traceCall(frame: FrameType, event: str, arg: Any) -> Optional[Callable]:
    global _IsWanted

    if event == "line":
        if _IsWanted(frame.f_code.co_filename):
            executedLine = (frame.f_code.co_filename, frame.f_lineno)
            _ExecutedLinesList.append(executedLine)
            _ExecutedLinesSet.add(executedLine)

    return _traceCall


def start(isWanted: Callable = lambda x: True):
    global _ExecutedLinesList
    global _ExecutedLinesSet
    global _OriginalTracer
    global _IsWanted

    _ExecutedLinesList = []
    _ExecutedLinesSet = set()
    _OriginalTracer = sys.gettrace()
    _IsWanted = isWanted
    sys.settrace(_traceCall)


def stop():
    global _OriginalTracer
    sys.settrace(_OriginalTracer)


def getExecutionTrace():
    return ExecutionTrace(_ExecutedLinesList, _ExecutedLinesSet)
