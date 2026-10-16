# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

f0727 =r'C:\Users\Home\Desktop\理论生成汇总\0727理论生成汇总\十批次统一汇总表_完整40变量_最终版.md'
f0730 = r'C:\Users\Home\Desktop\理论生成汇总\0730理论生成汇总\新10批次R2-R5实验数据.md'

def fl(x):
    if x is None: return None
    x = str(x).replace('**','').replace('*','').strip()
    if x in ('N/A','—','∞','','-'): return None
    try: return float(x)
    except: return None

# 0727 R5: offset + cos_rin
r5_0727 = {'offset':[], 'cos_rin':[], 'cos_gen':[], 'gravity':[]}
cur = None
for ln in open(f0727, encoding='utf-8'):
    s = ln.strip()
    if s.startswith('## '):
        cur = 'core' if '核心变量' in s else None
        continue
    if cur != 'core' or not s.startswith('|'): continue
    parts = [c.strip() for c in s.strip('|').split('|')]
    if len(parts)<3 or not parts[0].startswith('batch') or parts[1]!='R5': continue
    vals = parts[2:]
    r5_0727['offset'].append(fl(vals[0]))
    r5_0727['cos_rin'].append(fl(vals[5]))
    r5_0727['cos_gen'].append(fl(vals[6]))
    r5_0727['gravity'].append(fl(vals[7]))

print("=== 0727 文件 R5（10批）===")
for i in range(10):
    print("batch%-3d offset=%.4f cos_rin=%.4f cos_gen=%.4f gravity=%.4f" % (i+1, r5_0727['offset'][i], r5_0727['cos_rin'][i], r5_0727['cos_gen'][i], r5_0727['gravity'][i]))
import numpy as np
for k,v in r5_0727.items():
    print("R5-0727 %s: mean=%.4f sd=%.4f" % (k, np.mean(v), np.std(v,ddof=1)))

# 0730 R5
r5_0730 = {'offset':[], 'cos_rin':[], 'cos_gen':[], 'gravity':[]}
for ln in open(f0730, encoding='utf-8'):
    if not ln.startswith('|'): continue
    parts = [c.strip() for c in ln.strip().strip('|').split('|')]
    if len(parts)<3 or parts[1]!='R5': continue
    vals = parts[2:]
    # v01=idx0, v38=idx33, v39=idx34, v40=idx35
    r5_0730['offset'].append(fl(vals[0]))
    r5_0730['cos_rin'].append(fl(vals[33]))
    r5_0730['cos_gen'].append(fl(vals[34]))
    r5_0730['gravity'].append(fl(vals[35]))
print("\n=== 0730 文件 R5（10批）===")
for i in range(10):
    print("batch%-3d offset=%.4f cos_rin=%.4f cos_gen=%.4f gravity=%.4f" % (i+1, r5_0730['offset'][i], r5_0730['cos_rin'][i], r5_0730['cos_gen'][i], r5_0730['gravity'][i]))
for k,v in r5_0730.items():
    print("R5-0730 %s: mean=%.4f sd=%.4f" % (k, np.mean(v), np.std(v,ddof=1)))
