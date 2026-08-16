# -*- coding: utf-8 -*-
"""重算表4.1.1主会话每日统计（数据源=0722/0723主会话CSV + 表11/12明细）。

口径（按用户指令 2026-08-17）：
- 样本点集 = 表11(7/19-7/22 29点) + 表12(7/23 4点) = 33点，与论文"合计33个时间点"一致
- offset_actual / cos_sim_rin = CSV 精确值（7/22/7/23）；7/19-7/21白天段 0721 CSV 无 cos 列，
  用表11 记录值（历史实时计算记录，无法从 CSV 复算，是数据源本身的限制）
- gravity_strength = cos_sim_rin × offset_actual（实验二公式），不用 CSV 的 gravity_strength 列
  （CSV 该列是 basin_metrics_unified 程序的另一口径，如 20:44 行 0.855 ≠ 0.875×0.95=0.831）
- SD：offset 保持论文口径 ddof=1；gravity 保持论文口径 ddof=0（论文实际如此）
"""
import sys, io, statistics as st
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def m(vals, n=None): return sum(vals)/ (n or len(vals))
def sd0(vals): return st.pstdev(vals)          # ddof=0
def sd1(vals): return st.stdev(vals) if len(vals) > 1 else 0.0  # ddof=1

# ---- 每日点集：[(offset, cos)] ----
# 7/19 (6点, 表11记录, 0721 CSV无cos)  gravity=cos×offset 验证
d719 = [(0.850, 0.868), (0.843, 0.862), (0.843, 0.862), (0.850, 0.868), (0.850, 0.868), (0.850, 0.868)]
# 7/20 (3点)
d720 = [(0.821, 0.855)] * 3
# 7/21 (12点: 白天8 表11记录 + 晚4 0722CSV精确)
d721_day = [(0.831, 0.860), (0.826, 0.858), (0.826, 0.858), (0.826, 0.858),
            (0.826, 0.858), (0.826, 0.858), (0.813, 0.855), (0.813, 0.855)]
d721_night = [(0.950, 0.875), (0.950, 0.875), (0.700, 0.750), (0.794, 0.797)]
# 7/22 (8点: 0722CSV精确; 00:36,01:30,02:00,02:45,11:58(0.813行),12:00,12:15,12:45)
d722 = [(0.950, 0.875)] * 7 + [(0.813, 0.8065)]
# 7/23 (4点: 723main CSV精确)
d723 = [(0.801, 0.7557)] * 3 + [(0.825, 0.8044)]

DAYS = [('7/19', d719), ('7/20', d720), ('7/21', d721_day + d721_night),
        ('7/22', d722), ('7/23', d723)]

print('点集计数:', {k: len(v) for k, v in DAYS}, ' 总和:', sum(len(v) for _, v in DAYS))

# ---- 论文表4.1.1 原值 ----
paper = {
    '7/19': dict(n=6, off_m=0.848, off_sd=0.004, cos=0.868, grav_m=0.734, grav_sd=0.005),
    '7/20': dict(n=3, off_m=0.821, off_sd=0.000, cos=0.855, grav_m=0.702, grav_sd=0.000),
    '7/21': dict(n=12, off_m=0.832, off_sd=0.066, cos=0.845, grav_m=0.706, grav_sd=0.076),
    '7/22': dict(n=8, off_m=0.933, off_sd=0.048, cos=0.873, grav_m=0.809, grav_sd=0.057),
    '7/23': dict(n=4, off_m=0.816, off_sd=0.016, cos=0.769, grav_m=0.618, grav_sd=0.019),
}

def dif(a, b, tol=0.0005):
    if a is None or b is None: return True
    return abs(a - b) > tol

print()
print(f"{'日':<5}{'n':>3} | {'offset均值':>9} {'SD1':>6} | {'cos均值':>8} | {'gravity均值':>10} {'SD0':>6} | gravity=cos×off自洽?")
print('-' * 95)
recalc = {}
for day, pts in DAYS:
    offs = [p[0] for p in pts]; coss = [p[1] for p in pts]
    gravs = [p[0] * p[1] for p in pts]
    self_ok = all(abs(g - o * c) < 1e-9 for (o, c), g in zip(pts, gravs))
    off_m, off_sd1 = m(offs), sd1(offs)
    cos_m = m(coss)
    grav_m, grav_sd0 = m(gravs), sd0(gravs)
    recalc[day] = dict(n=len(pts), off_m=off_m, off_sd=off_sd1, cos=cos_m, grav_m=grav_m, grav_sd=grav_sd0)
    p = paper[day]
    flag = []
    if p['off_sd'] is not None and abs(p['off_sd'] - off_sd1) > 0.001: flag.append('SD1改')
    if dif(p['off_m'], off_m): flag.append('off改')
    if dif(p['cos'], cos_m): flag.append('cos改')
    if dif(p['grav_m'], grav_m): flag.append('grav改')
    if p['grav_sd'] is not None and abs(p['grav_sd'] - grav_sd0) > 0.001: flag.append('gSD0改')
    fstr = ','.join(flag) if flag else '—'
    print(f"{day:<5}{len(pts):>3} | {off_m:9.4f} {off_sd1:6.4f} | {cos_m:8.4f} | {grav_m:10.4f} {grav_sd0:6.4f} | 自洽={self_ok}  {'<< '+fstr if flag else ''}")

print()
print('== 各日 gravity 逐点（cos×offset 公式值）==')
for day, pts in DAYS:
    gs = [f"{o}×{c}={o*c:.4f}" for o, c in pts]
    print(f"{day}: " + "; ".join(gs[:4]) + (' ...' if len(gs) > 4 else ''))

print()
print('== 结论：表4.1.1 需修正项 ==')
for day in ['7/19', '7/20', '7/21', '7/22', '7/23']:
    p, r = paper[day], recalc[day]
    chg = []
    for k, lab in [('off_m', 'offset均值'), ('off_sd', 'offset SD1'), ('cos', 'cos均值'),
                   ('grav_m', 'gravity均值'), ('grav_sd', 'gravity SD0')]:
        if dif(p.get(k, 0), r.get(k, 0)):
            chg.append(f"{lab}: {p.get(k):.3f}→{r[k]:.3f}")
    print(f"{day}: {'; '.join(chg) if chg else '无需修改'}")
