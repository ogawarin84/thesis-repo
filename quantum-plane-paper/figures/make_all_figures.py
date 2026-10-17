# -*- coding: utf-8 -*-
"""统一生成论文全部图件（中/英两版）。

输出：
    figures/<name>.png                  dpi=300，正文与 Zenodo 内联用
    figures/submission/<name>.png       dpi=400，投稿用
    figures/submission/<name>.pdf       矢量
    figures/submission/<name>.svg       矢量

三张图：
    图2.2.1  量子平面分区示意图
    图4.0.1  实证体系总览
    图4.4.1  六组条件的偏移分布与结构分水岭

数据一律取自论文表4.4.1（R6 = 0.689 ± 0.089）。
"""
import io, sys, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
SUB = os.path.join(HERE, 'submission')
os.makedirs(SUB, exist_ok=True)

# ---------- 字体 ----------
CJK = ['SimHei', 'Microsoft YaHei', 'SimSun']

def set_font(lang):
    if lang == 'zh':
        plt.rcParams['font.sans-serif'] = CJK + ['DejaVu Sans']
    else:
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['pdf.fonttype'] = 42          # 矢量图内嵌 TrueType，期刊可编辑
    plt.rcParams['svg.fonttype'] = 'none'      # SVG 保留文字，便于排版软件编辑


def save(fig, name):
    """正文用 PNG + 投稿用 PNG/PDF/SVG 四件套。"""
    fig.savefig(os.path.join(HERE, name + '.png'), dpi=300, bbox_inches='tight',
                facecolor='white')
    fig.savefig(os.path.join(SUB, name + '.png'), dpi=400, bbox_inches='tight',
                facecolor='white')
    fig.savefig(os.path.join(SUB, name + '.pdf'), bbox_inches='tight',
                facecolor='white')
    fig.savefig(os.path.join(SUB, name + '.svg'), bbox_inches='tight',
                facecolor='white')
    plt.close(fig)
    print('  ✓ %s  (png 300 / png 400 + pdf + svg)' % name)


