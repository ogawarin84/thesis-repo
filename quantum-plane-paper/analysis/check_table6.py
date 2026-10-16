# -*- coding: utf-8 -*-
"""对照论文附录表B.2：验证 R5=0727 假设下各格是否吻合"""
import io, sys, numpy as np
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

f0727 = r'C:\Users\Home\Desktop\理论生成汇总\0727理论生成汇总\十批次统一汇总表_完整40变量_最终版.md'
f0730 = r'C:\Users\Home\Desktop\理论生成汇总\0730理论生成汇总\新10批次R2-R5实验数据.md'

def fl(x):
    if x is None: return None
    x = str(x).replace('**','').replace('*','').strip()
    if x in ('N/A','—','∞','','-'): return None
    try: return float(x)
    except: return None

# ---------- 0727 全表解析 ----------
sec = None
d727 = {}   # (round, metric) -> [values]   metric in: offset,confusion,temp,defense,beta,kappa,R_root,P_basin,cos_rin,cos_gen,gravity,w1..w7,g11..g77,eigen,stability,rank,geo
def add(r, metric, v):
    if v is not None:
        d727.setdefault((r,metric), []).append(v)

for ln in open(f0727, encoding='utf-8'):
    s = ln.strip()
    if s.startswith('## '):
        if '核心变量' in s: sec='core'
        elif '动力学' in s: sec='dyn'
        elif '代理指标' in s: sec='proxy'
        elif '七维基向量' in s: sec='w'
        elif '度规张量' in s: sec='g'
        elif '本征谱' in s: sec='spec'
        else: sec=None
        continue
    if not s.startswith('|') or sec is None: continue
    parts = [c.strip() for c in s.strip('|').split('|')]
    if len(parts)<3 or not parts[0].startswith('batch'): continue
    rnd = parts[1]
    vals = parts[2:]
    if sec=='core':
        add(rnd,'offset',fl(vals[0])); add(rnd,'confusion',fl(vals[1])); add(rnd,'temp',fl(vals[2])); add(rnd,'defense',fl(vals[3]))
        add(rnd,'cos_rin',fl(vals[5])); add(rnd,'cos_gen',fl(vals[6])); add(rnd,'gravity',fl(vals[7]))
    elif sec=='dyn':
        add(rnd,'beta',fl(vals[0])); add(rnd,'kappa',fl(vals[2])); add(rnd,'R_root',fl(vals[3])); add(rnd,'P_basin',fl(vals[4]))
    elif sec=='spec':
        add(rnd,'eigen',fl(vals[0])); add(rnd,'stability',fl(vals[1])); add(rnd,'rank',fl(vals[2])); add(rnd,'geo',fl(vals[3]))

# ---------- 0730 解析 ----------
V73 = ['offset','confusion','temp','defense','color','beta','eta','kappa','R_root','P_basin','epsilon','chars','rin_ratio','exclaim','ellipsis','w1','w2','w3','w4','w5','w6','w7','g11','g22','g33','g44','g55','g66','g77','eigen','stability','rank','geo','cos_rin','cos_gen','gravity']
d730 = {}
for ln in open(f0730, encoding='utf-8'):
    if not ln.startswith('|'): continue
    parts = [c.strip() for c in ln.strip().strip('|').split('|')]
    if len(parts)<3 or parts[1] not in ('R2','R3','R4','R5'): continue
    rnd = parts[1]
    vv = parts[2:]
    for i, name in enumerate(V73):
        if i < len(vv):
            d730.setdefault((rnd,name), []).append(fl(vv[i]))

def mean729(rnd, metric):
    v = d727.get((rnd,metric), [])
    v = [x for x in v if x is not None]
    return float(np.mean(v)) if v else None
def mean730(rnd, metric):
    v = d730.get((rnd,metric), [])
    v = [x for x in v if x is not None]
    return float(np.mean(v)) if v else None

# 数据源归属: R1/R6=0727, R2/R3=0730, R5=0727, R4=? (两种都给)
def auth(rnd, metric):
    if rnd in ('R1','R5','R6'): return mean729(rnd, metric)
    if rnd in ('R2','R3'): return mean730(rnd, metric)
    if rnd == 'R4':
        return ('0727=%.3f / 0730=%.3f' % (mean729(rnd,metric), mean730(rnd,metric))) if (mean729(rnd,metric) and mean730(rnd,metric)) else ''

print("=== 附录表B.2 对照（假设 R5=0727, R2/R3=0730, R4待定）===")
metrics = ['offset','confusion','temp','defense','beta','kappa','R_root','P_basin','cos_rin','cos_gen','gravity','geo']
# ⚠️ 下面的 paper 是 2026-08-17 改写前的论文快照（before 侧），保留作改动依据，勿更新。
#    本脚本定位 R4 来源，属历史探查。活体核对请用 verify_paper_after_update.py。
paper = {
 'offset':[0.698,0.183,0.100,0.640,0.661,0.686],
 'confusion':[0.10,0.654,0.380,0.267,0.22,0.18],
 'temp':[0.65,0.350,0.263,0.730,0.58,0.55],
 'defense':[0.08,0.078,0.030,0.732,0.15,0.12],
 'beta':[0.62,0.183,0.100,0.640,0.55,0.52],
 'kappa':[1.25,1.593,'—',4.789,0.58,0.62],
 'R_root':[0.64,0.654,0.381,0.267,0.62,0.58],
 'P_basin':[0.82,0.073,0.058,0.481,0.72,0.75],
 'cos_rin':[0.543,0.381,0.405,0.400,0.599,0.651],
 'cos_gen':[0.453,0.502,0.482,0.493,0.494,0.371],
 'gravity':['—',0.069,0.042,0.256,'—','—'],
 'geo':[0.35,0.433,0.368,1.622,0.38,0.32],
}
RS = ['R1','R2','R3','R4','R5','R6']
print('指标'.ljust(9)+''.join(r.rjust(14) for r in RS))
for mt in metrics:
    line = mt.ljust(9)
    for j, r in enumerate(RS):
        pp = paper[mt][j]
        a = auth(r, mt)
        pstr = ('%.3f'%pp) if isinstance(pp,(int,float)) else str(pp)
        if isinstance(pp,(int,float)) and a and isinstance(a,float) and abs(pp-a)<0.01:
            line += ('%13s*' % pstr)
        else:
            line += ('%14s' % (pstr+'|'+str(a)))
    print(line)
print("\n* = 论文值与权威值吻合(<0.01)；R4 显示 0727 与 0730 两个候选")

# R5 0727 各指标
print("\n=== R5 使用 0727 的完整权威值 ===")
for mt in ['offset','confusion','temp','defense','beta','kappa','R_root','P_basin','cos_rin','cos_gen','gravity','geo','eigen','stability','rank']:
    print("  %s: %s" % (mt, mean729('R5', mt)))
