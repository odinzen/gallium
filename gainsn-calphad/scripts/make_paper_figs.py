# -*- coding: utf-8 -*-
"""Publication figures for the Ga-In-Sn paper.

Fig5  Ga-Sn binary  (GaInSn.tdb, fitted Ga-Sn liquid)
Fig6  In-Sn binary  (InSn_David2004.tdb) -- beta/gamma intermediate phases
Fig7  isopleth In=18 at% (GaInSn_fitted.tdb) -- passes through computed eutectic
Fig7b isopleth Sn=12 at% (GaInSn_fitted.tdb)

Manual liquidus scan (refined_val.py pattern): at each composition the liquidus is the
highest T at which only LIQUID is stable; NaN if it lies below the scanned window.
Phase boundaries for the binaries come from where the stable phase-set changes on a
(T,x) grid, same idea as plot_pbsn.py. Run from the calphad/ dir.
"""
import sys, json
import numpy as np, warnings
warnings.filterwarnings("ignore")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pycalphad import Database, equilibrium, variables as v

OUT = "../figures"
plt.rcParams.update({
    "font.family": "serif", "font.serif": ["DejaVu Serif", "Times New Roman"],
    "font.size": 14, "axes.linewidth": 1.2, "axes.edgecolor": "black",
    "axes.facecolor": "white", "figure.facecolor": "white", "axes.grid": False,
    "savefig.facecolor": "white",
})
K = 273.15

def pset(cell):
    return frozenset(p for p in cell if p)

def liquidus_T(db, comps, phases, cdict, Ts):
    """Highest T in Ts at which the only stable phase is LIQUID, else NaN."""
    e = equilibrium(db, comps, phases, {**cdict, v.T: Ts, v.P: 101325, v.N: 1})
    ph = e.Phase.values[0, 0]  # (T, [X=1,] vtx) when X conditions are scalar
    idx = [i for i in range(ph.shape[0])
           if frozenset(p for p in ph[i].ravel() if p) == frozenset({"LIQUID"})]
    return Ts[max(idx)] if idx else np.nan


# ---------------------------------------------------------------- binary helpers
def binary_grid(db, comps, phases, xvar, others, Xs, Ts):
    """Return phase-set grid ph[i,j] over (Ts, Xs) for a pseudo-binary along xvar.

    others: dict of the components held at trace (e.g. {'GA':1e-9} for In-Sn out of
    the ternary db, or {} for a true binary db).
    """
    cond = {v.X(xvar): Xs, v.T: Ts, v.P: 101325, v.N: 1}
    for c, val in others.items():
        cond[v.X(c)] = val
    e = equilibrium(db, comps, phases, cond)
    return e.Phase.values[0, 0]  # (T, X, vtx) when both T and X are arrays


def boundary_points(ph, Xs, Ts):
    bx, by = [], []
    nT, nX = ph.shape[0], ph.shape[1]
    for i in range(nT):
        for j in range(nX - 1):
            if pset(ph[i, j]) != pset(ph[i, j + 1]):
                bx.append((Xs[j] + Xs[j + 1]) / 2)
                by.append(Ts[i] - K)
    for j in range(nX):
        for i in range(nT - 1):
            if pset(ph[i, j]) != pset(ph[i + 1, j]):
                bx.append(Xs[j])
                by.append((Ts[i] + Ts[i + 1]) / 2 - K)
    return np.array(bx), np.array(by)


def find_eutectic(db, comps, phases, others, lo, hi, step, Tlo, Thi):
    best = (9e9, None)
    for x in np.round(np.arange(lo, hi, step), 4):
        cd = {v.X("SN"): float(x)}
        cd.update(others)
        T = liquidus_T(db, comps, phases, cd, np.arange(Thi, Tlo, -0.25))
        if np.isfinite(T) and T < best[0]:
            best = (T, float(x))
    return best


def style_axes(ax):
    for s in ax.spines.values():
        s.set_linewidth(1.2)
        s.set_color("black")
    ax.tick_params(labelsize=12, width=1.1)


results = {}

