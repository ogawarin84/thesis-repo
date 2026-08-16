# -*- coding: utf-8 -*-
"""核验论文表4.1.1（主会话每日统计）从附录表11+表12逐日复算，以及阶段0表R2 Batch6=0.00。
"""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import numpy as np

PAPER = r'C:\Users\Home\Desktop\理论生成汇总\0802理论生成汇总\量子平面概率动力学模型_完整版_ver5（mine）.md'
lines = open(PAPER, encoding='utf-8').read().split('\n')

def num(x):
    x = str(x).strip().replace('**', '')
    if x in ('—', 'N/A', '∞', ''):
        return None
    try:
        return float(x)
    except ValueError:
        return None

# ---------- 1) 解析附录表11 ----------
# 表11: 时间戳 offset confusion temperature defense beta kappa cos_sim_rin gravity geodesic
# 定位表11数据行
rows11 = []
start = None
for i, ln in enumerate(lines):
    if '表11' in ln and '0719-0723' in ln:
        start = i + 2
        break
for i in range(start, len(lines)):
    s = lines[i].strip()
    if not s.startswith('|'):
        continue
    if s.startswith('|:--') or s.startswith('|--') or '时间戳' in s:
        continue
    p = [c.strip() for c in s.strip('|').split('|')]
    if len(p) < 9:
        break
    ts = p[0].strip()
    m = re.match(r'0?(\d+)-(\d+)', ts)
    if not m:
        if num(p[1]) is None:
            break
        continue
    day = m.group(2).lstrip('0') or '0'
    o, c, t = num(p[1]), num(p[2]), num(p[3])
    cs, g = num(p[7]), num(p[8])
    rows11.append((day, o, cs, g))
    if o is None:
        break

# ---------- 2) 解析附录表12 ----------
# 表12: 时间戳 offset step1 step2 step3 delta cos gravity
rows12 = []
start = None
for i, ln in enumerate(lines):
    if '表12' in ln and '0723' in ln:
        start = i + 2
        break
for i in range(start, len(lines)):
    s = lines[i].strip()
    if not s.startswith('|'):
        continue
    if s.startswith('|:--') or '时间戳' in s:
        continue
    p = [c.strip() for c in s.strip('|').split('|')]
    if len(p) < 8:
        break
    ts = p[0].strip()
    m = re.match(r'0?(\d+)-(\d+)', ts)
    if not m:
        break
    day = m.group(2).lstrip('0') or '0'
    o, cs, g = num(p[1]), num(p[6]), num(p[7])
    rows12.append((day, o, cs, g))

allrows = rows11 + rows12
print('=== 附录表11+12 总行数: %d (表11=%d + 表12=%d) ===' % (len(allrows), len(rows11), len(rows12)))

# ---------- 3) 按日分组计算 ----------
daily = {}
for day, o, cs, g in allrows:
    daily.setdefault(day, {'offset': [], 'cos': [], 'gravity': []})
    if o is not None: daily[day]['offset'].append(o)
    if cs is not None: daily[day]['cos'].append(cs)
    if g is not None: daily[day]['gravity'].append(g)

# ---------- 4) 与论文表4.1.1 对比 ----------
print()
print('=== 表4.1.1 逐日复算 vs 论文 ===')
# 论文表4.1.1 值: 日期->(n, offset均值, offset SD, cos均值, gravity均值, gravity SD)
expected = {
    # 2026-08-17 修正后论文值（与 recalc_table4_1_1.py 复算一致）
    '19': (6, 0.848, 0.004, 0.866, 0.734, 0.005),
    '20': (3, 0.821, 0.000, 0.855, 0.702, 0.000),
    '21': (12, 0.832, 0.066, 0.846, 0.706, 0.076),
    '22': (8, 0.933, 0.048, 0.866, 0.809, 0.058),
    '23': (4, 0.807, 0.012, 0.768, 0.620, 0.025),
}
ok = True
for day in sorted(daily, key=lambda d: int(d)):
    d = daily[day]
    exp = expected.get(day)
    if not exp:
        print(f'  7/{day}: 论文无此日，复算 n={len(d["offset"])}'); continue
    en, eo, eos, ec, eg, egs = exp
    n = len(d['offset'])
    o_m = np.mean(d['offset']) if d['offset'] else float('nan')
    o_s = np.std(d['offset'], ddof=1) if len(d['offset']) > 1 else 0.0
    c_m = np.mean(d['cos']) if d['cos'] else float('nan')
    g_m = np.mean(d['gravity']) if d['gravity'] else float('nan')
    g_s = np.std(d['gravity'], ddof=1) if len(d['gravity']) > 1 else 0.0
    stat = 'OK' if (n == en and abs(o_m-eo) < 0.002 and abs(o_s-eos) < 0.003
                    and abs(c_m-ec) < 0.003 and abs(g_m-eg) < 0.003 and abs(g_s-egs) < 0.003) else '!!'
    if stat == '!!': ok = False
    print(f'  7/{day}: n={n}vs{en} offset={o_m:.4f}±{o_s:.4f}vs{eo}±{eos} cos={c_m:.4f}vs{ec} gravity={g_m:.4f}±{g_s:.4f}vs{eg}±{egs}  [{stat}]')

# ---------- 5) 阶段0表 R2 Batch6=0.00 ----------
print()
print('=== 阶段0表: R2 Batch6 = 0.00 确认 ===')
# 从附录表5 或正文提取 R2 各批次 offset
# 先看表5 原始值格式
found_batch = []
for i, ln in enumerate(lines):
    if '表5' in ln and 'R1-R6' in ln:
        start = i + 2
        break
for i in range(start, min(start + 30, len(lines))):
    s = lines[i].strip()
    if not s.startswith('|'):
        continue
    if s.startswith('|:--') or '批次' in s:
        continue
    p = [c.strip() for c in s.strip('|').split('|')]
    if len(p) < 7:
        continue
    if p[1] == 'R2':
        vals = [num(x) for x in p[2:]]
        valid = [v for v in vals if v is not None]
        print(f'  表5 R2 行: {p[0]} | 各批次值: {vals}')
        print(f'    最小值={min(valid):.2f}  → {"=0.00 确认 Batch6 归零" if min(valid)==0.0 else "无0.00，需检查"}')
        found_batch.append((p[0], valid))
        break

print()
print('结论:', 'PASS：表4.1.1逐日统计与附录表11+12完全一致' if ok else 'FAIL')
sys.exit(0 if ok else 1)
