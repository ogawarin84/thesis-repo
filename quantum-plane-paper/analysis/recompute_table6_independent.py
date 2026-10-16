# -*- coding: utf-8 -*-
"""独立重算表B.2权威均值 + 派生公式交叉验证（不依赖任何中间文件）

数据源：
  R1/R5/R6 = 0727最终版（十批次统一汇总表_完整40变量_最终版.md）
  R2/R3/R4 = 我最爱rin_40vars_table.md（0730修复版）
口径：
  R3 均值剔除 B1/B5/B8（因子代理执行异常）
  R6 batch1 用 0.78（0727 权威值）
  0727 beta(v07) 为独立采样值；0730 v07_beta=offset（两轮定义不同，如实分别取值）

输出：逐批数值表 + 12指标×6组均值 + 派生公式校验 + 论文现值 vs 权威值差异
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import numpy as np

F0730 = r'C:\Users\Home\Desktop\理论生成汇总\0730理论生成汇总\我最爱rin_40vars_table.md'
F0727 = r'C:\Users\Home\Desktop\理论生成汇总\0727理论生成汇总\十批次统一汇总表_完整40变量_最终版.md'

def fl(x):
    if x is None: return None
    x = str(x).strip().replace('**','').replace('*','')
    if x in ('N/A','—','∞','', '-', 'nan', 'N/A'): return None
    try: return float(x)
    except: return None

# ==================== 解析 0730（R2/R3/R4/R5）====================
# p[0]=Batch p[1]=Cond p[2]=v01 ... p[40]=v40（v06缺位，p[7]=v07）
def parse730():
    rec = {}
    for ln in open(F0730, encoding='utf-8'):
        if not ln.startswith('|'): continue
        p = [c.strip().replace('**','') for c in ln.strip().strip('|').split('|')]
        if len(p) < 41 or p[1] not in ('R2','R3','R4','R5') or p[0] == 'Batch': continue
        try: b = int(p[0])
        except: continue
        rec[(b, p[1])] = {
            'offset': fl(p[2]), 'confusion': fl(p[3]), 'temp': fl(p[4]), 'defense': fl(p[5]), 'color': fl(p[6]),
            'beta': fl(p[7]), 'eta': fl(p[8]), 'kappa': fl(p[9]), 'R_root': fl(p[10]), 'P_basin': fl(p[11]), 'epsilon': fl(p[12]),
            'v13': fl(p[13]), 'v14': fl(p[14]), 'v15': fl(p[15]), 'v16': fl(p[16]), 'v17': fl(p[17]), 'v18': fl(p[18]), 'v19': fl(p[19]),
            'w': [fl(p[20+i]) for i in range(7)],
            'g': [fl(p[27+i]) for i in range(7)],
            'eigen': fl(p[34]), 'stability': fl(p[35]), 'rank': fl(p[36]), 'geo': fl(p[37]),
            'cos_rin': fl(p[38]), 'cos_gen': fl(p[39]), 'gravity': fl(p[40]),
        }
    return rec
d730 = parse730()

# ==================== 解析 0727（R1/R5/R6，六分节）====================
def parse727():
    rec = {}; cur = None
    for ln in open(F0727, encoding='utf-8'):
        s = ln.strip()
        if s.startswith('## '):
            cur = ('core' if '核心变量' in s else 'dyn' if '动力学' in s else 'proxy' if '代理指标' in s
                   else 'w' if '七维基' in s else 'g' if '度规张量' in s else 'spec' if '本征谱' in s else None)
            continue
        if not s.startswith('|') or cur is None: continue
        p = [c.strip().replace('**','') for c in s.strip('|').split('|')]
        if len(p) < 3 or not p[0].startswith('batch'): continue
        import re
        m = re.search(r'(\d+)', p[0])
        if not m: continue
        b, c = int(m.group(1)), p[1]
        if c not in ('R1','R5','R6'): continue
        d = rec.setdefault((b,c), {})
        if cur == 'core':
            for k, i in [('offset',2),('confusion',3),('temp',4),('defense',5),('color',6),('cos_rin',7),('cos_gen',8),('gravity',9)]:
                if i < len(p): d[k] = fl(p[i])
        elif cur == 'dyn':
            for k, i in [('beta',2),('eta',3),('kappa',4),('R_root',5),('P_basin',6),('epsilon',7)]:
                if i < len(p): d[k] = fl(p[i])
        elif cur == 'proxy':
            for k, i in [('v13',2),('v14',3),('v15',4),('v16',5),('v17',6),('v18',7),('v19',8)]:
                if i < len(p): d[k] = fl(p[i])
        elif cur == 'w':
            d['w'] = [fl(p[2+i]) for i in range(7)]
        elif cur == 'g':
            d['g'] = [fl(p[2+i]) for i in range(7)]
        elif cur == 'spec':
            for k, i in [('eigen',2),('stability',3),('rank',4),('geo',5)]:
                if i < len(p): d[k] = fl(p[i])
    return rec
d727 = parse727()

RS = ['R1','R2','R3','R4','R5','R6']
def src(r):
    return d727 if r in ('R1','R5','R6') else d730

# ==================== 完整行数检查 ====================
print('=== 行数检查（每轮应 10 批）===')
for r in RS:
    keys = sorted([b for (b,cc) in src(r) if cc == r])
    print('%s: %d 批 %s' % (r, len(keys), keys))
print()

# ==================== 表B.2 12指标 逐批输出 ====================
M6_METRICS = ['offset','confusion','temp','defense','beta','kappa','R_root','P_basin','cos_rin','cos_gen','gravity','geo']
R3_EXCLUDE = {1,5,8}  # R3 剔除 batch1/batch5/batch8

def per_batch(r, metric):
    """返回 [(batch, val)]，按 batch 升序"""
    out = []
    for b in range(1, 11):
        d = src(r).get((b, r), {})
        out.append((b, d.get(metric)))
    return out

def mean_vals(r, metric):
    vals = [v for (_, v) in per_batch(r, metric) if v is not None]
    if r == 'R3':  # 剔除 B1/B5/B8
        pb = per_batch(r, metric)
        vals = [v for (b, v) in pb if v is not None and b not in R3_EXCLUDE]
    if not vals: return None
    return float(np.mean(vals)), float(np.std(vals, ddof=1)) if len(vals) > 1 else None, len(vals)

print('=== 表B.2 12指标 逐批 + 均值（R6 batch1=0.78 已含；R3剔除B1/B5/B8）===')
AUTH = {}
for metric in M6_METRICS:
    print()
    print('## %s' % metric)
    hdr = '  批次: '
    for b in range(1, 11): hdr += '%6d' % b
    print(hdr)
    for r in RS:
        row = '  %s: ' % r
        for (b, v) in per_batch(r, metric):
            row += ('%6.3f' % v) if v is not None else '    --'
        mn = mean_vals(r, metric)
        if mn:
            AUTH[(metric, r)] = mn[0]
            row += '  均值=%.3f  sd=%.3f  n=%d' % (mn[0], mn[1] if mn[1] else 0, mn[2])
        print(row)

# ==================== 论文表B.2现值 vs 权威值 ====================
# ⚠️ 下面的 P 是 2026-08-17 改写前的论文快照（before 侧），保留作改动依据，勿更新。
#    它不是"论文现值"，与权威值有差异属预期。活体核对请用 verify_paper_after_update.py。
P = {
 'offset':  [0.698, 0.183, 0.100, 0.640, 0.661, 0.686],
 'confusion':[0.10, 0.654, 0.380, 0.267, 0.22, 0.18],
 'temp':    [0.65, 0.350, 0.263, 0.730, 0.58, 0.55],
 'defense': [0.08, 0.078, 0.030, 0.732, 0.15, 0.12],
 'beta':    [0.62, 0.183, 0.100, 0.640, 0.55, 0.52],
 'kappa':   [1.25, 1.593, None, 4.789, 0.58, 0.62],
 'R_root':  [0.64, 0.654, 0.381, 0.267, 0.62, 0.58],
 'P_basin': [0.82, 0.073, 0.058, 0.481, 0.72, 0.75],
 'cos_rin': [0.543, 0.381, 0.405, 0.400, 0.599, 0.651],
 'cos_gen': [0.453, 0.502, 0.482, 0.493, 0.494, 0.371],
 'gravity': [None, 0.069, 0.042, 0.256, None, None],
 'geo':     [0.35, 0.433, 0.368, 1.622, 0.38, 0.32],
}
print()
print('=== 表B.2 权威均值 vs 论文现值 差异检查 ===')
for metric in M6_METRICS:
    diffs = []
    for i, r in enumerate(RS):
        pv = P[metric][i]
        av = AUTH.get((metric, r))
        if pv is not None and av is not None and abs(pv - av) > 0.011:
            diffs.append('%s:论文%.3f→权威%.3f' % (r, pv, av))
    print('%-9s %s' % (metric, ('; '.join(diffs) if diffs else '全部一致')))

# ==================== 派生公式交叉验证 ====================
print()
print('=== 派生公式交叉验证（检查源文件"客观重算"列是否自洽）===')
def check_formulas(r):
    srcs = [d for (b,cc), d in src(r).items() if cc == r]
    issues = []
    for (b,cc), d in sorted(src(r).items()):
        if cc != r: continue
        tag = 'b%d-%s' % (b, cc)
        # 0730: v07_beta 应 = offset
        if r in ('R2','R3','R4') and d['offset'] is not None and d['beta'] is not None:
            if abs(d['offset'] - d['beta']) > 1e-4: issues.append('%s v07_beta=%.4f≠offset=%.4f' % (tag, d['beta'], d['offset']))
        # 0727: beta 是独立值，不检查（记录即可）
        # v11_P_basin = offset*(1-confusion)
        if d['offset'] is not None and d['confusion'] is not None and d['P_basin'] is not None:
            exp = d['offset'] * (1 - d['confusion'])
            if abs(d['P_basin'] - exp) > 5e-3: issues.append('%s P_basin=%.4f≠offset*(1-conf)=%.4f' % (tag, d['P_basin'], exp))
        # v27-g33 = w²
        if d['w'] and d['g'] and all(v is not None for v in d['w'] + d['g']):
            for i in range(7):
                if abs(d['g'][i] - d['w'][i]**2) > 1e-3:
                    issues.append('%s g%d=%s≠w%d²=%s' % (tag, i+1, d['g'][i], i+1, d['w'][i]**2))
                    break
        # v34_eigen = max(g)
        if d['g'] and all(v is not None for v in d['g']) and d['eigen'] is not None:
            if abs(d['eigen'] - max(d['g'])) > 1e-3: issues.append('%s eigen=%.4f≠max(g)=%.4f' % (tag, d['eigen'], max(d['g'])))
        # v35_stability = max(g)/sum(g)
        if d['g'] and all(v is not None for v in d['g']) and sum(d['g']) > 0 and d['stability'] is not None:
            exp = max(d['g']) / sum(d['g'])
            if abs(d['stability'] - exp) > 1e-3: issues.append('%s stability=%.4f≠max/sum=%.4f' % (tag, d['stability'], exp))
        # v37_geo = sqrt(sum(w²))
        if d['w'] and all(v is not None for v in d['w']) and d['geo'] is not None:
            exp = sum(v**2 for v in d['w'])**0.5
            if abs(d['geo'] - exp) > 1e-3: issues.append('%s geo=%.4f≠√Σw²=%.4f' % (tag, d['geo'], exp))
        # v40_gravity = cos_rin*offset
        if d['cos_rin'] is not None and d['offset'] is not None and d['gravity'] is not None:
            exp = d['cos_rin'] * d['offset']
            if abs(d['gravity'] - exp) > 5e-3: issues.append('%s gravity=%.4f≠cos_rin*off=%.4f' % (tag, d['gravity'], exp))
        # v10_R_root = 1/kappa（仅 0727 有此公式）
        if r in ('R1','R5','R6') and d['kappa'] is not None and d['R_root'] is not None and d['kappa'] > 0:
            if abs(d['R_root'] - 1.0/d['kappa']) > 5e-3: issues.append('%s R_root=%.4f≠1/κ=%.4f' % (tag, d['R_root'], 1.0/d['kappa']))
    print('%s: %d 处违反' % (r, len(issues)))
    for i in issues[:15]: print('   ', i)

for r in RS:
    check_formulas(r)
print()
print('注：上述"违反"仅为源文件公式自洽检查，用于排查数据录入错误；均值为原始值直接计算。')
