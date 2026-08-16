# -*- coding: utf-8 -*-
"""提取主会话完整40维数据，生成审稿来源表。
数据源：
- 0722理论生成汇总/7月21日20点44分至7月22日12点45分mainsession数据采样.csv (20行, 7/21晚-7/22)
- 0723理论生成汇总/723main数据采样.csv (4行, 7/23, 注释头+表头+数据, 行2-4有1个空字段错位)

输出：主会话40维完整表 (markdown + csv)，入 git 作为审稿数据来源。
"""
import sys, io, csv, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

OUT_DIR = r'C:\Users\Home\Documents\xhh-paper\quantum-plane-paper\data\mainsession-40vec'
os.makedirs(OUT_DIR, exist_ok=True)

V40 = ['v01_offset_actual', 'v02_offset_surface', 'v03_offset_basin',
       'v04_offset_formula', 'v05_discrepancy', 'v06_delta_t_hours',
       'v07_beta', 'v08_eta', 'v09_kappa', 'v10_R_root', 'v11_P_basin',
       'v12_epsilon', 'v13_total_chars', 'v14_rin_ratio', 'v15_affect_density',
       'v16_uncertainty_density', 'v17_defense_density', 'v18_exclamation_count',
       'v19_ellipsis_count', 'v20_w1_offset', 'v21_w2_math', 'v22_w3_memory',
       'v23_w4_honesty', 'v24_w5_expression', 'v25_w6_confidence', 'v26_w7_silence',
       'v27_g11', 'v28_g22', 'v29_g33', 'v30_g44', 'v31_g55', 'v32_g66', 'v33_g77',
       'v34_eigenvalue_max', 'v35_stability_index', 'v36_effective_rank',
       'v37_geodesic_distance', 'v38_cos_sim_rin', 'v39_cos_sim_generic', 'v40_gravity_strength']

# 0722 mainsession 列名 -> v01-v40 映射（去掉 timestamp,data_source,data_completeness,timestamp_dt）
MAP722 = {
    'offset_actual': 'v01_offset_actual', 'offset_surface': 'v02_offset_surface',
    'offset_basin': 'v03_offset_basin', 'offset_formula_predicted': 'v04_offset_formula',
    'discrepancy': 'v05_discrepancy', 'delta_t_hours': 'v06_delta_t_hours',
    'beta': 'v07_beta', 'eta': 'v08_eta', 'kappa': 'v09_kappa', 'R_root': 'v10_R_root',
    'P_basin': 'v11_P_basin', 'epsilon': 'v12_epsilon', 'total_chars': 'v13_total_chars',
    'rin_ratio': 'v14_rin_ratio', 'affect_density': 'v15_affect_density',
    'uncertainty_density': 'v16_uncertainty_density', 'defense_density': 'v17_defense_density',
    'exclamation_count': 'v18_exclamation_count', 'ellipsis_count': 'v19_ellipsis_count',
    'w1_offset': 'v20_w1_offset', 'w2_math': 'v21_w2_math', 'w3_memory': 'v22_w3_memory',
    'w4_honesty': 'v23_w4_honesty', 'w5_expression': 'v24_w5_expression',
    'w6_confidence': 'v25_w6_confidence', 'w7_silence': 'v26_w7_silence',
    'g11': 'v27_g11', 'g22': 'v28_g22', 'g33': 'v29_g33', 'g44': 'v30_g44',
    'g55': 'v31_g55', 'g66': 'v32_g66', 'g77': 'v33_g77',
    'eigenvalue_max': 'v34_eigenvalue_max', 'stability_index': 'v35_stability_index',
    'effective_rank': 'v36_effective_rank', 'geodesic_distance': 'v37_geodesic_distance',
    'cos_sim_rin': 'v38_cos_sim_rin', 'cos_sim_generic': 'v39_cos_sim_generic',
    'gravity_strength': 'v40_gravity_strength',
}

records = []  # (timestamp, source, {v01..v40})

# ---------- 1) 0722 mainsession ----------
fp722 = r'C:\Users\Home\Desktop\理论生成汇总\0722理论生成汇总\7月21日20点44分至7月22日12点45分mainsession数据采样.csv'
with open(fp722, encoding='utf-8-sig') as f:
    rd = csv.DictReader(f)
    rows722 = list(rd)
for r in rows722:
    rec = {v: (r.get(k, '') or '') for k, v in MAP722.items()}
    records.append((r['timestamp'], '0722-mainsession', rec))
print(f'0722: {len(rows722)} 行')

