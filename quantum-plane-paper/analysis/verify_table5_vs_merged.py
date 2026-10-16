# -*- coding: utf-8 -*-
"""论文表B.1（10批×6组 offset 原始值）vs 合并权威表 v01 列，逐格核对
注意：论文表B.1中 R3 的 † 标记批次（B1/B5/B8）值与合并表一致（仍是原值，剔除仅影响均值）。
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PAPER = r'C:\Users\Home\Desktop\理论生成汇总\0802理论生成汇总\量子平面概率动力学模型_完整版_ver5（mine）.md'
MERGED = r'C:\Users\Home\Desktop\理论生成汇总\0730理论生成汇总\十批次R1R6完整40变量_合并权威版.md'

def num(x):
    x = str(x).strip().replace('**','').replace('†','').replace('‡','')
    if x in ('—','N/A','∞',''): return None
    try: return float(x)
    except: return None

# 合并表 v01 (offset)
mv = {}
for ln in open(MERGED, encoding='utf-8'):
    if not ln.startswith('|'): continue
    p = [c.strip().replace('**','') for c in ln.strip().strip('|').split('|')]
    if len(p) < 4 or p[0] in ('Batch',':--:'): continue
    try: b = int(p[0])
    except: continue
    mv[(b,p[1])] = num(p[2])  # v01

# 论文表B.1
pv = {}
in_t5 = False
for ln in open(PAPER, encoding='utf-8'):
    s = ln.strip()
    if '**表B.1' in s: in_t5 = True; continue
    if in_t5 and ('**表B.2' in s or '### 附录' in s): in_t5 = False
    if not in_t5 or not s.startswith('|'): continue
    p = [c.strip() for c in s.strip('|').split('|')]
    if not p[0].startswith('Batch'): continue
    try: b = int(p[0].replace('Batch',''))
    except: continue
    pv[b] = {r: num(p[1+i]) for i, r in enumerate(['R1','R2','R3','R4','R5','R6'])}
    if b == 10: in_t5 = False

errs = []
for b in range(1,11):
    for r in ['R1','R2','R3','R4','R5','R6']:
        a, c = pv.get(b,{}).get(r), mv.get((b,r))
        if a is None or c is None:
            if a != c: errs.append('B%d-%s: paper=%s merge=%s' % (b,r,a,c))
        elif abs(a-c) > 1e-9:
            errs.append('B%d-%s: paper=%s merge=%s' % (b,r,a,c))

print('论文表B.1 offset 核对：60 格')
if errs:
    print('不一致 %d 处:' % len(errs))
    for e in errs: print('  ', e)
    sys.exit(1)
print('PASS：表B.1 全部 60 格与合并权威表 v01 列一致。')
