import numpy as np
from scipy.optimize import curve_fit
# Zivkovic 2003, Tables 1 & 3: x_Ga and integral molar enthalpy of mixing (J/mol)
xGa=np.array([1.0,0.95,0.9258,0.80,0.60,0.30,0.0])
HM =np.array([0.0,95.0,306.0,673.0,907.0,723.0,0.0])
xSn=1-xGa
def rk(xSn,h0,h1,h2):
    xGa=1-xSn; d=xGa-xSn
    return xGa*xSn*(h0+h1*d+h2*d*d)
p,_=curve_fit(rk,xSn,HM,p0=[3600,0,0])
h0,h1,h2=p
pred=rk(xSn,*p)
ss=np.sum((HM-pred)**2); rms=np.sqrt(ss/len(HM))
print(f"Ga-Sn liquid RK (enthalpy = GE approx): L0={h0:.0f}, L1={h1:.0f}, L2={h2:.0f} J/mol")
print(f"fit RMS = {rms:.1f} J/mol; peak data 907 J/mol at xSn=0.40")
for x,h,pr in zip(xSn,HM,pred): print(f"  xSn={x:.3f}  data={h:5.0f}  fit={pr:6.0f}")
np.save("gasn_rk.npy", np.array([h0,h1,h2]))
