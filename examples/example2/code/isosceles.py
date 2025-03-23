import math


def isosceles_area(leg, base):
    def height():
        t1, t2 = math.pow(leg, 2), math.pow(base, 2) / 4
        return math.sqrt(t1 - t2)

    if leg == 0 or base == 0:
        return 0

    area = 0.5 * base * height()
    return base