# ============================================================ Fig5  Ga-Sn binary
def fig5():
    db = Database("GaInSn.tdb")
    comps = ["GA", "SN", "VA"]
    phases = ["LIQUID", "ORTHORHOMBIC_GA", "BCT_A5"]
    Xs = np.round(np.arange(0.0, 1.0001, 0.002), 4)
    Ts = np.arange(295.0, 515.0, 1.0)
    ph = binary_grid(db, comps, phases, "SN", {}, Xs, Ts)
    bx, by = boundary_points(ph, Xs, Ts)

    eutT, eutX = find_eutectic(db, comps, phases, {}, 0.02, 0.16, 0.002, 290.0, 320.0)
    results["GaSn"] = {"eut_C": round(eutT - K, 1), "x_Sn": eutX}

    fig, ax = plt.subplots(figsize=(7.2, 5.4))
    fig.subplots_adjust(left=0.13, right=0.95, top=0.95, bottom=0.13)
    ax.scatter(bx, by, s=12, c="black", marker="o", linewidths=0, zorder=3)
    eutC = eutT - K
    ax.hlines(eutC, 0.0, 1.0, color="black", lw=1.0, linestyles=(0, (5, 3)), zorder=2)
    ax.plot([eutX], [eutC], marker="o", ms=8, mfc="white", mec="black", mew=1.6, zorder=6)
    ax.plot([0], [29.9], marker="_", ms=12, color="black")
    ax.plot([1], [231.9], marker="_", ms=12, color="black")
    ax.annotate(f"eutectic\n{eutC:.1f} °C, {eutX*100:.1f} at% Sn",
                xy=(eutX, eutC), xytext=(0.22, 95), fontsize=12, ha="left",
                bbox=dict(fc="white", ec="0.5", pad=2),
                arrowprops=dict(arrowstyle="->", lw=1.0))
    def rl(x, y, t, b=True):
        ax.text(x, y, t, ha="center", va="center", fontsize=13,
                fontweight=("bold" if b else "normal"),
                bbox=dict(fc="white", ec="none", pad=0.5))
    rl(0.5, 300, "L")
    rl(0.035, 60, "(Ga)")
    rl(0.965, 120, "(Sn)")
    rl(0.55, 60, "(Ga) + (Sn)", False)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 260)
    ax.set_xlabel("Mole fraction Sn, $x_{\\mathrm{Sn}}$")
    ax.set_ylabel("Temperature ($^{\\circ}$C)")
    style_axes(ax)
    fig.savefig(f"{OUT}/Fig5.png", dpi=600)
    plt.close(fig)
    print("Fig5 done:", results["GaSn"])


# ============================================================ Fig6  In-Sn binary
def fig6():
    db = Database("InSn_David2004.tdb")
    comps = ["IN", "SN", "VA"]
    phases = sorted(db.phases.keys())  # LIQUID, TETRAGONAL_A6, BCT_A5, BETA, GAMMA
    Xs = np.round(np.arange(0.0, 1.0001, 0.002), 4)
    Ts = np.arange(300.0, 510.0, 1.0)
    ph = binary_grid(db, comps, phases, "SN", {}, Xs, Ts)
    bx, by = boundary_points(ph, Xs, Ts)

    eutT, eutX = find_eutectic(db, comps, phases, {}, 0.40, 0.58, 0.005, 380.0, 420.0)
    results["InSn"] = {"eut_C": round(eutT - K, 1), "x_Sn": eutX}

    fig, ax = plt.subplots(figsize=(7.2, 5.4))
    fig.subplots_adjust(left=0.13, right=0.95, top=0.95, bottom=0.13)
    ax.scatter(bx, by, s=12, c="black", marker="o", linewidths=0, zorder=3)
    eutC = eutT - K
    ax.plot([eutX], [eutC], marker="o", ms=8, mfc="white", mec="black", mew=1.6, zorder=6)
    ax.plot([0], [156.6], marker="_", ms=12, color="black")
    ax.plot([1], [231.9], marker="_", ms=12, color="black")
    ax.annotate(f"eutectic\n{eutC:.1f} °C, {eutX*100:.0f} at% Sn",
                xy=(eutX, eutC), xytext=(0.18, 175), fontsize=12, ha="left",
                bbox=dict(fc="white", ec="0.5", pad=2),
                arrowprops=dict(arrowstyle="->", lw=1.0))
    def rl(x, y, t, b=True, fs=13):
        ax.text(x, y, t, ha="center", va="center", fontsize=fs,
                fontweight=("bold" if b else "normal"),
                bbox=dict(fc="white", ec="none", pad=0.5))
    rl(0.5, 215, "L")
    rl(0.04, 110, "(In)")
    rl(0.97, 150, "(Sn)")
    rl(0.46, 90, "$\\beta$", fs=14)
    rl(0.62, 90, "$\\gamma$", fs=14)
    ax.set_xlim(0, 1)
    ax.set_ylim(80, 250)
    ax.set_xlabel("Mole fraction Sn, $x_{\\mathrm{Sn}}$")
    ax.set_ylabel("Temperature ($^{\\circ}$C)")
    style_axes(ax)
    fig.savefig(f"{OUT}/Fig6.png", dpi=600)
    plt.close(fig)
    print("Fig6 done:", results["InSn"])


# ====================================================== Fig7  isopleth In=20 at%
def isopleth(db, comps, phases, fixed_comp, fixed_val, free_comp, third_comp,
             free_lo, free_hi, free_step, Tlo, Thi):
    """Liquidus T (C) along a line of constant fixed_comp, varying free_comp."""
    xs, Ts_out = [], []
    Tscan = np.arange(Thi, Tlo, -0.25)
    for xf in np.round(np.arange(free_lo, free_hi, free_step), 4):
        cd = {v.X(fixed_comp): float(fixed_val), v.X(free_comp): float(xf)}
        # third component is the dependent balance; pycalphad infers it
        T = liquidus_T(db, comps, phases, cd, Tscan)
        xs.append(xf)
        Ts_out.append(T - K if np.isfinite(T) else np.nan)
    return np.array(xs), np.array(Ts_out)


