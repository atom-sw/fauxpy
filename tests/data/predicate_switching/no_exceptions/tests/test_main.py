from src.main import mainFunction


def test_mainFunction():
    a = 2
    b = mainFunction(a)
    assert b == -1
