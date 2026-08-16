# -*- coding: utf-8 -*-
"""论文ver5(mine) 第二批数字同步：
1) p=0.53 → p=0.51（自锚vs外锚，权威R5vsR1 p=0.514）
2) η²=0.792 → η²=0.791（offset ANOVA 权威）
3) cos_sim_用户 → cos_sim_rin（术语统一，Task#17）
4) 行1158 分支表 "offset 0.67" → "offset 0.66–0.69"（权威 R5=0.661/R6=0.689）
d=0.30 在效应量排序/大小描述处保留（1281/1327/1234 为大小或 R1vsR5 方向，+0.30 正确）。
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

F = r'C:\Users\Home\Desktop\理论生成汇总\0802理论生成汇总\量子平面概率动力学模型_完整版_ver5（mine）.md'
content = open(F, encoding='utf-8').read()

reps = [
    ('p=0.53', 'p=0.51'),
    ('η²=0.792', 'η²=0.791'),
    ('cos_sim_用户', 'cos_sim_rin'),
    ('offset 0.67', 'offset 0.66–0.69'),
]
for old, new in reps:
    n = content.count(old)
    print('%-14s x%-3d ->' % (old, n), new)
    content = content.replace(old, new)

open(F, 'w', encoding='utf-8').write(content)
print('已写回', F)
