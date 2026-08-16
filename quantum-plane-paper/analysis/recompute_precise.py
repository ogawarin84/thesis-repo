# -*- coding: utf-8 -*-
"""Decimal 精确重算表6权威均值（避免浮点四舍五入误差）
口径：R1/R5/R6=0727最终版；R2/R3/R4=我最爱rin(0730修复版)
R3均值剔除B1/B5/B8；R6 batch1 用 0.78
四舍五入：ROUND_HALF_UP（学术标准）
"""
from decimal import Decimal, ROUND_HALF_UP, getcontext
getcontext().prec = 30

F0730 = r'C:\Users\Home\Desktop\理论生成汇总\0730理论生成汇总\我最爱rin_40vars_table.md'
F0727 = r'C:\Users\Home\Desktop\理论生成汇总\0727理论生成汇总\十批次统一汇总表_完整40变量_最终版.md'

def D(x):
    """字符串/数字 -> Decimal 或 None"""
    if x is None: return None
    s = str(x).strip().replace('**','').replace('*','')
    if s in ('N/A','—','∞','','-','nan'): return None
    try: return Decimal(s)
    except: return None

def dround(v, nd=3):
    if v is None: return None
    q = Decimal(1).scaleb(-nd)
    return v.quantize(q, rounding=ROUND_HALF_UP)

# ============ 解析 0730 ============
d730 = {}
for ln in open(F0730, encoding='utf-8'):
    if not ln.startswith('|'): continue
    p = [c.strip().replace('**','') for c in ln.strip().strip('|').split('|')]
    if len(p) < 41 or p[1] not in ('R2','R3','R4','R5') or p[0] == 'Batch': continue
    try: b = int(p[0])
    except: continue
    d730[(b,p[1])] = {
        'offset': D(p[2]), 'confusion': D(p[3]), 'temp': D(p[4]), 'defense': D(p[5]),
        'beta': D(p[7]), 'kappa': D(p[9]), 'R_root': D(p[10]), 'P_basin': D(p[11]),
        'geo': D(p[37]), 'cos_rin': D(p[38]), 'cos_gen': D(p[39]), 'gravity': D(p[40]),
    }

# ============ 解析 0727 ============
d727 = {}; cur = None
import re
for ln in open(F0727, encoding='utf-8'):
    s = ln.strip()
    if s.startswith('## '):
        cur = ('core' if '核心变量' in s else 'dyn' if '动力学' in s else 'spec' if '本征谱' in s else None)
        continue
    if not s.startswith('|') or cur is None: continue
    p = [c.strip().replace('**','') for c in s.strip('|').split('|')]
    if len(p) < 3 or not p[0].startswith('batch'): continue
    m = re.search(r'(\d+)', p[0])
    if not m: continue
    b, c = int(m.group(1)), p[1]
    if c not in ('R1','R5','R6'): continue
    d = d727.setdefault((b,c), {})
    if cur == 'core':
        for k,i in [('offset',2),('confusion',3),('temp',4),('defense',5),('cos_rin',7),('cos_gen',8),('gravity',9)]:
            if i < len(p): d[k] = D(p[i])
    elif cur == 'dyn':
        for k,i in [('beta',2),('kappa',4),('R_root',5),('P_basin',6)]:
            if i < len(p): d[k] = D(p[i])
    elif cur == 'spec':
        if 5 < len(p): d['geo'] = D(p[5])

RS = ['R1','R2','R3','R4','R5','R6']
R3EX = {1,5,8}
METS = ['offset','confusion','temp','defense','beta','kappa','R_root','P_basin','cos_rin','cos_gen','gravity','geo']

def src(r): return d727 if r in ('R1','R5','R6') else d730

def vals(r, m):
    out = []
    for b in range(1, 11):
        v = src(r).get((b,r), {}).get(m)
        if v is None: continue
        if r == 'R3' and b in R3EX: continue
        out.append(v)
    return out

AUTH = {}
print('=== 表6 权威均值（Decimal 精确重算）===')
print('指标'.ljust(11) + ''.join(r.rjust(9) for r in RS))
for m in METS:
    row = m.ljust(11)
    for r in RS:
        v = vals(r, m)
        if not v: row += '      --'; AUTH[(m,r)] = None; continue
        total = sum(v, Decimal(0))
        mean = total / len(v)
        AUTH[(m,r)] = mean
        row += ('%9.3f' % dround(mean)) if dround(mean) is not None else '      --'
    print(row)

print()
print('=== 4位小数版（供合并表/精确对照）===')
for m in METS:
    row = m.ljust(11)
    for r in RS:
        v = AUTH.get((m,r))
        row += ('%10.4f' % dround(v,4)) if dround(v,4) is not None else '      --'
    print(row)

# 保存权威值 JSON 供论文更新使用
import json
json.dump({('%s|%s' % (m,r)): (str(dround(AUTH[(m,r)])) if AUTH[(m,r)] is not None else None) for m in METS for r in RS},
          open(r'C:\Users\Home\Documents\xhh-paper\quantum-plane-paper\analysis\table6_authoritative.json','w',encoding='utf-8'),
          ensure_ascii=False, indent=1)
print()
print('已保存 table6_authoritative.json（3位，ROUND_HALF_UP）')
