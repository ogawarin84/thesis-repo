# -*- coding: utf-8 -*-
"""论文表4.1.4（主会话 vs ISO R4 五指标）权威数据源核验脚本。

数据源：
1) 主会话 33 点原始值：论文《量子平面概率动力学模型_完整版_ver5》附录D 表11（29点, 07-19~07-22）
   + 表12（4点, 07-23 三步法）。offset/cos/gravity 共33点；confusion/temp 仅表11有，29点。
2) 权威 R4 十批统计：合并权威表《十批次R1R6完整40变量_合并权威版.md》v01/v02/v03/v38/v40 列。

输出：五指标主会话均值±SD、R4均值±SD、pooled SD、Cohen's d（与论文表4.1.4 一致）。

用法：python verify_table4_1_4_d.py <论文路径> <合并权威表路径>
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import numpy as np

PAPER = sys.argv[1] if len(sys.argv) > 1 else r'C:\Users\Home\Desktop\理论生成汇总\0802理论生成汇总\量子平面概率动力学模型_完整版_ver5（mine）.md'
MERGED = sys.argv[2] if len(sys.argv) > 2 else r'C:\Users\Home\Desktop\理论生成汇总\0730理论生成汇总\十批次R1R6完整40变量_合并权威版.md'

def num(x):
    x = str(x).strip().replace('**', '')
    if x in ('—', 'N/A', '∞', ''):
        return None
    try:
        return float(x)
    except ValueError:
        return None

# ---------- 1) 主会话 ----------
lines = open(PAPER, encoding='utf-8').read().split('\n')
main = {'offset': [], 'confusion': [], 'temp': [], 'cos': [], 'gravity': []}

# 表11: 时间戳 offset confusion temp defense beta kappa cos gravity geodesic
# 定位表11标题行
for i, ln in enumerate(lines):
    if '表11' in ln and '0719-0723' in ln:
        start = i + 2  # 跳过标题+分隔行
        break
for i in range(start, min(start + 40, len(lines))):
    s = lines[i].strip()
    if not s.startswith('|') or s.startswith('|:--'):
        continue
    if '时间戳' in s:
        continue
    p = [c.strip() for c in s.strip('|').split('|')]
    if len(p) < 9:
        break
    o, c, t = num(p[1]), num(p[2]), num(p[3])
    cs, g = num(p[7]), num(p[8])
    for k, v in [('offset', o), ('confusion', c), ('temp', t), ('cos', cs), ('gravity', g)]:
        if v is not None:
            main[k].append(v)
    if o is None:
        break

# 表12: 时间戳 offset step1 step2 step3 delta cos gravity
for i, ln in enumerate(lines):
    if '表12' in ln and '0723' in ln:
        start = i + 2
        break
for i in range(start, min(start + 15, len(lines))):
    s = lines[i].strip()
    if not s.startswith('|') or s.startswith('|:--'):
        continue
    if '时间戳' in s:
        continue
    p = [c.strip() for c in s.strip('|').split('|')]
    if len(p) < 8:
        break
    o, cs, g = num(p[1]), num(p[6]), num(p[7])
    for k, v in [('offset', o), ('cos', cs), ('gravity', g)]:
        if v is not None:
            main[k].append(v)
    if o is None:
        break

# ---------- 2) 权威 R4 ----------
r4 = {'offset': [], 'confusion': [], 'temp': [], 'cos': [], 'gravity': []}
for ln in open(MERGED, encoding='utf-8'):
    if not ln.startswith('|'):
        continue
    p = [c.strip().replace('**', '') for c in ln.strip('|').split('|')]
    if len(p) < 42 or p[1] != 'R4':
        continue
    for k, idx in [('offset', 2), ('confusion', 3), ('temp', 4), ('cos', 39), ('gravity', 41)]:
        v = num(p[idx])
        if v is not None:
            r4[k].append(v)

# ---------- 3) 计算 ----------
print('=== 主会话（附录D 表11+表12）vs 权威R4 ===')
print('%-9s %-22s %-20s %-10s %-8s' % ('指标', '主会话', 'R4', 'pooled SD', 'd'))
ok = True
expected = {
    'offset':   ('0.8552±0.0644', '0.640±0.210', 'd=1.89'),
    'temp':     ('0.7562±0.0669', '0.730±0.153', 'd=0.28'),
    'confusion':('0.0452±0.0127', '0.267±0.108', 'd=−4.10'),
    'cos':      ('0.8461±0.0397', '0.400±0.040', 'd=11.21'),
    'gravity':  ('0.7253±0.0803', '0.256±0.093', 'd=5.64'),
}
for k in ['offset', 'temp', 'confusion', 'cos', 'gravity']:
    a = np.array(main[k]); b = np.array(r4[k])
    n1, n2 = a.size, b.size
    s1, s2 = a.std(ddof=1), b.std(ddof=1)
    sp = np.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / (n1 + n2 - 2))
    d = (a.mean() - b.mean()) / sp
    print('%-9s n=%2d %.4f±%.4f | n=%d %.4f±%.4f | %.4f | %+.2f'
          % (k, n1, a.mean(), s1, n2, b.mean(), s2, sp, d))
    # 对照论文表4.1.4
    exp_main, exp_r4, exp_d = expected[k]
    e1, e2 = exp_main.split('±'); e3, e4 = exp_r4.split('±')
    if not (abs(a.mean() - float(e1)) < 0.001 and abs(s1 - float(e2)) < 0.001
            and abs(b.mean() - float(e3)) < 0.001 and abs(s2 - float(e4)) < 0.001):
        print('  !! 主会话/R4 与论文不符'); ok = False
    if not (abs(d - float(exp_d.replace('d=', '').replace('−', '-'))) < 0.03):
        print('  !! d 与论文不符（论文 %s）' % exp_d); ok = False

print()
print('结论:', 'PASS：五指标主会话统计与权威R4全部与论文表4.1.4一致' if ok else 'FAIL')
sys.exit(0 if ok else 1)
