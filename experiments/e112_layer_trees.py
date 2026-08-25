"""e112_layer_trees: TASK P -- consolidated machine ledger for the layer-1
and layer-2 steps of the S1 hand proof (notes/33).

All verdicts here are CLOSURE verdicts (R1-R4 reflection + transitivity
fixpoint, no SAT search): a "CONTRA" is a unit-propagation refutation whose
step-by-step derivation can be printed by e109 and checked by hand at any
single scale.  This is a strictly stronger certificate than a bare UNSAT.

Ledger:
  A. Layer-1 entanglement (given L0):  L1b + not-L1a  and  L1a + not-L1b
     both closure-refute at every M == 0 (mod 4)  [used as a proof step];
     sharpness: both FAIL to refute at M == 2 (mod 4).
  B. Layer-1 joint core: L0 + {t5<t3, b3<b5} with the fixed 2-split tree
     splits = (m0 vs t5), (b1 vs b5), m0 = 3M/2: all 4 leaves closure-
     refute at every M == 0 (mod 4)  [proof step];
     control: at M == 2 (mod 4) the joint core refutes with NO splits.
  C. Layer-2 flip: L0 + L1 + {t5<b5} with the fixed 2-split tree
     splits = (b1 vs b5), (t2 vs t4): all 4 leaves closure-refute at every
     M == 0 (mod 8)  [proof step];
     sharpness: at M == 4 (mod 8) at least one leaf must stay open
     (the flip is genuinely free there); record which leaves.

Run: .venv/bin/python experiments/e112_layer_trees.py [Mmax] [--dyadic]
Output: data/e112_layer_trees.json
"""
import itertools
import json
import sys
import time

sys.path.insert(0, "/Users/will/Dev/personal/tasks/math/erdos197/experiments")
from e109_l0_trace import Tracer

DATA = "/Users/will/Dev/personal/tasks/math/erdos197/data/e112_layer_trees.json"


def sixL(M):
    return dict(t3=2 * M - 3, t5=2 * M - 5, t10=2 * M - 10,
                b3=M + 3, b5=M + 5, b6=M + 6,
                b1=M + 1, t2=2 * M - 2, t4=2 * M - 4, m0=3 * M // 2)


def closes(M, units):
    tr = Tracer(M)
    return tr.run(units)


def ledger_A(M):
    v = sixL(M)
    base = [(v["t3"], v["b6"]), (v["t10"], v["b3"]),
            (v["t3"], v["b3"]), (v["t10"], v["b6"])]
    r1 = closes(M, base + [(v["b5"], v["b3"]), (v["t5"], v["t3"])])
    r2 = closes(M, base + [(v["t3"], v["t5"]), (v["b3"], v["b5"])])
    return {"L1b+negL1a": "CONTRA" if r1 else "open",
            "L1a+negL1b": "CONTRA" if r2 else "open"}


def ledger_B(M):
    v = sixL(M)
    base = [(v["t3"], v["b6"]), (v["t10"], v["b3"]),
            (v["t3"], v["b3"]), (v["t10"], v["b6"]),
            (v["t5"], v["t3"]), (v["b3"], v["b5"])]
    nosplit = closes(M, base)
    leaves = {}
    for o1, o2 in itertools.product((0, 1), repeat=2):
        s1 = (v["m0"], v["t5"]) if o1 else (v["t5"], v["m0"])
        s2 = (v["b1"], v["b5"]) if o2 else (v["b5"], v["b1"])
        leaves[f"{o1}{o2}"] = "CONTRA" if closes(M, base + [s1, s2]) \
            else "open"
    return {"nosplit": "CONTRA" if nosplit else "open", "leaves": leaves}


def ledger_C(M):
    v = sixL(M)
    base = [(v["t3"], v["b6"]), (v["t10"], v["b3"]),
            (v["t3"], v["b3"]), (v["t10"], v["b6"]),
            (v["t3"], v["t5"]), (v["b5"], v["b3"]),
            (v["t5"], v["b5"])]
    leaves = {}
    for o1, o2 in itertools.product((0, 1), repeat=2):
        s1 = (v["b1"], v["b5"]) if o1 else (v["b5"], v["b1"])
        s2 = (v["t2"], v["t4"]) if o2 else (v["t4"], v["t2"])
        leaves[f"{o1}{o2}"] = "CONTRA" if closes(M, base + [s1, s2]) \
            else "open"
    return {"leaves": leaves}


def main():
    Mmax = int(sys.argv[1]) if len(sys.argv) > 1 else 160
    out = {"A": {}, "B": {}, "C": {}}
    okA = okB = okC = True
    for M in range(40, Mmax + 1, 2):
        t0 = time.time()
        if M % 4 == 0:
            a = ledger_A(M)
            b = ledger_B(M)
            out["A"][str(M)] = a
            out["B"][str(M)] = {"leaves": b["leaves"]}
            okA &= all(x == "CONTRA" for x in a.values())
            okB &= all(x == "CONTRA" for x in b["leaves"].values())
        elif M % 4 == 2:
            a = ledger_A(M)
            b = ledger_B(M)
            out["A"][str(M)] = a
            out["B"][str(M)] = {"nosplit": b["nosplit"]}
            # sharpness at 2 mod 4: entanglement must NOT close (models
            # with exactly one L1 literal exist), joint core must close.
            okA &= all(x == "open" for x in a.values())
            okB &= (b["nosplit"] == "CONTRA")
        if M % 8 == 0:
            c = ledger_C(M)
            out["C"][str(M)] = c
            okC &= all(x == "CONTRA" for x in c["leaves"].values())
        elif M % 8 == 4:
            c = ledger_C(M)
            out["C"][str(M)] = c
            okC &= any(x == "open" for x in c["leaves"].values())
        if M % 8 in (0, 2, 4, 6) and str(M) in out["A"] or M % 8 in (0, 4):
            print(f"M={M} (mod8={M%8}) "
                  f"A={out['A'].get(str(M))} "
                  f"B={out['B'].get(str(M))} "
                  f"C={out['C'].get(str(M), {}).get('leaves')} "
                  f"({time.time()-t0:.1f}s)", flush=True)
    print(f"VERDICT: A(entangle 0mod4 + sharp 2mod4)={'OK' if okA else 'FAIL'} "
          f"B(tree 0mod4 + nosplit 2mod4)={'OK' if okB else 'FAIL'} "
          f"C(tree 0mod8 + open-leaf 4mod8)={'OK' if okC else 'FAIL'}")
    json.dump(out, open(DATA, "w"), indent=1)
    print(f"-> {DATA}")


if __name__ == "__main__":
    main()
