if not line or \
        x > 12 and \
        y <= z:
    raise TokenError("EOF in multi-line string", strstart)
