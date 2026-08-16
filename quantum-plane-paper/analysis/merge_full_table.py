# -*- coding: utf-8 -*-
"""合并权威完整表：batch1-10 x R1-R6 x 40维
数据源：R1/R5/R6 = 0727最终版, R2/R3/R4 = 我最爱rin(0730修复版)
输出：0730文件夹/十批次R1R6完整40变量_合并权威版.md"""
import re

F0730 = r'C:\Users\Home\Desktop\理论生成汇总\0730理论生成汇总\我最爱rin_40vars_table.md'
F0727 = r'C:\Users\Home\Desktop\理论生成汇总\0727理论生成汇总\十批次统一汇总表_完整40变量_最终版.md'
OUT = r'C:\Users\Home\Desktop\理论生成汇总\0730理论生成汇总\十批次R1R6完整40变量_合并权威版.md'

def fl(x):
    if x is None: return None
    x = str(x).strip().replace('**','').replace('*','')
    if x in ('N/A','—','∞','', '-'): return None
    try: return float(x)
    except: return None

# ============ 解析 0730 我最爱rin (单表40列) ============
# strip('|').split('|') 后 p[0]=Batch p[1]=Cond p[2..41]=v01..v40 (v06缺, v01=offset)
# 索引: v01=2 v02=3 v03=4 v04=5 v05=6 v07=7 v08=8 v09=9 v10=10 v11=11 v12=12
#       v13=13 v14=14 v15=15 v16=16 v17=17 v18=18 v19=19 v20=20 ... v26=26
#       v27=27 v28=28 v29=29 v30=30 v31=31 v32=32 v33=33 v34=34 v35=35 v36=36 v37=37 v38=38 v39=39 v40=40
COL0730 = {2:'v01',3:'v02',4:'v03',5:'v04',6:'v05',7:'v07',8:'v08',9:'v09',10:'v10',11:'v11',12:'v12',
           13:'v13',14:'v14',15:'v15',16:'v16',17:'v17',18:'v18',19:'v19',
           20:'v20',21:'v21',22:'v22',23:'v23',24:'v24',25:'v25',26:'v26',
           27:'v27',28:'v28',29:'v29',30:'v30',31:'v31',32:'v32',33:'v33',
           34:'v34',35:'v35',36:'v36',37:'v37',38:'v38',39:'v39',40:'v40'}
data = {}  # (batch, cond) -> {vNN: val}
for ln in open(F0730, encoding='utf-8'):
    if not ln.startswith('|'): continue
    p = [c.strip() for c in ln.strip().strip('|').split('|')]
    if len(p) < 41 or p[1] not in ('R2','R3','R4','R5'): continue
    if p[0] == 'Batch': continue
    try: b = int(p[0])
    except: continue
    d = {}
    for idx, vn in COL0730.items():
        d[vn] = fl(p[idx])
    data[(b, p[1])] = d

