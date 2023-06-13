from src.main import absolute


def test_absolute_postive_number():
    a = 100
    b = absolute(a)
    assert b == 100


def test_absolute_zero():
    a = 0
    b = absolute(a)
    assert b == 0


def test_absolute_negative_number():
    a = -100
    b = absolute(a)
    assert b == 100
