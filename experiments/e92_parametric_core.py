"""P3: parametric skeleton of the OG(M) triple-MUS. Parses data/og_mus_M.log
(from e90) for several M, expresses every MUS value v in anchor coordinates
v = (p*M+q)/4 with p in {4,5,6,7,8}:
  p=4: M+a       (a=v-M,    1<=a<=20)
  p=5: (5M+a)/4  (a=4v-5M,  |a|<=20)   [quarter point]
  p=6: (3M+a)/2  (a=2v-3M,  |a|<=20)   [midpoint]
  p=7: (7M+a)/4  (a=4v-7M,  |a|<=20)   [three-quarter point]
  p=8: 2M-a      (a=2M-v,   0<=a<=20)
A pattern common to >=2 distinct M must be an AP identically in M, which
forces p1+p3=2*p2 (then q1+q3=2*q2 is automatic at any single M). We
enumerate all consistent representation-tuples per MUS triple, intersect the
pattern sets across M, and report per-residue-class (M mod 4) structure.
"""
import re, sys, json
from pathlib import Path
from itertools import product

DATA = Path(__file__).resolve().parent.parent / "data"
MS = [40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 60]
TARGET = [40, 44, 48, 52]
ABOUND = 20

def parse(M):
    txt = (DATA / f"og_mus_{M}.log").read_text()
    trips = []
    grab = False
    for line in txt.splitlines():
        if line.startswith("MUS ("):
            grab = True
            continue
        if grab:
            m = re.match(r"\s+\((\d+), (\d+), (\d+)\)", line)
            if m:
                trips.append(tuple(int(g) for g in m.groups()))
    return trips

def forms(v, M):
    """all (p,q) with v=(p*M+q)/4, small anchor offset"""
    out = []
    a = v - M
    if 1 <= a <= ABOUND: out.append((4, 4 * a))
    a = 4 * v - 5 * M
    if abs(a) <= ABOUND: out.append((5, a))
    a = 2 * v - 3 * M
    if abs(a) <= ABOUND: out.append((6, 2 * a))
    a = 4 * v - 7 * M
    if abs(a) <= ABOUND: out.append((7, a))
    a = 2 * M - v
    if 0 <= a <= ABOUND: out.append((8, -4 * a))
    return out

def render1(p, q):
    if p == 4: return f"M{q//4:+d}"
    if p == 8: return f"2M{q//4:+d}"
    if p == 6:
        h = q // 2
        return f"(3M{h:+d})/2"
    return f"({p}M{q:+d})/4"

def render(pat):
    return "(" + ", ".join(render1(p, q) for p, q in pat) + ")"

def patterns_of(trip, M):
    reps = [forms(v, M) for v in trip]
    out = set()
    for f1, f2, f3 in product(*reps):
        if f1[0] + f3[0] == 2 * f2[0]:
            # q consistency is then automatic at this M, but keep the check
            if f1[1] + f3[1] == 2 * f2[1]:
                out.add((f1, f2, f3))
    return out

pats = {}       # M -> set of patterns
inst = {}       # M -> pattern -> concrete triple
mus = {}
for M in MS:
    mus[M] = parse(M)
    s = set()
    d = {}
    for t in mus[M]:
        for pat in patterns_of(t, M):
            s.add(pat)
            d[pat] = t
    pats[M] = s
    inst[M] = d
    print(f"M={M}: MUS {len(mus[M])} triples -> {len(s)} consistent patterns")

def inter(ms):
    s = set(pats[ms[0]])
    for M in ms[1:]:
        s &= pats[M]
    return s

common_target = inter(TARGET)
common_all = inter(MS)
res = {r: [M for M in MS if M % 4 == r] for r in range(4)}
common_res = {r: inter(ms) for r, ms in res.items() if ms}

print(f"\n=== patterns at ALL target M {TARGET}: {len(common_target)} ===")
def key(pat):
    return (tuple(p for p, _ in pat), tuple(q for _, q in pat))
for pat in sorted(common_target, key=key):
    where = "".join("y" if pat in pats[M] else "." for M in MS)
    print(f"  {render(pat):42s} presence[{','.join(map(str,MS))}]={where} "
          f"e.g. M=40 -> {inst[40].get(pat)}")

print(f"\n=== patterns at ALL 11 tested M: {len(common_all)} ===")
for pat in sorted(common_all, key=key):
    print(f"  {render(pat)}")

for r in sorted(common_res):
    print(f"\n=== common within M≡{r} (mod 4) {res[r]}: {len(common_res[r])} ===")
    for pat in sorted(common_res[r], key=key):
        mark = " [ALL-M]" if pat in common_all else ""
        print(f"  {render(pat)}{mark}")

# family view: group residue-class-common patterns by p-vector
print("\n=== p-vector families (which residue classes have a common pattern"
      " with this shape) ===")
fam = {}
for r in sorted(common_res):
    for pat in common_res[r]:
        pv = tuple(p for p, _ in pat)
        fam.setdefault(pv, {}).setdefault(r, []).append(pat)
for pv in sorted(fam):
    shape = "(" + ",".join({4: "M+a", 5: "5M/4", 6: "3M/2", 7: "7M/4",
                            8: "2M-a"}[p] for p in pv) + ")"
    rs = {r: sorted(render(p) for p in ps) for r, ps in sorted(fam[pv].items())}
    print(f"  {shape}: residues {sorted(fam[pv])}")
    for r, ps in rs.items():
        print(f"      r={r}: {ps}")

out = {
    "M_tested": MS,
    "target": TARGET,
    "mus_sizes": {M: len(mus[M]) for M in MS},
    "common_target": [[render1(*f) for f in pat] for pat in sorted(common_target, key=key)],
    "common_all": [[render1(*f) for f in pat] for pat in sorted(common_all, key=key)],
    "common_by_residue": {r: [[render1(*f) for f in pat]
                              for pat in sorted(common_res[r], key=key)]
                          for r in sorted(common_res)},
}
(DATA / "parametric_core.json").write_text(json.dumps(out, indent=1))
print("\nwrote data/parametric_core.json")
