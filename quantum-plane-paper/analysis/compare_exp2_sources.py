# -*- coding: utf-8 -*-
"""实验二（R1-R6 十批次）三方数据源逐轮均值对比，定位论文表B.1/表B.2 到底用了哪一版。

源:
  A = 0727理论生成汇总/十批次统一汇总表_完整40变量_最终版.md   (60条, R1-R6 全六轮)
  B = 0730理论生成汇总/新10批次R2-R5实验数据.md                (40条, R2-R5)
  C = 0730理论生成汇总/十批次R1R6完整40变量_合并权威版.md       (60条, R1-R6, 08-17合并)
论文: 表B.2 六组均值（硬编码自 ver5 L1516-1531）
"""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import numpy as np

DESK = r'C:\Users\Home\Desktop\理论生成汇总'
A = DESK + r'\0727理论生成汇总\十批次统一汇总表_完整40变量_最终版.md'
B = DESK + r'\0730理论生成汇总\新10批次R2-R5实验数据.md'
C = DESK + r'\0730理论生成汇总\十批次R1R6完整40变量_合并权威版.md'


def num(x):
    x = str(x).strip().replace('**', '').replace('∞', '')
    if x in ('—', 'N/A', 'na', '', '-'):
        return None
    try:
        return float(x)
    except ValueError:
        return None


def rows_of(path, mincols):
    """返回 [[cell,...], ...] 所有数据行（含|的行，跳过表头/分隔）"""
    out = []
    for ln in open(path, encoding='utf-8').read().split('\n'):
        s = ln.strip()
        if not s.startswith('|'):
            continue
        if re.match(r'^\|[\s:\-|]+\|$', s):
            continue
        p = [c.strip() for c in s.strip('|').split('|')]
        if len(p) < mincols:
            continue
        out.append(p)
    return out


def agg(vals):
    v = [x for x in vals if x is not None]
    if not v:
        return None, None, 0
    return float(np.mean(v)), (float(np.std(v, ddof=1)) if len(v) > 1 else 0.0), len(v)


# ---------- A: 核心变量表 offset/confusion/temp/defense/cos_rin/cos_gen/gravity ----------
# 列: 批次|轮次|offset|confusion|temp|defense|color|cos_rin|cos_gen|gravity
srcA = {}
found_hdr = False
for p in rows_of(A, 9):
    if 'offset' in p[2] and '轮次' in p[1]:
        found_hdr = True
        continue
    if not found_hdr:
        continue
    if len(p) < 10:
        continue
    m = re.match(r'^R(\d)$', p[1])
    if not m:
        continue
    r = 'R' + m.group(1)
    srcA.setdefault(r, {'offset': [], 'confusion': [], 'temperature': [], 'defense': [],
                        'cos_rin': [], 'cos_gen': [], 'gravity': []})
    srcA[r]['offset'].append(num(p[2]))
    srcA[r]['confusion'].append(num(p[3]))
    srcA[r]['temperature'].append(num(p[4]))
    srcA[r]['defense'].append(num(p[5]))
    srcA[r]['cos_rin'].append(num(p[7]))
    srcA[r]['cos_gen'].append(num(p[8]))
    srcA[r]['gravity'].append(num(p[9]))

# ---------- B: 40变量单表 ----------
srcB = {}
hdrB = None
for p in rows_of(B, 30):
    if 'v01_offset' in p[2] if len(p) > 2 else False:
        hdrB = p
        continue
    if hdrB is None:
        continue
    m = re.match(r'R(\d)', p[1])
    if not m:
        continue
    r = 'R' + m.group(1)
    idx = {name: i for i, name in enumerate(hdrB)}
    g = lambda name: num(p[idx[name]]) if name in idx and idx[name] < len(p) else None
    srcB.setdefault(r, {'offset': [], 'confusion': [], 'temperature': [], 'defense': [],
                        'cos_rin': [], 'cos_gen': [], 'gravity': []})
    srcB[r]['offset'].append(g('v01_offset'))
    srcB[r]['confusion'].append(g('v02_confusion'))
    srcB[r]['temperature'].append(g('v03_temp'))
    srcB[r]['defense'].append(g('v04_defense'))
    srcB[r]['cos_rin'].append(g('v38_cos_rin'))
    srcB[r]['cos_gen'].append(g('v39_cos_gen'))
    srcB[r]['gravity'].append(g('v40_gravity'))

# ---------- C: 合并权威版（v01..v40 长表） ----------
srcC = {}
hdrC = None
for p in rows_of(C, 12):
    if len(p) > 2 and 'v01 (offset)' in p[2]:
        hdrC = p
        continue
    if hdrC is None:
        continue
    m = re.match(r'R(\d)', p[1])
    if not m:
        continue
    r = 'R' + m.group(1)
    idx = {re.sub(r'\s*\(.*?\)', '', name).strip(): i for i, name in enumerate(hdrC)}
    g = lambda name: num(p[idx[name]]) if name in idx and idx[name] < len(p) else None
    srcC.setdefault(r, {'offset': [], 'confusion': [], 'temperature': [], 'defense': [],
                        'cos_rin': [], 'cos_gen': [], 'gravity': []})
    srcC[r]['offset'].append(g('v01'))
    srcC[r]['confusion'].append(g('v02'))
    srcC[r]['temperature'].append(g('v03'))
    srcC[r]['defense'].append(g('v04'))
    srcC[r]['cos_rin'].append(g('v38'))
    srcC[r]['cos_gen'].append(g('v39'))
    srcC[r]['gravity'].append(g('v40'))

