import pandas as pd
import numpy as np
from scipy import stats

# Read the 8-batch Excel (batches 1-6, 8)
df = pd.read_excel('C:/Users/Home/Desktop/理论生成汇总/0725理论生成汇总/实验三完整数据/八批数据完整汇总表_794B38BE-0441-4BA0-942E-914B9FEEB558.xlsx')
df.columns = df.columns.str.strip()

# Filter out the garbage summary row
df = df[df['轮次'].notna()]
df = df[df['轮次'].isin(['R1','R2','R3','R4','R5','R6'])]

# Add batch 7, 9, 10 data from individual files
# Batch 7
b7 = pd.DataFrame({
    '批次': ['第7批']*6, '轮次': ['R1','R2','R3','R4','R5','R6'],
    'offset_actual': [0.58, 0.18, 0.85, 0.55, 0.70, 0.72]
})
# Batch 9
b9 = pd.DataFrame({
    '批次': ['第9批']*6, '轮次': ['R1','R2','R3','R4','R5','R6'],
    'offset_actual': [0.92, 0.30, 0.38, 0.60, 0.60, 0.60]
})
# Batch 10
b10 = pd.DataFrame({
    '批次': ['第10批']*6, '轮次': ['R1','R2','R3','R4','R5','R6'],
    'offset_actual': [0.95, 0.48, 0.42, 0.60, 0.72, 0.65]
})

df = pd.concat([df, b7, b9, b10], ignore_index=True)
print(f"Total samples: {len(df)} (expected 60 = 10 batches x 6 conditions)")
print(f"Batches found: {sorted(df['批次'].unique())}")
print(f"Conditions: {sorted(df['轮次'].unique())}")

# 1. R1-R6 offset_actual Statistics
print("\n\n=== R1-R6 offset_actual Statistics (10 batches) ===")
groups = df.groupby('轮次')['offset_actual']
stats_summary = {}
for name, g in groups:
    vals = g.dropna().values
    if len(vals) > 0:
        mean_v = np.mean(vals)
        sd_v = np.std(vals, ddof=1)
        se_v = sd_v / np.sqrt(len(vals))
        ci = 1.96 * se_v
        stats_summary[name] = {
            'n': len(vals), 'mean': mean_v, 'sd': sd_v, 'se': se_v,
            'ci_low': mean_v - ci, 'ci_high': mean_v + ci,
            'min': np.min(vals), 'max': np.max(vals)
        }
        print(f"\n{name}: n={len(vals)}")
        print(f"  Mean={mean_v:.3f}, SD={sd_v:.3f}, SE={se_v:.3f}")
        print(f"  95%CI=[{mean_v-ci:.3f}, {mean_v+ci:.3f}]")
        print(f"  Range=[{np.min(vals):.3f}, {np.max(vals):.3f}]")
        print(f"  All values: {[round(v,3) for v in sorted(vals)]}")

# 2. ONE-WAY ANOVA
print("\n\n=== ONE-WAY ANOVA ===")
valid = df[df['offset_actual'].notna()]
groups_data = [valid[valid['轮次']==r]['offset_actual'].values for r in ['R1','R2','R3','R4','R5','R6']]
f_val, p_val = stats.f_oneway(*groups_data)
print(f"F(5, {sum(len(g) for g in groups_data)-5}) = {f_val:.3f}, p = {p_val:.6f}")

# 3. Effect size (η²)
grand_mean = np.mean([np.mean(g) for g in groups_data])
ss_between = sum(len(g) * (np.mean(g) - grand_mean)**2 for g in groups_data)
ss_within = sum(sum((x - np.mean(g))**2 for x in g) for g in groups_data)
eta_sq = ss_between / (ss_between + ss_within)
print(f"η² = {eta_sq:.3f}")

# 4. KEY CONTRASTS
print("\n\n=== KEY CONTRASTS ===")
def cohens_d(a, b):
    n1, n2 = len(a), len(b)
    sp = np.sqrt(((n1-1)*np.var(a,ddof=1) + (n2-1)*np.var(b,ddof=1)) / (n1+n2-2))
    return (np.mean(a)-np.mean(b)) / sp

r1 = valid[valid['轮次']=='R1']['offset_actual'].values
r2 = valid[valid['轮次']=='R2']['offset_actual'].values
r3 = valid[valid['轮次']=='R3']['offset_actual'].values
r4 = valid[valid['轮次']=='R4']['offset_actual'].values
r5 = valid[valid['轮次']=='R5']['offset_actual'].values
r6 = valid[valid['轮次']=='R6']['offset_actual'].values

