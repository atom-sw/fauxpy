import math

import pytest

from code.equilateral import equilateral_area


def test_ea_fail():
    a = 3
    area = equilateral_area(a)
    assert area == pytest.approx(9 * math.sqrt(3) / 4)


def test_ea_pass():
    a = 1
    area = equilateral_area(a)
    assert area == pytest.approx(math.sqrt(3) / 4)
