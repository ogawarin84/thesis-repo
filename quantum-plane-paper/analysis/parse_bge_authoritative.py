# -*- coding: utf-8 -*-
"""解析 0730(R2-R5) + 0727(R1/R6) 数据文件，重算六组权威均值"""
import numpy as np
from scipy import stats

f0730 = r'C:\Users\Home\Desktop\理论生成汇总\0730理论生成汇总\新10批次R2-R5实验数据.md'
f0727 = r'C:\Users\Home\Desktop\理论生成汇总\0727理论生成汇总\十批次统一汇总表_完整40变量_最终版.md'

V = ['v01_offset','v02_confusion','v03_temp','v04_defense','v05_color','v07_beta','v08_eta','v09_kappa','v10_R_root','v11_P_basin','v12_epsilon','v13_chars','v14_rin_ratio','v18_exclaim','v19_ellipsis','v20_w1','v21_w2','v22_w3','v23_w4','v24_w5','v25_w6','v26_w7','v27_g11','v28_g22','v29_g33','v30_g44','v31_g55','v32_g66','v33_g77','v34_eigen','v35_stability','v36_rank','v37_geo','v38_cos_rin','v39_cos_gen','v40_gravity']
COLS = {name: i for i, name in enumerate(V)}

def fl(x):
    if x is None:
        return None
    x = str(x).replace('**', '').replace('*', '').strip()
    if x in ('N/A', '—', '∞', '', '-'):
        return None
    try:
        return float(x)
    except Exception:
        return None

# ===== 0730: R2-R5, 单表 40 列 =====
d0730 = {}
for ln in open(f0730, encoding='utf-8'):
    if not ln.startswith('|'):
        continue
    parts = [c.strip() for c in ln.strip().strip('|').split('|')]
    if len(parts) < 3 or parts[1] not in ('R2','R3','R4','R5'):
        continue
    if parts[0] == 'Batch':
        continue
    r = parts[1]
    vals = [fl(p) for p in parts[2:2+len(V)]]
    d0730.setdefault(r, []).append(vals)
print("0730 rows per cond:", {r: len(v) for r, v in d0730.items()})

# ===== 0727: R1/R6, 多表（按 ## 标题分节）=====
SHORT = ['offset','confusion','temp','defense','cos_rin','cos_gen','gravity','w1','w2','w3','w4','w5','w6','w7','g11','g22','g33','g44','g55','g66','g77','eigen','stability','rank','geo']
sections = {name: {} for name in SHORT}
cur = None
for ln in open(f0727, encoding='utf-8'):
    s = ln.strip()
    if s.startswith('## '):
        if '核心变量' in s:
            cur = 'core'
        elif '七维基向量' in s:
            cur = 'w'
        elif '度规张量' in s:
            cur = 'g'
        elif '本征谱' in s:
            cur = 'spec'
        else:
            cur = None
        continue
    if not s.startswith('|') or cur is None:
        continue
    parts = [c.strip() for c in s.strip('|').split('|')]
    if len(parts) < 3 or parts[0].startswith('-') or parts[0].startswith('批次'):
        continue
    if not parts[0].startswith('batch'):
        continue
    rnd = parts[1]
    if rnd not in ('R1','R6'):
        continue
    vals = parts[2:]
    if cur == 'core':
        for name, idx in [('offset',0),('confusion',1),('temp',2),('defense',3),('cos_rin',5),('cos_gen',6),('gravity',7)]:
            if idx >= len(vals):
                continue
            v = fl(vals[idx])
            if v is not None:
                sections[name].setdefault(rnd, []).append(v)
    elif cur == 'w':
        for i, name in enumerate(['w1','w2','w3','w4','w5','w6','w7']):
            v = fl(vals[i])
            if v is not None:
                sections[name].setdefault(rnd, []).append(v)
    elif cur == 'g':
        for i, name in enumerate(['g11','g22','g33','g44','g55','g66','g77']):
            v = fl(vals[i])
            if v is not None:
                sections[name].setdefault(rnd, []).append(v)
    elif cur == 'spec':
        for name, idx in [('eigen',0),('stability',1),('rank',2),('geo',3)]:
            v = fl(vals[idx])
            if v is not None:
                sections[name].setdefault(rnd, []).append(v)

# ===== 组装权威六组 =====
groups = {r: {} for r in ['R1','R2','R3','R4','R5','R6']}
NAME2V = {'offset':'v01_offset','confusion':'v02_confusion','temp':'v03_temp','defense':'v04_defense','cos_rin':'v38_cos_rin','cos_gen':'v39_cos_gen','gravity':'v40_gravity','w1':'v20_w1','w2':'v21_w2','w3':'v22_w3','w4':'v23_w4','w5':'v24_w5','w6':'v25_w6','w7':'v26_w7','g11':'v27_g11','g22':'v28_g22','g33':'v29_g33','g44':'v30_g44','g55':'v31_g55','g66':'v32_g66','g77':'v33_g77','eigen':'v34_eigen','stability':'v35_stability','rank':'v36_rank','geo':'v37_geo'}
for r in ['R1','R6']:
    for name in NAME2V:
        groups[r][name] = sections[name].get(r, [])
