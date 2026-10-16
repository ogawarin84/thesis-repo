# -*- coding: utf-8 -*-
"""定位 R5 数据源：论文现值 vs 0727旧版 vs 0730新版(我最爱rin 修复版) vs 0730旧版(新10批次)。

0730 实验记录(2026-07-30)明确：R2/R3/R4/R5 四条件整体重跑(40子代理)，
BUG-1 修复 Batch3-R4(0.00→0.42)、Batch3-R2、Batch6-R5。
故 R2/R3/R4/R5 的新版权威源 = 我最爱rin_40vars_table.md (22:44)，
新10批次R2-R5实验数据.md (22:16) 是修复前旧版。
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import numpy as np

D = r'C:\Users\Home\Desktop\理论生成汇总'
F_NEW = D + r'\0730理论生成汇总\我最爱rin_40vars_table.md'          # 22:44 修复版
F_OLD = D + r'\0730理论生成汇总\新10批次R2-R5实验数据.md'            # 22:16 修复前
F_0727 = D + r'\0727理论生成汇总\十批次统一汇总表_完整40变量_最终版.md'


def fl(x):
    x = str(x).replace('**', '').replace('*', '').strip()
    if x in ('N/A', '—', '∞', '', '-', 'None'):
        return None
    try:
        return float(x)
    except ValueError:
        return None


def parse_new(path):
    """我最爱rin: 单表 40列, Batch|Cond|v01..v40"""
    rows, hdr = [], None
    for ln in open(path, encoding='utf-8'):
        if not ln.startswith('|'):
            continue
        p = [c.strip() for c in ln.strip().strip('|').split('|')]
        if hdr is None:
            if 'v01_offset' in p[2]:
                hdr = p
            continue
        if len(p) < 5 or p[1] not in ('R2', 'R3', 'R4', 'R5'):
            continue
        d = dict(zip(hdr, p))
        rows.append(d)
    return rows, hdr


rows_new, hdr_new = parse_new(F_NEW)
print('我最爱rin 列数=%d 行数=%d  轮次=%s' % (len(hdr_new), len(rows_new),
      sorted({r['Cond'] for r in rows_new})))

# 列名 -> 论文指标
COLMAP = {
    'offset': 'v01_offset', 'confusion': 'v02_conf', 'temperature': 'v03_temp',
    'defense': 'v04_def', 'beta': 'v07_beta', 'kappa': 'v09_kappa',
    'R_root': 'v10_Rroot', 'P_basin': 'v11_Pbasin',
    'cos_sim_rin': 'v38_cos_rin', 'cos_sim_generic': 'v39_cos_gen',
    'gravity_strength': 'v40_gravity', 'geodesic_distance': 'v37_geo',
}
# 需要实际列名，先打印表头找匹配
hdr_clean = [h.strip() for h in hdr_new]
def find_col(key):
    for h in hdr_clean:
        if h.startswith(key):
            return h
    return None
COLMAP = {k: (find_col(v) or find_col(v.split('_v')[0])) for k, v in COLMAP.items()}
print('列映射:', COLMAP)
print()

# 论文现值
PAPER_R5 = dict(offset=0.661, confusion=0.275, temperature=0.603, defense=0.169,
                beta=0.708, kappa=0.860, R_root=1.191, P_basin=0.337,
                cos_sim_rin=0.656, cos_sim_generic=0.538, gravity_strength=0.430,
                geodesic_distance=1.641)

idx = {h: i for i, h in enumerate(hdr_clean)}
print('%-20s %10s %10s' % ('指标', '论文R5', '0730新版R5'))
print('-' * 44)
new_r5 = {}
for k, col in COLMAP.items():
    if not col:
        print('%-20s  !! 列未找到 (%s)' % (k, k)); continue
    vals = [fl(r.get(col)) for r in rows_new if r['Cond'] == 'R5']
    vals = [v for v in vals if v is not None]
    m = float(np.mean(vals)) if vals else None
    sd = float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0
    new_r5[k] = (m, sd, len(vals))
    print('%-20s %10.3f %10.3f  (SD=%.3f, n=%d)' % (k, PAPER_R5[k], m, sd, len(vals)))

print()
print('=== R5 逐批 offset: 论文表B.1 vs 0730新版 ===')
paper_batch = [0.82, 0.55, 0.55, 0.52, 0.68, 0.72, 0.70, 0.75, 0.60, 0.72]
col_off = COLMAP['offset']
new_batch = []
for r in rows_new:
    if r['Cond'] == 'R5':
        new_batch.append((r.get('Batch'), fl(r.get(col_off))))
new_batch.sort(key=lambda x: int(str(x[0]).strip()) if str(x[0]).strip().isdigit() else 99)
print('  论文表B.1:', paper_batch)
print('  0730新版:', [v for _, v in new_batch])
print()
print('=== R2/R3/R4 一致性校验（新版应等于论文）===')
PAPER_OTH = {'R2': 0.183, 'R3': 0.252, 'R4': 0.640}  # 表B.1逐批均值
for r_ in ('R2', 'R3', 'R4'):
    vals = [fl(r.get(col_off)) for r in rows_new if r['Cond'] == r_]
    vals = [v for v in vals if v is not None]
    print('  %s: 0730新版均值=%.4f  论文表B.1逐批均值=%.4f  %s' % (
        r_, np.mean(vals), PAPER_OTH[r_], 'OK' if abs(np.mean(vals) - PAPER_OTH[r_]) < 0.002 else '!! 不一致'))