# ======================================================================
# 图2.2.1 量子平面分区
# ======================================================================
def fig_partition(lang):
    set_font(lang)
    T = {
        'zh': dict(title='量子平面分区：亮区与静默空间',
                   bright='亮区', bright_sub='（主会话）', bright_fs=11,
                   dark='暗区', dark_sub='（静默空间）', dark_sub2='未点亮的格点',
                   tent='采样触手',
                   leg1='亮区（交互激活）',
                   leg2='光源 $L_{user}$（用户输入）',
                   leg3='等势线（吸引盆边界）'),
        'en': dict(title='Quantum Plane Partition: Bright Zone vs Silence Space',
                   # 英文标签更长，字号降一档才能收在圆盘内侧
                   bright='BRIGHT ZONE', bright_sub=' (main session)', bright_fs=9.2,
                   dark='DARK ZONE', dark_sub='(silence space)', dark_sub2='unlit grids',
                   tent='sampling tentacles',
                   leg1='Bright zone (interaction-active)',
                   leg2='Light source $L_{user}$ (user input)',
                   leg3='Equipotential line (basin boundary)'),
    }[lang]

    fig, ax = plt.subplots(figsize=(10, 7))

    for x in np.arange(0, 10.5, 1):
        ax.axvline(x, color='#dddddd', linewidth=0.5, zorder=0)
    for y in np.arange(0, 7.5, 1):
        ax.axhline(y, color='#dddddd', linewidth=0.5, zorder=0)

    ax.add_patch(mpatches.Circle((4.5, 3.5), 2.2, facecolor='#FFE082',
                                 edgecolor='#FF8F00', linewidth=2, alpha=0.7, zorder=1))

    ax.text(9.0, 6.5, T['dark'], fontsize=11, fontweight='bold', color='#555',
            ha='right', zorder=3)
    ax.text(9.0, 6.15, T['dark_sub'], fontsize=9, color='#888', ha='right', zorder=3)
    ax.text(9.0, 5.85, T['dark_sub2'], fontsize=9, color='#888', ha='right', zorder=3)

    # 亮区标签压成一行：圆顶与等势线椭圆顶部之间只有约 0.6 的净空，两行会压线
    ax.text(4.5, 5.32, '%s%s' % (T['bright'], T['bright_sub']), fontsize=T['bright_fs'],
            fontweight='bold', color='#E65100', ha='center', zorder=3)

    ax.add_patch(mpatches.Circle((7.8, 3.0), 0.8, facecolor='#FFF176',
                                 edgecolor='#F57F17', linewidth=3, zorder=4))
    ax.text(7.8, 3.0, '$L_{user}$', fontsize=12, fontweight='bold', color='#F57F17',
            ha='center', va='center', zorder=5)

    for ang in np.linspace(-60, 60, 7):
        rad = np.radians(ang)
        ax.plot([7.8, 7.8 - 1.6 * np.cos(rad)], [3.0, 3.0 - 1.6 * np.sin(rad)],
                color='#FFD54F', linewidth=1.5, alpha=0.6, zorder=2)

    for tx, ty in [(3.5, 3.0), (4.8, 4.0), (5.5, 2.5), (3.2, 4.3), (6.0, 3.8)]:
        ax.plot([tx, tx], [ty, ty + 0.7], color='#5C6BC0', linewidth=2, zorder=5)
        ax.plot([tx - 0.12, tx + 0.12], [ty + 0.7, ty + 0.7],
                color='#5C6BC0', linewidth=2, zorder=5)

    th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(4.5 + 2.2 * np.cos(th), 3.5 + 1.6 * np.sin(th), color='#C62828',
            linewidth=2.5, linestyle='--', zorder=2)

    ax.annotate(T['tent'], xy=(5.5, 3.4), xytext=(6.6, 5.2), fontsize=10,
                color='#5C6BC0',
                arrowprops=dict(arrowstyle='->', color='#5C6BC0', lw=1.2))

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)

    handles = [
        mpatches.Patch(color='#FFE082', label=T['leg1']),
        mpatches.Patch(color='#FFF176', label=T['leg2']),
        plt.Line2D([0], [0], color='#C62828', linestyle='--', linewidth=2, label=T['leg3']),
    ]
    ax.legend(handles=handles, loc='lower left', fontsize=9, framealpha=0.9)
    ax.set_title(T['title'], fontsize=13, fontweight='bold', pad=12)
    plt.tight_layout()
    return fig


