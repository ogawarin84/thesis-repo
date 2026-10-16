# -*- coding: utf-8 -*-
"""按权威数据源重算附录表B.2：R2/R3/R4/R5=0730(我最爱rin 40vars), R1/R6=0727"""
import numpy as np

f0727 = r'C:\Users\Home\Desktop\理论生成汇总\0727理论生成汇总\十批次统一汇总表_完整40变量_最终版.md'
f0730 = r'C:\Users\Home\Desktop\理论生成汇总\0730理论生成汇总\新10批次R2-R5实验数据.md'

def fl(x):
    if x is None: return None
    x = str(x).replace('**','').replace('*','').strip()
    if x in ('N/A','—','∞','','-'): return None
    try: return float(x)
    except: return None

# 0727 R1/R6
sec = None
d727 = {}
def add(r, mt, v):
    if v is not None:
        d727.setdefault((r,mt), []).append(v)
for ln in open(f0727, encoding='utf-8'):
    s = ln.strip()
    if s.startswith('## '):
        if '核心变量' in s: sec='core'
        elif '动力学' in s: sec='dyn'
        elif '本征谱' in s: sec='spec'
        else: sec=None
        continue
    if not s.startswith('|') or sec is None: continue
    parts = [c.strip() for c in s.strip('|').split('|')]
    if len(parts)<3 or not parts[0].startswith('batch'): continue
    r = parts[1]
    if r not in ('R1','R6'): continue
    vv = parts[2:]
    if sec=='core':
        add(r,'offset',fl(vv[0])); add(r,'confusion',fl(vv[1])); add(r,'temp',fl(vv[2])); add(r,'defense',fl(vv[3]))
        add(r,'cos_rin',fl(vv[5])); add(r,'cos_gen',fl(vv[6])); add(r,'gravity',fl(vv[7]))
    elif sec=='dyn':
        add(r,'beta',fl(vv[0])); add(r,'kappa',fl(vv[2])); add(r,'R_root',fl(vv[3])); add(r,'P_basin',fl(vv[4]))
    elif sec=='spec':
        add(r,'geo',fl(vv[3]))

# 0730 R2-R5 (v01..v40 skipping v06/v15-17)
V73 = ['offset','confusion','temp','defense','color','beta','eta','kappa','R_root','P_basin','epsilon','chars','rin_ratio','exclaim','ellipsis','w1','w2','w3','w4','w5','w6','w7','g11','g22','g33','g44','g55','g66','g77','eigen','stability','rank','geo','cos_rin','cos_gen','gravity']
d730 = {}
for ln in open(f0730, encoding='utf-8'):
    if not ln.startswith('|'): continue
    parts = [c.strip() for c in ln.strip().strip('|').split('|')]
    if len(parts)<3 or parts[1] not in ('R2','R3','R4','R5'): continue
    r = parts[1]; vv = parts[2:]
    for i, nm in enumerate(V73):
        if i < len(vv):
            d730.setdefault((r,nm), []).append(fl(vv[i]))

def m729(r, mt):
    v = [x for x in d727.get((r,mt),[]) if x is not None]
    return float(np.mean(v)) if v else None
def m730(r, mt):
    v = [x for x in d730.get((r,mt),[]) if x is not None]
    return float(np.mean(v)) if v else None

def src(r, mt):
    return m729(r,mt) if r in ('R1','R6') else m730(r,mt)

RS = ['R1','R2','R3','R4','R5','R6']
metrics = ['offset','confusion','temp','defense','beta','kappa','R_root','P_basin','cos_rin','cos_gen','gravity','geo','eigen','stability','rank']
print('=== 重算表B.2（R1/R6=0727, R2-R5=0730 我最爱rin 40vars）===')
print('指标'.ljust(10)+''.join(r.rjust(8) for r in RS))
for mt in metrics:
    line = mt.ljust(10)
    for r in RS:
        v = src(r, mt)
        line += ('%8.3f' % v) if v is not None else '     N/A'
    print(line)

# 论文现值（旧表B.2）—— 2026-08-17 改写前的快照，保留作 before 侧证据，勿更新。
# 活体核对请用 verify_paper_after_update.py。
paper = {
 'offset':[0.698,0.183,0.100,0.640,0.661,0.686],
 'confusion':[0.10,0.654,0.380,0.267,0.22,0.18],
 'temp':[0.65,0.350,0.263,0.730,0.58,0.55],
 'defense':[0.08,0.078,0.030,0.732,0.15,0.12],
 'beta':[0.62,0.183,0.100,0.640,0.55,0.52],
 'kappa':[1.25,1.593,None,4.789,0.58,0.62],
 'R_root':[0.64,0.654,0.381,0.267,0.62,0.58],
 'P_basin':[0.82,0.073,0.058,0.481,0.72,0.75],
 'cos_rin':[0.543,0.381,0.405,0.400,0.599,0.651],
 'cos_gen':[0.453,0.502,0.482,0.493,0.494,0.371],
 'gravity':[None,0.069,0.042,0.256,None,None],
 'geo':[0.35,0.433,0.368,1.622,0.38,0.32],
}
print('\n=== 论文现值 vs 重算（差>0.01 即标出）===')
for mt in metrics:
    diffs = []
    for j, r in enumerate(RS):
        pv = paper.get(mt,[None]*6)[j] if mt in paper else None
        av = src(r, mt)
        if pv is not None and av is not None and abs(pv-av)>0.01:
            diffs.append('%s:论文%.3f→重算%.3f' % (r, pv, av))
    if diffs:
        print('%s: %s' % (mt, ' | '.join(diffs)))
    else:
        print('%s: ✓ 全部吻合' % mt)
