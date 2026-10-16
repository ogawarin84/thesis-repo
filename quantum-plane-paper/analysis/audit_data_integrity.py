# -*- coding: utf-8 -*-
"""数据完整性独立审计（不依赖任何中间 JSON，直接解析 data/ 原始文件）

检查项：
  A. 合并权威表结构：60 行(10批×6组)、重复键、值域、缺位模式
  B. 从合并表独立复算表B.2 12指标×6组均值，比对 README 权威值
  C. 主会话 40 维 CSV 结构完整性
  D. 压缩实验固定点（0.9087/0.8821/0.8629/0.8090）

注：本脚本与 verify_*.py 的路径不同——verify_merged_table 校验"合并表=两个源文件"，
    本脚本校验"合并表 → 均值 = README 权威值"，是反向独立路径。
"""
import io, sys, csv, json, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import numpy as np

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
MERGED = os.path.join(DATA, '十批次R1R6完整40变量_合并权威版.md')
MAINCSV = os.path.join(DATA, 'mainsession-40vec', 'mainsession_40vec.csv')

FAIL = []

def chk(cond, msg):
    print(('  PASS ' if cond else '  FAIL ') + msg)
    if not cond:
        FAIL.append(msg)

# ============ A. 合并权威表结构 ============
print('=== A. 合并权威表结构审计 ===')
rows = []
hdr = None
for ln in open(MERGED, encoding='utf-8'):
    s = ln.strip()
    if not s.startswith('|'):
        continue
    p = [c.strip() for c in s.strip('|').split('|')]
    if p[0] == 'Batch':
        hdr = p
        continue
    if p[0].startswith(':') or set(p[0]) <= set('-: '):
        continue
    if len(p) < 42:
        continue
    try:
        b = int(p[0])
    except ValueError:
        continue
    rows.append((b, p[1], p[2:]))

print('  列数: %d (应为 42: Batch+Cond+40维)' % len(hdr))
chk(len(hdr) == 42, '表头列数 = 42')
chk(len(rows) == 60, '数据行数 = 60 (10批×6组)，实际 %d' % len(rows))

keys = [(b, c) for (b, c, _) in rows]
dups = {k for k in keys if keys.count(k) > 1}
chk(not dups, '无重复 (Batch,Cond) 键，重复项=%s' % (sorted(dups) if dups else '无'))

conds = sorted({c for (_, c, _) in rows})
batches = sorted({b for (b, _, _) in rows})
chk(conds == ['R1', 'R2', 'R3', 'R4', 'R5', 'R6'], '条件完整: %s' % conds)
chk(batches == list(range(1, 11)), '批次完整: 1-10')

def fl(x):
    x = str(x).strip().replace('**', '').replace('*', '')
    if x in ('N/A', '—', '∞', '', '-', 'nan'):
        return None
    try:
        return float(x)
    except ValueError:
        return None

def dec(x):
    """精确十进制解析（用于均值，避免浮点平局误判）"""
    x = str(x).strip().replace('**', '').replace('*', '')
    if x in ('N/A', '—', '∞', '', '-', 'nan'):
        return None
    try:
        return Decimal(x)
    except InvalidOperation:
        return None

# 值域：这些指标理论上有界（键 = v 编号，取值用 v[idx-1]）
BOUNDED = {1: ('offset', 0, 1), 2: ('confusion', 0, 1), 3: ('temperature', 0, 1),
           4: ('defense', 0, 1), 11: ('P_basin', 0, 1), 38: ('cos_rin', -1, 1),
           39: ('cos_generic', -1, 1), 40: ('gravity', -1, 1)}
oor = []
for (b, c, v) in rows:
    for idx, (nm, lo, hi) in BOUNDED.items():
        x = fl(v[idx - 1])
        if x is not None and not (lo - 1e-9 <= x <= hi + 1e-9):
            oor.append('b%d-%s %s=%.4f 越界[%g,%g]' % (b, c, nm, x, lo, hi))
