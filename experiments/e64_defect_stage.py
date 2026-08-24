import sys
exec(open('experiments/e62_skeleton_check.py').read().replace(
"""def stagefn(v, dshift):
    k = block(v)
    s0 = k // 2
    if v % (2 ** s0) == 0 and v >= 3 * 4 ** (s0 - 1):
        return s0
    return s0 + 1""",
"""def stagefn(v, dshift):
    k = block(v)
    s0 = k // 2
    if v % (2 ** dshift) == 2:
        return s0 + 1
    return s0"""))
