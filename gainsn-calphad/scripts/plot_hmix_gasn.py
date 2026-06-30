"""Excess mixing enthalpy for Ga-Sn liquid from Redlich-Kister fit."""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Redlich-Kister parameters (J/mol), temperature-independent
L0 = 3744.0
L1 =  643.0
L2 = -413.0

EUTECTIC_XSN = 0.072
OUT_PATH = r"C:\Users\busta\Downloads\Calphad_GaInSn_Assessment\figures\FigS1_Hmix_GaSn.png"

# Experimental data from Table 3, Zivkovic et al. (2003)
exp_xsn = np.array([0.000, 0.050, 0.0742, 0.200, 0.400, 0.700, 1.000])
exp_hmix = np.array([0.0, 95.0, 306.0, 673.0, 907.0, 723.0, 0.0])

x_sn = np.linspace(0.0, 1.0, 500)
x_ga = 1.0 - x_sn
delta = x_ga - x_sn
hmix = x_ga * x_sn * (L0 + L1 * delta + L2 * delta**2)

idx_max = np.argmax(hmix)
x_max = x_sn[idx_max]
h_max = hmix[idx_max]

# Interpolate at eutectic
x_ga_eut = 1.0 - EUTECTIC_XSN
delta_eut = x_ga_eut - EUTECTIC_XSN
h_eut = x_ga_eut * EUTECTIC_XSN * (L0 + L1 * delta_eut + L2 * delta_eut**2)

print(f"max H^E = {h_max:.1f} J/mol at x_Sn = {x_max:.4f}")
print(f"H^E at eutectic (x_Sn=0.072) = {h_eut:.1f} J/mol")

# --- Figure ---
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 11,
    "axes.linewidth": 1.2,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.major.width": 1.0,
    "ytick.major.width": 1.0,
    "axes.grid": False,
})

fig, ax = plt.subplots(figsize=(7.2, 5.0))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

ax.plot(x_sn, hmix, color="black", lw=1.8, label="RK fit (this work)")
ax.plot(exp_xsn, exp_hmix, marker="s", ms=7,
        mfc="white", mec="black", mew=1.5, ls="none", zorder=5,
        label="Zivkovic et al. [10] (DTA)")

# Eutectic vertical line
ax.axvline(EUTECTIC_XSN, color="black", lw=1.0, ls="--")
ax.text(EUTECTIC_XSN + 0.015, 50, "eutectic\n(7.2 at% Sn)",
        fontsize=9, color="black", va="bottom")

ax.legend(frameon=False, fontsize=10, loc="upper right")

# RMSD annotation
ax.text(0.38, 0.55 * h_max, "RMSD = 41 J/mol",
        fontsize=10, color="black", va="top")

ax.set_xlabel("Mole fraction Sn, $x$(Sn)", fontsize=13, color="black")
ax.set_ylabel(r"Excess mixing enthalpy, $H^{\mathrm{E}}$ (J/mol)", fontsize=13, color="black")
ax.tick_params(labelsize=11, colors="black")
for spine in ax.spines.values():
    spine.set_edgecolor("black")

ax.set_xlim(0.0, 1.0)
ax.set_ylim(bottom=0.0)

fig.tight_layout()
fig.savefig(OUT_PATH, dpi=600, facecolor="white")
print(f"Saved: {OUT_PATH}")
