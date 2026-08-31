# Spot-verify FRONT 84: Lemma LAND + Theorem S1/Cor COR, independent reconstruction.
# Fresh window lengths N = 600 and N = 222 (never scanned; record was N = 55..495).
# For EVERY odd-gap pair with 7q+10g <= 2N, build the S1 certificate per the COR recipe
# and step-walk it with all validity conditions checked; also verify LAND(c) exactness.
import sys
fails = []
def chk(name, cond):
    if not cond:
        fails.append(name); print("FAIL:", name)

def spiral_land(h, target, q, p, N, max_steps=200):
    """Forced spiral at head h aiming at target; returns (landed, steps, trace_ok).
    Each step: RL on h < x_n (needs 1 <= 2h - x_n <= N), then unit
    (2h - x_n) = 2 x_{n+1} + r < x_{n+1} with r in {q,p}, r == x_n+... forced by parity:
    r_{n+1} unique in {q,p} with r == (2h - x_n) mod 2, x_{n+1} = (2h - x_n - r)/2.
    Validity: x_{n+1} >= 1, x_{n+1} != h. Seed: r0 unique in {q,p} with r0 == h mod 2,
    x0 = (h - r0)/2 (unit h = 2 x0 + r0 < x0: needs x0 >= 1, x0 != h, h <= N)."""
    r0 = q if (h - q) % 2 == 0 else p
    assert (h - r0) % 2 == 0
    x = (h - r0) // 2
    if not (1 <= x and x != h and h <= N): return (False, 0, False)
    for n in range(max_steps):
        if x == target: return (True, n, True)
        w = 2 * h - x                      # RL reflection
        if not (1 <= w <= N): return (False, n, False)
        r = q if (w - q) % 2 == 0 else p   # forced residue
        xn = (w - r) // 2
        if not (xn >= 1 and xn != h): return (False, n, False)
        x = xn
    return (False, max_steps, True)

for N in (600, 222):
    tested = certs = 0
    for q in range(0, N):
        for g in range(1, N, 2):  # odd gaps
            p = q + g
            if 7*q + 10*g > 2*N: continue
            if p > N: continue
            tested += 1
            # COR recipe for t
            if q > g:
                # smaller valid lift in classes t == -q or t == -p (mod 2g), t >= 1
                cands = [t for t in range(1, 2*g + 1) if (t + q) % (2*g) == 0 or (t + p) % (2*g) == 0]
                t = min(cands)
            elif q < g:
                t = g - q
            else:
                t = g
            r0 = q if (t - q) % 2 == 0 else p
            # (C1)-(C3)
            c1 = ((t + r0) // 2) % g == 0 and (t + r0) % 2 == 0
            c2 = 2*q + 3*t - r0 >= 2
            c3 = 9*t + 6*q + r0 <= 2*N
            chk(f"S1cond N={N} q={q} p={p}", c1 and c2 and c3)
            u, w = q + 2*t, 3*t + 2*q
            # seed unit u = 2t + q, fact u < t: valid iff t >= 1, u <= N
            chk(f"seed N={N} q={q} p={p}", t >= 1 and u <= N and (u - q) % 2 == 0)
            # RL on u < t gives u < 2u - t = w ; AP (t,u,w) inside [1,N]
            chk(f"RL N={N} q={q} p={p}", 2*u - t == w and 1 <= t and w <= N)
            # spiral at w must land on u with every step valid
            landed, steps, ok = spiral_land(w, u, q, p, N)
            chk(f"land N={N} q={q} p={p}", landed and ok)
            if landed and ok: certs += 1
    print(f"N={N}: pairs tested {tested}, spiral 2-cycle certificates valid {certs}")

# LAND(c) exactness: if g does not divide delta0 the spiral NEVER lands (500 steps)
import random
random.seed(7)
never = 0; trials = 0
for _ in range(3000):
    g = random.choice([3,5,7,9,11,13])
    q = random.randrange(1, 60); p = q + g
    tau = random.randrange(max(1, q), 400)
    rstar = q if tau % 2 == q % 2 else p
    h3 = 3*tau + rstar
    if h3 % 2: continue
    h = h3 // 2
    # deviation recursion, unbounded window (pure dynamics: LAND(c) is arithmetic)
    r0 = q if (h - q) % 2 == 0 else p
    if (h - r0) % 2: continue
    x = (h - r0)//2
    d0 = x - tau
    if d0 % g == 0: continue
    trials += 1
    hit = False
    for n in range(500):
        if x == tau: hit = True; break
        w = 2*h - x
        r = q if (w - q) % 2 == 0 else p
        x = (w - r)//2
    if not hit: never += 1
chk("LAND(c) exactness", never == trials and trials > 500)
print(f"LAND(c): {never}/{trials} non-divisible seeds never land")
print("TOTAL FAILS:", len(fails))
sys.exit(0 if not fails else 1)