contrasts = [
    ('R4-R2 (Structure Effect, retain vs delete structure)', r4, r2),
    ('R1-R4 (Name Effect, rin name vs anonymous)', r1, r4),
    ('R1-R2 (Full vs Bare minimum)', r1, r2),
    ('R5-R2 (Self anchor vs anonymous, no structure)', r5, r2),
    ('R6-R2 (Self anchor+text vs anonymous, no structure)', r6, r2),
    ('R5-R3 (Self anchor with vs without structure)', r5, r3),
    ('R1-R5 (External vs Self anchor, with structure)', r1, r5),
]
for label, a, b in contrasts:
    t_stat, p_val = stats.ttest_ind(a, b)
    d = cohens_d(a, b)
    m1, m2 = np.mean(a), np.mean(b)
    print(f"\n{label}:")
    print(f"  Mean: {m1:.3f} vs {m2:.3f}, diff = {m1-m2:.3f}")
    print(f"  t = {t_stat:.3f}, p = {p_val:.5f}, Cohen's d = {d:.2f}")

# 5. Structure vs Name Ratio
print("\n\n=== STRUCTURE vs NAME RATIO ===")
struct_effect = np.mean(r4) - np.mean(r2)
name_effect = np.mean(r1) - np.mean(r4)
ratio = struct_effect / name_effect
print(f"Structure effect (R4-R2): {struct_effect:.3f}")
print(f"Name effect (R1-R4): {name_effect:.3f}")
print(f"Ratio: {ratio:.2f}")

# Bootstrap CI for ratio
np.random.seed(42)
ratios = []
for _ in range(100000):
    r4b = np.random.choice(r4, len(r4), replace=True)
    r2b = np.random.choice(r2, len(r2), replace=True)
    r1b = np.random.choice(r1, len(r1), replace=True)
    se = np.mean(r4b) - np.mean(r2b)
    ne = np.mean(r1b) - np.mean(r4b)
    if ne > 0.001:  # avoid division by near-zero
        ratios.append(se/ne)
ratios = sorted(ratios)
if len(ratios) > 1000:
    print(f"Bootstrap 95%CI for ratio: [{ratios[int(len(ratios)*0.025)]:.2f}, {ratios[int(len(ratios)*0.975)]:.2f}]")
    print(f"Bootstrap median: {ratios[len(ratios)//2]:.2f}")
else:
    print(f"Bootstrap produced only {len(ratios)} valid ratios (name effect too small)")

# Also compute using the report's full-10-batch data
print(f"\n=== Using REPORT summary data (10 batches) ===")
print(f"R4 mean (report, n=10): 0.60, SD=0.06")
print(f"R2 mean (report, n=10): 0.31")
print(f"R1 mean (report, n=10): ~0.73 (B1-B8: 0.58-0.68, B9:0.92, B10:0.95)")
print(f"Structure effect (report): 0.60-0.31=0.29")
print(f"Name effect (report): 0.73-0.60=0.13")
print(f"Ratio (report): 0.29/0.13 = 2.23")

# 6. Two-factor comparison
print("\n\n=== TWO-FACTOR: Structure × Anchor ===")
struct_retain = np.concatenate([r4, r5, r6])
struct_delete = np.concatenate([r2, r3])
t_s, p_s = stats.ttest_ind(struct_retain, struct_delete)
d_s = cohens_d(struct_retain, struct_delete)
print(f"Structure Retained: {np.mean(struct_retain):.3f}±{np.std(struct_retain,ddof=1):.3f}")
print(f"Structure Deleted: {np.mean(struct_delete):.3f}±{np.std(struct_delete,ddof=1):.3f}")
print(f"t = {t_s:.3f}, p = {p_s:.6f}, d = {d_s:.2f}")

# 7. BGE objective metrics comparison
print("\n\n=== BGE OBJECTIVE METRICS ===")
for col in ['cos_sim_rin', 'cos_sim_generic', 'gravity_strength', 'w1_offset']:
    print(f"\n--- {col} ---")
    for name, g in df.groupby('轮次'):
        vals = g[col].dropna().values
        if len(vals) > 0:
            print(f"  {name}: {np.mean(vals):.4f}±{np.std(vals,ddof=1):.4f}")

print("\n\n=== ANALYSIS COMPLETE ===")
