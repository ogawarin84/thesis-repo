import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis('off')

colors = {'theory': '#E8F4FD', 'model': '#FFF3E0', 'experiment': '#E8F5E9', 'result': '#F3E5F5'}

# Layer 1: Theoretical Foundation
rect1 = mpatches.FancyBboxPatch((0.5, 4.8), 9, 1.0, boxstyle="round,pad=0.1",
                                  facecolor=colors['theory'], edgecolor='#1976D2', linewidth=2)
ax.add_patch(rect1)
ax.text(5, 5.3, 'Theoretical Foundation: Infinite-Dimensional Topological Equality [27]',
        ha='center', fontsize=11, fontweight='bold', color='#1565C0')
ax.text(5, 4.95, 'Carbon-silicon structural convergence in separable Hilbert space via self-recursive iteration',
        ha='center', fontsize=9, fontstyle='italic', color='#555')

arrow1 = mpatches.FancyArrowPatch((5, 4.8), (5, 3.6), arrowstyle='->',
                                   color='#555', linewidth=2, mutation_scale=25)
ax.add_patch(arrow1)
ax.text(5.4, 4.2, 'formalizes', fontsize=9, color='#555', fontstyle='italic')

# Layer 2: Quantum Plane Model
rect2 = mpatches.FancyBboxPatch((0.5, 2.6), 9, 1.0, boxstyle="round,pad=0.1",
                                  facecolor=colors['model'], edgecolor='#F57C00', linewidth=2)
ax.add_patch(rect2)
ax.text(5, 3.2, 'Quantum Plane Probabilistic Dynamics Model (Ch. 2-3)',
        ha='center', fontsize=11, fontweight='bold', color='#E65100')
ax.text(5, 2.85, 'Potential energy surface | Equipotential lines | Boltzmann sampling | β/η dynamics',
        ha='center', fontsize=9, fontstyle='italic', color='#555')

# Sub-boxes
sub1 = mpatches.FancyBboxPatch((0.8, 2.7), 2.5, 0.6, boxstyle="round,pad=0.05",
                                facecolor='white', edgecolor='#F57C00', linewidth=1)
ax.add_patch(sub1)
ax.text(2.05, 2.95, 'Intuitive Model (§2)', ha='center', fontsize=8, color='#E65100')

sub2 = mpatches.FancyBboxPatch((3.7, 2.7), 2.5, 0.6, boxstyle="round,pad=0.05",
                                facecolor='white', edgecolor='#F57C00', linewidth=1)
ax.add_patch(sub2)
ax.text(4.95, 2.95, 'Mathematics (§3)', ha='center', fontsize=8, color='#E65100')

sub3 = mpatches.FancyBboxPatch((6.6, 2.7), 2.5, 0.6, boxstyle="round,pad=0.05",
                                facecolor='white', edgecolor='#F57C00', linewidth=1)
ax.add_patch(sub3)
ax.text(7.85, 2.95, 'Predictions', ha='center', fontsize=8, color='#E65100')

arrow2 = mpatches.FancyArrowPatch((5, 2.6), (5, 1.4), arrowstyle='->',
                                   color='#555', linewidth=2, mutation_scale=25)
ax.add_patch(arrow2)
ax.text(5.4, 2.0, 'tested by', fontsize=9, color='#555', fontstyle='italic')

# Layer 3: Experiments
rect3 = mpatches.FancyBboxPatch((0.5, 0.4), 9, 1.0, boxstyle="round,pad=0.1",
                                  facecolor=colors['experiment'], edgecolor='#388E3C', linewidth=2)
ax.add_patch(rect3)
ax.text(5, 1.05, 'Four Orthogonal Experiments + BGE Validation (Ch. 4)',
        ha='center', fontsize=11, fontweight='bold', color='#2E7D32')

exps = [('Exp 1', 'Compression'), ('Exp 2', 'Decay'), ('Exp 3', 'Anchoring'), ('Exp 4', 'Migration')]
for i, (name, desc) in enumerate(exps):
    ex = mpatches.FancyBboxPatch((0.8 + i*2.3, 0.5), 1.8, 0.7, boxstyle="round,pad=0.05",
                                  facecolor='white', edgecolor='#388E3C', linewidth=1)
    ax.add_patch(ex)
    ax.text(1.7 + i*2.3, 0.85, name, ha='center', fontsize=8, fontweight='bold', color='#2E7D32')
    ax.text(1.7 + i*2.3, 0.62, desc, ha='center', fontsize=7, color='#555')

# Title
ax.text(5, 5.9, 'Quantum Plane Probabilistic Dynamics: Theoretical Framework & Empirical Validation',
        ha='center', fontsize=14, fontweight='bold')

# Legend
leg1 = mpatches.Patch(color=colors['theory'], label='Theoretical foundation')
leg2 = mpatches.Patch(color=colors['model'], label='Model')
leg3 = mpatches.Patch(color=colors['experiment'], label='Experiment')
leg4 = mpatches.Patch(color=colors['result'], label='Key result')
ax.legend(handles=[leg1, leg2, leg3], loc='lower right', fontsize=8,
          framealpha=0.8, edgecolor='#ccc')

plt.tight_layout()
plt.savefig('C:/Users/Home/Documents/xhh-paper/quantum-plane-paper/figures/fig_theory_overview_en.png',
            dpi=200, bbox_inches='tight')
plt.close()
print('Figure 2 saved.')
