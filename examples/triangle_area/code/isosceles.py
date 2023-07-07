import math


def isosceles_area(leg, base):
    def height():
        t1, t2 = math.pow(base, 2), math.pow(leg, 2) / 4  # bug
        # t1, t2 = math.pow(leg, 2), math.pow(base, 2) / 4  # patch
        return math.sqrt(t1 - t2)

    area = 0.5 * base * height()
    return area
