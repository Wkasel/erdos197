"""repro_e113b_subset: step 2 of the reproducibility package (AUDIT A4).

Cross-validates the e113 hand-proof branches with the INDEPENDENT e109
closure engine (R1-R4 + transitivity fixpoint), via the e113b harness, on
a subset of scales:

    Layer-1 branches (8 per scale): M = 12, 16, ..., 60 (step 4) and 128
    Flip branches    (4 per scale): M = 16, 24, ..., 64 (step 8) and 128

The full run (M <= 200 plus 256/400/512) is `python experiments/
e113b_closure_crossval.py`; archived output: data/e113b_crossval.json.

Run: .venv/bin/python experiments/repro_e113b_subset.py
Exit code 0 iff every branch of every scale closes.
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e113b_closure_crossval import cross_l1, cross_flip

t0 = time.time()
l1_scales = list(range(12, 61, 4)) + [128]
fl_scales = list(range(16, 65, 8)) + [128]
fails = []
for M in l1_scales:
    if not cross_l1(M):
        fails.append(("layer1", M))
for M in fl_scales:
    if not cross_flip(M):
        fails.append(("flip", M))
print(f"e113b subset: layer1 x{len(l1_scales)} "
      f"({l1_scales[0]}..{l1_scales[-1]}), flip x{len(fl_scales)} "
      f"({fl_scales[0]}..{fl_scales[-1]})  [{time.time()-t0:.0f}s]")
if fails:
    print("FAILURES:", fails)
    sys.exit(1)
print("all branches close")
