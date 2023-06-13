def absolute(a):
    if a > 0:
        return a
    elif a == 0:
        return 0
    else:
        return a  # bug (fix return -1 * a)