# ============ 解析 0727 最终版 (六分节) ============
def parse727(f):
    """返回 {(batch, cond): {vNN: val}}"""
    rec = {}
    cur = None
    for ln in open(f, encoding='utf-8'):
        s = ln.strip()
        if s.startswith('## '):
            if '核心变量' in s: cur = 'core'
            elif '动力学' in s: cur = 'dyn'
            elif '代理指标' in s: cur = 'proxy'
            elif '七维基向量' in s: cur = 'w'
            elif '度规张量' in s: cur = 'g'
            elif '本征谱' in s: cur = 'spec'
            else: cur = None
            continue
        if not s.startswith('|') or cur is None: continue
        p = [c.strip().replace('**','') for c in s.strip('|').split('|')]
        if len(p) < 4 or not p[0].startswith('batch'): continue
        m = re.search(r'(\d+)', p[0])
        if not m: continue
        b = int(m.group(1)); c = p[1]
        if c not in ('R1','R5','R6'): continue
        key = (b, c)
        d = rec.setdefault(key, {})
        if cur == 'core':
            for vn, idx in [('v01',2),('v02',3),('v03',4),('v04',5),('v05',6),('v38',7),('v39',8),('v40',9)]:
                if idx < len(p): d[vn] = fl(p[idx])
        elif cur == 'dyn':
            for vn, idx in [('v07',2),('v08',3),('v09',4),('v10',5),('v11',6),('v12',7)]:
                if idx < len(p): d[vn] = fl(p[idx])
        elif cur == 'proxy':
            for vn, idx in [('v13',2),('v14',3),('v15',4),('v16',5),('v17',6),('v18',7),('v19',8)]:
                if idx < len(p): d[vn] = fl(p[idx])
        elif cur == 'w':
            for i, vn in enumerate(['v20','v21','v22','v23','v24','v25','v26']):
                if 2+i < len(p): d[vn] = fl(p[2+i])
        elif cur == 'g':
            for i, vn in enumerate(['v27','v28','v29','v30','v31','v32','v33']):
                if 2+i < len(p): d[vn] = fl(p[2+i])
        elif cur == 'spec':
            for vn, idx in [('v34',2),('v35',3),('v36',4),('v37',5)]:
                if idx < len(p): d[vn] = fl(p[idx])
    return rec

d727 = parse727(F0727)

# ============ 合并 ============
# R1/R5/R6 -> 0727; R2/R3/R4 -> 0730
COND_ORDER = ['R1','R2','R3','R4','R5','R6']
VORDER = ['v01','v02','v03','v04','v05','v06','v07','v08','v09','v10','v11','v12',
          'v13','v14','v15','v16','v17','v18','v19','v20','v21','v22','v23','v24','v25','v26',
          'v27','v28','v29','v30','v31','v32','v33','v34','v35','v36','v37','v38','v39','v40']
VNAMES = {
 'v01':'offset','v02':'confusion','v03':'temperature','v04':'defense','v05':'color','v06':'(v06缺)',
 'v07':'beta','v08':'eta','v09':'kappa','v10':'R_root','v11':'P_basin','v12':'epsilon',
 'v13':'total_chars','v14':'rin_ratio','v15':'affect_density','v16':'uncertainty_density','v17':'defense_density',
 'v18':'exclamations','v19':'ellipsis','v20':'w1','v21':'w2','v22':'w3','v23':'w4','v24':'w5','v25':'w6','v26':'w7',
 'v27':'g11','v28':'g22','v29':'g33','v30':'g44','v31':'g55','v32':'g66','v33':'g77',
 'v34':'eigen_max','v35':'stability','v36':'rank','v37':'geodesic','v38':'cos_rin','v39':'cos_generic','v40':'gravity'}

def get_row(b, c):
    if c in ('R1','R5','R6'):
        src = d727.get((b, c), {})
    else:
        src = data.get((b, c), {})
    return {vn: src.get(vn, None) for vn in VORDER}

