# -*- coding: utf-8 -*-
"""Fine refinement of the ternary eutectic (unfitted GaInSn.tdb and fitted GaInSn_fitted.tdb) around
the grid minima, to a definitive value for the §9 validation table."""
import numpy as np, warnings, json; warnings.filterwarnings("ignore")
from pycalphad import Database, equilibrium, variables as v
comps = ["GA","IN","SN","VA"]

def liquidus(db, phases, xIn, xSn, Ts):
    e = equilibrium(db, comps, phases, {v.X('IN'):round(float(xIn),4), v.X('SN'):round(float(xSn),4),
                                        v.T: Ts, v.P: 101325, v.N: 1})
    ph = e.Phase.values[0,0]
    idx = [i for i in range(ph.shape[0]) if set(p for p in ph[i].ravel() if p) == {'LIQUID'}]
    return Ts[max(idx)] if idx else np.nan

def refine(tdb, inlo, inhi, snlo, snhi, Tlo, Thi):
    db = Database(tdb); phases = sorted(db.phases.keys())
    best = (9e9, None, None)
    for xIn in np.round(np.arange(inlo, inhi, 0.01), 3):
        for xSn in np.round(np.arange(snlo, snhi, 0.01), 3):
            if xIn + xSn > 0.97: continue
            T = liquidus(db, phases, xIn, xSn, np.arange(Thi, Tlo, -0.25))
            if np.isfinite(T) and T < best[0]:
                best = (T, xIn, xSn)
    return best

res = {}
b = refine("GaInSn.tdb", 0.08, 0.17, 0.01, 0.09, 285.0, 298.0)
res["unfitted_C"] = round(b[0]-273.15,2); res["unfitted_GaInSn_at"] = [round(1-b[1]-b[2],2), b[1], b[2]]
b = refine("GaInSn_fitted.tdb", 0.16, 0.25, 0.08, 0.17, 279.0, 293.0)
res["fitted_C"] = round(b[0]-273.15,2); res["fitted_GaInSn_at"] = [round(1-b[1]-b[2],2), b[1], b[2]]
open("refine_tern_out.json","w").write(json.dumps(res, indent=2))
print(json.dumps(res, indent=2))