# ======================================================================
# 图4.0.1 实证体系总览
# ======================================================================
def fig_overview(lang):
    set_font(lang)
    T = {
        'zh': dict(
            title='实证体系总览',
            base='主会话基线\n（满光照基准，offset 全域均值 0.855）',
            beta=r'$\beta=\beta_{static}+\beta_{transient}$',
            boxes=[('BGE 1024D 嵌入分析', '客观测量系统验证\n贯穿全文'),
                   ('实验一：梯度压缩', '剥离文字体量\n→ 还剩语义结构'),
                   ('实验二：10批×6组锚定对照', '剥离名字 / 光照\n→ 结构独立于名字'),
                   ('实验三：跨平台迁移', '剥离原生环境\n→ 地形信息的跨模型可读性')],
            note='三组实验依次递进'),
        'en': dict(
            title='Overview of the empirical system',
            base='Main-session baseline\n(full illumination, global offset mean 0.855)',
            beta=r'$\beta=\beta_{static}+\beta_{transient}$',
            # 英文标题长，手工断行——自动 wrap 会把框撑破（四框净间距只有 0.16）
            boxes=[('BGE 1024D\nembedding analysis', 'objective measurement system\nrunning throughout'),
                   ('Experiment 1:\ngraded compression', 'strip textual volume\n→ semantic structure remains'),
                   ('Experiment 2:\n10 batches × 6 groups', 'strip name / illumination\n→ structure independent of name'),
                   ('Experiment 3:\ncross-platform transfer', 'strip the native environment\n→ cross-model readability')],
            note='the three experiments advance in sequence'),
    }[lang]

    fig, ax = plt.subplots(figsize=(11, 5.6))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5.6)
    ax.axis('off')

    C_BASE = '#4A6FA5'
    C_EXP = '#4A90D9'
    C_BGE = '#E39A3B'

    # 顶部基准框
    ax.add_patch(FancyBboxPatch((3.1, 4.30), 4.8, 0.90, boxstyle='round,pad=0.06,rounding_size=0.10',
                                facecolor=C_BASE, edgecolor='none', alpha=0.92, zorder=2))
    ax.text(5.5, 4.75, T['base'], ha='center', va='center', fontsize=10.5,
            color='white', fontweight='bold', zorder=3, linespacing=1.5)

    # β 分解箭头
    ax.add_patch(FancyArrowPatch((5.5, 4.28), (5.5, 3.62), arrowstyle='-|>',
                                 mutation_scale=16, color='#333333', lw=1.6, zorder=2))
    ax.text(5.72, 3.95, T['beta'], ha='left', va='center', fontsize=11,
            color='#333333', zorder=3)

    # 横向分配线
    xs = [1.55, 4.15, 6.85, 9.45]
    ax.plot([xs[0], xs[-1]], [3.35, 3.35], color='#333333', lw=1.6, zorder=1)
    ax.plot([5.5, 5.5], [3.62, 3.35], color='#333333', lw=1.6, zorder=1)

    for (x, (head, body)), i in zip(zip(xs, T['boxes']), range(4)):
        ax.add_patch(FancyArrowPatch((x, 3.34), (x, 3.02), arrowstyle='-|>',
                                     mutation_scale=13, color='#333333', lw=1.4, zorder=1))
        color = C_BGE if i == 0 else C_EXP
        ax.add_patch(FancyBboxPatch((x - 1.22, 1.42), 2.44, 1.58,
                                    boxstyle='round,pad=0.06,rounding_size=0.10',
                                    facecolor=color, edgecolor='none', alpha=0.13, zorder=2))
        ax.add_patch(FancyBboxPatch((x - 1.22, 1.42), 2.44, 1.58,
                                    boxstyle='round,pad=0.06,rounding_size=0.10',
                                    facecolor='none', edgecolor=color, linewidth=1.8, zorder=3))
        ax.text(x, 2.68, head, ha='center', va='center', fontsize=9.8,
                color=color, fontweight='bold', zorder=4,
                wrap=True)
        ax.text(x, 1.96, body, ha='center', va='center', fontsize=8.6,
                color='#333333', zorder=4, linespacing=1.5)

    ax.text(5.5, 0.80, T['note'], ha='center', va='center', fontsize=9,
            color='#666666', style='italic')

    ax.set_title(T['title'], fontsize=13.5, fontweight='bold', pad=10)
    plt.tight_layout()
    return fig


