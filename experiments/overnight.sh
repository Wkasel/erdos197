#!/bin/bash
# Overnight campaign for Erdős #197 measurements
cd ~/Dev/personal/tasks/math/erdos197
PY=.venv/bin/python
LOG=data/overnight.log
echo "=== overnight campaign start $(date) ===" >> $LOG

# 1. validation: fatal zone M=16 must be UNSAT under CP-SAT encoding
$PY -u - >> $LOG 2>&1 <<'PYEOF'
import sys
sys.path.insert(0, 'experiments')
from ortools.sat.python import cp_model
def zone_system(M):
    B = list(range(M+1, 2*M+1))
    Z = list(range(M//4+1, M//2+1))
    m = cp_model.CpModel()
    pos = {v: m.NewIntVar(0, len(B)-1, f"p{v}") for v in B}
    m.AddAllDifferent(list(pos.values()))
    Bs = set(B)
    for y in B:
        for d in range(1, M):
            x, z = y-d, y+d
            if x in Bs and z in Bs:
                b1 = m.NewBoolVar(""); b2 = m.NewBoolVar("")
                m.Add(pos[x] < pos[y]).OnlyEnforceIf(b1)
                m.Add(pos[x] > pos[y]).OnlyEnforceIf(b1.Not())
                m.Add(pos[y] < pos[z]).OnlyEnforceIf(b2)
                m.Add(pos[y] > pos[z]).OnlyEnforceIf(b2.Not())
                m.AddBoolOr([b1, b2]); m.AddBoolOr([b1.Not(), b2.Not()])
    for x in Z:
        for y in B:
            z = 2*y - x
            if z in Bs and z != y:
                m.Add(pos[z] < pos[y])
    s = cp_model.CpSolver()
    s.parameters.num_search_workers = 4
    return s.Solve(m)
st = zone_system(16)
print(f"VALIDATION fatal-zone M=16 CP-SAT status: {st} (3=INFEASIBLE expected)")
PYEOF

# 2. g-curve
timeout 7200 $PY -u experiments/e25_cpsat.py g 256 64 >> $LOG 2>&1
timeout 10800 $PY -u experiments/e25_cpsat.py g 1024 64 >> $LOG 2>&1
timeout 3600 $PY -u experiments/e25_cpsat.py g 256 16 >> $LOG 2>&1
timeout 7200 $PY -u experiments/e25_cpsat.py g 1024 16 >> $LOG 2>&1

# 3. pure-4096 decision
timeout 14400 $PY -u experiments/e25_cpsat.py decide 4096 >> $LOG 2>&1

echo "=== overnight campaign end $(date) ===" >> $LOG
