"""Erdős #197 — generic prefix verifier with doom-detection + delayed-dyadic schemes.

A team's proposed (finite prefix of an) infinite sequence is checked for:
 - violation: monotone 3-AP already present among placed values;
 - doom: an increasingly-placed pair (x, y) whose completion 2y-x is in the
   team's set but not yet placed (it must eventually be placed => increasing
   3-AP guaranteed). Downward analogue for decreasingly-placed pairs whose
   completion 2y-x (< y) is in the team's unplaced future.

If a prefix passes with no violation and no doom, it is a certified partial
solution: any doom-free extension strategy remains possible so far.
"""


def check_team(seq, team_set, verbose=False):
    """seq: list of placed values (the team's sequence prefix).
    team_set: set of ALL values owned by the team within the examined range
    (must contain every element of seq; unplaced = team_set - seq).
    Returns (status, info): status in {'ok', 'violation', 'doom'}."""
    pos = {v: i for i, v in enumerate(seq)}
    placed = set(seq)
    unplaced = team_set - placed
    n = len(seq)
    for i in range(n):
        x = seq[i]
        for j in range(i + 1, n):
            y = seq[j]
            z = 2 * y - x  # completion continuing the (x -> y) direction
            if z <= 0 or z == y:
                continue
            if z in placed:
                if pos[z] > j:
                    return 'violation', (x, y, z)
            elif z in unplaced:
                return 'doom', (x, y, z)
    return 'ok', None


def dyadic_blocks(kmax):
    """block k = (2^(k-1), 2^k], k = 1..kmax"""
    return {k: list(range(2 ** (k - 1) + 1, 2 ** k + 1)) for k in range(1, kmax + 1)}


def team_sets(kmax, parity):
    s = set()
    if parity == 0:
        s.add(1)
    for k in range(1, kmax + 1):
        if k % 2 == parity:
            s.update(range(2 ** (k - 1) + 1, 2 ** k + 1))
    return s


def ap_free_order(vals):
    """classic 3-AP-free arrangement of an arbitrary finite set: odds-first
    recursion on the *ranks* (values sorted; pattern by binary reversal)."""
    vals = sorted(vals)
    n = len(vals)

    def pattern(m):
        if m == 1:
            return [0]
        odds = pattern((m + 1) // 2)
        evens = pattern(m // 2)
        return [2 * i for i in odds] + [2 * i + 1 for i in evens]

    # pattern on 0..n-1 avoiding rank-3-APs is NOT enough for value-3-APs
    # unless vals is an interval; for intervals it is exact.
    idx = pattern(n)
    return [vals[i] for i in idx]


if __name__ == "__main__":
    # Baseline: alternating dyadic, no delays, blocks in order with the
    # odds-evens arrangement — expect doom/violation (we proved UNSAT).
    kmax = 8
    blocks = dyadic_blocks(kmax)
    for parity in (0, 1):
        tset = team_sets(kmax, parity)
        seq = []
        if parity == 0:
            seq.append(1)
        for k in range(1, kmax + 1):
            if k % 2 == parity:
                seq += ap_free_order(blocks[k])
        st, info = check_team(seq, tset)
        print(f"baseline parity={parity}: {st} {info}")
