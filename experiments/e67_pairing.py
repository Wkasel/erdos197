import sys
body = open('experiments/e62_skeleton_check.py').read()
mode = int(sys.argv[3]) if len(sys.argv) > 3 else 0
if mode == 0:  # good pairing (4,6),(8,10),...
    fn = """def stagefn(v, dshift):
    return max(block(v) // 4, 1) if block(v) >= 4 else 0"""
else:  # bad pairing (2,4),(6,8),...
    fn = """def stagefn(v, dshift):
    return (block(v) + 2) // 4"""
import re
body = re.sub(r"def stagefn\(v, dshift\):.*?return s0 \+ 1", fn, body, flags=re.S)
exec(body)
