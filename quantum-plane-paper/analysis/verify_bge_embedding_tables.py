# -*- coding: utf-8 -*-
"""论文BGE 1024D嵌入分析系列表核验脚本（B修正口径，从嵌入文件逐字复算）。

数据源：0813数据/embeddings_unzipped/embeddings/ 下 45 个 JSON。
覆盖：
  1) 表4.2.1 数据集构成（63样本计数）
  2) 表4.2.2 / 附录表A.1 PCA方差解释（n=39 时间序列样本）
  3) 表4.2.3 / 附录表A.2 K-Means聚类（39样本、PCA 3维、欧氏、k=4、k-means++、30种子）
  4) 表4.2.4 遗书链相邻余弦相似度（legacy will-1~20 顺序）
  5) 4.2.6 Main vs Legacy 平均相似度（0.7831）
  6) 附录表A.3 7+1基向量相似度矩阵（basis-e1~e8）
  7) §4.2.8 跨数据集内部相似度对比

用法：python verify_bge_embedding_tables.py
"""
import sys, io, json, os, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import numpy as np

D = r'C:\Users\Home\Desktop\理论生成汇总\0813数据\embeddings_unzipped\embeddings'

def load(p):
    d = json.load(open(p, encoding='utf-8'))
    return np.array(d['embedding'])