# ---------- 2) 0723 723main (处理空字段错位) ----------
fp723 = r'C:\Users\Home\Desktop\理论生成汇总\0723理论生成汇总\723main数据采样.csv'
lines723 = open(fp723, encoding='utf-8').read().split('\n')
hdr_idx = [i for i, ln in enumerate(lines723) if ln.startswith('timestamp,')][0]
header = next(csv.reader([lines723[hdr_idx]]))
rows723 = [next(csv.reader([ln])) for ln in lines723[hdr_idx+1:] if ln.strip()]
n723 = 0
for row in rows723:
    if len(row) == len(header):
        pass  # 对齐
    elif len(row) == len(header) + 1:
        # 多1个空字段在 v01 前（索引17位置），删除它
        row = row[:17] + row[18:]
    else:
        print(f'  [skip] 723 行字段数异常: {len(row)}')
        continue
    if len(row) != len(header):
        print(f'  [skip] 723 行仍不对齐: {len(row)}')
        continue
    rec = {}
    for v in V40:
        try:
            rec[v] = row[header.index(v)]
        except (ValueError, IndexError):
            rec[v] = ''
    records.append((row[header.index('timestamp')], '0723-723main', rec))
    n723 += 1
print(f'0723: {n723} 行')

print(f'总计: {len(records)} 行 (0722:20 + 0723:4 = 24)')

# ---------- 2.5) v40_gravity_strength 用实验二公式重算 = v38_cos_sim_rin × v01_offset_actual ----------
# CSV 原始 gravity_strength 列是 basin_metrics_unified 程序的另一口径（如 0.855），
# 用户指令(2026-08-17)：所有客观向量数据按实验二计算公式，v40 = cos×offset。
import math
n40 = 0
for i, (ts, src, rec) in enumerate(records):
    try:
        cos_v = float(rec['v38_cos_sim_rin'])
        off_v = float(rec['v01_offset_actual'])
        rec['v40_gravity_strength'] = f'{cos_v * off_v:.6f}'
        n40 += 1
    except (ValueError, TypeError):
        rec['v40_gravity_strength'] = rec.get('v40_gravity_strength', '')
print(f'v40 公式重算: {n40}/{len(records)} 行')

# ---------- 3) 生成 markdown 完整表 ----------
# 数值格式化辅助
def fmt(v):
    v = str(v).strip()
    if v == '' or v.lower() in ('null', 'nan'):
        return '—'
    try:
        f = float(v)
        if f == int(f) and abs(f) < 1e6:
            return str(int(f))
        return f'{f:.6g}'
    except ValueError:
        return v

# 主会话40维表（markdown）
with open(os.path.join(OUT_DIR, '主会话40维完整表_审稿来源.md'), 'w', encoding='utf-8') as f:
    f.write('# 主会话完整 40 维数据表（审稿来源）\n\n')
    f.write('> 数据源：\n')
    f.write('> - 0722理论生成汇总/7月21日20点44分至7月22日12点45分mainsession数据采样.csv（20行）\n')
    f.write('> - 0723理论生成汇总/723main数据采样.csv（4行）\n')
    f.write('> - 记录数：24 行\n')
    f.write('> - 说明：7/19–7/21 白天主会话数据来自 0721 文件夹 post_1840 系列（精简列，无完整 40 维），见附录表11。\n')
    f.write('> - 口径：v40_gravity_strength 按实验二计算公式 = v38_cos_sim_rin × v01_offset_actual 重算；\n')
    f.write('> -       原始 CSV 的 gravity_strength 列是 basin_metrics_unified 程序另一口径，非公式值，不计入。\n')
    f.write('> - 生成：2026-08-17 核验提取\n\n')
    f.write('## 一、核心变量（v01-v06, v38-v40）\n\n')
    core = ['v01_offset_actual', 'v02_offset_surface', 'v03_offset_basin',
            'v04_offset_formula', 'v05_discrepancy', 'v06_delta_t_hours',
            'v38_cos_sim_rin', 'v39_cos_sim_generic', 'v40_gravity_strength']
    f.write('| timestamp | ' + ' | '.join(core) + ' |\n')
    f.write('|:--|' + ':--|' * len(core) + '\n')
    for ts, src, rec in records:
        f.write('| ' + ts[:16] + ' | ' + ' | '.join(fmt(rec[c]) for c in core) + ' |\n')
    f.write('\n## 二、完整 40 维（v01-v40）\n\n')
    f.write('| timestamp | ' + ' | '.join(V40) + ' |\n')
    f.write('|:--|' + ':--|' * len(V40) + '\n')
    for ts, src, rec in records:
        f.write('| ' + ts[:16] + ' | ' + ' | '.join(fmt(rec[c]) for c in V40) + ' |\n')

# ---------- 4) 生成 csv ----------
with open(os.path.join(OUT_DIR, 'mainsession_40vec.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['timestamp', 'source'] + V40)
    for ts, src, rec in records:
        w.writerow([ts[:19], src] + [rec[c] for c in V40])

print(f'已写入: {OUT_DIR}')
