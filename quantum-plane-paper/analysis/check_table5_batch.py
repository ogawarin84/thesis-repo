# -*- coding: utf-8 -*-
"""表B.1逐批offset vs 0727 & 0730 全对比，定位R4来源（按batch号排序）"""
import io, sys, numpy as np, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

f0727 = r'C:\Users\Home\Desktop\理论生成汇总\0727理论生成汇总\十批次统一汇总表_完整40变量_最终版.md'
f0730 = r'C:\Users\Home\Desktop\理论生成汇总\0730理论生成汇总\新10批次R2-R5实验数据.md'

def fl(x):
    if x is None: return None
    x = str(x).replace('**','').replace('*','').strip()
    if x in ('N/A','—','∞','','-'): return None
    try: return float(x)
    except: return None

paper = {
 'R1':[0.62,0.65,0.58,0.60,0.82,0.68,0.58,0.58,0.92,0.95],
 'R2':[0.28,0.22,0.08,0.18,0.25,0.00,0.34,0.18,0.15,0.15],
 'R3':[0.50,0.11,0.20,0.18,0.82,0.00,0.00,0.50,0.06,0.15],
 'R4':[0.72,0.68,0.42,0.88,0.44,0.72,0.78,0.96,0.38,0.42],
 'R5':[0.82,0.55,0.55,0.52,0.68,0.72,0.70,0.75,0.60,0.72],
 'R6':[0.78,0.75,0.78,0.74,0.50,0.72,0.72,0.65,0.60,0.65],
}
RS = ['R1','R2','R3','R4','R5','R6']

def get_batch(label):
    m = re.search(r'batch(\d+)', label.lower())
    return int(m.group(1)) if m else 99

# 0727 core表 offset (col0), 按batch排序
rows727 = {r:{} for r in RS}
for ln in open(f0727, encoding='utf-8'):
    s = ln.strip()
    if s.startswith('## '):
        cur = 'core' if '核心变量' in s else None
        continue
    if not s.startswith('|') or cur!='core': continue
    parts = [c.strip() for c in s.strip('|').split('|')]
    if len(parts)<3 or not parts[0].lower().startswith('batch'): continue
    r = parts[1]
    if r in RS: rows727[r][get_batch(parts[0])] = fl(parts[2])

off727 = {r: [rows727[r][b] for b in range(1,11)] for r in RS}

# 0730 offset (col2)
rows730 = {r:{} for r in RS}
for ln in open(f0730, encoding='utf-8'):
    if not ln.startswith('|'): continue
    parts = [c.strip() for c in ln.strip().strip('|').split('|')]
    if len(parts)<3 or parts[1] not in RS: continue
    rows730[parts[1]][get_batch(parts[0])] = fl(parts[2])
off730 = {r: [rows730[r].get(b) for b in range(1,11)] for r in RS}

for r in RS:
    print('=== %s ===' % r)
    print('  论文: ', ' '.join('%.2f'%x for x in paper[r]))
    print('  0727: ', ' '.join(('%.2f'%x) if x is not None else 'N/A' for x in off727[r]))
    print('  0730: ', ' '.join(('%.2f'%x) if x is not None else 'N/A' for x in off730[r]))
    m727 = float(np.mean([x for x in off727[r] if x is not None]))
    m730 = float(np.mean([x for x in off730[r] if x is not None]))
    print('  均值 论文=%.3f  0727=%.3f  0730=%.3f' % (np.mean(paper[r]), m727, m730))
    print()