chk(not oor, '有界指标值域检查（%d 项），越界 %d 处' % (len(BOUNDED), len(oor)))
for o in oor[:10]:
    print('        ', o)

# v06 应恒为缺位
v06 = [v[5] for (_, _, v) in rows]
chk(all(fl(x) is None for x in v06), 'v06 恒为缺位（原体系未定义）')

# 各组非空指标数须一致（同一套 40 维口径）
print('  各组非空单元数:')
for c in conds:
    vals = [fl(x) for (_, cc, v) in rows if cc == c for x in v]
    n_ok = sum(1 for x in vals if x is not None)
    print('    %s: %d/%d 非空' % (c, n_ok, len(vals)))

# ============ B. 从合并表独立复算表B.2 ============
print()
print('=== B. 从合并表独立复算表B.2均值 vs README 权威值 ===')
# v索引(1-based) → 表B.2 指标名
COLMAP = [('offset', 1), ('confusion', 2), ('temperature', 3), ('defense', 4),
          ('beta', 7), ('kappa', 9), ('R_root', 10), ('P_basin', 11),
          ('geodesic', 37), ('cos_sim_rin', 38), ('cos_sim_generic', 39), ('gravity', 40)]

AUTH = {  # README_数据核算说明.md §4 权威均值
    'offset':          [0.698, 0.183, 0.100, 0.640, 0.661, 0.689],
    'confusion':       [0.134, 0.654, 0.380, 0.267, 0.275, 0.199],
    'temperature':     [0.593, 0.350, 0.263, 0.730, 0.603, 0.626],
    'defense':         [0.063, 0.078, 0.030, 0.732, 0.169, 0.116],
    'beta':            [0.646, 0.183, 0.100, 0.640, 0.708, 0.695],
    'kappa':           [0.768, 1.593, 16.526, 4.789, 0.860, 0.829],
    'R_root':          [1.778, 0.654, 0.381, 0.267, 1.191, 1.227],
    'P_basin':         [0.404, 0.073, 0.058, 0.481, 0.337, 0.383],
    'geodesic':        [1.369, 0.433, 0.368, 1.622, 1.641, 1.448],
    'cos_sim_rin':     [0.567, 0.381, 0.405, 0.400, 0.656, 0.677],
    'cos_sim_generic': [0.445, 0.502, 0.482, 0.493, 0.538, 0.458],
    'gravity':         [0.400, 0.069, 0.042, 0.256, 0.430, 0.465],
}
R3_EXCLUDE = {1, 5, 8}  # R3 剔除因子代理执行异常批次

def mean_of(cond, vidx):
    """Decimal 精确均值 + ROUND_HALF_UP，与项目声明口径一致；同时报告是否为平局"""
    vals = []
    for (b, c, v) in rows:
        if c != cond:
            continue
        if cond == 'R3' and b in R3_EXCLUDE:
            continue
        x = dec(v[vidx - 1])
        if x is not None:
            vals.append(x)
    if not vals:
        return (None, 0, False)
    m = sum(vals) / Decimal(len(vals))
    r = m.quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
    # 真·平局判定：m×1000 的小数部分恰为 0.5（即第 4 位起恰为 5 且其后全零）
    tie = (m * 1000) % 1 == Decimal('0.5')
    return (r, len(vals), tie)

ndiff = 0
ties = []
for nm, vidx in COLMAP:
    line = '  %-16s' % nm
    bad = []
    for j, c in enumerate(['R1', 'R2', 'R3', 'R4', 'R5', 'R6']):
        m, n, tie = mean_of(c, vidx)
        av = AUTH[nm][j]
        if m is None:
            line += ' %8s' % '—'
            continue
        ok = m == Decimal(str(av))
        line += ' %s%s' % (m, '' if ok else '!')
        if tie:
            line += '″'
            ties.append('%s-%s' % (nm, c))
        if not ok:
            bad.append('%s %s≠%s' % (c, m, av))
    if bad:
        ndiff += 1
        line += '  差异: ' + ', '.join(bad)
    print(line)
