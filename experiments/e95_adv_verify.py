"""Adversarial re-verification of notes/30-og-proof-draft.md.

Independent encoding: eager full transitivity (2 clauses per index triple
i<j<k), AP constraints as the two forbidden monotone patterns.  No code
shared with e94_step_check.py; no lazy loop.

Checks (numbered in output):
 V1  j*(M) at 40,44,48,52,60 (claim 3,3,2,3,3); fam15 SAT everywhere.
 V2  H* SAT; bottom-vs-guard forced table (S11) incl. b6<t4 rows.
 V3  b5 vs t6 under fam15 alone: neither direction forced (S11 neg).
 V4  O1..O8 literals forced under H* at each of 40,44,48,52,60 (S12).
 V5  chain literals (Part 10 analogue): b7<m2, m2<t2, m2<b4, b7<b21,
     b21<t2, b7<t2 status at each M (S13/S14 + caveats).
 V6  kernel 66<53: ALL 5x5 slope lifts incl. the PIN-excluded midband
     (3M+12)/2 and quarterband (7M-16)/4 lifts of 66 -- is ANY lift
     forced at all of 44,48,52,60?  (attack on S12/G4 'does not lift')
 V7  M=50: j*=1; b7 vs t2 undetermined under bare fam15 (caveat c).
 V8  j* at 56,64,72,80 (claims 3,2,2,2 from P1, cited in S6).
 V9  10-unit core at 51: SAT (exception), and j*(51)=4 (S7/S9); same 67.
 V10 C4 = {15:1,15:2,15:5,16:3}: UNSAT at 40,44,48,52,56,60,64,68;
     SAT at 42,45,46,50,51,54,58 (S8).
 V11 C3 = {15:5,15:6,16:3}: UNSAT at 40,48,56,64; SAT at 42,44,46,50,
     52,60,68 (S8).
 V12 F1..F7 arithmetic identities + interval membership, symbolic in M
     (S16 arithmetic part) at M=40..60 even.
 V13 S5 coincidences: solve each linear equation for M, assert unique
     solution M=40.
 V14 shared-AP counts of the S12 support table vs data/step_check.json.
"""
import json
import sys
import time
from fractions import Fraction

from pysat.solvers import Cadical195

T0 = time.time()


def log(s=""):
    print(s, flush=True)


class EOG:
    """Eager full-transitivity encoding of OG(M)'s constraint (i)."""

    def __init__(self, M):
        self.M = M
        self.V = list(range(M + 1, 2 * M + 1))
        self.idx = {v: i for i, v in enumerate(self.V)}
        n = len(self.V)
        self.n = n
        self.var = {}
        c = 0
        for i in range(n):
            for j in range(i + 1, n):
                c += 1
                self.var[(i, j)] = c
        cl = []
        # (i): for AP a<b<c forbid a<b<c and c<b<a  (=> o(a,b) != o(b,c))
        self.ntrip = 0
        for b in self.V:
            d = 1
            while b + d <= 2 * M:
                a, cc = b - d, b + d
                if a > M:
                    self.ntrip += 1
                    cl.append([-self.o(a, b), -self.o(b, cc)])
                    cl.append([self.o(a, b), self.o(b, cc)])
                d += 1
        # transitivity, both directions, all index triples
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    vij = self.var[(i, j)]
                    vjk = self.var[(j, k)]
                    vik = self.var[(i, k)]
                    cl.append([-vij, -vjk, vik])
                    cl.append([vij, vjk, -vik])
        self.sol = Cadical195(bootstrap_with=cl)

    def o(self, u, w):
        i, j = self.idx[u], self.idx[w]
        return self.var[(i, j)] if i < j else -self.var[(j, i)]

    def solve(self, assumps):
        return self.sol.solve(assumptions=assumps)

    def a15(self, j):
        return self.o(2 * self.M + 2 * j - 15, self.M + j)

    def a16(self, j):
        return self.o(2 * self.M + 2 * j - 16, self.M + j)

    def fam15(self):
        return [self.a15(j) for j in range(1, 8)]

    def pre16(self, upto):
        return [self.a16(j) for j in range(1, upto + 1)]

    def status(self, H, u, v):
        """'F' u<v forced, 'R' v<u forced, '-' neither, 'X' both (H UNSAT)."""
        fa = not self.solve(H + [self.o(v, u)])
        fb = not self.solve(H + [self.o(u, v)])
        return {(True, False): "F", (False, True): "R",
                (False, False): "-", (True, True): "X"}[(fa, fb)]

    def delete(self):
        self.sol.delete()


FAILS = []


def chk(name, cond, detail=""):
    tag = "ok" if cond else "FAIL"
    if not cond:
        FAILS.append((name, detail))
    log(f"  [{tag}] {name} {detail}")


