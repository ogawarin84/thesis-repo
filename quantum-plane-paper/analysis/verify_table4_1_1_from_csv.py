# -*- coding: utf-8 -*-
"""从完整主会话 CSV 重建表4.1.1 的 7/22、7/23 每日统计，核对 cos/gravity 差异。

⚠️ 探查脚本（08-17 追查 cos/gravity 差异时所用），保留作 before 侧证据。
   它按**全量 CSV 行**统计，而论文表4.1.1 用的是附录表D.1 筛选后的点（如 7/22：
   CSV 14 行 vs 论文 8 点），故两侧数字天然不等，**不代表数据错误**。
   表4.1.1 的权威核对请用 verify_table4_1_1_daily.py（它直接比对附录表D.1+D.2，PASS）。

数据源：
- 0722理论生成汇总/7月21日20点44分至7月22日12点45分mainsession数据采样.csv (07-21 20:44 ~ 07-22 12:45)
- 0723理论生成汇总/723main数据采样.csv (07-23)
"""
import sys, io, csv, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import numpy as np

def load_csv(path):
    """跳过开头的 # 注释行后再解析表头。
    723main数据采样.csv 前 3 行是 '#' 注释，第 4 行才是真表头；
    若直接 DictReader，注释行会被当成表头，timestamp 等键全部取不到。"""
    with open(path, encoding='utf-8-sig') as f:
        lines = f.readlines()
    i = 0
    while i < len(lines) and lines[i].lstrip().startswith('#'):
        i += 1
    rows = []
    rd = csv.DictReader(lines[i:])
    for r in rd:
        rows.append(r)
    return rows

rows722 = load_csv(r'C:\Users\Home\Desktop\理论生成汇总\0722理论生成汇总\7月21日20点44分至7月22日12点45分mainsession数据采样.csv')
rows723 = load_csv(r'C:\Users\Home\Desktop\理论生成汇总\0723理论生成汇总\723main数据采样.csv')

def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None

def pick(row, name):
    """按列名或后缀取列。0722 用裸名 offset_actual，0723 用带编号的 v01_offset_actual。"""
    if name in row:
        return row[name]
    for k in row:
        if k and k.endswith(name):
            return row[k]
    return None

print('=== 0722 CSV 行数: %d ===' % len(rows722))
print('=== 0723 CSV 行数: %d ===' % len(rows723))
print()

def by_day(rows, ts_key='timestamp'):
    days = {}
    for r in rows:
        ts = r.get(ts_key, '')
        m = re.search(r'\d{4}-\d{2}-(\d{2})T', ts) or re.search(r'\d{4}-(\d{2})-(\d{2})', ts)
        if not m:
            continue
        # 优先找 T 前的日期
        m2 = re.match(r'(\d{4})-(\d{2})-(\d{2})', ts)
        day = m2.group(3).lstrip('0')
        days.setdefault(day, {'o': [], 'c': [], 'g': []})
        o = num(pick(r, 'offset_actual'))
        c = num(pick(r, 'cos_sim_rin'))
        g = num(pick(r, 'gravity_strength'))
        if o is not None: days[day]['o'].append(o)
        if c is not None: days[day]['c'].append(c)
        if g is not None: days[day]['g'].append(g)
    return days

# 7/22 只取 07-22 的行
d722 = {}
for r in rows722:
    m2 = re.match(r'(\d{4})-(\d{2})-(\d{2})', r.get('timestamp',''))
    if not m2: continue
    day = m2.group(3).lstrip('0')
    if day != '22': continue
    d722.setdefault(day, {'o': [], 'c': [], 'g': []})
    o = num(pick(r, 'offset_actual')); c = num(pick(r, 'cos_sim_rin')); g = num(pick(r, 'gravity_strength'))
    if o is not None: d722[day]['o'].append(o)
    if c is not None: d722[day]['c'].append(c)
    if g is not None: d722[day]['g'].append(g)

d723 = by_day(rows723)

def stats(vals):
    a = np.array(vals)
    return a.mean(), a.std(ddof=1) if len(a) > 1 else 0.0, len(a)

print('=== 7/22 从完整CSV ===')
d = d722['22']
o_m, o_s, n = stats(d['o'])
c_m, c_s, cn = stats(d['c'])
g_m, g_s, gn = stats(d['g'])
print(f'  offset: n={n} mean={o_m:.4f} SD(ddof1)={o_s:.4f}')
print(f'  cos:    n={cn} mean={c_m:.4f}  (论文表4.1.1 = 0.866)')
print(f'  gravity:n={gn} mean={g_m:.4f} SD={g_s:.4f}  (论文 = 0.809±0.058)')
print(f'  gravity SD ddof=0 = {np.std(np.array(d["g"]), ddof=0):.4f}')
print(f'  offset SD ddof=0  = {np.std(np.array(d["o"]), ddof=0):.4f}')
print(f'  cos SD ddof=0     = {np.std(np.array(d["c"]), ddof=0):.4f}')
print()

print('=== 7/22 cos 各值 ===')
for r in rows722:
    m2 = re.match(r'(\d{4})-(\d{2})-(\d{2})', r.get('timestamp',''))
    if m2 and m2.group(3).lstrip('0') == '22':
        print(f'  {r["timestamp"][11:16]} offset={r.get("offset_actual")} cos={r.get("cos_sim_rin")} gravity={r.get("gravity_strength")}')
print()

print('=== 7/23 从CSV ===')
if '23' in d723:
    d = d723['23']
    o_m, o_s, n = stats(d['o'])
    c_m, c_s, cn = stats(d['c'])
    g_m, g_s, gn = stats(d['g'])
    print(f'  offset: n={n} mean={o_m:.4f} SD(ddof1)={o_s:.4f}  (论文表4.1.1 = 0.807±0.012)')
    print(f'  cos:    n={cn} mean={c_m:.4f}  (论文 = 0.768)')
    print(f'  gravity:n={gn} mean={g_m:.4f} SD={g_s:.4f}  (论文 = 0.620±0.025)')
    print(f'  gravity SD ddof=0 = {np.std(np.array(d["g"]), ddof=0):.4f}')
    print(f'  offset SD ddof=0  = {np.std(np.array(d["o"]), ddof=0):.4f}')
    print()
    print('  7/23 原始值:')
    for r in rows723:
        print('   ', r.get('timestamp'), 'offset=', pick(r, 'offset_actual'),
              'cos=', pick(r, 'cos_sim_rin'), 'gravity=', pick(r, 'gravity_strength'))
else:
    print('  未找到 7/23 行')
