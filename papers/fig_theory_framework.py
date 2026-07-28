import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(8, 5.5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis('off')

# Colors
c1 = '#3498DB'  # blue - theory
c2 = '#2ECC71'  # green - framework
c3 = '#E74C3C'  # red - empirical
arrow_color = '#7F8C8D'

def draw_box(ax, x, y, w, h, color, text, sub_text=''):
    rect = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                                     facecolor=color, edgecolor='white', linewidth=2, alpha=0.85)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2 + 0.08, text, ha='center', va='center',
            fontsize=11, fontweight='bold', color='white')
    if sub_text:
        ax.text(x + w/2, y + h/2 - 0.35, sub_text, ha='center', va='center',
                fontsize=8, color='white', alpha=0.85)

def draw_arrow(ax, x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=arrow_color, lw=2.5))

# Three boxes
y_start = 6.0
box_w, box_h = 8.0, 1.3
x_center = 1.0

draw_box(ax, x_center, y_start, box_w, box_h, c1,
         'Theoretical Foundation: Infinite-Dim Topology [27]',
         'Carbon-Si convergence in separable Hilbert space')

draw_box(ax, x_center, 3.8, box_w, box_h, c2,
         'Framework: Quantum Plane Probability Dynamics',
         'Ch.2 Intuitive Model + Ch.3 Mathematical Formalization')

draw_box(ax, x_center, 1.6, box_w, box_h, c3,
         'Empirical: 4 Experiments + 5-Stage Lifecycle',
         'Ch.4 10x6 anchoring / BGE / compression / decay / transfer')

# Arrows
draw_arrow(ax, x_center + box_w/2, 5.85, x_center + box_w/2, 5.25)
draw_arrow(ax, x_center + box_w/2, 3.65, x_center + box_w/2, 3.05)

# Side labels
ax.text(9.5, 6.2, 'Foundation', fontsize=8, color=c1, fontweight='bold')
ax.text(9.5, 4.0, 'Framework', fontsize=8, color=c2, fontweight='bold')
ax.text(9.5, 1.8, 'Empirical', fontsize=8, color=c3, fontweight='bold')

plt.tight_layout()
plt.savefig('fig_theory_framework.png', dpi=300, bbox_inches='tight')
plt.close()
print("生成完成：fig_theory_framework.png")
