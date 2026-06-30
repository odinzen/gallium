import numpy as np, warnings; warnings.filterwarnings("ignore")
from pycalphad import Database, equilibrium, variables as v
db=Database("GaInSn.tdb"); comps=["GA","IN","SN","VA"]; phases=sorted(db.phases.keys())
Ts=np.arange(458,277,-1.5)
step=0.02
gridIn=[]; gridSn=[]
for xIn in np.arange(0.0,1.0001,step):
    for xSn in np.arange(0.0,1.0001-xIn+1e-9,step):
        if xIn+xSn>0.999: continue
        gridIn.append(round(xIn,3)); gridSn.append(round(xSn,3))
res=[]
# process in chunks of compositions to limit memory
CH=40
import itertools
for k in range(0,len(gridIn),CH):
    ci=gridIn[k:k+CH]; cs=gridSn[k:k+CH]
    for a,b in zip(ci,cs):
        e=equilibrium(db,comps,phases,{v.X('IN'):a,v.X('SN'):b,v.T:Ts,v.P:101325,v.N:1})
        ph=e.Phase.values[0,0]
        idx=[i for i in range(ph.shape[0]) if set(p for p in ph[i].ravel() if p)=={'LIQUID'}]
        TL=Ts[max(idx)] if idx else np.nan
        res.append((1-a-b,a,b,TL))
res=np.array(res)
np.save("tern_full_grid.npy",res)
ok=np.isfinite(res[:,3])
interior=ok&(res[:,0]>0.02)&(res[:,1]>0.02)&(res[:,2]>0.02)
im=res[interior]; j=np.argmin(im[:,3]); mn=im[j]
print(f"TERNARY EUTECTIC (full model): {mn[3]-273.15:.1f} C at Ga{mn[0]*100:.0f}-In{mn[1]*100:.0f}-Sn{mn[2]*100:.0f}")
print("Real Galinstan eutectic: ~10.5 C, ~Ga68.5-In21.5-Sn10 (eutectic comp ~Ga61-In25-Sn13)")
# Galinstan point liquidus
e=equilibrium(db,comps,phases,{v.X('IN'):0.215,v.X('SN'):0.10,v.T:Ts,v.P:101325,v.N:1})
ph=e.Phase.values[0,0]; idx=[i for i in range(ph.shape[0]) if set(p for p in ph[i].ravel() if p)=={'LIQUID'}]
print(f"Galinstan point Ga68.5-In21.5-Sn10 liquidus: {Ts[max(idx)]-273.15:.1f} C")
