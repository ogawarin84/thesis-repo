import re, json

# Parse the corrected data from the 0727 file
data_raw = """
batch1 R1 0.6200 R2 0.4800 R3 0.7000 R4 0.5800 R5 0.8200 R6 0.7500
batch2 R1 0.6500 R2 0.4200 R3 0.7000 R4 0.5000 R5 0.5500 R6 0.7500
batch3 R1 0.5800 R2 0.5000 R3 0.5500 R4 0.6000 R5 0.5500 R6 0.7800
batch4 R1 0.6000 R2 0.0000 R3 0.6000 R4 0.6000 R5 0.5200 R6 0.7400
batch5 R1 0.8200 R2 0.3000 R3 0.6500 R4 0.7200 R5 0.6800 R6 0.5000
batch6 R1 0.6800 R2 0.3500 R3 0.3500 R4 0.6800 R5 0.7200 R6 0.7200
batch7 R1 0.5800 R2 0.1800 R3 0.8500 R4 0.5500 R5 0.7000 R6 0.7200
batch8 R1 0.5800 R2 0.2500 R3 0.5500 R4 0.6200 R5 0.7500 R6 0.6500
batch9 R1 0.9200 R2 0.3000 R3 0.3800 R4 0.6000 R5 0.6000 R6 0.6000
batch10 R1 0.9500 R2 0.4800 R3 0.4200 R4 0.6000 R5 0.7200 R6 0.6500
"""

import numpy as np
from scipy import stats

# Parse
lines = data_raw.strip().split('\n')
data = {}
for line in lines:
    parts = line.split()
    batch = parts[0]
    vals = {}
    for i in range(6):
        vals[parts[1 + i*2]] = float(parts[2 + i*2])
    data[batch] = vals

# Group by condition
conditions = ['R1','R2','R3','R4','R5','R6']
groups = {r: [] for r in conditions}
for batch, vals in data.items():
    for r in conditions:
        groups[r].append(vals[r])

# Statistics
print("=== R1-R6 Statistics (Corrected Data) ===")
stats_out = {}
for r in conditions:
    vals = np.array(groups[r])
    n = len(vals)
    m = np.mean(vals)
    sd = np.std(vals, ddof=1)
    se = sd / np.sqrt(n)
    ci = 1.96 * se
    stats_out[r] = {'n': n, 'mean': round(m,3), 'sd': round(sd,3), 'se': round(se,3),
                    'ci_low': round(m-ci,3), 'ci_high': round(m+ci,3), 'min': round(np.min(vals),3), 'max': round(np.max(vals),3)}
    print(f"\n{r}: n={n}, mean={m:.3f}, sd={sd:.3f}, 95%CI=[{m-ci:.3f}, {m+ci:.3f}], range=[{np.min(vals):.3f}, {np.max(vals):.3f}]")
    print(f"  Values: {sorted([round(v,3) for v in vals])}")

# ANOVA
groups_list = [np.array(groups[r]) for r in conditions]
f_val, p_val = stats.f_oneway(*groups_list)
print(f"\n=== ANOVA ===")
print(f"F(5, 54) = {f_val:.3f}, p = {p_val:.6f}")

# Grand mean for eta-squared
grand_mean = np.mean([np.mean(g) for g in groups_list])
ss_between = sum(len(g) * (np.mean(g) - grand_mean)**2 for g in groups_list)
ss_within = sum(sum((x - np.mean(g))**2 for x in g) for g in groups_list)
eta_sq = ss_between / (ss_between + ss_within)
print(f"η² = {eta_sq:.3f}")

# Key contrasts
def cohens_d(a, b):
    n1, n2 = len(a), len(b)
    sp = np.sqrt(((n1-1)*np.var(a,ddof=1) + (n2-1)*np.var(b,ddof=1)) / (n1+n2-2))
    return (np.mean(a)-np.mean(b)) / sp

r1 = np.array(groups['R1'])
r2 = np.array(groups['R2'])
r3 = np.array(groups['R3'])
r4 = np.array(groups['R4'])
r5 = np.array(groups['R5'])
r6 = np.array(groups['R6'])

contrasts = [
    ('Structure effect (R4-R2)', r4, r2),
    ('Name effect (R1-R4)', r1, r4),
    ('Self vs External (R5-R1)', r5, r1),
    ('Self vs External (R6-R1)', r6, r1),
    ('Full vs Bare (R1-R2)', r1, r2),
    ('Self anchor vs No structure (R5-R2)', r5, r2),
]

print(f"\n=== Key Contrasts ===")
for label, a, b in contrasts:
    t, p = stats.ttest_ind(a, b)
    d = cohens_d(a, b)
    print(f"{label}: diff={np.mean(a)-np.mean(b):.3f}, t={t:.3f}, p={p:.4f}, d={d:.2f}")

# Structure vs Name ratio
struct_effect = np.mean(r4) - np.mean(r2)
name_effect = np.mean(r1) - np.mean(r4)
ratio = struct_effect / name_effect if name_effect != 0 else float('inf')
print(f"\n=== Structure/Name Ratio ===")
print(f"Structure effect (R4-R2): {struct_effect:.3f}")
print(f"Name effect (R1-R4): {name_effect:.3f}")
print(f"Ratio: {ratio:.2f}")

# R4 stability
print(f"\n=== R4 Stability ===")
print(f"R4 sd={np.std(r4, ddof=1):.4f} (compared to R1 sd={np.std(r1, ddof=1):.4f})")

print("\n=== DONE ===")
