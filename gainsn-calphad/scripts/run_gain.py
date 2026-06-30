import numpy as np
from scipy.optimize import brentq
R=8.314462618
# Ga-In liquid excess (Rugg & Chart, Table 4): GE = xGa*xIn*[L0 + L1*(xGa-xIn) + L2*(xGa-xIn)^2]
def L(T): return (4345+1.700*T, -146+0.464*T, 248.0)
def GE(xIn,T):
    xGa=1-xIn; d=xGa-xIn; L0,L1,L2=L(T)
    return xGa*xIn*(L0+L1*d+L2*d*d)
def dGE_dxIn(xIn,T,h=1e-6):
    return (GE(xIn+h,T)-GE(xIn-h,T))/(2*h)
def gbar_Ga(xIn,T):  # partial molar excess of Ga (A)
    return GE(xIn,T)-xIn*dGE_dxIn(xIn,T)
def gbar_In(xIn,T):  # partial molar excess of In (B)
    return GE(xIn,T)+(1-xIn)*dGE_dxIn(xIn,T)
# pure-element fusion (SGTE/Dinsdale standard): Tm (K), dHfus (J/mol)
TmGa,HGa=302.91,5590.0
TmIn,HIn=429.75,3283.0
def dGfus_Ga(T): return HGa*(1-T/TmGa)
def dGfus_In(T): return HIn*(1-T/TmIn)
# liquidus branches: solid assumed pure (terminal). Ga branch (pure Ga solid):
def fGa(xIn,T): return R*T*np.log(1-xIn)+gbar_Ga(xIn,T)+dGfus_Ga(T)
def fIn(xIn,T): return R*T*np.log(xIn)+gbar_In(xIn,T)+dGfus_In(T)
def xGa_branch(T):
    try: return brentq(lambda x: fGa(x,T),1e-6,0.6)
    except Exception: return np.nan
def xIn_branch(T):
    try: return brentq(lambda x: fIn(x,T),0.05,1-1e-6)
    except Exception: return np.nan
# eutectic: T where the two branch compositions coincide
def diff(T): return xGa_branch(T)-xIn_branch(T)
Ts=np.arange(430,260,-0.25); prev=None; eutT=None
for T in Ts:
    d=diff(T)
    if prev is not None and np.isfinite(d) and np.isfinite(prev[1]) and d*prev[1]<0:
        eutT=brentq(diff,T,prev[0]); break
    prev=(T,d)
xe=xGa_branch(eutT)
print(f"COMPUTED Ga-In eutectic: T={eutT:.1f} K ({eutT-273.15:.1f} C), x_In={xe:.3f} ({xe*100:.1f} mol%)")
print(f"RUGG & CHART optimised  : T=289.0 K (15.9 C), x_In=0.142 (14.2 mol%)")
# save liquidus for plotting
xg=np.linspace(0.0001,0.30,500); Tg=[]
for x in xg:
    try: Tg.append(brentq(lambda T: fGa(x,T),260,303)); 
    except Exception: Tg.append(np.nan)
xi=np.linspace(0.10,0.9999,600); Ti=[]
for x in xi:
    try: Ti.append(brentq(lambda T: fIn(x,T),260,430))
    except Exception: Ti.append(np.nan)
np.savez("gain_liquidus.npz", xg=xg,Tg=Tg,xi=xi,Ti=Ti,eutT=eutT,xe=xe)
print("saved")
