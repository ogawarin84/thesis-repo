# -*- coding: utf-8 -*-
"""论文ver5(mine)更新后交叉验证：
1) 表6 12行×6列 vs table6_authoritative.json（权威）
2) 表4.4.1 R6统计 vs recompute_statistics.py 权威值
3) 表4.4.2 三对比 vs 权威
4) 确认 cos_sim_user 旧术语不再出现在实验二范围
"""
import sys, io, json, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

F = r'C:\Users\Home\Desktop\理论生成汇总\0802理论生成汇总\量子平面概率动力学模型_完整版_ver5（mine）.md'
AUTH = r'C:\Users\Home\Documents\xhh-paper\quantum-plane-paper\analysis\table6_authoritative.json'
text = open(F, encoding='utf-8').read()
lines = text.split('\n')
auth = json.load(open(AUTH, encoding='utf-8'))

def num(x):
    x = str(x).strip().replace('**','').replace('*','').replace('†','').replace('‡','')
    if x in ('—','N/A','∞',''): return None
    try: return float(x)
    except: return None

errs = []
# ---- 1) 表6 ----
# 定位表6行
t6 = {}
for i, ln in enumerate(lines):
    if ln.strip() == '**表6 六组条件核心40维指标均值汇总**':
        start = i+3  # 跳表头两行
        for j in range(start, start+12):
            p = [c.strip().replace('**','') for c in lines[j].strip().strip('|').split('|')]
            if len(p) < 7: continue
            t6[p[0]] = {r: p[k] for k, r in enumerate(['R1','R2','R3','R4','R5','R6'], start=1)}
        break
else:
    errs.append('找不到表6标题')

def key(metric):
    return {'offset_actual':'offset','temperature':'temp','geodesic_distance':'geo','cos_sim_rin':'cos_rin','cos_sim_generic':'cos_gen','gravity_strength':'gravity'}.get(metric, metric)

for metric, rows in t6.items():
    for r in ['R1','R2','R3','R4','R5','R6']:
        paper_v = num(rows[r])
        auth_v = num(auth.get('%s|%s' % (key(metric), r)))
        if metric == 'kappa' and r == 'R3':
            if rows[r] != '—':
                errs.append('表6 kappa R3 应为"—"，实际 %s' % rows[r])
            continue
        if paper_v is None or auth_v is None:
            if paper_v != auth_v: errs.append('表6 %s %s: paper=%s auth=%s' % (metric, r, rows[r], auth.get('%s|%s'%(key(metric),r))))
        elif abs(paper_v - auth_v) > 1e-9:
            errs.append('表6 %s %s: paper=%s auth=%s' % (metric, r, rows[r], auth['%s|%s'%(key(metric),r)]))
print('表6: %d 行已解析，交叉核对完成' % len(t6))

# ---- 2) 表4.4.1 R6 ----
# 权威：mean=0.689 sd=0.089 se=0.028 CI=[0.625,0.753] 范围0.50-0.78
found = [l for l in lines if l.strip().startswith('| R6（完整+自锚有文本） |')]
if found:
    p = [c.strip() for c in found[0].strip().strip('|').split('|')]
    exp = ['0.689','0.089','0.028','[0.625, 0.753]','0.50–0.78']
    got = [p[1],p[2],p[3],p[4],p[5]]
    for e, g in zip(exp, got):
        if e != g: errs.append('表4.4.1 R6: 期望 %s 实得 %s' % (e, g))
else:
    errs.append('找不到表4.4.1 R6行')

# ---- 3) 表4.4.2 ----
exp_pairs = [
    ('R5（保留认知结构+自锚）vs R1（完整+外锚）', ['−0.037','−0.666','0.514','−0.30']),
    ('R6（完整+自锚）vs R1（完整+外锚）', ['−0.009','−0.168','0.869','−0.07']),
    ('R5 vs R6（自锚用户文本效应）', ['−0.028','−0.660','0.517','−0.30']),
]
for name, exp in exp_pairs:
    hit = [l for l in lines if l.strip().startswith('| %s |' % name)]
    if not hit:
        errs.append('表4.4.2 缺行: %s' % name); continue
    p = [c.strip() for c in hit[0].strip().strip('|').split('|')]
    got = p[1:5]
    for e, g in zip(exp, got):
        if e != g: errs.append('表4.4.2 %s: 期望 %s 实得 %s' % (name, e, g))

# ---- 4) 旧术语 ----
# 实验二范围（行1494附录B 到附录C前）不应再有 cos_sim_user / cos_sim_用户
in_appendix_b = False; bad_term = []
for ln in lines:
    if '### 附录B' in ln: in_appendix_b = True
    elif '### 附录C' in ln: in_appendix_b = False
    if in_appendix_b and re.search(r'cos_sim_user|cos_sim_用户|cos_sim_\u7528\u6237', ln):
        bad_term.append(ln.strip()[:60])
if bad_term:
    errs.append('附录B仍有旧术语: %s' % bad_term)

# 表6注释存在
if '两轮同名列口径不同' not in text:
    errs.append('表6口径注释缺失')

print('=== 验证结果 ===')
if errs:
    print('发现 %d 处不一致:' % len(errs))
    for e in errs: print('  ', e)
    sys.exit(1)
print('全部通过：表6 12行×6列、表4.4.1 R6、表4.4.2 三对比、术语统一、口径注释 均与权威一致。')