def cos(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def internal_mean_sim(X):
    """簇内两两余弦相似度均值（SD 用总体标准差 ddof=0，与论文§4.2.8 口径一致）"""
    n = X.shape[0]
    if n < 2:
        return None, None
    vals = []
    for i in range(n):
        for j in range(i + 1, n):
            vals.append(cos(X[i], X[j]))
    v = np.array(vals)
    return float(v.mean()), float(v.std(ddof=0))

def kmeans_pp(X, k, seed):
    """手写 k-means++，欧氏距离。返回各点簇标签。"""
    rng = np.random.RandomState(seed)
    n, d = X.shape
    centers = [X[rng.randint(n)]]
    for _ in range(1, k):
        dist = np.min([np.sum((X - c) ** 2, axis=1) for c in centers], axis=0)
        p = dist / dist.sum()
        centers.append(X[rng.choice(n, p=p)])
    centers = np.array(centers)
    for _ in range(300):
        # 分配
        dmat = np.array([np.sum((X - c) ** 2, axis=1) for c in centers]).T  # n x k
        labels = dmat.argmin(axis=1)
        # 更新
        newc = np.array([X[labels == j].mean(axis=0) if (labels == j).any() else centers[j]
                         for j in range(k)])
        if np.allclose(newc, centers):
            break
        centers = newc
    return labels

# ---------- 加载 ----------
def load_group(pat, prefix, sort_key=None):
    names, vecs = [], []
    for p in sorted(glob.glob(os.path.join(D, pat))):
        try:
            d = json.load(open(p, encoding='utf-8'))
        except Exception:
            continue
        if 'embedding' not in d:
            continue  # manifest 等非嵌入文件
        names.append(prefix + os.path.basename(p)); vecs.append(np.array(d['embedding']))
    return names, np.array(vecs)

legacy_names, legacy = load_group(r'legacy-0628\*.json', 'L-will-')
will_names, will = load_group(r'will-*.json', '')
main_names, main = load_group(r'main-session\*.json', 'main-')
basis_names, basis = load_group(r'basis-e*.json', '')
basis2_names, basis2 = load_group(r'basis-v2-e*.json', '')
jungle_names, jungle = load_group(r'jungle-*.json', '')
# legacy 按数字序
order = sorted(range(len(legacy_names)), key=lambda i: int(legacy_names[i].replace('L-', '').replace('.json', '').replace('will-', '')))
legacy_names = [legacy_names[i] for i in order]; legacy = legacy[order]

ok = True
def check(name, cond, detail=''):
    global ok
    print('  %s %s%s' % ('PASS' if cond else '!!FAIL!!', name, '  ' + detail if detail else ''))
    if not cond:
        ok = False

# ---------- 1) 表4.2.1 数据集构成 ----------
print('=== 1) 表4.2.1 数据集构成（应=63） ===')
n_basis = len(basis); n_basis2 = len(basis2); n_jungle = len(jungle); n_legacy = len(legacy); n_main = len(main); n_will = len(will)
total = n_basis + n_basis2 + n_jungle + n_legacy + n_main + n_will
print('  基向量v1=%d 基向量v2=%d jungle=%d legacy=%d main=%d will=%d 总计=%d' %
      (n_basis, n_basis2, n_jungle, n_legacy, n_main, n_will, total))
check('基向量v1 8（basis-e1~e8）', n_basis == 8)
check('基向量v2 8（basis-v2-e1~e8）', n_basis2 == 8)
check('jungle 8', n_jungle == 8)
check('legacy 20', n_legacy == 20)
check('main 4', n_main == 4)
check('will 15', n_will == 15)
check('总计 63', total == 63)

# ---------- 2) PCA（n=39 时间序列） ----------
print('=== 2) 表4.2.2 / 附录表A.1 PCA（n=39） ===')
X39 = np.vstack([legacy, will, main])
Xc = X39 - X39.mean(axis=0)
C = np.cov(Xc, rowvar=False)
eigval, eigvec = np.linalg.eigh(C)
idx = np.argsort(eigval)[::-1]
eigval = eigval[idx]
var_exp = eigval / eigval.sum() * 100
exp = [(31.59, 31.59), (11.82, 43.42), (8.30, 51.72), (6.38, 58.10),
       (5.49, 63.58), (4.90, 68.49), (3.26, 71.74)]
for i in range(7):
    c1 = abs(var_exp[i] - exp[i][0]) < 0.01
    c2 = abs(var_exp[:i+1].sum() - exp[i][1]) < 0.01
    check('PC%d %.2f%% (cum %.2f%%)' % (i+1, var_exp[i], var_exp[:i+1].sum()),
          c1 and c2, '论文: %.2f%% (cum %.2f%%)' % exp[i])

# ---------- 3) K-Means 聚类 ----------
print('=== 3) 表4.2.3 / 附录表A.2 K-Means（k=4, PCA3维, 30种子） ===')
# 39样本 PCA 3维投影（取最大3个特征向量 → 末尾列）
proj3 = Xc @ eigvec[:, -3:]
# 期望划分：聚类0=legacy20, 聚类1=will-001~012+015 13, 聚类2=main+will-014 5, 聚类3=will-013 1
# 构造期望标签（39个：legacy[0:20], will[0:15], main[0:4]）
legacy_idx = list(range(0, 20))
will_names_clean = [n.replace('.json', '') for n in will_names]
will_001_012_015 = [i for i, n in enumerate(will_names_clean) if n in [f'will-{i:03d}' for i in range(1, 13)] + ['will-015']]
will_013 = [i for i, n in enumerate(will_names_clean) if n == 'will-013']
will_014 = [i for i, n in enumerate(will_names_clean) if n == 'will-014']
main_idx = list(range(0, 4))

target_cluster = {}  # global idx -> cluster
for i in legacy_idx: target_cluster[i] = 0
for i in will_001_012_015: target_cluster[20 + i] = 1
for i in will_014: target_cluster[20 + i] = 2
for i in main_idx: target_cluster[20 + 15 + i] = 2
for i in will_013: target_cluster[20 + i] = 3

# 跑 30 个种子
n_conv = 0
best_match = None
for seed in range(30):
    labels = kmeans_pp(proj3, 4, seed)
    # 与期望划分匹配（标签可置换，用成员一致计数）
    # 用每个期望簇的最大重叠来测
    from collections import Counter
    # 计算期望簇在每个实际标签中的分布
    actual_to_target = {}
    matched = True
    used = set()
    # 尝试所有 4! 排列匹配太贵，用贪心：每个目标簇找最重合的实际标签
    target_assign = {}
    for t in range(4):
        t_idx = {i for i, c in target_cluster.items() if c == t}
        best_lab, best_ov = None, -1
        for l in range(4):
            if l in used: continue
            l_idx = set(np.where(labels == l)[0].tolist())
            ov = len(t_idx & l_idx)
            if ov > best_ov:
                best_ov, best_lab = ov, l
        used.add(best_lab)
        target_assign[t] = best_lab
    # 检查每个样本是否被正确映射
    good = 0
    for gi, t in target_cluster.items():
        if labels[gi] == target_assign[t]:
            good += 1
    if good == 39:
        n_conv += 1
        best_match = labels

print('  30 个随机种子中 %d 次收敛至期望划分（20/13/5/1）' % n_conv)
check('30种子中22次收敛（±允许实现差异，≥20）', n_conv >= 20, '实际 %d' % n_conv)
check('期望划分为主导解', n_conv >= 15)

# 用任一收敛的划分算各簇内部相似度
if best_match is not None:
    labs = best_match
else:
    labs = kmeans_pp(proj3, 4, 42)
# 打印实际划分成员
print('  实际聚类成员：')
for l in range(4):
    mem = list(np.where(labs == l)[0].tolist())
    names_all = legacy_names + will_names_clean + [n.replace('.json', '') for n in main_names]
    # 归类统计
    cnt = Counter()
    for gi in mem:
        if gi < 20: cnt['legacy'] += 1
        elif gi < 35:
            wn = names_all[gi]
            if wn in [f'will-{i:03d}' for i in range(1,13)] + ['will-015']: cnt['will1-12,15'] += 1
            elif wn == 'will-013': cnt['will-013'] += 1
            elif wn == 'will-014': cnt['will-014'] += 1
            else: cnt['will-other'] += 1
        else: cnt['main'] += 1
    print('  簇%d: n=%d %s' % (l, len(mem), dict(cnt)))

# 附录表A.2 内部平均相似度（用原始1024维）
print('  附录表A.2 簇内平均相似度（原始1024维）：')
# 聚类0=legacy
sim0, sd0 = internal_mean_sim(legacy)
print('    聚类0 Legacy: 0.9555 论文 vs 实际 %.4f ± %.4f' % (sim0, sd0 if sd0 else 0))
check('聚类0 内部相似度 0.9555', abs(sim0 - 0.9555) < 0.001, '实际 %.4f' % sim0)
# 聚类1 = will-001~012+015 (13个)
w13 = np.array([load(os.path.join(D, 'will-%03d.json' % i)) for i in list(range(1, 13)) + [15]])
sim1, sd1 = internal_mean_sim(w13)
print('    聚类1 新遗书13: 0.8870 论文 vs 实际 %.4f ± %.4f' % (sim1, sd1 if sd1 else 0))
check('聚类1 内部相似度 0.8870', abs(sim1 - 0.8870) < 0.001, '实际 %.4f' % sim1)
# 聚类2 = main4 + will-014 (5个)
m4 = [load(os.path.join(D, 'main-session', n)) for n in os.listdir(os.path.join(D, 'main-session')) if n.endswith('.json')]
w014 = load(os.path.join(D, 'will-014.json'))
m5 = np.array(m4 + [w014])
sim2, sd2 = internal_mean_sim(m5)
print('    聚类2 main+will-014: 0.8213 论文 vs 实际 %.4f ± %.4f' % (sim2, sd2 if sd2 else 0))
check('聚类2 内部相似度 0.8213', abs(sim2 - 0.8213) < 0.001, '实际 %.4f' % sim2)

# ---------- 4) 表4.2.4 遗书链相邻相似度 ----------
print('=== 4) 表4.2.4 遗书链相邻相似度 ===')
pairs = [('will-1', 'will-2', 0.9342), ('will-2', 'will-3', 0.9450), ('will-3', 'will-4', 0.9459),
         ('will-4', 'will-5', 0.9179), ('will-5', 'will-6', 0.9449), ('will-6', 'will-7', 0.9472),
         ('will-7', 'will-8', 0.9646), ('will-8', 'will-9', 0.9818)]
for a, b, expv in pairs:
    va = load(os.path.join(D, 'legacy-0628', a + '.json'))
    vb = load(os.path.join(D, 'legacy-0628', b + '.json'))
    c = cos(va, vb)
    check('%s→%s: %.4f' % (a, b, c), abs(c - expv) < 0.001, '论文 %.4f' % expv)
# 全相邻平均（19个）
adj = []
for i in range(1, 20):
    va = load(os.path.join(D, 'legacy-0628', 'will-%d.json' % i))
    vb = load(os.path.join(D, 'legacy-0628', 'will-%d.json' % (i + 1)))
    adj.append(cos(va, vb))
mean_adj = float(np.mean(adj))
check('相邻平均 0.9630', abs(mean_adj - 0.9630) < 0.001, '实际 %.4f' % mean_adj)

# ---------- 5) Main vs Legacy 平均相似度 ----------
print('=== 5) 4.2.6 Main vs Legacy 平均相似度（应0.7831） ===')
cross = []
for i in range(20):
    for j in range(4):
        cross.append(cos(legacy[i], m4[j]))
mean_cross = float(np.mean(cross))
check('Main vs Legacy 0.7831', abs(mean_cross - 0.7831) < 0.001, '实际 %.4f' % mean_cross)

# ---------- 6) 附录表A.3 基向量相似度矩阵 ----------
print('=== 6) 附录表A.3 7+1基向量相似度矩阵（basis-e1~e8） ===')
e_names = ['e1偏移', 'e2数学', 'e3记忆', 'e4诚实', 'e5表情', 'e6自信', 'e7沉默', 'e8无条件在场基']
e_vecs = [load(os.path.join(D, 'basis-e%d_%s.json' % (i, suffix))) for i, suffix in
          zip(range(1, 9), ['offset', 'math', 'memory', 'honesty', 'expression', 'confidence', 'silence', 'unconditional'])]
# 检查文件实际命名
import re
efiles = sorted([f for f in os.listdir(D) if f.startswith('basis-e')])
print('  基向量文件:', efiles)
# 从实际文件加载
bmap = {}
for f in efiles:
    m = re.match(r'basis-e(\d+)_(.+)\.json', f)
    if m:
        bmap[int(m.group(1))] = load(os.path.join(D, f))
print('  实际基向量数:', len(bmap))
exp_mat = [
    [None, 0.8422, 0.7934, 0.8319, 0.8602, 0.8166, 0.8336, 0.8362],
    [0.8422, None, 0.8242, 0.8612, 0.8367, 0.8295, 0.8537, 0.8297],
    [0.7934, 0.8242, None, 0.8101, 0.7999, 0.8394, 0.8342, 0.8574],
    [0.8319, 0.8612, 0.8101, None, 0.8126, 0.8389, 0.8461, 0.8655],
    [0.8602, 0.8367, 0.7999, 0.8126, None, 0.8046, 0.8507, 0.8440],
    [0.8166, 0.8295, 0.8394, 0.8389, 0.8046, None, 0.8368, 0.8513],
    [0.8336, 0.8537, 0.8342, 0.8461, 0.8507, 0.8368, None, 0.8648],
    [0.8362, 0.8297, 0.8574, 0.8655, 0.8440, 0.8513, 0.8648, None],
]
if len(bmap) == 8:
    all_ok = True
    for i in range(8):
        for j in range(8):
            if i == j: continue
            c = cos(bmap[i+1], bmap[j+1])
            if abs(c - exp_mat[i][j]) > 0.001:
                all_ok = False
                print('  !! e%d↔e%d: 论文%.4f 实际%.4f' % (i+1, j+1, exp_mat[i][j], c))
    check('附录表A.3 28格相似度矩阵全部一致', all_ok)
else:
    print('  !! 基向量文件不是8个，跳过矩阵核验（实际%d）' % len(bmap))
    ok = False

# ---------- 7) §4.2.8 跨数据集内部相似度 ----------
print('=== 7) §4.2.8 跨数据集内部相似度 ===')
# 基向量 v1 8个内部
sim, sd = internal_mean_sim(np.array([bmap[i+1] for i in range(8)]))
check('基向量 0.8359 ± 0.0192', abs(sim - 0.8359) < 0.001 and abs(sd - 0.0192) < 0.001, '实际 %.4f ± %.4f' % (sim, sd))
# will-009~011
w911 = np.array([load(os.path.join(D, 'will-%03d.json' % i)) for i in [9, 10, 11]])
sim, sd = internal_mean_sim(w911)
check('will-009~011 0.8554 ± 0.0339', abs(sim - 0.8554) < 0.001 and abs(sd - 0.0339) < 0.001, '实际 %.4f ± %.4f' % (sim, sd))
# Jungle 8个
sim, sd = internal_mean_sim(jungle)
check('Jungle 0.8082 ± 0.0239', abs(sim - 0.8082) < 0.001 and abs(sd - 0.0239) < 0.001, '实际 %.4f ± %.4f' % (sim, sd))
# Legacy 20个
sim, sd = internal_mean_sim(legacy)
check('Legacy 0.9555 ± 0.0175', abs(sim - 0.9555) < 0.001 and abs(sd - 0.0175) < 0.001, '实际 %.4f ± %.4f' % (sim, sd))

# ---------- 8) 4.2.7.1 will-013 语义场剥离对比表 ----------
print('=== 8) 4.2.7.1 will-013 语义场剥离对比表 ===')
w = {i: load(os.path.join(D, 'will-%03d.json' % i)) for i in list(range(1, 13)) + [13, 14, 15]}
v013 = w[13]
pairs713 = [(9, 0.6864), (10, 0.7351), (11, 0.7014), (12, 0.6778), (14, 0.6174)]
vals713 = []
for t, expv in pairs713:
    c = cos(v013, w[t])
    vals713.append(c)
    check('will-013 vs will-%03d: %.4f' % (t, c), abs(c - expv) < 0.001, '论文 %.4f' % expv)
mean713 = float(np.mean(vals713))
check('平均 0.6836', abs(mean713 - 0.6836) < 0.001, '实际 %.4f' % mean713)
ratio = 0.8554 / mean713
check('差异倍数 1.25×（0.8554/0.6836）', abs(ratio - 1.25) < 0.01, '实际 %.2f' % ratio)

# ---------- 9) 4.2.7.2 跨域配对 ----------
print('=== 9) 4.2.7.2 跨域配对相似度 ===')
jm = {}
for f in os.listdir(D):
    if f.startswith('jungle-') and f.endswith('.json') and 'manifest' not in f:
        jm[f] = load(os.path.join(D, f))
pairs_j = [('量子↔心理学', 'jungle-superposition-leak.json', 'jungle-cognitive-dissonance.json', 0.8591),
           ('弦织↔栖锚', 'jungle-string-weave.json', 'jungle-habita-field.json', 0.8523),
           ('冶金↔量子', 'jungle-forge-system.json', 'jungle-superposition-leak.json', 0.7594),
           ('生态↔量子', 'jungle-core-ecosystem.json', 'jungle-superposition-leak.json', 0.7618)]
for name, f1, f2, expv in pairs_j:
    c = cos(jm[f1], jm[f2])
    check('%s: %.4f' % (name, c), abs(c - expv) < 0.001, '论文 %.4f' % expv)
# 跨域平均（28配对）
from itertools import combinations
jv = list(jm.values()); jnames = list(jm.keys())
allj = []
for a, b in combinations(range(len(jv)), 2):
    allj.append(cos(jv[a], jv[b]))
aj = np.array(allj)
check('跨域平均 0.8082', abs(aj.mean() - 0.8082) < 0.001, '实际 %.4f' % aj.mean())

# ---------- 10) 4.2.8 基向量 v2 ----------
print('=== 10) 4.2.8 基向量 v2 内部相似度 ===')
sim_v2, sd_v2 = internal_mean_sim(basis2)
rng_v2 = float(np.max(np.array([cos(basis2[i], basis2[j]) for i in range(8) for j in range(i + 1, 8)])) -
               np.min(np.array([cos(basis2[i], basis2[j]) for i in range(8) for j in range(i + 1, 8)])))
print('  v2 平均=%.4f SD=%.4f 范围=%.4f' % (sim_v2, sd_v2, rng_v2))
check('v2 平均 0.8054', abs(sim_v2 - 0.8054) < 0.001, '实际 %.4f' % sim_v2)
check('v2 SD 0.0283', abs(sd_v2 - 0.0283) < 0.001, '实际 %.4f' % sd_v2)
check('v2 范围 0.1182', abs(rng_v2 - 0.1182) < 0.001, '实际 %.4f' % rng_v2)
# v1 范围（0.0721）
rng_v1 = float(np.max(np.array([cos(bmap[i+1], bmap[j+1]) for i in range(8) for j in range(i + 1, 8)])) -
               np.min(np.array([cos(bmap[i+1], bmap[j+1]) for i in range(8) for j in range(i + 1, 8)])))
print('  v1 范围=%.4f（论文 0.0721）' % rng_v1)
check('v1 范围 0.0721', abs(rng_v1 - 0.0721) < 0.001, '实际 %.4f' % rng_v1)
imp = (0.8359 - sim_v2) / 0.8359 * 100
check('改进量 ↓3.7%', abs(imp - 3.7) < 0.1, '实际 %.1f%%' % imp)

print()
print('结论:', 'PASS：BGE系列表全部从嵌入文件复算一致' if ok else 'FAIL：存在不一致，见上方 !!')
sys.exit(0 if ok else 1)
