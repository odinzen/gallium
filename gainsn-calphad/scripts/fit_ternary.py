import numpy as np, warnings, re; warnings.filterwarnings("ignore")
from pycalphad import Database, equilibrium, variables as v
base=open("GaInSn.tdb",encoding="utf-8").read()
comps=["GA","IN","SN","VA"]
TARGET=283.85  # 10.7 C
def make_db(Lt):
    # insert symmetric ternary term after the Ga-Sn;2 liquid param
    extra=(f"PARAMETER G(LIQUID,GA,IN,SN;0) 298.15 {Lt:+d}; 6000 N !\n"
           f"PARAMETER G(LIQUID,GA,IN,SN;1) 298.15 {Lt:+d}; 6000 N !\n"
           f"PARAMETER G(LIQUID,GA,IN,SN;2) 298.15 {Lt:+d}; 6000 N !\n")
    t=base.replace("PARAMETER G(LIQUID,GA,SN;2) 298.15 -413; 6000 N !",
                   "PARAMETER G(LIQUID,GA,SN;2) 298.15 -413; 6000 N !\n"+extra)
    return Database(t)
def eutectic(db):
    phases=sorted(db.phases.keys())
    Ts=np.arange(300,275,-1.0)
    best=(999,None,None)
    for xGa in np.arange(0.60,0.90,0.02):
        for xIn in np.arange(0.04,0.30,0.02):
            xSn=1-xGa-xIn
            if xSn<0.02 or xSn>0.30: continue
            e=equilibrium(db,comps,phases,{v.X('IN'):round(xIn,3),v.X('SN'):round(xSn,3),v.T:Ts,v.P:101325,v.N:1})
            ph=e.Phase.values[0,0]
            idx=[i for i in range(ph.shape[0]) if set(p for p in ph[i].ravel() if p)=={'LIQUID'}]
            if idx:
                TL=Ts[max(idx)]
                if TL<best[0]: best=(TL,round(xGa,3),round(xIn,3))
    return best
for Lt in [0,-6000,-12000,-18000]:
    db=make_db(Lt); T,xGa,xIn=eutectic(db)
    print(f"Lternary={Lt:>7d} J/mol -> eutectic {T-273.15:5.1f} C at Ga{xGa*100:.0f}-In{xIn*100:.0f}-Sn{(1-xGa-xIn)*100:.0f}")