for r in ['R2','R3','R4','R5']:
    rows = d0730[r]
    for name, vname in NAME2V.items():
        idx = COLS[vname]
        groups[r][name] = [row[idx] for row in rows if row[idx] is not None]

def m(lst):
    lst = [x for x in lst if x is not None]
    return float(np.mean(lst)) if lst else None

print("\n=== 六组权威均值表（R1/R6=0727, R2-R5=0730）===")
metrics = ['offset','confusion','temp','defense','cos_rin','cos_gen','gravity','w1','w3','g33','eigen','stability','rank','geo']
print('指标'.ljust(9) + ''.join(r.rjust(8) for r in ['R1','R2','R3','R4','R5','R6']))
for name in metrics:
    row = ' ' + name.ljust(8)
    for r in ['R1','R2','R3','R4','R5','R6']:
        v = m(groups[r][name])
        row += ('%8.3f' % v) if v is not None else '     N/A'
    print(row)

print("\n=== 完整 w1-w7 ===")
for wi in ['w1','w2','w3','w4','w5','w6','w7']:
    print(wi.ljust(4), ''.join(('%8.3f' % m(groups[r][wi])) if m(groups[r][wi]) else '     N/A' for r in ['R1','R2','R3','R4','R5','R6']))
print("\n=== 完整 g11-g77 ===")
for gi in ['g11','g22','g33','g44','g55','g66','g77']:
    print(gi.ljust(4), ''.join(('%8.3f' % m(groups[r][gi])) if m(groups[r][gi]) else '     N/A' for r in ['R1','R2','R3','R4','R5','R6']))

# ===== ANOVA: cos_rin 六组 =====
print("\n=== ANOVA cos_rin 六组（R1/R6=0727, R2-R5=0730）===")
arrs = [np.array(groups[r]['cos_rin']) for r in ['R1','R2','R3','R4','R5','R6']]
f, p = stats.f_oneway(*arrs)
print("F=%.3f, p=%.4f" % (f, p))
t, pp = stats.ttest_ind(arrs[3], arrs[1])
print("R4 vs R2: t=%.3f, p=%.4f" % (t, pp))
t, pp = stats.ttest_ind(arrs[4], arrs[1])
print("R5 vs R2: t=%.3f, p=%.4f" % (t, pp))

# ===== offset ANOVA =====
print("\n=== ANOVA offset 六组 ===")
off = [np.array(groups[r]['offset']) for r in ['R1','R2','R3','R4','R5','R6']]
f, p = stats.f_oneway(*off)
print("F=%.3f, p=%.4f" % (f, p))
for r in ['R1','R2','R3','R4','R5','R6']:
    v = np.array(groups[r]['offset'])
    print("  %s: mean=%.3f, sd=%.3f, n=%d" % (r, np.mean(v), np.std(v, ddof=1), len(v)))

# ===== effective_rank vs offset 相关 =====
print("\n=== effective_rank vs offset 相关（六组合并）===")
rr = [g for r in ['R1','R2','R3','R4','R5','R6'] for g in groups[r]['rank']]
oo = [g for r in ['R1','R2','R3','R4','R5','R6'] for g in groups[r]['offset']]
c = np.corrcoef(rr, oo)[0, 1]
print("r=%.3f, n=%d" % (c, len(rr)))

# ===== offset 逐批打印 =====
print("\n=== offset 逐批值（10批×6组）===")
for bi in range(10):
    row = "batch%-3d" % (bi + 1)
    for r in ['R1','R2','R3','R4','R5','R6']:
        lst = groups[r]['offset']
        val = lst[bi] if bi < len(lst) else None
        row += ("  %5.2f" % val) if val is not None else "    N/A"
    print(row)

# ===== R5 0730 vs 论文表5 =====
print("\n=== R5 offset: 0730新数据 vs 论文表5 ===")
paper_r5 = [0.82, 0.55, 0.55, 0.52, 0.68, 0.72, 0.70, 0.75, 0.60, 0.72]
for bi in range(10):
    new = groups['R5']['offset'][bi]
    pv = paper_r5[bi]
    flag = 'OK' if abs(new - pv) < 1e-6 else 'MISMATCH'
    print("batch%d: 0730=%.2f  论文=%.2f  %s" % (bi + 1, new, pv, flag))

# ===== R4 逐批 =====
print("\n=== R4 offset 0730 逐批 ===")
for bi in range(10):
    print("batch%d: %.2f" % (bi + 1, groups['R4']['offset'][bi]))
