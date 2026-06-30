# -*- coding: utf-8 -*-
"""
Sensitivity of the ternary eutectic (T and x_Ga) to +/-1000 J/mol perturbations
of the 0L parameter in each binary and in the ternary interaction.

Prints a comparison table against the manuscript Table 3 claims.
"""
import numpy as np
import warnings
import json
warnings.filterwarnings("ignore")

from pycalphad import Database, equilibrium, variables as v

BASE_TDB = "GaInSn_fitted.tdb"

# Baseline parameters (0L only, what we perturb)
# These are added to the base TDB's 0L for each binary/ternary.
PERTURB = 1000.0  # J/mol


def find_eutectic(db, comps, phases, xIn_range, xSn_range, T_range):
    """Coarse + fine grid search for the liquidus minimum (eutectic)."""
    best = (9e9, None, None)
    for xIn in xIn_range:
        for xSn in xSn_range:
            if xIn + xSn > 0.93:
                continue
            try:
                e = equilibrium(
                    db, comps, phases,
                    {v.X('IN'): float(xIn), v.X('SN'): float(xSn),
                     v.T: T_range, v.P: 101325, v.N: 1}
                )
                ph = e.Phase.values[0, 0]
                idx = [i for i in range(ph.shape[0])
                       if set(p for p in ph[i].ravel() if p) == {'LIQUID'}]
                if not idx:
                    continue
                T = T_range[max(idx)]
                if T < best[0]:
                    best = (T, float(xIn), float(xSn))
            except Exception:
                continue
    return best


def build_perturbed_tdb(base_tdb_path, param_key, delta):
    """
    Read the base TDB text, find the PARAMETER line for param_key (one of
    'GA,IN;0', 'GA,SN;0', 'IN,SN;0', 'GA,IN,SN;0') in LIQUID, and shift its
    constant term by delta J/mol.  Returns a modified TDB string.
    """
    with open(base_tdb_path) as f:
        lines = f.readlines()

    # Map shorthand keys to the substring that uniquely identifies the line.
    search_map = {
        'GA,IN;0':    'G(LIQUID,GA,IN;0)',
        'GA,SN;0':    'G(LIQUID,GA,SN;0)',
        'IN,SN;0':    'G(LIQUID,IN,SN;0)',
        'GA,IN,SN;0': 'G(LIQUID,GA,IN,SN;0)',
    }
    target = search_map[param_key]

    new_lines = []
    for line in lines:
        if target in line:
            # The PARAMETER line looks like:
            #   PARAMETER G(LIQUID,GA,IN;0) 298.15 +4345+1.700*T; 6000 N !
            # or
            #   PARAMETER G(LIQUID,GA,SN;0) 298.15 +3744; 6000 N !
            # We inject +delta (or -delta) at the very start of the expression,
            # right after the temperature token (298.15).
            import re
            # Find the expression between the second number and the semicolon.
            m = re.match(
                r'(PARAMETER\s+G\([^)]+\)\s+[\d.]+\s+)(\+.+?)(;\s*\d+\s+N\s+!\s*)$',
                line.strip()
            )
            if m:
                prefix = m.group(1)
                expr   = m.group(2)
                suffix = m.group(3)
                sign = '+' if delta >= 0 else ''
                new_expr = f"{sign}{delta:g}{expr}"
                new_lines.append(f" {prefix}{new_expr}{suffix}\n")
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    return ''.join(new_lines)


def eut_from_tdb_text(tdb_text):
    """Write a temp TDB and find the eutectic."""
    import tempfile, os
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tdb',
                                    delete=False, dir='.') as f:
        f.write(tdb_text)
        fname = f.name
    try:
        db = Database(fname)
        comps = ['GA', 'IN', 'SN', 'VA']
        phases = sorted(db.phases.keys())
        T_range = np.arange(298.0, 276.0, -0.5)
        xIn_range = np.round(np.arange(0.12, 0.28, 0.02), 3)
        xSn_range = np.round(np.arange(0.06, 0.20, 0.02), 3)
        T, xIn, xSn = find_eutectic(db, comps, phases, xIn_range, xSn_range, T_range)
        if T > 1e8:
            return None
        # refine
        xIn_r = np.round(np.arange(xIn - 0.03, xIn + 0.031, 0.005), 4)
        xSn_r = np.round(np.arange(xSn - 0.03, xSn + 0.031, 0.005), 4)
        T2, xIn2, xSn2 = find_eutectic(db, comps, phases, xIn_r, xSn_r, T_range)
        if T2 < T:
            T, xIn, xSn = T2, xIn2, xSn2
        return {'T_C': round(T - 273.15, 2), 'xGa': round(1 - xIn - xSn, 3),
                'xIn': round(xIn, 3), 'xSn': round(xSn, 3)}
    finally:
        os.unlink(fname)