MS_ALL = [40, 44, 48, 52, 60]
EXPECT_JSTAR = {40: 3, 44: 3, 48: 2, 52: 3, 60: 3}

inst = {}
jstar = {}

log("== V1: j*(M), fam15 SAT")
for M in MS_ALL:
    g = EOG(M)
    inst[M] = g
    s15 = g.solve(g.fam15())
    js = None
    for j in range(1, 9):
        if not g.solve(g.fam15() + g.pre16(j)):
            js = j
            break
    jstar[M] = js
    chk(f"M={M}: fam15 SAT", s15)
    chk(f"M={M}: j*={js} (expect {EXPECT_JSTAR[M]})", js == EXPECT_JSTAR[M])
log(f"  ({time.time()-T0:.0f}s)")

log("== V2: H* SAT + bottom-vs-guard table (S11)")
EXPECT_BVG = {
    40: {1: "R", 2: "R", 3: "F", 4: "-", 5: "F", 6: "-", 7: "F"},
    44: {1: "R", 2: "R", 3: "F", 4: "-", 5: "F", 6: "F", 7: "F"},
    48: {1: "R", 2: "F", 3: "F", 4: "-", 5: "F", 6: "-", 7: "F"},
    52: {1: "R", 2: "R", 3: "F", 4: "-", 5: "F", 6: "F", 7: "F"},
    60: {1: "R", 2: "R", 3: "F", 4: "-", 5: "F", 6: "F", 7: "F"},
}
# 'F' means b_j < t_{16-2j} forced; 'R' means guard first (axiom rows).
for M in MS_ALL:
    g = inst[M]
    H = g.fam15() + g.pre16(jstar[M] - 1)
    chk(f"M={M}: H* SAT", g.solve(H))
    row = {}
    for j in range(1, 8):
        t = 2 * M - (16 - 2 * j)
        b = M + j
        row[j] = g.status(H, b, t)
    exp = EXPECT_BVG[M]
    chk(f"M={M}: bvg row {row}", row == exp, f"(expect {exp})")
log(f"  ({time.time()-T0:.0f}s)")

log("== V3: b5 vs t6 under fam15 alone (should be '-' at every M)")
for M in MS_ALL:
    g = inst[M]
    st = g.status(g.fam15(), M + 5, 2 * M - 6)
    chk(f"M={M}: b5 vs t6 under fam15: {st}", st == "-")
log(f"  ({time.time()-T0:.0f}s)")

log("== V4: O1..O8 forced under H* (S12), each M separately")
def m2(M):
    return (3 * M + 2) // 2
OLIT = {
    "O1a M+19<M+13": lambda M: (M + 19, M + 13),
    "O1b t21<t27": lambda M: (2 * M - 21, 2 * M - 27),
    "O2a M+11<M+21": lambda M: (M + 11, M + 21),
    "O2b t29<t19": lambda M: (2 * M - 29, 2 * M - 19),
    "O3a t13<t19": lambda M: (2 * M - 13, 2 * M - 19),
    "O3b t13<t23": lambda M: (2 * M - 13, 2 * M - 23),
    "O3c t13<M+17": lambda M: (2 * M - 13, M + 17),
    "O4a t9<t11": lambda M: (2 * M - 9, 2 * M - 11),
    "O4b t9<t7": lambda M: (2 * M - 9, 2 * M - 7),
    "O4c t11<t2": lambda M: (2 * M - 11, 2 * M - 2),
    "O5  M+7<M+21": lambda M: (M + 7, M + 21),
    "O6a M+21<t2": lambda M: (M + 21, 2 * M - 2),
    "O6b m2<t2": lambda M: (m2(M), 2 * M - 2),
    "O6c t19<t2": lambda M: (2 * M - 19, 2 * M - 2),
    "O7a m2<M+4": lambda M: (m2(M), M + 4),
    "O7b M+21<M+4": lambda M: (M + 21, M + 4),
    "O7c t19<M+4": lambda M: (2 * M - 19, M + 4),
    "O8a M+31<M+21": lambda M: (M + 31, M + 21),
    "O8b t9<M+21": lambda M: (2 * M - 9, M + 21),
}
for name, f in OLIT.items():
    sts = {}
    for M in MS_ALL:
        g = inst[M]
        H = g.fam15() + g.pre16(jstar[M] - 1)
        u, v = f(M)
        sts[M] = g.status(H, u, v)
    allF = all(s == "F" for s in sts.values())
    testF = all(sts[M] == "F" for M in (44, 48, 52, 60))
    chk(f"{name}: {sts}", testF,
        "(claim: F at 44,48,52,60%s)" % ("; also F at 40" if allF else
                                         "; NOT F at 40!"))
log(f"  ({time.time()-T0:.0f}s)")

