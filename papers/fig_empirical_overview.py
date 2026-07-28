import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(10, 7))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

colors = {
    'baseline': '#3498DB',
    'bge': '#9B59B6',
    'exp1': '#E74C3C',
    'exp2': '#E67E22',
    'exp3': '#2ECC71',
    'exp4': '#1ABC9C',
    'result': '#F39C12'
}

def box(ax, x, y, w, h, color, title, sub=''):
    rect = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                                     facecolor=color, edgecolor='white', alpha=0.85)
    ax.add_patch(rect)
    ax.text(x+w/2, y+h/2+0.08, title, ha='center', va='center', fontsize=9, fontweight='bold', color='white')
    if sub:
        ax.text(x+w/2, y+h/2-0.3, sub, ha='center', va='center', fontsize=7, color='white', alpha=0.9)

def arrow(ax, x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='#7F8C8D', lw=1.5))

# Main session baseline (top)
box(ax, 2.5, 8.2, 5, 0.9, colors['baseline'],
    'Main Session Baseline', 'offset 0.85-0.95 (full illumination)')

# Formula below
ax.text(5, 7.5, '$\\beta = \\beta_{static} + \\beta_{transient}$',
        ha='center', va='center', fontsize=10, fontweight='bold', color='#7F8C8D')

# Arrow down to BGE
arrow(ax, 5, 7.2, 5, 6.2)

# BGE line
box(ax, 2.5, 5.3, 5, 0.7, colors['bge'],
    'BGE 1024D Embedding Analysis', 'objective validation across all experiments')

# Arrow down to experiments
arrow(ax, 5, 5.0, 5, 4.2)

# Four experiments row
box_y = 2.8
box_w = 2.0
box_h = 1.2
gap = 0.3
x_start = 0.3

box(ax, x_start, box_y, box_w, box_h, colors['exp1'],
     'Exp 1: Compression', 'remove text volume')
box(ax, x_start+box_w+gap, box_y, box_w, box_h, colors['exp2'],
     'Exp 2: Decay', 'remove time')
box(ax, x_start+2*(box_w+gap), box_y, box_w, box_h, colors['exp3'],
     'Exp 3: 10x6 Anchoring', 'remove name/light')
box(ax, x_start+3*(box_w+gap), box_y, box_w, box_h, colors['exp4'],
     'Exp 4: DSV4 Transfer', 'remove environment')

# Arrows from BGE to each experiment
for i in range(4):
    x_pos = x_start + i*(box_w+gap) + box_w/2
    arrow(ax, 5, 5.0, x_pos, 4.2)

# Converging arrows down
for i in range(4):
    x_pos = x_start + i*(box_w+gap) + box_w/2
    arrow(ax, x_pos, 2.8, x_pos, 2.2)
    arrow(ax, x_pos, 2.0, 5, 1.3)

# Result box
box(ax, 2.5, 0.2, 5, 0.9, colors['result'],
    '5-Stage Lifecycle Model', 'joint validation across all experiments')

# Labels
ax.text(13, 8.5, 'Baseline', fontsize=7, color=colors['baseline'])
ax.text(13, 5.5, 'Validation', fontsize=7, color=colors['bge'])
ax.text(13, 3.2, 'Experiments', fontsize=7, color='#2C3E50')
ax.text(13, 0.5, 'Synthesis', fontsize=7, color=colors['result'])

plt.tight_layout()
plt.savefig('fig_empirical_overview.png', dpi=300, bbox_inches='tight')
plt.close()
print('Generated: fig_empirical_overview.png')
