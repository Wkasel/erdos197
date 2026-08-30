"""e187_split_hunt: GAP-AFFORD'''-SPLIT inhabitant-hunt driver
(notes/83 SS0).  Parametrized weak-censor HSPLIT cells via
e186.partHSPLIT; rows merge into data/e186_altclosure.json
partHSPLIT as pre-registered in notes/81 SS2.

Run: .venv/bin/python experiments/e187_split_hunt.py HOR F U0 K8 [BUDGET]
     K8 in {1, 0}: 1 = HSPLIT mods 4+8, 0 = mod-4-only attribution.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import e186_altclosure as e186  # noqa: E402

if __name__ == "__main__":
    hor = int(sys.argv[1])
    F = int(sys.argv[2])
    u0 = int(sys.argv[3])
    k8 = sys.argv[4] not in ("0", "False", "false")
    budget = float(sys.argv[5]) if len(sys.argv) > 5 else 7200.0
    e186.partHSPLIT(hor=hor, F=F, u0=u0, budget=budget, k8=k8)