log("== V5: final-chain literals (S13/S14, Part-10 analogue)")
EXPECT_CHAIN = {
    40: {"b7<m2": "F", "m2<t2": "F", "m2<b4": "F", "b7<b21": "F",
         "b21<t2": "F", "b7<t2": "F"},
    44: {"b7<m2": "-", "m2<t2": "F", "m2<b4": "F", "b7<b21": "F",
         "b21<t2": "F", "b7<t2": "F"},
    48: {"b7<m2": "F", "m2<t2": "F", "m2<b4": "F", "b7<b21": "F",
         "b21<t2": "F", "b7<t2": "F"},
    52: {"b7<m2": "-", "m2<t2": "F", "m2<b4": "F", "b7<b21": "F",
         "b21<t2": "F", "b7<t2": "F"},
    60: {"b7<m2": "-", "m2<t2": "F", "m2<b4": "F", "b7<b21": "F",
         "b21<t2": "F", "b7<t2": "F"},
}
for M in MS_ALL:
    g = inst[M]
    H = g.fam15() + g.pre16(jstar[M] - 1)
    row = {}
    for name, (u, v) in [
            ("b7<m2", (M + 7, m2(M))), ("m2<t2", (m2(M), 2 * M - 2)),
            ("m2<b4", (m2(M), M + 4)), ("b7<b21", (M + 7, M + 21)),
            ("b21<t2", (M + 21, 2 * M - 2)),
            ("b7<t2", (M + 7, 2 * M - 2))]:
        row[name] = g.status(H, u, v)
    chk(f"M={M}: chain {row}", row == EXPECT_CHAIN[M],
        f"(expect {EXPECT_CHAIN[M]})")
log(f"  ({time.time()-T0:.0f}s)")

log("== V6: kernel 66<53 -- ALL 25 slope lifts incl. PIN-excluded ones")
def lift40(v0, p, M):
    q = 4 * v0 - 40 * p
    num = p * M + q
    return num // 4 if num % 4 == 0 else None
found = []
for pu in (4, 5, 6, 7, 8):
    for pv in (4, 5, 6, 7, 8):
        ok = True
        for M in (44, 48, 52, 60):
            u = lift40(66, pu, M)
            v = lift40(53, pv, M)
            if (u is None or v is None or u == v
                    or not (M < u <= 2 * M) or not (M < v <= 2 * M)):
                ok = False
                break
            g = inst[M]
            H = g.fam15() + g.pre16(jstar[M] - 1)
            if g.solve(H + [g.o(v, u)]):   # reverse SAT => not forced
                ok = False
                break
        if ok:
            found.append((pu, pv))
chk(f"66<53 forced lifts over ALL slope pairs: {found}", len(found) == 0,
    "(G4 claims NONE; any hit breaks S12/G4)")
log(f"  ({time.time()-T0:.0f}s)")

log("== V7: M=50 (caveat c)")
g50 = EOG(50)
s15 = g50.solve(g50.fam15())
j1 = not g50.solve(g50.fam15() + g50.pre16(1))
chk("M=50: fam15 SAT", s15)
chk("M=50: fam15+16{1} UNSAT (j*=1)", j1)
st = g50.status(g50.fam15(), 57, 98)
chk(f"M=50: b7 vs t2 under fam15: {st} (claim not forced)", st == "-")
g50.delete()
log(f"  ({time.time()-T0:.0f}s)")

log("== V8: j* at 56,64,72,80 (claims 3,2,2,2)")
for M, exp in ((56, 3), (64, 2), (72, 2), (80, 2)):
    g = EOG(M)
    js = None
    for j in range(1, 9):
        if not g.solve(g.fam15() + g.pre16(j)):
            js = j
            break
    chk(f"M={M}: j*={js} (expect {exp})", js == exp)
    g.delete()
log(f"  ({time.time()-T0:.0f}s)")

log("== V9: exceptional M=51, 67")
for M in (51, 67):
    g = EOG(M)
    s10 = g.solve(g.fam15() + g.pre16(3))
    s11u = not g.solve(g.fam15() + g.pre16(4))
    chk(f"M={M}: 10-unit core SAT (exception)", s10)
    chk(f"M={M}: fam15+16{{1..4}} UNSAT (j*=4)", s11u)
    g.delete()
log(f"  ({time.time()-T0:.0f}s)")

