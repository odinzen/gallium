import numpy as np, warnings; warnings.filterwarnings("ignore")
from pycalphad import Database, equilibrium, variables as v
db=Database("InSn_David2004.tdb")
print("phases:",sorted(db.phases.keys()))
comps=["IN","SN","VA"]; phases=sorted(db.phases.keys())
# scan liquidus: for each xSn find lowest T at which only LIQUID stable
Xs=np.round(np.arange(0.02,0.99,0.02),3)
Ts=np.arange(540,360,-2.0)
eq=equilibrium(db,comps,phases,{v.X('SN'):Xs,v.T:Ts,v.P:101325,v.N:1})
ph=eq.Phase.values[0,0]  # (T,X,vtx)
nT,nX,_=ph.shape
def S(c): return set(p for p in c if p)
liqT=np.full(nX,np.nan)
for j in range(nX):
    idx=[i for i in range(nT) if S(ph[i,j])=={'LIQUID'}]
    if idx: liqT[j]=Ts[max(idx)]
j=np.nanargmin(liqT); 
print(f"Liquidus minimum (eutectic): {liqT[j]-273.15:.1f} C at X(Sn)={Xs[j]:.3f}")
print("David 2004 In-Sn eutectic: 120 C (393 K) at 48.3 at% Sn")
# report stable phases at a few points to confirm beta/gamma appear
for xq in [0.20,0.45,0.60,0.90]:
    e=equilibrium(db,comps,phases,{v.X('SN'):xq,v.T:380.0,v.P:101325,v.N:1})
    print(f"  x(Sn)={xq} at 380K (107C): phases={sorted(S(e.Phase.values.ravel()))}")
