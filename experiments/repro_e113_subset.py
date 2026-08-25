"""repro_e113_subset: step 1 of the reproducibility package (AUDIT A4).

Runs the e113 hand-proof schema checker (the rung-by-rung verifier of the
notes/33 Layer-1 and Flip theorem schemas) at the representative scale set:

    Layer-1:   M = 12, 16, ..., 100 (step 4)  and M = 512
    Flip:      M = 16, 24, ..., 104 (step 8)  and M = 512
    Sharpness: M = 4 mod 8 schema inapplicability, M = 20..100

This imports the checker functions unchanged from e113_c3_hand_proof (the
full run over M <= 400 plus 512/1024 is `python experiments/
e113_c3_hand_proof.py`; its archived output is data/e113_hand_proof.json).

Run: .venv/bin/python experiments/repro_e113_subset.py
Exit code 0 iff every scale passes.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e113_c3_hand_proof import check_layer1, check_flip, sharpness_4mod8

fails = []

l1_scales = list(range(12, 101, 4)) + [512]
fl_scales = list(range(16, 105, 8)) + [512]
sh_scales = [M for M in range(20, 101, 8) if M % 8 == 4]

for M in l1_scales:
    try:
        check_layer1(M)
    except AssertionError as ex:
        fails.append(("layer1", M, repr(ex.args[:2])))
for M in fl_scales:
    try:
        check_flip(M)
    except AssertionError as ex:
        fails.append(("flip", M, repr(ex.args[:2])))
for M in sh_scales:
    try:
        sharpness_4mod8(M)
    except AssertionError as ex:
        fails.append(("sharp", M, repr(ex.args[:2])))

print(f"e113 subset: layer1 at {len(l1_scales)} scales "
      f"({l1_scales[0]}..{l1_scales[-1]}), flip at {len(fl_scales)} scales "
      f"({fl_scales[0]}..{fl_scales[-1]}), sharpness at {len(sh_scales)}")
if fails:
    print("FAILURES:", fails)
    sys.exit(1)
print("all scales OK")