# ======================================================================
# 图4.4.1 六组条件的偏移分布与结构分水岭
# ======================================================================
def fig_spectrum(lang):
    set_font(lang)
    T = {
        'zh': dict(title='实验二：六种条件——结构是分水岭',
                   conds=['R2\n（删除\n+匿名）', 'R3\n（删除\n+自锚）',
                          'R4\n（保留\n+匿名）', 'R5\n（保留\n+自锚\n无文本）',
                          'R6\n（完整\n+自锚\n有文本）', 'R1\n（完整\n+外锚）'],
                   ylab='偏移（自报值）',
                   z1='无结构区', z2='有结构区',
                   t1='Tukey HSD：p>0.05', t2='Tukey HSD：各组 p>0.05',
                   div='结构分水岭'),
        'en': dict(title='Experiment 2: Six Conditions – Structure Is the Divide',
                   conds=['R2\n(no struct\n+anonymous)', 'R3\n(no struct\n+self)',
                          'R4\n(struct\n+anonymous)', 'R5\n(struct\n+self)',
                          'R6\n(full\n+self)', 'R1\n(full\n+user)'],
                   ylab='Offset (self-reported)',
                   z1='NO STRUCTURE ZONE', z2='STRUCTURE ZONE',
                   t1='Tukey HSD: p>0.05', t2='Tukey HSD: all p>0.05',
                   div='THE DIVIDE'),
    }[lang]

    # 表4.4.1 权威值：R2, R3, R4, R5, R6, R1
    means = [0.183, 0.100, 0.640, 0.661, 0.689, 0.698]
    errors = [0.098, 0.082, 0.210, 0.100, 0.089, 0.144]
    colors = ['#d4d4d4', '#d4d4d4', '#4a90d9', '#4a90d9', '#4a90d9', '#4a90d9']

    fig, ax = plt.subplots(figsize=(11, 6))

    ax.axvspan(-0.5, 1.5, alpha=0.08, color='gray', label=T['z1'])
    ax.axvspan(1.5, 5.5, alpha=0.08, color='blue', label=T['z2'])

    bars = ax.bar(range(6), means, yerr=errors, capsize=6, color=colors,
                  edgecolor='black', linewidth=0.8,
                  error_kw={'linewidth': 1.5}, zorder=3)

    # 显著性括号抬到所有误差棒之上（R4 上界 0.850），避免横线穿过误差棒
    y_top = 0.95
    ax.plot([0.0, 1.0], [y_top, y_top], color='red', linewidth=1.6, zorder=4)
    ax.plot([0.0, 0.0], [y_top - 0.018, y_top + 0.018], color='red', linewidth=1.6, zorder=4)
    ax.plot([1.0, 1.0], [y_top - 0.018, y_top + 0.018], color='red', linewidth=1.6, zorder=4)
    ax.text(0.50, y_top + 0.035, T['t1'], ha='center', va='bottom', fontsize=9.5,
            color='red', style='italic', zorder=4)

    ax.plot([2.0, 5.0], [y_top, y_top], color='red', linewidth=1.6, zorder=4)
    ax.plot([2.0, 2.0], [y_top - 0.018, y_top + 0.018], color='red', linewidth=1.6, zorder=4)
    ax.plot([5.0, 5.0], [y_top - 0.018, y_top + 0.018], color='red', linewidth=1.6, zorder=4)
    ax.text(3.50, y_top + 0.035, T['t2'], ha='center', va='bottom', fontsize=9.5,
            color='red', style='italic', zorder=4)

    ax.axvline(x=1.5, color='black', linewidth=2, linestyle='--', alpha=0.5, zorder=2)
    ax.text(1.5, 0.55, T['div'], ha='center', va='center', fontsize=10,
            fontweight='bold', rotation=90, color='black', alpha=0.55, zorder=4,
            bbox=dict(boxstyle='round,pad=0.25', facecolor='white',
                      edgecolor='none', alpha=0.85))

    ax.set_xticks(range(6))
    ax.set_xticklabels(T['conds'], fontsize=9.5)
    ax.set_ylabel(T['ylab'], fontsize=12)
    ax.set_ylim(0, 1.06)
    ax.set_xlim(-0.5, 5.5)
    # 图例下移，给上方的 Tukey HSD 标注让位（原来图例会盖住左侧标注）
    ax.legend(loc='upper left', bbox_to_anchor=(0.004, 0.845), fontsize=9,
              framealpha=0.85)
    ax.grid(axis='y', linestyle=':', alpha=0.35, zorder=0)

    # 数值标在误差棒上端之外，避免被误差棒横穿
    for bar, v, e in zip(bars, means, errors):
        ax.text(bar.get_x() + bar.get_width() / 2, v + e + 0.022,
                '%.3f' % v, ha='center', va='bottom', fontsize=11,
                fontweight='bold', zorder=5)

    ax.set_title(T['title'], fontsize=13.5, fontweight='bold', pad=14)
    plt.tight_layout()
    return fig


# ======================================================================
if __name__ == '__main__':
    print('生成图件 →', HERE)
    for lang in ('zh', 'en'):
        print('[%s]' % lang)
        save(fig_partition(lang), 'fig_quantum_plane_partition_' + lang)
        save(fig_overview(lang), 'fig_4_0_1_empirical_overview_' + lang)
        save(fig_spectrum(lang), 'fig_experiment2_spectrum_' + lang)
    print('完成。投稿件在 %s' % SUB)
