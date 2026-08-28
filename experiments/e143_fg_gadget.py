"""e143: audited machine check of Lemma FG-high (notes/55 SS5.3b).

The hand proof: attackers x1 = 4M-p, x2 = 4M-q, 0 <= q < p <= M+15,
with p >= 2q+1 (the attacker pair is itself HIGH: 2x2 - x1 >= 4M+1)
and room 5p - 6q <= 2M+15.  In offsets t (value 4M+t), with
s := p - 2q >= 1 and s' := 2p - 3q:

  U1 = A(s):  2s+q  = 2p-3q  before  s   (fan of x2 at midpoint s)
  U2 = B(s):  2s+p  = 3p-4q  before  s   (fan of x1 at midpoint s)
  U3 = B(s'): 2s'+p = 5p-6q  before  s'  (fan of x1 at midpoint s')

  R4 on AP (s, 2p-3q, 3p-4q):   2p-3q  before  3p-4q
  R4 on AP (s, 3p-4q, 5p-6q):   3p-4q  before  5p-6q
  trans with U3 (s' = 2p-3q):   3p-4q  before  2p-3q   -- 2-cycle.

Executed with the e139 ICtx (strict AP membership/arithmetic/rule
pattern asserts + audit of the hypothesis log) for EVERY admissible
(q, p) at every M = 0 mod 16 in 48..400.

Run: .venv/bin/python experiments/e143_fg_gadget.py
Log: data/e143_fg_gadget.log
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from e139_flood6M import ICtx, audit


def check(M, q, p):
    lo, hi = 4 * M + 1, 6 * M + 15
    s = p - 2 * q
    sp = 2 * p - 3 * q
    assert s >= 1 and 5 * p - 6 * q <= 2 * M + 15
    x1, x2 = 4 * M - p, 4 * M - q

    def val(t):
        return 4 * M + t

    ctx = ICtx(lo, hi)
    # the three fan units (hypotheses of the lemma); verify their
    # attack arithmetic before assuming them
    hyps = []
    for (x, mid) in ((x2, s), (x1, s), (x1, sp)):
        y = val(mid)
        z = 2 * y - x
        assert lo <= y <= hi and lo <= z <= hi, (M, q, p, x, mid)
        assert 3 * M - 15 <= x <= 4 * M, (M, q, p, x)
        ctx.assume(z, y)
        hyps.append((z, y))
    # named offsets
    a, b, c = val(2 * p - 3 * q), val(3 * p - 4 * q), val(5 * p - 6 * q)
    assert hyps[0] == (a, val(s))
    assert hyps[1] == (b, val(s))
    assert hyps[2] == (c, val(sp)) and val(sp) == a
    # R4 twice
    ctx.rule(val(s), a, b, (a, val(s)), (a, b))
    ctx.rule(val(s), b, c, (b, val(s)), (b, c))
    # transitivity to the 2-cycle
    ctx.trans(b, c, a)
    assert ctx.has(a, b) and ctx.has(b, a)          # explicit 2-cycle
    audit(ctx, hyps)


def main():
    total = 0
    for M in range(48, 401, 16):
        n = 0
        for p in range(1, M + 16):
            for q in range(0, (p - 1) // 2 + 1):
                if p - 2 * q >= 1 and 5 * p - 6 * q <= 2 * M + 15:
                    check(M, q, p)
                    n += 1
        total += n
        if M in (48, 80, 400):
            print(f'  M={M}: {n} admissible (q,p) pairs verified',
                  flush=True)
    print(f'e143: ALL CHECKS PASSED ({total} gadget instances, '
          f'23 scales)', flush=True)


if __name__ == '__main__':
    main()
