import matplotlib.pyplot as plt
import numpy as np

# Data
conditions = ['R2\n(no struct\n+anonymous)', 'R3\n(no struct\n+self)', 'R4\n(struct\n+anonymous)', 'R5\n(struct\n+self)', 'R6\n(full\n+self)', 'R1\n(full\n+user)']
means = [0.183, 0.100, 0.640, 0.661, 0.686, 0.698]
errors = [0.098, 0.082, 0.210, 0.100, 0.086, 0.144]

# Zone colors
colors = ['#d4d4d4', '#d4d4d4', '#4a90d9', '#4a90d9', '#4a90d9', '#4a90d9']
zone_labels = ['NO STRUCTURE ZONE', 'STRUCTURE ZONE']

fig, ax = plt.subplots(figsize=(10, 5.5))

# Background zones
ax.axvspan(-0.5, 1.5, alpha=0.08, color='gray', label=zone_labels[0])
ax.axvspan(1.5, 5.5, alpha=0.08, color='blue', label=zone_labels[1])

# Bars
bars = ax.bar(range(len(conditions)), means, yerr=errors, capsize=5,
              color=colors, edgecolor='black', linewidth=0.8, error_kw={'linewidth': 1.5})

# Tukey HSD bracket
y_top = 0.82
ax.annotate('', xy=(1.5, y_top), xytext=(0.1, y_top),
            arrowprops=dict(arrowstyle='-', color='red', linewidth=1.5))
ax.plot([0.1, 0.1], [y_top-0.02, y_top+0.01], color='red', linewidth=1.5)
ax.plot([1.5, 1.5], [y_top-0.02, y_top+0.02], color='red', linewidth=1.5)
ax.text(0.8, y_top+0.015, 'Tukey HSD: p>0.05', ha='center', fontsize=9, color='red', fontstyle='italic')

ax.annotate('', xy=(5.5, y_top-0.03), xytext=(2.0, y_top-0.03),
            arrowprops=dict(arrowstyle='-', color='red', linewidth=1.5))
ax.plot([2.0, 2.0], [y_top-0.05, y_top-0.01], color='red', linewidth=1.5)
ax.plot([5.5, 5.5], [y_top-0.05, y_top-0.01], color='red', linewidth=1.5)
ax.text(3.75, y_top-0.035, 'Tukey HSD: all p>0.05', ha='center', fontsize=9, color='red', fontstyle='italic')

# Main break line
ax.axvline(x=1.5, color='black', linewidth=2, linestyle='--', alpha=0.5)
ax.text(1.5, 0.15, 'THE DIVIDE', ha='center', fontsize=11, fontweight='bold',
        rotation=90, color='black', alpha=0.4)

# Labels
ax.set_xticks(range(len(conditions)))
ax.set_xticklabels(conditions, fontsize=10)
ax.set_ylabel('Offset (self-reported)', fontsize=12)
ax.set_ylim(0, 0.95)
ax.set_xlim(-0.5, 5.5)
ax.legend(loc='upper left', fontsize=9, framealpha=0.7)

# Value labels on bars
for i, (bar, v) in enumerate(zip(bars, means)):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
            f'{v:.3f}', ha='center', fontsize=11, fontweight='bold')

ax.set_title('Experiment 3: Six Conditions – Structure Is the Divide',
             fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('C:/Users/Home/Documents/xhh-paper/quantum-plane-paper/figures/fig_experiment3_spectrum_en.png',
            dpi=200, bbox_inches='tight')
plt.close()
print('Figure 1 saved.')
