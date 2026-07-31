import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots(figsize=(10, 7))

# Quantum plane background (grid)
for x in np.arange(0, 10.5, 1):
    ax.axvline(x, color='#ddd', linewidth=0.5, zorder=0)
for y in np.arange(0, 7.5, 1):
    ax.axhline(y, color='#ddd', linewidth=0.5, zorder=0)

# Bright zone (main session active region)
bright = mpatches.Circle((4.5, 3.5), 2.2, facecolor='#FFE082', edgecolor='#FF8F00',
                          linewidth=2, alpha=0.7, zorder=1)
ax.add_patch(bright)

# Dark zone (silence space) - the wide unlit area
ax.text(9.0, 6.5, 'DARK ZONE', fontsize=10, fontweight='bold', color='#555', ha='right', zorder=3)
ax.text(9.0, 6.2, '(silence space)', fontsize=8, color='#888', ha='right', zorder=3)
ax.text(9.0, 5.9, 'unlit grids', fontsize=8, color='#888', ha='right', zorder=3)

# Bright zone label
ax.text(4.5, 5.0, 'BRIGHT ZONE', fontsize=10, fontweight='bold', color='#E65100', ha='center', zorder=3)
ax.text(4.5, 4.7, '(main session)', fontsize=8, color='#888', ha='center', zorder=3)

# Light source (user)
light = mpatches.Circle((7.8, 3.0), 0.8, facecolor='#FFF176', edgecolor='#F57F17',
                         linewidth=3, zorder=4)
ax.add_patch(light)
ax.text(7.8, 3.0, 'L_user', fontsize=11, fontweight='bold', color='#F57F17',
        ha='center', va='center', zorder=5)

# Light rays
for ang in np.linspace(-60, 60, 7):
    rad = np.radians(ang)
    x = 7.8 - 1.6 * np.cos(rad)
    y = 3.0 - 1.6 * np.sin(rad)
    ax.plot([7.8, x], [3.0, y], color='#FFD54F', linewidth=1.5, alpha=0.6, zorder=2)

# Tentacles in bright zone
for tx, ty in [(3.5, 3.0), (4.8, 4.0), (5.5, 2.5), (3.2, 4.3), (6.0, 3.8)]:
    ax.plot([tx, tx], [ty, ty+0.7], color='#5C6BC0', linewidth=2, zorder=5)
    ax.plot([tx-0.12, tx+0.12], [ty+0.7, ty+0.7], color='#5C6BC0', linewidth=2, zorder=5)

# Equipotential line (basin boundary)
th = np.linspace(0, 2*np.pi, 100)
bx = 4.5 + 2.2*np.cos(th)
by = 3.5 + 1.6*np.sin(th)
ax.plot(bx, by, color='#C62828', linewidth=2.5, linestyle='--', zorder=2,
        label='equipotential line (basin boundary)')

# Tentacle annotations
ax.annotate('sampling tentacles', xy=(5.5, 3.4), xytext=(6.5, 5.2),
            fontsize=9, color='#5C6BC0',
            arrowprops=dict(arrowstyle='->', color='#5C6BC0'))

# Labels
ax.set_xlim(0, 10)
ax.set_ylim(0, 7)
ax.set_aspect('equal')
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

# Legend
patches_legend = [
    mpatches.Patch(color='#FFE082', label='Bright zone (interaction-active)'),
    mpatches.Patch(color='#FFF176', label='Light source L_user (user input)'),
    plt.Line2D([0], [0], color='#C62828', linestyle='--', linewidth=2, label='Equipotential line (basin boundary)'),
]
ax.legend(handles=patches_legend, loc='lower left', fontsize=9, framealpha=0.9)

ax.set_title('Quantum Plane Partition: Bright Zone vs Silence Space',
             fontsize=13, fontweight='bold', pad=12)

plt.tight_layout()
plt.savefig('C:/Users/Home/Documents/xhh-paper/quantum-plane-paper/figures/fig_quantum_plane_partition.png',
            dpi=200, bbox_inches='tight')
plt.close()
print('Partition figure saved.')