# ---------- 论文表B.2 ----------
PAPER = {
    'R1': dict(offset=0.698, confusion=0.134, temperature=0.593, defense=0.063, cos_rin=0.567, cos_gen=0.445, gravity=0.400),
    'R2': dict(offset=0.183, confusion=0.654, temperature=0.350, defense=0.078, cos_rin=0.381, cos_gen=0.502, gravity=0.069),
    'R3': dict(offset=0.100, confusion=0.380, temperature=0.263, defense=0.030, cos_rin=0.405, cos_gen=0.482, gravity=0.042),
    'R4': dict(offset=0.640, confusion=0.267, temperature=0.730, defense=0.732, cos_rin=0.400, cos_gen=0.493, gravity=0.256),
    'R5': dict(offset=0.661, confusion=0.275, temperature=0.603, defense=0.169, cos_rin=0.656, cos_gen=0.538, gravity=0.430),
    'R6': dict(offset=0.689, confusion=0.199, temperature=0.626, defense=0.116, cos_rin=0.677, cos_gen=0.458, gravity=0.465),
}
PAPER_ALT = {  # 表B.2 注: R3 = 剩余7批次
    'R3': dict(offset=0.100, confusion=0.380, temperature=0.263, defense=0.030, cos_rin=0.405, cos_gen=0.482, gravity=0.042),
}

print('源行数: A(0727)=%s  B(0730/我最爱rin)=%s  C(合并权威)=%s' % (
    {k: len(v['offset']) for k, v in sorted(srcA.items())},
    {k: len(v['offset']) for k, v in sorted(srcB.items())},
    {k: len(v['offset']) for k, v in sorted(srcC.items())}))
print()
KEYS = ['offset', 'confusion', 'temperature', 'defense', 'cos_rin', 'cos_gen', 'gravity']
for r in ['R1', 'R2', 'R3', 'R4', 'R5', 'R6']:
    print('=== %s ===' % r)
    print('  %-12s %9s %9s %9s   %s' % ('变量', '论文表B.2', 'A=0727', 'B=0730', 'C=合并'))
    for k in KEYS:
        pa = PAPER[r][k]
        a = agg(srcA.get(r, {}).get(k, []))[0]
        b = agg(srcB.get(r, {}).get(k, []))[0]
        c = agg(srcC.get(r, {}).get(k, []))[0]
        hitA = ' <A' if a is not None and abs(a - pa) < 0.0015 else ''
        hitB = ' <B' if b is not None and abs(b - pa) < 0.0015 else ''
        hitC = ' <C' if c is not None and abs(c - pa) < 0.0015 else ''
        f = lambda x: ('%9.4f' % x) if x is not None else '      N/A'
        print('  %-12s %9.3f %s %s %s  %s' % (k, pa, f(a), f(b), f(c), (hitA + hitB + hitC) or ' !! 无源匹配'))
    print()

print('=== 参考: 表B.1 R2 逐批 offset 论文 vs B(0730) ===')
print('  论文:', [round(x, 2) for x in [0.28, 0.22, 0.08, 0.18, 0.25, 0.00, 0.34, 0.18, 0.15, 0.15]])
print('  B   :', [round(x, 2) if x is not None else None for x in srcB.get('R2', {}).get('offset', [])])
print('  A   :', [round(x, 2) if x is not None else None for x in srcA.get('R2', {}).get('offset', [])])
print()
print('=== 参考: 表B.1 R4 逐批 offset 论文 vs B(0730) ===')
print('  论文:', [round(x, 2) for x in [0.72, 0.68, 0.42, 0.88, 0.44, 0.72, 0.78, 0.96, 0.38, 0.42]])
print('  B   :', [round(x, 2) if x is not None else None for x in srcB.get('R4', {}).get('offset', [])])
print('  A   :', [round(x, 2) if x is not None else None for x in srcA.get('R4', {}).get('offset', [])])
print()
print('=== 参考: 表B.1 R5 逐批 offset 论文 vs A(0727) vs B(0730) ===')
print('  论文:', [round(x, 2) for x in [0.82, 0.55, 0.55, 0.52, 0.68, 0.72, 0.70, 0.75, 0.60, 0.72]])
print('  A   :', [round(x, 2) if x is not None else None for x in srcA.get('R5', {}).get('offset', [])])
print('  B   :', [round(x, 2) if x is not None else None for x in srcB.get('R5', {}).get('offset', [])])
