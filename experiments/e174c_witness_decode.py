"""e174c_witness_decode: decode the KCRIT escape witnesses (x = 15 and
27, M = 80, full bottom-transversal punctures) and print their order
anatomy.  Finding (notes/74 SSI.6): the witnesses are PARITY SPLITS
(all even values before all odd values), which by hand satisfies every
constraint except the odd-attacker even-j units -- the transversal lane.

Run: .venv/bin/python experiments/e174c_witness_decode.py
Output: data/e174c_witness.log (via tee in caller)
"""
import sys

sys.path.insert(0, "/Users/will/Dev/personal/tasks/math/erdos197/experiments")
from e174_n3_growth import Gadget, offset  # noqa: E402

for (x, M, P) in [(15, 80, [82, 84, 86]),
                  (27, 80, [82, 84, 86, 88, 90, 92])]:
    g = Gadget(M, x)
    sat = g.query(P)
    assert sat, (x, M, P)
    pos_lits = set(l for l in g.solver.get_model() if l > 0)

    def before(w, u):
        lit = g.o(w, u)
        return (lit in pos_lits) if lit > 0 else (-lit not in pos_lits)

    keep = [v for v in g.vals if v not in set(P)]
    order = sorted(keep, key=lambda u: sum(
        1 for w in keep if w != u and before(w, u)))
    par = ["E" if v % 2 == 0 else "O" for v in order]
    split = par == sorted(par, reverse=True)  # all E before all O
    print(f"x={x} M={M} P={[offset(v, M) for v in P]}: free model is a "
          f"clean parity split: {split}")

    # THE (N3-a) check: does a parity-split witness EXIST?  Constrain
    # every even value before every odd value and re-solve.
    Pset = set(P)
    assump = [(-g.sel[v] if v in Pset else g.sel[v]) for v in g.vals]
    evens = [v for v in keep if v % 2 == 0]
    odds = [v for v in keep if v % 2 == 1]
    assump += [g.o(u, w) for u in evens for w in odds]
    sat2 = g.solver.solve(assumptions=assump)
    print(f"  parity-split-CONSTRAINED witness exists: "
          f"{'YES (SAT)' if sat2 else 'NO (UNSAT)'}")
    if sat2:
        g._audit(Pset)  # independent scanner on the decoded order
        print("  (constrained model re-audited: no monotone AP, "
              "all units hold)")
    g.delete()
