import math

import pytest

from code.isosceles import isosceles_area


def test_ia_crash():
    leg, base = 9, 4

    area = isosceles_area(leg, base)
    assert area == pytest.approx(2 * math.sqrt(77))


def test_ia_pass():
    leg = base = 4

    area = isosceles_area(leg, base)
    assert area == pytest.approx(2 * math.sqrt(12))
