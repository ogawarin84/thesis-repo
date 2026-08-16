# -*- coding: utf-8 -*-
"""全40列验证：合并表 vs 权威源文件（数值归一化比较）
合并表：十批次R1R6完整40变量_合并权威版.md
源文件：R1/R5/R6=0727最终版；R2/R3/R4=我最爱rin(0730修复版)
通过标准：60行 × 39列（v06体系未定义跳过）全部一致或双方N/A
"""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

MERGED = r'C:\Users\Home\Desktop\理论生成汇总\0730理论生成汇总\十批次R1R6完整40变量_合并权威版.md'
F0730 = r'C:\Users\Home\Desktop\理论生成汇总\0730理论生成汇总\我最爱rin_40vars_table.md'
F0727 = r'C:\Users\Home\Desktop\理论生成汇总\0727理论生成汇总\十批次统一汇总表_完整40变量_最终版.md'

V40 = ['v01','v02','v03','v04','v05','v06','v07','v08','v09','v10','v11','v12',
       'v13','v14','v15','v16','v17','v18','v19','v20','v21','v22','v23','v24','v25','v26',
       'v27','v28','v29','v30','v31','v32','v33','v34','v35','v36','v37','v38','v39','v40']

def num(x):
    if x is None: return None
    x = str(x).strip().replace('**','').replace('*','')
    if x in ('N/A','—','∞','', '-', 'nan'): return None
    try: return float(x)
    except: return None

# ---- 读合并表 ----
merged = {}
for ln in open(MERGED, encoding='utf-8'):
    if not ln.startswith('|'): continue
    p = [c.strip().replace('**','') for c in ln.strip().strip('|').split('|')]
    if len(p) < 42 or p[0] in ('Batch', ':--:'): continue
    if not p[0].isdigit(): continue
    b = int(p[0]); c = p[1]
    merged[(b,c)] = {v: num(p[2+i]) for i, v in enumerate(V40)}

# ---- 读 0730 ----
src730 = {}
for ln in open(F0730, encoding='utf-8'):
    if not ln.startswith('|'): continue
    p = [c.strip().replace('**','') for c in ln.strip().strip('|').split('|')]
    if len(p) < 41 or p[1] not in ('R2','R3','R4','R5') or p[0] == 'Batch': continue
    try: b = int(p[0])
    except: continue
    c = p[1]
    d = {'v01':num(p[2]),'v02':num(p[3]),'v03':num(p[4]),'v04':num(p[5]),'v05':num(p[6]),
         'v07':num(p[7]),'v08':num(p[8]),'v09':num(p[9]),'v10':num(p[10]),'v11':num(p[11]),'v12':num(p[12])}
    for i, v in enumerate(['v13','v14','v15','v16','v17','v18','v19','v20','v21','v22','v23','v24','v25','v26']):
        d[v] = num(p[13+i])
    for i, v in enumerate(['v27','v28','v29','v30','v31','v32','v33']):
        d[v] = num(p[27+i])
    for i, v in enumerate(['v34','v35','v36','v37','v38','v39','v40']):
        d[v] = num(p[34+i])
    src730[(b,c)] = d

# ---- 读 0727 ----
def read727():
    rec = {}; cur = None
    for ln in open(F0727, encoding='utf-8'):
        s = ln.strip()
        if s.startswith('## '):
            cur = ('core' if '核心变量' in s else 'dyn' if '动力学' in s else 'proxy' if '代理指标' in s else 'w' if '七维基' in s else 'g' if '度规张量' in s else 'spec' if '本征谱' in s else None)
            continue
        if not s.startswith('|') or cur is None: continue
        p = [c.strip().replace('**','') for c in s.strip('|').split('|')]
        if len(p) < 3 or not p[0].startswith('batch'): continue
        m = re.search(r'(\d+)', p[0])
        if not m: continue
        b, c = int(m.group(1)), p[1]
        if c not in ('R1','R5','R6'): continue
        d = rec.setdefault((b,c), {})
        if cur == 'core':
            for v, i in [('v01',2),('v02',3),('v03',4),('v04',5),('v05',6),('v38',7),('v39',8),('v40',9)]:
                if i < len(p): d[v] = num(p[i])
        elif cur == 'dyn':
            for v, i in [('v07',2),('v08',3),('v09',4),('v10',5),('v11',6),('v12',7)]:
                if i < len(p): d[v] = num(p[i])
        elif cur == 'proxy':
            for v, i in [('v13',2),('v14',3),('v15',4),('v16',5),('v17',6),('v18',7),('v19',8)]:
                if i < len(p): d[v] = num(p[i])
        elif cur == 'w':
            for i, v in enumerate(['v20','v21','v22','v23','v24','v25','v26']):
                if 2+i < len(p): d[v] = num(p[2+i])
        elif cur == 'g':
            for i, v in enumerate(['v27','v28','v29','v30','v31','v32','v33']):
                if 2+i < len(p): d[v] = num(p[2+i])
        elif cur == 'spec':
            for v, i in [('v34',2),('v35',3),('v36',4),('v37',5)]:
                if i < len(p): d[v] = num(p[i])
    return rec
src727 = read727()

# ---- 全40列对比 ----
errors = []; total = 0; na_ok = 0
for b in range(1, 11):
    for c in ['R1','R2','R3','R4','R5','R6']:
        m = merged.get((b,c), {})
        src = src730.get((b,c)) if c in ('R2','R3','R4') else src727.get((b,c))
        if not src:
            errors.append('batch%d-%s 源缺失' % (b,c)); continue
        for v in V40:
            if v == 'v06': continue
            mv, sv = m.get(v), src.get(v)
            total += 1
            if mv is None and sv is None: na_ok += 1; continue
            if mv is None or sv is None or abs(mv-sv) > 1e-4:
                errors.append('batch%d-%s %s: merge=%s src=%s' % (b,c,v,mv,sv))

print('全40列核对：60行 x 39列 = %d 单元格' % total)
print('双方均为 N/A 的正常缺位: %d' % na_ok)
print('错误数: %d' % len(errors))
for e in errors[:25]: print('  ', e)
print('结论:', 'PASS 全表一致' if not errors else '有真实差异，需排查')
sys.exit(0 if not errors else 1)