def fig7():
    db = Database("GaInSn_fitted.tdb")
    comps = ["GA", "IN", "SN", "VA"]
    phases = sorted(db.phases.keys())
    # In fixed 0.18 -- passes through the computed eutectic (Ga0.72, In0.18, Sn0.10)
    # Ga = 0.82 - xSn; xSn free from ~0 up to 0.815
    xs, Tc = isopleth(db, comps, phases, "IN", 0.18, "SN", "GA",
                      0.005, 0.815, 0.002, 280.0, 480.0)
    m = np.isfinite(Tc)
    jmin = np.nanargmin(Tc)
    results["isopleth_In18_minT_C"] = round(float(Tc[jmin]), 1)
    results["isopleth_In18_xSn_at_min"] = round(float(xs[jmin]), 3)

    fig, ax = plt.subplots(figsize=(7.2, 5.4))
    fig.subplots_adjust(left=0.13, right=0.95, top=0.95, bottom=0.13)
    ax.plot(xs[m], Tc[m], color="black", lw=1.8, zorder=4)
    xmn, ymn = xs[jmin], Tc[jmin]
    ax.plot([xmn], [ymn], marker="o", ms=8, mfc="white", mec="black", mew=1.6, zorder=6)
    ax.annotate(f"liquidus min\n{ymn:.1f} °C\n$x_{{\\mathrm{{Sn}}}}$={xmn:.2f}",
                xy=(xmn, ymn), xytext=(xmn + 0.10, ymn + 45), fontsize=12, ha="left",
                bbox=dict(fc="white", ec="0.5", pad=2),
                arrowprops=dict(arrowstyle="->", lw=1.0))
    ax.text(0.5, 0.92, "constant $x_{\\mathrm{In}}=0.18$", transform=ax.transAxes,
            ha="center", va="top", fontsize=13)
    ax.text(0.30, 0.40, "L", transform=ax.transAxes, fontsize=14, fontweight="bold")
    ax.set_xlabel("Mole fraction Sn, $x_{\\mathrm{Sn}}$  (Ga = 0.82 $-\\ x_{\\mathrm{Sn}}$)")
    ax.set_ylabel("Liquidus temperature ($^{\\circ}$C)")
    ax.set_xlim(0, 0.8)
    style_axes(ax)
    fig.savefig(f"{OUT}/Fig7.png", dpi=600)
    plt.close(fig)
    print("Fig7 done:", results["isopleth_In18_minT_C"], "at xSn", results["isopleth_In18_xSn_at_min"])


# ================================================== Fig7b isopleth Sn=12 at%
def fig7b():
    db = Database("GaInSn_fitted.tdb")
    comps = ["GA", "IN", "SN", "VA"]
    phases = sorted(db.phases.keys())
    # Sn fixed 0.12; x(In) free from ~0 to 0.80 (Ga = 0.88 - xIn)
    xs, Tc = isopleth(db, comps, phases, "SN", 0.12, "IN", "GA",
                      0.005, 0.795, 0.002, 280.0, 460.0)
    m = np.isfinite(Tc)
    jmin = np.nanargmin(Tc)
    results["isopleth_Sn12_minT_C"] = round(float(Tc[jmin]), 1)
    results["isopleth_Sn12_xIn_at_min"] = round(float(xs[jmin]), 3)

    fig, ax = plt.subplots(figsize=(7.2, 5.4))
    fig.subplots_adjust(left=0.13, right=0.95, top=0.95, bottom=0.13)
    ax.plot(xs[m], Tc[m], color="black", lw=1.8, zorder=4)
    xmn, ymn = xs[jmin], Tc[jmin]
    ax.plot([xmn], [ymn], marker="o", ms=8, mfc="white", mec="black", mew=1.6, zorder=6)
    ax.annotate(f"liquidus min\n{ymn:.1f} °C\n$x_{{\\mathrm{{In}}}}$={xmn:.2f}",
                xy=(xmn, ymn), xytext=(xmn + 0.10, ymn + 45), fontsize=12, ha="left",
                bbox=dict(fc="white", ec="0.5", pad=2),
                arrowprops=dict(arrowstyle="->", lw=1.0))
    ax.text(0.5, 0.92, "constant $x_{\\mathrm{Sn}}=0.12$", transform=ax.transAxes,
            ha="center", va="top", fontsize=13)
    ax.text(0.30, 0.40, "L", transform=ax.transAxes, fontsize=14, fontweight="bold")
    ax.set_xlabel("Mole fraction In, $x_{\\mathrm{In}}$  (Ga = 0.88 $-\\ x_{\\mathrm{In}}$)")
    ax.set_ylabel("Liquidus temperature ($^{\\circ}$C)")
    ax.set_xlim(0, 0.8)
    style_axes(ax)
    fig.savefig(f"{OUT}/Fig7b_isopleth_GaSn.png", dpi=600)
    plt.close(fig)
    print("Fig7b done:", results["isopleth_Sn12_minT_C"], "at xIn", results["isopleth_Sn12_xIn_at_min"])


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "5"):
        fig5()
    if which in ("all", "6"):
        fig6()
    if which in ("all", "7"):
        fig7()
    if which in ("all", "7b"):
        fig7b()
    with open("paper_figs_invariants.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(json.dumps(results, indent=2))
