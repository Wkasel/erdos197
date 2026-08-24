import sys, re
body = open('experiments/e62_skeleton_check.py').read()
fn = '''def stagefn(v, dshift):
    k = block(v)
    s0 = k // 2
    if v % 2 == 1 and v % (2 ** s0) == 2 ** s0 - 1 and v > 5 * 2 ** (k - 3):
        return s0
    return s0 + dshift'''
body = re.sub(r"def stagefn\(v, dshift\):.*?return s0 \+ 1", fn, body, flags=re.S)
exec(body)
