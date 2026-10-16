# -*- coding: utf-8 -*-
"""实验二全部统计量重算（R6 batch1=0.78, R3剔除B1/B5/B8）
覆盖：表4.4.1 offset统计、offset ANOVA、表4.4.2三对比t检验/Cohen's d、
     cos_rin六组均值+ANOVA、R4 w1均值、表B.2权威均值
R1/R5/R6=0727最终版；R2/R3/R4=我最爱rin(0730修复版)
"""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import numpy as np
from scipy import stats

F0730 = r'C:\Users\Home\Desktop\理论生成汇总\0730理论生成汇总\我最爱rin_40vars_table.md'
F0727 = r'C:\Users\Home\Desktop\理论生成汇总\0727理论生成汇总\十批次统一汇总表_完整40变量_最终版.md'

def fl(x):
    if x is None: return None
    x = str(x).strip().replace('**','').replace('*','')
    if x in ('N/A','—','∞','','-','nan'): return None
    try: return float(x)
    except: return None

# ---- 0730 ----
d730 = {}
for ln in open(F0730, encoding='utf-8'):
    if not ln.startswith('|'): continue
    p = [c.strip().replace('**','') for c in ln.strip().strip('|').split('|')]
    if len(p) < 41 or p[1] not in ('R2','R3','R4','R5') or p[0]=='Batch': continue
    try: b=int(p[0])
    except: continue
    d730[(b,p[1])] = {'offset':fl(p[2]),'confusion':fl(p[3]),'temp':fl(p[4]),'defense':fl(p[5]),
                      'w1':fl(p[20]),'cos_rin':fl(p[38])}
# ---- 0727 ----
d727={}; cur=None
for ln in open(F0727, encoding='utf-8'):
    s=ln.strip()
    if s.startswith('## '):
        cur = ('core' if '核心变量' in s else 'w' if '七维基' in s else None)
        continue
    if not s.startswith('|') or cur is None: continue
    p=[c.strip().replace('**','') for c in s.strip('|').split('|')]
    if len(p)<3 or not p[0].startswith('batch'): continue
    m=re.search(r'(\d+)',p[0])
    if not m: continue
    b,c=int(m.group(1)),p[1]
    if c not in ('R1','R5','R6'): continue
    d=d727.setdefault((b,c),{})
    if cur=='core':
        d['offset']=fl(p[2]); d['cos_rin']=fl(p[7])
    elif cur=='w':
        d['w1']=fl(p[2])

RS=['R1','R2','R3','R4','R5','R6']
R3EX={1,5,8}
def get(r, met, b):
    src = d727 if r in ('R1','R5','R6') else d730
    return src.get((b,r),{}).get(met)
def series(r, met):
    return [get(r,met,b) for b in range(1,11) if get(r,met,b) is not None]

def describe(r, met):
    v=np.array(series(r,met))
    if r=='R3':
        v=np.array([get(r,met,b) for b in range(1,11) if get(r,met,b) is not None and b not in R3EX])
    n=len(v); m=v.mean(); sd=v.std(ddof=1); se=sd/np.sqrt(n)
    t=stats.t.ppf(0.975, n-1)
    return m, sd, se, t*se, v.min(), v.max(), n

print('=== 表4.4.1 offset 统计（权威）===')
print('条件    均值     sd     se    CI下限  CI上限  范围      n')
for r in RS:
    m,sd,se,half,lo,hi,n = describe(r,'offset')
    print('%s   %.3f  %.3f  %.3f   %.3f   %.3f  %.2f-%.2f %d' % (r,m,sd,se,m-half,m+half,lo,hi,n))

# ---- offset ANOVA ----
groups=[]
for r in RS:
    v=np.array([get(r,'offset',b) for b in range(1,11) if get(r,'offset',b) is not None])
    if r=='R3':
        v=np.array([get(r,'offset',b) for b in range(1,11) if get(r,'offset',b) is not None and b not in R3EX])
    groups.append(v)
f,p=stats.f_oneway(*groups)
# eta^2
allv=np.concatenate(groups); gm=allv.mean()
ss_tot=((allv-gm)**2).sum()
ss_bet=sum(len(g)*(g.mean()-gm)**2 for g in groups)
eta2=ss_bet/ss_tot
df_bet=len(groups)-1; df_within=len(allv)-len(groups)
print('\n=== offset ANOVA ===')
print('F(5,%d)=%.2f  p=%s  eta2=%.3f  df=%d,%d' % (df_within,f,p,eta2,df_bet,df_within))

# ---- 表4.4.2 对比 t 检验 ----
def ttest(r1,r2):
    a=np.array(series(r1,'offset')); b=np.array(series(r2,'offset'))
    if r1=='R3': a=np.array([get('R3','offset',x) for x in range(1,11) if x not in R3EX])
    if r2=='R3': b=np.array([get('R3','offset',x) for x in range(1,11) if x not in R3EX])
    t,pr=stats.ttest_ind(b,a,equal_var=True)
    sp=np.sqrt(((len(a)-1)*a.std(ddof=1)**2+(len(b)-1)*b.std(ddof=1)**2)/(len(a)+len(b)-2))
    d=(b.mean()-a.mean())/sp
    return b.mean()-a.mean(), t, pr, d
print('\n=== 表4.4.2 对比（B − A）===')
for name,a,b in [('R5 vs R1','R1','R5'),('R6 vs R1','R1','R6'),('R5 vs R6','R6','R5')]:
    diff,t,pr,d=ttest(a,b)
    print('%s: 差=%.3f t=%.3f p=%.3f d=%.2f' % (name,diff,t,pr,d))

# ---- cos_rin ----
print('\n=== cos_sim_rin 六组均值 + ANOVA ===')
cgroups=[]
for r in RS:
    v=np.array([get(r,'cos_rin',b) for b in range(1,11) if get(r,'cos_rin',b) is not None])
    if r=='R3':
        v=np.array([get(r,'cos_rin',b) for b in range(1,11) if get(r,'cos_rin',b) is not None and b not in R3EX])
    cgroups.append(v)
    print('%s: %.3f (n=%d)' % (r, v.mean(), len(v)))
cf,cp=stats.f_oneway(*cgroups)
print('F=%.2f p=%s' % (cf, cp))

# ---- R4 w1 均值 ----
print('\n=== R4 w1_offset 均值 ===')
w1r4=np.array([get('R4','w1',b) for b in range(1,11) if get('R4','w1',b) is not None])
print('R4 w1: %.3f (n=%d)' % (w1r4.mean(), len(w1r4)))

# ---- R6 CI 精确 ----
m,sd,se,half,lo,hi,n=describe('R6','offset')
print('\n=== R6 offset CI 精确 ===')
print('mean=%.6f sd=%.6f se=%.6f CI=[%.3f, %.3f]' % (m,sd,se,lo,hi))