log("== V10/V11: C4 and C3 residue behavior")
C4 = lambda g: [g.a15(1), g.a15(2), g.a15(5), g.a16(3)]
C3 = lambda g: [g.a15(5), g.a15(6), g.a16(3)]
for M in (40, 42, 44, 45, 46, 48, 50, 51, 52, 54, 56, 58, 60, 64, 68):
    g = inst[M] if M in inst else EOG(M)
    r4 = g.solve(C4(g))
    r3 = g.solve(C3(g))
    e4 = (M % 4 != 0)     # claim: SAT iff not divisible by 4
    e3 = (M % 8 != 0)     # claim: SAT iff not divisible by 8
    chk(f"M={M}: C4 SAT={r4} (expect {e4}); C3 SAT={r3} (expect {e3})",
        r4 == e4 and r3 == e3)
    if M not in inst:
        g.delete()
log(f"  ({time.time()-T0:.0f}s)")

log("== V12: F1..F7 arithmetic (symbolic + numeric)")
F = {
    "F1": lambda M: (M + 1, Fraction(3 * M - 6, 2), 2 * M - 7),
    "F2": lambda M: (M + 5, Fraction(3 * M + 2, 2), 2 * M - 3),
    "F3": lambda M: (M + 7, Fraction(3 * M + 2, 2), 2 * M - 5),
    "F4": lambda M: (M + 17, Fraction(3 * M - 2, 2), 2 * M - 19),
    "F5": lambda M: (M + 19, Fraction(3 * M + 14, 2), 2 * M - 5),
    "F6": lambda M: (Fraction(3 * M - 2, 2), Fraction(3 * M + 6, 2),
                     Fraction(3 * M + 14, 2)),
    "F7": lambda M: (Fraction(3 * M + 2, 2), Fraction(7 * M - 16, 4),
                     2 * M - 9),
}
for name, f in F.items():
    ok = True
    for M in range(40, 61, 4):
        a, b, c = f(M)
        if not (a + c == 2 * b and M < a <= 2 * M and M < b <= 2 * M
                and M < c <= 2 * M and a < b < c
                and all(Fraction(x).denominator == 1 for x in (a, b, c))):
            ok = False
    chk(f"{name}: AP + interval + integrality at M=40,44,...,60", ok)

log("== V13: S5 coincidence equations (unique solution M=40)")
# each: LHS-RHS linear in M; solve
eqs = {
    "M+17=m_-6": (Fraction(1) - Fraction(3, 2), 17 - Fraction(-6, 2)),
    "M+19=m_-2": (Fraction(1) - Fraction(3, 2), 19 - Fraction(-2, 2)),
    "M+21=m_2": (Fraction(1) - Fraction(3, 2), 21 - Fraction(2, 2)),
    "m_2=t_19": (Fraction(3, 2) - 2, Fraction(2, 2) + 19),
    "m_12=t_14": (Fraction(3, 2) - 2, Fraction(12, 2) + 14),
    "m_12=q_-16": (Fraction(3, 2) - Fraction(7, 4),
                   Fraction(12, 2) + Fraction(16, 4)),
    "q_-16=t_14": (Fraction(7, 4) - 2, Fraction(-16, 4) + 14),
}
for name, (a, b) in eqs.items():
    # aM + b = 0 -> M = -b/a
    sol = -b / a
    chk(f"{name}: M={sol}", sol == 40)

log("== V14: shared-AP counts vs step_check.json (S12 table)")
sc = json.load(open("/Users/will/Dev/personal/tasks/math/erdos197/data/"
                    "step_check.json"))
sup = sc["supports"]
expect = {"b7<b21": (41, 37), "b21<t2": (42, 39), "m2<b4": (37, 36),
          "b7<t2": (41, 42)}
for name, (eb, et) in expect.items():
    d = sup[name]
    t44 = {tuple(t) for t in d["44"]["triples"]}
    t60 = {tuple(t) for t in d["60"]["triples"]}
    nb = len({tuple(x - 44 for x in t) for t in t44}
             & {tuple(x - 60 for x in t) for t in t60})
    nt = len({tuple(x - 88 for x in t) for t in t44}
             & {tuple(x - 120 for x in t) for t in t60})
    n44, n60 = len(t44), len(t60)
    chk(f"{name}: |44|={n44} |60|={n60} shared bottom={nb} top={nt}",
        (nb, nt) == (eb, et), f"(note claims {eb}/{et})")
    # also recheck note's support sizes
note_sizes = {"b7<b21": (124, 246), "b21<t2": (131, 262),
              "m2<b4": (131, 262), "b7<t2": (138, 270)}
for name, (s44, s60) in note_sizes.items():
    d = sup[name]
    chk(f"{name}: sizes {len(d['44']['triples'])}/{len(d['60']['triples'])}"
        f" (note {s44}/{s60})",
        (len(d["44"]["triples"]), len(d["60"]["triples"])) == (s44, s60))

log()
log(f"== TOTAL {time.time()-T0:.0f}s; failures: {len(FAILS)}")
for n, d in FAILS:
    log(f"  FAIL: {n} {d}")
sys.exit(0 if not FAILS else 1)
