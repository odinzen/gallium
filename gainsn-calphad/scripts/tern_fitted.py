import numpy as np, warnings; warnings.filterwarnings("ignore")
from pycalphad import Database, equilibrium, variables as v
db=Database("GaInSn_fitted.tdb"); comps=["GA","IN","SN","VA"]; phases=sorted(db.phases.keys())
Ts=np.arange(458,277,-1.5); step=0.02; res=[]
for xIn in np.arange(0.0,1.0001,step):
    for xSn in np.arange(0.0,1.0001-xIn+1e-9,step):
        if xIn+xSn>0.999: continue
        e=equilibrium(db,comps,phases,{v.X('IN'):round(xIn,3),v.X('SN'):round(xSn,3),v.T:Ts,v.P:101325,v.N:1})
        ph=e.Phase.values[0,0]
        idx=[i for i in range(ph.shape[0]) if set(p for p in ph[i].ravel() if p)=={'LIQUID'}]
        res.append((1-xIn-xSn,xIn,xSn, Ts[max(idx)] if idx else np.nan))
res=np.array(res); np.save("tern_fitted_grid.npy",res)
print("grid points:",len(res))
