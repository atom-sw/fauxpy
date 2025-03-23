import math

import pytest

from code.isosceles import isosceles_area


def test_ia_fail():
    leg, base = 9, 4

    area = isosceles_area(leg, base)
    assert area == pytest.approx(2 * math.sqrt(77))

def test_ia_pass():
    leg = 4
    base = 0

    area = isosceles_area(leg, base)
    assert area == 0
