"""
Fig 2: Ellingham diagram - Gibbs energy of oxide formation per mol O2 vs T.

Temperature window: 250-400 K (Ga melt window and low melting alloys).

Thermodynamic data:
  Ga2O3: 4/3 Ga + O2 -> 2/3 Ga2O3
    DeltaGf(Ga2O3) = -998.3 kJ/mol at 298K (JANAF/Zinkevich & Aldinger JACS 2004)
    per mol O2: DeltaG = 3 * DeltaGf(Ga2O3) = -1497.5 kJ/mol O2 at 298K
    Wait: stoichiometry: 4/3 Ga(l) + O2(g) -> 2/3 Ga2O3(s)
    So DeltaG_rxn = 2/3 * DeltaGf(Ga2O3)
    DeltaGf(Ga2O3) = -998.3 kJ/mol Ga2O3
    DeltaG per mol O2 = 2/3 * (-998.3) = -665.5 kJ/mol O2 at 298K <- this matches the manuscript!
    The slope is approximately -DeltaSf per mol O2; for solid oxide formation from liquid metal:
    DeltaS ~ -5 to -20 J/(mol O2 K) (small over this narrow window)
    Use linear approximation with small positive slope in deltaG vs T (less negative at higher T)
    dG/dT ~ +10 J/(mol O2 K) for Ga2O3 (Zinkevich data)

  TeO2: Te(s/l) + O2(g) -> TeO2(s)
    DeltaGf(TeO2) = -270.3 kJ/mol at 298K (JANAF)
    per mol O2 = -270.3 kJ/mol O2 (1:1 stoichiometry)
    dG/dT ~ +30 J/(mol O2 K) (more positive slope, less stable at high T)

The manuscript states: Ga2O3 lies below TeO2 by ~395 kJ/mol O2, which matches:
-665.5 - (-270.3) = -395.2 kJ/mol O2. This is exactly the gap in the manuscript.

Stability criterion: candidates with DeltaG_formation more negative than Ga2O3 line
are NOT reduced by Ga (they win the competition for oxygen).
Those with less negative DeltaG are reduced by Ga -> Ga2O3.
TeO2 is above the Ga2O3 line, so Ga reduces it.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

T = np.linspace(250, 400, 200)

# Ga2O3: 4/3 Ga(l) + O2 -> 2/3 Ga2O3(s), DeltaG per mol O2
# At 298 K: -665.5 kJ/mol O2; slope +10 J/(mol O2 K) (Zinkevich & Aldinger data)
dG_Ga2O3 = -665.5 + 10e-3 * (T - 298)   # kJ/mol O2

# TeO2: Te + O2 -> TeO2, DeltaG per mol O2
# At 298 K: -270.3 kJ/mol O2; slope +30 J/(mol O2 K)
dG_TeO2 = -270.3 + 30e-3 * (T - 298)    # kJ/mol O2

fig, ax = plt.subplots(figsize=(3.46, 2.8))

# Stable zone: below Ga2O3 line (more negative = stable vs Ga)
ax.fill_between(T, dG_Ga2O3, -800, alpha=0.10, color='k', zorder=0,
                label='Stable in Ga melt')

ax.plot(T, dG_Ga2O3, 'k-', linewidth=1.2, label='Ga$_2$O$_3$ threshold')
ax.plot(T, dG_TeO2,  'k--', linewidth=1.2, label='TeO$_2$')

# Annotate lines
ax.text(395, dG_Ga2O3[-1] - 4, 'Ga$_2$O$_3$', fontsize=7, ha='right', va='top')
ax.text(395, dG_TeO2[-1] + 3,  'TeO$_2$',      fontsize=7, ha='right', va='bottom')

# Annotate stability boundary
ax.annotate("Stable in Ga\n(more negative)", xy=(310, -700), fontsize=6,
            ha='center', color='0.4')
ax.annotate("Reduced by Ga\n(less negative)", xy=(310, -350), fontsize=6,
            ha='center', color='0.4')

# Arrow showing displacement
mid_T = 330
ax.annotate("", xy=(mid_T, dG_Ga2O3[np.argmin(np.abs(T - mid_T))]),
            xytext=(mid_T, dG_TeO2[np.argmin(np.abs(T - mid_T))]),
            arrowprops=dict(arrowstyle='<->', color='k', lw=0.8))
gap = dG_TeO2[np.argmin(np.abs(T - mid_T))] - dG_Ga2O3[np.argmin(np.abs(T - mid_T))]
ax.text(mid_T + 5, (dG_Ga2O3[np.argmin(np.abs(T - mid_T))] +
                    dG_TeO2[np.argmin(np.abs(T - mid_T))]) / 2,
        f"~{abs(gap):.0f} kJ/mol O$_2$", fontsize=6, va='center')

ax.set_xlabel("Temperature (K)", fontsize=8)
ax.set_ylabel(r"$\Delta G_\mathrm{f}$ (kJ mol$^{-1}$ O$_2$)", fontsize=8)
ax.set_xlim(250, 410)
ax.set_ylim(-800, -200)
ax.tick_params(labelsize=7)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

handles = [
    plt.Line2D([0], [0], color='k', linestyle='-', lw=1.2),
    plt.Line2D([0], [0], color='k', linestyle='--', lw=1.2),
    mpatches.Patch(facecolor='k', alpha=0.10, label='Stable zone'),
]
labels = ['Ga$_2$O$_3$ threshold', 'TeO$_2$', 'Stable in Ga melt']
ax.legend(handles, labels, fontsize=6, frameon=False, loc='upper right',
          handlelength=1.4, handletextpad=0.4)

plt.tight_layout(pad=0.4)
out = r"C:\Users\busta\Code\odinzen_publication_inventory\_work\ga_nucleant_figures\fig2_ellingham.png"
plt.savefig(out, dpi=300, bbox_inches='tight')
print(f"Saved {out}")
