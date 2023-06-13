from src.main import mainFunction, addOne


def test_mainFunction():
    a = 2
    b = mainFunction(a)
    assert b == -1


def test_addOne():
    a = 11
    b = addOne(a)
    assert b == 12
