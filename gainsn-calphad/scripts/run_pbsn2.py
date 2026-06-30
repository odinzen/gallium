import os, glob, numpy as np, pycalphad
from pycalphad import Database, equilibrium, variables as v
base=os.path.dirname(pycalphad.__file__)
tdb=[f for f in glob.glob(base+'/**/pbsn.tdb',recursive=True)][0]
db=Database(tdb); comps=['PB','SN','VA']; phases=['LIQUID','FCC_A1','BCT_A5']
MSn,MPb=118.71,207.2

# Liquidus + boundary map via equilibrium grid
Xs=np.round(np.arange(0.0,1.0001,0.005),4)
Ts=np.arange(398.0,615.0,1.0)
eq=equilibrium(db,comps,phases,{v.X('SN'):Xs, v.T:Ts, v.P:101325, v.N:1})
Phase=eq.Phase.values  # shape (...,T,X,vertex)
# reshape: dims order P,N,T,X,vertex
ph=Phase[0,0]  # (T, X, vertex)
nT,nX,_=ph.shape
# number of distinct stable phases per (T,X)
import numpy as np
def nphases(cell): 
    return len(set(p for p in cell if p))
np.save("pbsn_grid_phase.npy", ph)
np.save("pbsn_grid_axes.npy", np.array([Ts.min(),Ts.max(),nT,Xs.min(),Xs.max(),nX]))

# liquidus: highest T at each X where LIQUID present AND a solid present (i.e. boundary) -> approx by:
# for each X, find lowest T at which ONLY liquid is stable (above liquidus all liquid)
liqT=np.full(nX,np.nan)
for j in range(nX):
    col=ph[:,j,:]
    allliq=[ (set(p for p in col[i] if p)=={'LIQUID'}) for i in range(nT)]
    # liquidus = lowest T index that is all-liquid
    idx=[i for i,b in enumerate(allliq) if b]
    if idx: liqT[j]=Ts[min(idx)]
# eutectic = min of liquidus over interior
interior=(Xs>0.02)&(Xs<0.98)
jmin=np.nanargmin(np.where(interior,liqT,np.nan))
eutT=liqT[jmin]; eutX=Xs[jmin]
wSn=eutX*MSn/(eutX*MSn+(1-eutX)*MPb)*100
print(f"COMPUTED eutectic: {eutT-273.15:.1f} C  at X(Sn)={eutX:.3f}  ({wSn:.1f} wt% Sn)")
print("LITERATURE        : 183.0 C  at ~61.9 wt% Sn")
np.save("pbsn_liquidus.npy", np.vstack([Xs,liqT]))
print("saved grid+liquidus")