# ============ 生成 Markdown ============
lines = []
lines.append('# 十批次 R1-R6 完整 40 变量汇总表（合并权威版）')
lines.append('')
lines.append('> **生成**: 2026-08-17 | **数据源**: R1/R5/R6 = 0727十批次统一汇总表_完整40变量_最终版；R2/R3/R4 = 我最爱rin_40vars_table（0730修复版）')
lines.append('> **说明**: v06 原体系未定义（v01-v05 后直接 v07）；v05 color 为文本描述值；0727 batch3 的 v27-v33（g11-g77）原表为 N/A，此处保留；0727 batch7/8 的 R5/R6 g 列为原表独立值（非 w²）。')
lines.append('> **口径（两轮实验对派生指标定义不同，本表如实保留各源文件原值）**:')
lines.append('> - R2/R3/R4（0730 我最爱rin）：v07_beta=offset，v10_R_root=confusion（κ=1/max(confusion,0.01)），v11_P_basin=offset×(1-confusion)，v27-g33=w²，v40_gravity=cos_rin×offset')
lines.append('> - R1/R5/R6（0727 最终版）：v07_beta 为独立采样动力学值，v10_R_root=1/κ，v11_P_basin 为独立值，v27-g33=w²（batch7/8 的 R5/R6 除外），v40_gravity=cos_rin×offset')
lines.append('> - 同名列在两轮中的含义不同，跨轮次行内对比需注意口径。')
lines.append('')
hdr = '| Batch | Cond | ' + ' | '.join('%s (%s)' % (vn, VNAMES[vn]) for vn in VORDER) + ' |'
lines.append(hdr)
lines.append('|:--:|:--:|' + '|'.join(['---:']*40) + '|')
for b in range(1, 11):
    for c in COND_ORDER:
        row = get_row(b, c)
        cells = []
        for vn in VORDER:
            v = row[vn]
            if v is None:
                cells.append('N/A')
            elif isinstance(v, float) and v == int(v) and vn not in ('v36',):
                cells.append('%d' % v)
            else:
                cells.append(('%.4f' % v) if isinstance(v, float) else str(v))
        lines.append('| %d | %s | %s |' % (b, c, ' | '.join(cells)))
lines.append('')
open(OUT, 'w', encoding='utf-8').write('\n'.join(lines))
print('OK 写入', OUT)

# ============ 同时输出表6权威均值（含R6 batch1=0.78）============
def mean_of(vals):
    vals = [v for v in vals if v is not None]
    return sum(vals)/len(vals) if vals else None

# R1/R5/R6 均值来自 0727 各分节均值；R2/R3/R4 来自 我最爱rin
# 表6 指标映射
# 对 0730 数据直接取列均值；对 0727 需跨分节
M6 = {r: {} for r in ['R1','R2','R3','R4','R5','R6']}
# R1/R5/R6: 从 d727 聚合 (需按条件聚合10批)
agg727 = {}
for (b,c), d in d727.items():
    agg727.setdefault(c, []).append(d)
def m6_727(c, vn):
    vals = [d.get(vn) for d in agg727.get(c, [])]
    return mean_of(vals)
def m6_730(c, vn, excl3=False):
    vals = [data[(b,c)].get(vn) for b in range(1,11) if (b,c) in data]
    if excl3:  # R3 剔除 B1/B5/B8
        vals = [v for i, v in enumerate(vals) if i not in (0,4,7)]
    return mean_of(vals)

R3EX = {0,4,7}
for r in ['R1','R5','R6']:
    for vn in ['v01','v02','v03','v04','v07','v09','v10','v11','v37','v38','v39','v40']:
        M6[r][vn] = m6_727(r, vn)
for r in ['R2','R4']:
    for vn in ['v01','v02','v03','v04','v07','v09','v10','v11','v37','v38','v39','v40']:
        M6[r][vn] = m6_730(r, vn)
for vn in ['v01','v02','v03','v04','v07','v09','v10','v11','v37','v38','v39','v40']:
    M6['R3'][vn] = m6_730('R3', vn, excl3=True)

print()
print('=== 表6 权威均值（R6 batch1=0.78 已含；R3剔除B1/B5/B8）===')
print('指标'.ljust(16) + ''.join(r.rjust(9) for r in ['R1','R2','R3','R4','R5','R6']))
for vn, lab in [('v01','offset'),('v02','confusion'),('v03','temp'),('v04','defense'),
                ('v07','beta'),('v09','kappa'),('v10','R_root'),('v11','P_basin'),
                ('v38','cos_rin'),('v39','cos_gen'),('v40','gravity'),('v37','geo')]:
    row = lab.ljust(16)
    for r in ['R1','R2','R3','R4','R5','R6']:
        v = M6[r][vn]
        row += ('%9.3f' % v) if v is not None else '      N/A'
    print(row)