# --- Baseline ---
print("Computing baseline eutectic...")
with open(BASE_TDB) as f:
    base_text = f.read()
baseline = eut_from_tdb_text(base_text)
print(f"  Baseline: T={baseline['T_C']} C, Ga={baseline['xGa']*100:.1f}%, "
      f"In={baseline['xIn']*100:.1f}%, Sn={baseline['xSn']*100:.1f}%")

# Manuscript Table 3 claimed baseline
MS_T = 10.4   # C
MS_XGA = 0.72  # at fraction

# --- Sensitivity loop ---
params = ['GA,IN;0', 'GA,SN;0', 'IN,SN;0', 'GA,IN,SN;0']
param_labels = ['Ga-In 0L', 'Ga-Sn 0L', 'In-Sn 0L', 'L(Ga,In,Sn)']

# Manuscript Table 3 claims: [dT_plus, dT_minus, dxGa_plus, dxGa_minus]
ms_claims = {
    'GA,IN;0':    (+4.75, -5.25, +0.10, -0.06),
    'GA,SN;0':    (+3.50, -4.00, +0.08, -0.04),
    'IN,SN;0':    (+1.50, -1.00, +0.06, -0.06),
    'GA,IN,SN;0': (+0.25, -0.25, +0.02,  0.00),
}

results = {}
for key, label in zip(params, param_labels):
    print(f"\nPerturbing {label} by +{PERTURB:.0f} J/mol...")
    plus_text = build_perturbed_tdb(BASE_TDB, key, +PERTURB)
    plus = eut_from_tdb_text(plus_text)

    print(f"Perturbing {label} by -{PERTURB:.0f} J/mol...")
    minus_text = build_perturbed_tdb(BASE_TDB, key, -PERTURB)
    minus = eut_from_tdb_text(minus_text)

    if plus and minus:
        dT_plus  = plus['T_C']  - baseline['T_C']
        dT_minus = minus['T_C'] - baseline['T_C']
        dxGa_plus  = plus['xGa']  - baseline['xGa']
        dxGa_minus = minus['xGa'] - baseline['xGa']
    else:
        dT_plus = dT_minus = dxGa_plus = dxGa_minus = float('nan')

    results[key] = {
        'plus':  plus,
        'minus': minus,
        'dT_plus':    round(dT_plus, 2)  if plus  else None,
        'dT_minus':   round(dT_minus, 2) if minus else None,
        'dxGa_plus':  round(dxGa_plus, 3)  if plus  else None,
        'dxGa_minus': round(dxGa_minus, 3) if minus else None,
    }

# --- Report ---
print("\n" + "="*80)
print(f"BASELINE (computed): T = {baseline['T_C']} C, "
      f"Ga={baseline['xGa']*100:.1f}, In={baseline['xIn']*100:.1f}, Sn={baseline['xSn']*100:.1f} at%")
print(f"BASELINE (manuscript): T = {MS_T} C, Ga={MS_XGA*100:.1f} at%")
print("="*80)
print(f"\n{'Parameter':<20} {'dT+':>8} {'ms dT+':>8} {'dT-':>8} {'ms dT-':>8} "
      f"{'dxGa+':>8} {'ms+':>8} {'dxGa-':>8} {'ms-':>8}")
print("-"*80)
for key, label in zip(params, param_labels):
    r = results[key]
    c = ms_claims[key]
    print(f"{label:<20} {r['dT_plus']:>8.2f} {c[0]:>8.2f} "
          f"{r['dT_minus']:>8.2f} {c[1]:>8.2f} "
          f"{r['dxGa_plus']:>8.3f} {c[2]:>8.3f} "
          f"{r['dxGa_minus']:>8.3f} {c[3]:>8.3f}")

print("\nFull results saved to sensitivity_out.json")
with open('sensitivity_out.json', 'w') as f:
    json.dump({'baseline': baseline, 'results': results}, f, indent=2)
