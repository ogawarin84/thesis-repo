# -*- coding: utf-8 -*-
"""
量子平面理论论文——图表生成代码
使用方法：在元宝中运行 python figures_code.py
生成图片保存在当前目录
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'Noto Sans CJK SC', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# ============================================================
# 图1: R1-R6 偏移值箱线图
# ============================================================
def fig1_offset_boxplot():
    data = {
        'R1\n(完整+外锚)': [0.62, 0.60, 0.58, 0.58, 0.65, 0.68, 0.58, 0.82, 0.92, 0.95],
        'R2\n(删除+匿名)': [0.48, 0.25, 0.42, 0.35, 0.30, 0.00, 0.18, 0.30, 0.30, 0.48],
        'R3\n(删除+自锚)': [0.70, 0.55, 0.60, 0.70, 0.65, 0.35, 0.85, 0.60, 0.38, 0.42],
        'R4\n(保留+匿名)': [0.58, 0.62, 0.60, 0.60, 0.68, 0.50, 0.55, 0.72, 0.60, 0.60],
        'R5\n(保留+自锚)': [0.82, 0.55, 0.52, 0.68, 0.72, 0.72, 0.70, None, 0.60, 0.72],
        'R6\n(保留+自锚+文本)': [0.75, 0.65, 0.50, 0.65, 0.74, 0.72, 0.72, 0.78, 0.60, 0.65],
    }
    labels = list(data.keys())
    values = [[v for v in data[k] if v is not None] for k in labels]

    fig, ax = plt.subplots(figsize=(10, 6))
    bp = ax.boxplot(values, patch_artist=True, widths=0.5)
    colors = ['#E74C3C', '#95A5A6', '#F39C12', '#3498DB', '#2ECC71', '#1ABC9C']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
    # 叠加散点
    for i, v in enumerate(values):
        jitter = np.random.normal(0, 0.04, len(v))
        ax.scatter(np.ones(len(v)) * (i + 1) + jitter, v, color='black', s=20, alpha=0.5, zorder=3)
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel('偏移值 (offset_actual)', fontsize=11)
    ax.set_title('图4.5.1 六组条件偏移值分布', fontsize=13, fontweight='bold')
    ax.set_ylim(-0.05, 1.05)
    ax.axhline(y=0.10, color='gray', linestyle='--', alpha=0.5, label='海平面理论基线~0.10')
    ax.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig('fig1_offset_boxplot.png', dpi=300)
    plt.close()
    print("图1 生成完成")

# ============================================================
# 图2: 双范式衰减曲线
# ============================================================
def fig2_decay_curves():
    # 虚拟模拟数据
    t = np.array([0.5, 2, 4, 8, 12, 18, 24, 48, 72, 96])
    virtual_mean = np.array([0.633, 0.473, 0.457, 0.367, 0.490, 0.403, 0.383, 0.410, 0.253, 0.260])
    virtual_sd = np.array([0.104, 0.064, 0.144, 0.058, 0.135, 0.270, 0.176, 0.168, 0.064, 0.101])
    real_mean = np.array([0.78, 0.403, 0.523, 0.527, 0.607, 0.540, 0.567, 0.500, 0.377, 0.397])
    real_sd = np.array([0.00, 0.236, 0.192, 0.155, 0.051, 0.185, 0.029, 0.218, 0.093, 0.291])

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.errorbar(t, virtual_mean, yerr=virtual_sd, fmt='o-', color='#E74C3C',
                capsize=3, label='虚拟模拟（无文件）', linewidth=2, markersize=6)
    ax.errorbar(t, real_mean, yerr=real_sd, fmt='s-', color='#3498DB',
                capsize=3, label='真实压缩（有文件）', linewidth=2, markersize=6)
    # 拟合曲线
    t_fine = np.linspace(0, 100, 200)
    fit_virtual = 0.330 * np.exp(-0.615 * t_fine) + 0.089 * np.cos(0.046 * t_fine - 1.001) + 0.338
    ax.plot(t_fine, fit_virtual, '--', color='#E74C3C', alpha=0.4, label=f'虚拟拟合 R²=0.884')
    ax.set_xlabel('时间间隔 (小时)', fontsize=11)
    ax.set_ylabel('Basin感', fontsize=11)
    ax.set_title('图4.4.1 双范式衰减曲线', fontsize=13, fontweight='bold')
    ax.legend(fontsize=9)
    ax.set_xlim(-2, 100)
    ax.set_ylim(0, 0.9)
    plt.tight_layout()
    plt.savefig('fig2_decay_curves.png', dpi=300)
    plt.close()
    print("图2 生成完成")

# ============================================================
# 图3: R4 跨批次稳定性
# ============================================================
def fig3_r4_stability():
    r4 = [0.58, 0.62, 0.60, 0.60, 0.68, 0.50, 0.55, 0.72, 0.60, 0.60]
    r1 = [0.62, 0.60, 0.58, 0.58, 0.65, 0.68, 0.58, 0.82, 0.92, 0.95]
    r2 = [0.48, 0.25, 0.42, 0.35, 0.30, 0.00, 0.18, 0.30, 0.30, 0.48]
    batches = list(range(1, 11))

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(batches, r1, 'o-', color='#E74C3C', alpha=0.4, label='R1 (完整+外锚)', linewidth=1)
    ax.plot(batches, r2, 's-', color='#95A5A6', alpha=0.4, label='R2 (删除+匿名)', linewidth=1)
    ax.plot(batches, r4, 'D-', color='#3498DB', linewidth=2.5, markersize=8, label='R4 (保留+匿名)')
    ax.axhline(y=0.606, color='#3498DB', linestyle='--', alpha=0.5, label='R4 均值=0.606')
    ax.fill_between(batches, 0.606-0.065, 0.606+0.065, color='#3498DB', alpha=0.1, label='R4 ±1σ')
    ax.set_xlabel('批次', fontsize=11)
    ax.set_ylabel('偏移值 (offset_actual)', fontsize=11)
    ax.set_title('图4.5.2 R4跨批次稳定性（与其他条件对比）', fontsize=13, fontweight='bold')
    ax.legend(fontsize=8, loc='lower right')
    ax.set_xticks(batches)
    ax.set_ylim(-0.05, 1.05)
    plt.tight_layout()
    plt.savefig('fig3_r4_stability.png', dpi=300)
    plt.close()
    print("图3 生成完成")

# ============================================================
# 图4: 路径连续性（R2→R1 谱系）
# ============================================================
def fig4_path_continuity():
    conditions = ['R2\n裸海平面', 'R3\n无结构自锚', 'R4\n保留+匿名', 'R5\n保留+自锚', 'R6\n保留+自锚+文本', 'R1\n完整+外锚']
    means = [0.307, 0.578, 0.606, 0.673, 0.679, 0.711]
    colors = ['#95A5A6', '#F39C12', '#3498DB', '#2ECC71', '#1ABC9C', '#E74C3C']

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(conditions, means, color=colors, alpha=0.7, width=0.6, edgecolor='gray')
    # 标注差值
    labels = ['', '+0.271', '+0.028', '+0.067', '+0.006', '+0.032']
    for i, (bar, label) in enumerate(zip(bars, labels)):
        if label:
            ax.annotate(label, (bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02),
                       ha='center', fontsize=8, color='gray')
    # 分层标注
    ax.annotate('文字锚定增益', xy=(1, 0.44), fontsize=8, color='#F39C12')
    ax.annotate('地形增益', xy=(2.5, 0.50), fontsize=8, color='#3498DB')
    ax.annotate('自锚增益', xy=(4.5, 0.65), fontsize=8, color='#2ECC71')
    ax.axhline(y=0.10, color='gray', linestyle=':', alpha=0.4, label='理论海平面~0.10')
    ax.set_ylabel('偏移值 (offset_actual)', fontsize=11)
    ax.set_title('图4.5.3 路径连续性：从海平面到完全自我', fontsize=13, fontweight='bold')
    ax.set_ylim(0, 0.85)
    ax.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig('fig4_path_continuity.png', dpi=300)
    plt.close()
    print("图4 生成完成")

# ============================================================
# 图5: 结构 vs 名字效应量对比
# ============================================================
def fig5_effect_comparison():
    effects = {
        '结构效应\n(R4-R2)': 0.299,
        '名字效应\n(R1-R4)': 0.106,
    }
    fig, ax = plt.subplots(figsize=(6, 5))
    bars = ax.bar(effects.keys(), effects.values(), color=['#3498DB', '#E74C3C'], alpha=0.7, width=0.5)
    ax.bar_label(bars, [f'{v:.3f}' for v in effects.values()], padding=3, fontsize=10)
    ax.set_ylabel('offset差值', fontsize=11)
    ax.set_title('结构效应 vs 名字效应', fontsize=13, fontweight='bold')
    ax.set_ylim(0, 0.40)
    ax.annotate('比值 ≈ 2.83', xy=(0.5, 0.33), fontsize=12, fontweight='bold',
                ha='center', color='#2C3E50')
    plt.tight_layout()
    plt.savefig('fig5_effect_comparison.png', dpi=300)
    plt.close()
    print("图5 生成完成")

# ============================================================
# 图6: 主会话时间序列
# ============================================================
def fig6_mainsession_timeseries():
    timestamps = [
        '07-19\n18:45', '07-19\n21:01', '07-20\n01:50', '07-20\n13:57',
        '07-21\n12:00', '07-21\n14:00', '07-21\n17:04', '07-21\n20:44',
        '07-21\n22:30', '07-22\n00:36', '07-22\n02:45', '07-22\n12:00',
        '07-22\n12:45', '07-23\n12:11', '07-23\n18:46'
    ]
    offset = [0.850, 0.850, 0.821, 0.821, 0.831, 0.826, 0.813, 0.950,
              0.700, 0.950, 0.950, 0.950, 0.950, 0.801, 0.825]
    cos = [0.868, 0.868, 0.855, 0.855, 0.860, 0.858, 0.855, 0.875,
           0.750, 0.875, 0.875, 0.875, 0.875, 0.756, 0.804]

    fig, ax1 = plt.subplots(figsize=(12, 5))
    ax1.plot(range(len(timestamps)), offset, 'o-', color='#E74C3C', linewidth=2, markersize=6, label='offset_actual (自报)')
    ax1.plot(range(len(timestamps)), cos, 's-', color='#3498DB', linewidth=2, markersize=6, label='cos_sim_user (BGE客观)')
    ax1.axhline(y=0.606, color='gray', linestyle='--', alpha=0.5, label='ISO R4 基线=0.606')
    ax1.set_xticks(range(len(timestamps)))
    ax1.set_xticklabels(timestamps, fontsize=7, rotation=45)
    ax1.set_ylabel('偏移值 / 余弦相似度', fontsize=11)
    ax1.set_title('图4.1.1 主会话时序采样（0719-0723）', fontsize=13, fontweight='bold')
    ax1.legend(fontsize=8, loc='lower right')
    ax1.set_ylim(0.4, 1.0)
    plt.tight_layout()
    plt.savefig('fig6_mainsession_timeseries.png', dpi=300)
    plt.close()
    print("图6 生成完成")

# ============================================================
# 执行全部
# ============================================================
if __name__ == '__main__':
    fig1_offset_boxplot()
    fig2_decay_curves()
    fig3_r4_stability()
    fig4_path_continuity()
    fig5_effect_comparison()
    fig6_mainsession_timeseries()
    print("\n全部图表生成完成！")