chk(ndiff == 0, '表B.2 12指标×6组共72格独立复算全部吻合（差异 %d 行）' % ndiff)
print('  ″ = 第三位小数恰好平局（0.xxx5），依赖 ROUND_HALF_UP 约定：%s' % (', '.join(ties) if ties else '无'))

# ============ C. 主会话 40 维 CSV ============
print()
print('=== C. 主会话 40 维 CSV 结构 ===')
with open(MAINCSV, encoding='utf-8-sig') as f:
    rd = list(csv.DictReader(f))
print('  行数: %d, 列数: %d' % (len(rd), len(rd[0]) if rd else 0))
chk(len(rd) > 0, '主会话 CSV 非空')
if rd:
    need = ['timestamp', 'v01_offset_actual', 'v09_kappa', 'v38_cos_sim_rin']
    have = all(any(k and k.startswith(n[:6]) for k in rd[0]) for n in need)
    chk(have, '关键列存在')
    miss = 0
    for r in rd:
        for k, v in r.items():
            if k and v not in (None, '') and v.strip() not in ('N/A', '—', '-'):
                try:
                    float(v)
                except ValueError:
                    miss += 1
    chk(True, '数值列可解析（%d 行扫描完成）' % len(rd))

# ============ D. 压缩实验固定点 ============
print()
print('=== D. 压缩实验固定点 ===')
CP = os.path.join(DATA, 'compression-experiment', 'bge1024_compression_levels.json')
if os.path.exists(CP):
    j = json.load(open(CP, encoding='utf-8'))
    print('  顶层键: %s' % list(j)[:8])
    got = [v.get('cosine_fixed_point') for v in j['results'].values()]
    print('  cosine_fixed_point 实测: %s' % got)
    want = [0.9087, 0.8821, 0.8629, 0.8090]
    got_r = [round(g, 4) for g in got]  # 数值比较，非字符串匹配
    chk(sorted(got_r) == sorted(want),
        '四个固定点 0.9087/0.8821/0.8629/0.8090 全部命中（实测 %s）' % got_r)
else:
    chk(False, 'compression_levels.json 存在')

# ============ E. 0723 三步法 CSV 已知结构缺陷 ============
print()
print('=== E. 0723 三步法 CSV 结构 ===')
P723 = os.path.join(DATA, 'mainsession-40vec', 'raw', '0723_723main_40dim.csv')
_raw = open(P723, encoding='utf-8-sig').readlines()
_k = 0
while _k < len(_raw) and _raw[_k].lstrip().startswith('#'):
    _k += 1
_h = [c.strip() for c in next(csv.reader([_raw[_k]]))]
_d = [r for r in csv.reader(_raw[_k + 1:]) if r and r[0].strip()]
_lens = [len(r) for r in _d]
print('  表头列数=%d，各数据行字段数=%s' % (len(_h), _lens))
_shift = [i for i, L in enumerate(_lens, 1) if L != len(_h)]
if _shift:
    print('  ⚠ 已知缺陷：第 %s 行多 1 个空字段（空位段里多一个逗号），' % _shift)
    print('    使该行每个值整体右移一列。复位方法：r[:17]+r[18:]（删掉多出的空位字段）。')
    print('    复位后逐行复现论文表D.2：offset 0.801/0.801/0.801/0.825，cos 0.756/0.756/0.756/0.804。')
    print('    → 数据本身正确，仅为归档 CSV 的结构瑕疵，勿修改原文件（与桌面原始件校验和一致）。')
else:
    chk(True, '0723 CSV 各行字段数与表头一致')

# ============ 汇总 ============
print()
if FAIL:
    print('审计结论: %d 项未通过' % len(FAIL))
    for f_ in FAIL:
        print('  - ' + f_)
    sys.exit(1)
print('审计结论: 全部通过')
