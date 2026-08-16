# -*- coding: utf-8 -*-
"""表6权威核验 v3：R2/R3/R4=我最爱rin(修复版，R3剔除B1/B5/B8)，R1/R5/R6=0727最终版
输出：论文表6现值 vs 权威重算值对比"""
import numpy as np

F0730 = r'C:\Users\Home\Desktop\理论生成汇总\0730理论生成汇总\我最爱rin_40vars_table.md'
F0727 = r'C:\Users\Home\Desktop\理论生成汇总\0727理论生成汇总\十批次统一汇总表_完整40变量_最终版.md'

def fl(x):
    if x is None: return None
    x = str(x).strip().replace('**','').replace('*','')
    if x in ('N/A','—','∞','', '-'): return None
    try: return float(x)
    except: return None

# ==================== 0730: 我最爱rin (R2/R3/R4) ====================
# 列: 0Batch 1Cond 2offset 3conf 4temp 5def 6color 7beta 8eta 9kappa 10Rroot 11Pbasin 12epsilon
#     13chars 14rin 15affect 16uncert 17defense 18excl 19ellip 20w1..26w7 27g11..33g77 34eigen 35stab 36rank 37geo 38cosrin 39cosgen 40gravity
rin = {r: {nm: [] for nm in ['offset','conf','temp','def','beta','kappa','Rroot','Pbasin','geo','cosrin','cosgen','gravity']} for r in ['R2','R3','R4','R5']}
IDX = {'offset':2,'conf':3,'temp':4,'def':5,'beta':7,'kappa':9,'Rroot':10,'Pbasin':11,'geo':37,'cosrin':38,'cosgen':39,'gravity':40}
for ln in open(F0730, encoding='utf-8'):
    if not ln.startswith('|'): continue
    p = [c.strip() for c in ln.strip().strip('|').split('|')]
    if len(p) < 41 or p[1] not in ('R2','R3','R4','R5'): continue
    if p[0] == 'Batch': continue
    r = p[1]
    for nm, idx in IDX.items():
        v = fl(p[idx])
        if v is not None: rin[r][nm].append(v)

def m730(r, nm, exclude3=False):
    lst = rin[r][nm]
    if exclude3:  # R3剔除 B1/B5/B8 (0,4,7)
        lst = [v for i, v in enumerate(lst) if i not in (0,4,7)]
    return float(np.mean(lst)) if lst else None

# ==================== 0727: R1/R5/R6 ====================
secs = {}
cur = None
for ln in open(F0727, encoding='utf-8'):
    s = ln.strip()
    if s.startswith('## '):
        cur = ('core' if '核心变量' in s else 'dyn' if '动力学' in s else 'spec' if '本征谱' in s else None)
        continue
    if not s.startswith('|') or cur is None: continue
    p = [c.strip().replace('**','') for c in s.strip('|').split('|')]
    if len(p) < 3 or not p[0].startswith('batch') or p[1] not in ('R1','R5','R6'): continue
    secs.setdefault((cur,p[1]), []).append(p[2:])

def m727(sec, r, idx):
    vals = [fl(v[idx]) for v in secs.get((sec,r),[]) if idx < len(v)]
    vals = [x for x in vals if x is not None]
    return float(np.mean(vals)) if vals else None

# ==================== 权威组装 ====================
# core: offset0 conf1 temp2 def3 cosrin5 cosgen6 gravity7
# dyn: beta0 kappa2 Rroot3 Pbasin4
# spec: geo3
def auth(metric, r):
    if r in ('R1','R5','R6'):
        c = {'offset':0,'conf':1,'temp':2,'def':3,'cosrin':5,'cosgen':6,'gravity':7}[metric] if metric in ('offset','conf','temp','def','cosrin','cosgen','gravity') else None
        d = {'beta':0,'kappa':2,'Rroot':3,'Pbasin':4}.get(metric)
        if metric == 'geo': return m727('spec', r, 3)
        if c is not None: return m727('core', r, c)
        if d is not None: return m727('dyn', r, d)
        return None
    else:
        excl = (r == 'R3')
        return m730(r, metric, exclude3=excl)

# ==================== 论文表6现值 ====================
P = {
 'offset':  [0.698, 0.183, 0.100, 0.640, 0.661, 0.686],
 'conf':    [0.10, 0.654, 0.380, 0.267, 0.22, 0.18],
 'temp':    [0.65, 0.350, 0.263, 0.730, 0.58, 0.55],
 'def':     [0.08, 0.078, 0.030, 0.732, 0.15, 0.12],
 'beta':    [0.62, 0.183, 0.100, 0.640, 0.55, 0.52],
 'kappa':   [1.25, 1.593, None, 4.789, 0.58, 0.62],
 'Rroot':   [0.64, 0.654, 0.381, 0.267, 0.62, 0.58],
 'Pbasin':  [0.82, 0.073, 0.058, 0.481, 0.72, 0.75],
 'cosrin':  [0.543, 0.381, 0.405, 0.400, 0.599, 0.651],
 'cosgen':  [0.453, 0.502, 0.482, 0.493, 0.494, 0.371],
 'gravity': [None, 0.069, 0.042, 0.256, None, None],
 'geo':     [0.35, 0.433, 0.368, 1.622, 0.38, 0.32],
}
LABEL = {'offset':'offset_actual','conf':'confusion','temp':'temperature','def':'defense','beta':'beta','kappa':'kappa','Rroot':'R_root','Pbasin':'P_basin','cosrin':'cos_sim_rin','cosgen':'cos_sim_generic','gravity':'gravity','geo':'geodesic'}
RS = ['R1','R2','R3','R4','R5','R6']

print('=== 表6 权威重算 vs 论文现值 ===')
print('指标'.ljust(15) + ''.join(('%12s' % r) for r in RS))
print('-' * 15 + ''.join(['-'*12]*6))
for mt in P:
    print(LABEL[mt].ljust(15) + ''.join(('%12.3f' % pv) if pv is not None else ('%12s' % '—') for pv in P[mt]))
    print(''.join([' ']*15) + ''.join(('%12.3f' % av) if av is not None else ('%12s' % '—') for av in (auth(mt,r) for r in RS)))
    # 差异标记
    diffs = []
    for j, r in enumerate(RS):
        pv, av = P[mt][j], auth(mt, r)
        if pv is not None and av is not None and abs(pv-av) > 0.011:
            diffs.append(r)
    print(''.join([' ']*15) + ('  差异: ' + ','.join(diffs)) if diffs else '')
    print()

print('注: 每指标上=论文现值, 下=权威重算(R1/R5/R6=0727, R2/R3/R4=我最爱rin, R3剔除B1/B5/B8)')
