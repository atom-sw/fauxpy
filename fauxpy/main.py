"""Pytest plugin."""

from . import common, sbfl, stack_trace, mbfl, predicate_switching, collect_mode

_Src = None
_Family: str = None
_Granularity = None
_TopN = None
_Exclude = None
_CollectMode = None
_FileOrDir = None
_FailingFile = None
_FailingList = None

_ExTimer = common.Timer()


def pytest_addoption(parser):
    group = parser.getgroup('fauxpy')
    group.addoption('--src',
                    help="Directory to perform fault localization on.")
    group.addoption('--exclude',
                    default='[]',
                    help="List of paths to be excluded.")
    group.addoption('--family',
                    default='sbfl',
                    help="Options: sbfl/st/mbfl/ps")
    group.addoption('--granularity',
                    default='statement',
                    help="Options: statement/function")
    group.addoption('--top-n',
                    default='-1',
                    help="Options: int[1,]]/-1(all).")
    group.addoption('--failing-file',
                    default=None,
                    help="Path to the file containing the targeted failing tests.")
    group.addoption('--failing-list',
                    default=None,
                    help="A list containing the targeted failing tests.")


def pytest_configure(config):
    global _Src, _Family, _Granularity, _TopN, _Exclude, _CollectMode, _FileOrDir, _FailingFile, _FailingList

    _Src = config.getoption('--src')

    if not _Src:
        return

    _Family = config.getoption('--family')
    _Granularity = config.getoption('--granularity')

    _ExTimer.startTimer()
    common.init(_Family, _Granularity)

    _TopN = config.getoption('--top-n')
    _Exclude = common.convertArgumentListStringToList(config.getoption('--exclude'))
    _FileOrDir = config.getoption("file_or_dir")
    _FailingFile = config.getoption("--failing-file")
    _FailingList = config.getoption("--failing-list")

    # Both --failing-file and a --failing-list cannot be used at the same time
    assert _FailingFile is None or _FailingList is None

    targetFailingTests = None
    if _FailingFile is not None:
        targetFailingTests = common.TargetFailingTests.fromFile(_FailingFile)
    elif _FailingList is not None:
        failingList = common.convertArgumentListStringToList(_FailingList)
        targetFailingTests = common.TargetFailingTests.fromListString(failingList)

    if targetFailingTests is not None:
        print("----------- TARGET FAILING TESTS -----------")
        for item in targetFailingTests.getFailingTests():
            print(item)
        print("----------- TARGET FAILING TEST -----------")

    if _Family == 'sbfl':
        # _Granularity = config.getoption('--granularity')

        if _Granularity not in ["statement", "function"]:
            raise Exception(f"Granularity {_Granularity} is not supported.")

        sbfl.handlerConfigure(granularity=_Granularity,
                              src=_Src,
                              exclude=_Exclude,
                              topN=_TopN,
                              targetFailingTests=targetFailingTests)
    elif _Family == "st":
        stack_trace.handlerConfigure(src=_Src,
                                     exclude=_Exclude,
                                     topN=_TopN,
                                     targetFailingTests=targetFailingTests)
    elif _Family == "mbfl":
        # _Granularity = config.getoption('--granularity')

        if _Granularity not in ["statement", "function"]:
            raise Exception(f"Granularity {_Granularity} is not supported.")

        mbfl.handlerConfigure(granularity=_Granularity,
                              src=_Src,
                              exclude=_Exclude,
                              topN=_TopN,
                              fileOrDir=_FileOrDir,
                              targetFailingTests=targetFailingTests)
    elif _Family == "ps":
        # _Granularity = config.getoption('--granularity')

        if _Granularity not in ["statement", "function"]:
            raise Exception(f"Granularity {_Granularity} is not supported.")

        predicate_switching.handlerConfigure(granularity=_Granularity,
                                             src=_Src,
                                             exclude=_Exclude,
                                             topN=_TopN,
                                             targetFailingTests=targetFailingTests)
    elif _Family in ["collectmbfl", "collectpsinfo", "collectpsrun"]:
        collect_mode.handlerConfigure(src=_Src, exclude=_Exclude, family=_Family)
    else:
        raise Exception(f"{_Family} is not a supported family!")

    targetFailingTestsList = (targetFailingTests.getFailingTests()
                              if targetFailingTests is not None
                              else ["No specific target failing tests"])
    common.saveConfigToFile(src=_Src,
                            exclude=_Exclude,
                            family=_Family,
                            granularity=_Granularity,
                            topN=_TopN,
                            targetFailingTests=targetFailingTestsList)


def pytest_runtest_call(item):
    """
    Runs before the execution of the current test.
    """

    if not _Src:
        return

    if _Family == 'sbfl':
        sbfl.handlerRuntestCall(item)
    elif _Family == "st":
        stack_trace.handlerRuntestCall(item)
    elif _Family == "mbfl":
        mbfl.handlerRuntestCall(item)
    elif _Family == "ps":
        predicate_switching.handlerRuntestCall(item)
    elif _Family in ["collectmbfl", "collectpsinfo", "collectpsrun"]:
        collect_mode.handlerRuntestCall(item)
    else:
        raise Exception(f"{_Family} is not a supported family!")


def pytest_runtest_makereport(item, call):
    """
    Runs after the execution of the current test.
    """

    if not _Src:
        return

    if _Family == 'sbfl':
        sbfl.handlerRuntestMakereport(item, call)
    elif _Family == "st":
        stack_trace.handlerRuntestMakereport(item, call)
    elif _Family == "mbfl":
        mbfl.handlerRuntestMakereport(item, call)
    elif _Family == "ps":
        predicate_switching.handlerRuntestMakereport(item, call)
    elif _Family in ["collectmbfl", "collectpsinfo", "collectpsrun"]:
        collect_mode.handlerRuntestMakereport(item, call)
    else:
        raise Exception(f"{_Family} is not a supported family!")


def pytest_terminal_summary(terminalreporter, exitstatus):
    """
    Runs after the execution of all tests.
    """

    if not _Src:
        return

    if _Family == 'sbfl':
        scoreEntities = sbfl.handlerTerminalSummary(terminalreporter)
    elif _Family == "st":
        scoreEntities = stack_trace.handlerTerminalSummary(terminalreporter)
    elif _Family == "mbfl":
        scoreEntities = mbfl.handlerTerminalSummary(terminalreporter)
    elif _Family == "ps":
        scoreEntities = predicate_switching.handlerTerminalSummary(terminalreporter)
    elif _Family in ["collectmbfl", "collectpsinfo", "collectpsrun"]:
        scoreEntities = collect_mode.handlerTerminalSummary(terminalreporter)
    else:
        raise Exception(f"{_Family} is not a supported family!")

    for technique, scores in scoreEntities.items():
        common.saveScoresToFile(technique, scores)
        print(f" ----- Scores for {technique} ----- ")
        for score in scores:
            print(score)

    deltaTime = _ExTimer.endTimer()
    common.saveDeltaTimeToFile(deltaTime)
    print("DeltaTime: ", deltaTime)

    common.end()
