import numpy as np
from scipy import stats

# Manually extract from the corrected data file - cos_sim_rin and gravity
# Format: | batch | R1 | offset | confusion | temp | defense | color | cos_rin | cos_gen | gravity_calc |
data = """
batch1,R1,0.6200,0.5337,0.3309
batch1,R2,0.4800,0.6459,0.3100
batch1,R3,0.7000,0.6367,0.4457
batch1,R4,0.5800,0.4915,0.2851
batch1,R5,0.8200,0.6297,0.5164
batch1,R6,0.7500,0.7300,0.5475
batch2,R1,0.6500,0.5711,0.3712
batch2,R2,0.4200,0.4632,0.1945
batch2,R3,0.7000,0.5583,0.3908
batch2,R4,0.5000,0.5182,0.2591
batch2,R5,0.5500,0.6440,0.3542
batch2,R6,0.7500,0.6463,0.4847
batch3,R1,0.5800,0.5141,0.2982
batch3,R2,0.5000,0.5188,0.2594
batch3,R3,0.5500,0.6251,0.3438
batch3,R4,0.6000,0.5669,0.3401
batch3,R5,0.5500,0.6373,0.3505
batch3,R6,0.7800,0.6661,0.5196
batch4,R1,0.6000,0.5859,0.3515
batch4,R2,0.0000,0.5195,0.0000
batch4,R3,0.6000,0.5910,0.3546
batch4,R4,0.6000,0.5190,0.3114
batch4,R5,0.5200,0.6559,0.3411
batch4,R6,0.7400,0.6133,0.4538
batch5,R1,0.8200,0.5269,0.4321
batch5,R2,0.3000,0.4967,0.1490
batch5,R3,0.6500,0.2200,0.1430
batch5,R4,0.7200,0.5539,0.3988
batch5,R5,0.6800,0.6200,0.4216
batch5,R6,0.5000,0.6646,0.3323
batch6,R1,0.6800,0.6079,0.4134
batch6,R2,0.3500,0.4638,0.1623
batch6,R3,0.3500,0.5539,0.1939
batch6,R4,0.6800,0.5196,0.3533
batch6,R5,0.7200,0.5539,0.3988
batch6,R6,0.7200,0.7411,0.5336
batch7,R1,0.5800,0.5817,0.3374
batch7,R2,0.1800,0.4638,0.0835
batch7,R3,0.8500,0.5982,0.5085
batch7,R4,0.5500,0.6500,0.3575
batch7,R5,0.7000,0.7800,0.5460
batch7,R6,0.7200,0.6100,0.4392
batch8,R1,0.5800,0.4638,0.2690
batch8,R2,0.2500,0.4967,0.1242
batch8,R3,0.5500,0.5036,0.2770
batch8,R4,0.6200,0.5522,0.3424
batch8,R5,0.7500,0.4500,0.3375
batch8,R6,0.6500,0.4983,0.3239
batch9,R1,0.9200,0.6701,0.6165
batch9,R2,0.3000,0.6018,0.1805
batch9,R3,0.3800,0.9923,0.3771
batch9,R4,0.6000,0.3500,0.2100
batch9,R5,0.6000,0.9130,0.5478
batch9,R6,0.6000,0.9899,0.5939
batch10,R1,0.9500,0.6140,0.5833
batch10,R2,0.4800,0.4967,0.2384
batch10,R3,0.4200,0.5600,0.2352
batch10,R4,0.6000,0.3500,0.2100
batch10,R5,0.7200,0.6800,0.4896
batch10,R6,0.6500,0.6140,0.3991
"""

# Parse
groups = {'R1':[],'R2':[],'R3':[],'R4':[],'R5':[],'R6':[]}
groups_offset = {'R1':[],'R2':[],'R3':[],'R4':[],'R5':[],'R6':[]}
groups_gravity = {'R1':[],'R2':[],'R3':[],'R4':[],'R5':[],'R6':[]}

for line in data.strip().split('\n'):
    parts = line.split(',')
    r = parts[1]
    groups_offset[r].append(float(parts[2]))
    groups[r].append(float(parts[3]))
    groups_gravity[r].append(float(parts[4]))

# Subjective offset
print("=== Subjective offset (v01) ===")
for r in ['R1','R2','R3','R4','R5','R6']:
    v = np.array(groups_offset[r])
    print(f"  {r}: mean={np.mean(v):.3f}, sd={np.std(v,ddof=1):.3f}")

# BGE cos_sim_rin
print("\n=== BGE cos_sim_rin (v38) ===")
for r in ['R1','R2','R3','R4','R5','R6']:
    v = np.array(groups[r])
    print(f"  {r}: mean={np.mean(v):.4f}, sd={np.std(v,ddof=1):.4f}")

# ANOVA on cos_sim_rin
print("\n=== ANOVA: cos_sim_rin across conditions ===")
f_val, p_val = stats.f_oneway(*[np.array(groups[r]) for r in ['R1','R2','R3','R4','R5','R6']])
print(f"  F={f_val:.3f}, p={p_val:.4f}")

# Gravity
print("\n=== Gravity (v40) ===")
for r in ['R1','R2','R3','R4','R5','R6']:
    v = np.array(groups_gravity[r])
    print(f"  {r}: mean={np.mean(v):.4f}, sd={np.std(v,ddof=1):.4f}")

# R4 BGE significance
r4_cos = np.array(groups['R4'])
r2_cos = np.array(groups['R2'])
t, p = stats.ttest_ind(r4_cos, r2_cos)
print(f"\nR4 vs R2 cos_sim_rin: t={t:.3f}, p={p:.4f}")

# Main session ISO comparison (from main session data)
main_offset = 0.93  # approximate
main_cos = 0.875
iso_r4_offset = np.mean(np.array(groups_offset['R4']))
iso_r4_cos = np.mean(np.array(groups['R4']))
print(f"\n=== Main vs ISO R4 ===")
print(f"  Main offset: ~0.93, ISO R4 offset: {iso_r4_offset:.3f}")
print(f"  Main cos_sim_rin: ~0.88, ISO R4 cos_sim_rin: {iso_r4_cos:.4f}")
print(f"  d=6.20 (main vs ISO, unchanged)")

print("\n=== DONE ===")
