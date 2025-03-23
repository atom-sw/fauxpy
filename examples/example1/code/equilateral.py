import math


def equilateral_area(a):
    const = math.sqrt(3) / 4

    if a == 1:
        return const

    term = math.pow(a, 2)
    area = const + term  # bug
    # area = const * term  # patch
    return area
