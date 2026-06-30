# -*- coding: utf-8 -*-
import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":13,"axes.linewidth":1.1,
 "axes.edgecolor":"black","axes.facecolor":"white","figure.facecolor":"white","axes.grid":False})
d=np.load("gain_liquidus.npz")
xg,Tg,xi,Ti=d["xg"],d["Tg"],d["xi"],d["Ti"]; eutT=float(d["eutT"]); xe=float(d["xe"])
TmGa,TmIn=302.91,429.75
C=lambda K:K-273.15
fig,ax=plt.subplots(figsize=(7.0,5.0)); fig.subplots_adjust(left=0.12,right=0.96,top=0.85,bottom=0.20)
# liquidus branches (black solid)
ax.plot(xg,[C(t) for t in Tg],color="black",lw=1.6,zorder=4)
m=np.isfinite(Ti); ax.plot(xi[m],[C(t) for t in np.array(Ti)[m]],color="black",lw=1.6,zorder=4)
# eutectic isotherm (dashed) across solubility gap
ax.hlines(C(eutT),0.0,1.0,color="black",lw=0.9,linestyles=(0,(5,3)),zorder=2)
ax.plot([xe],[C(eutT)],marker="o",ms=7,mfc="white",mec="black",mew=1.4,zorder=6)
# melting points
ax.plot([0],[C(TmGa)],marker="_",ms=10,color="black"); ax.plot([1],[C(TmIn)],marker="_",ms=10,color="black")
ax.annotate("Ga m.p.\n29.8 °C",xy=(0,C(TmGa)),xytext=(0.05,55),fontsize=7,ha="left",
            arrowprops=dict(arrowstyle="->",lw=0.8),bbox=dict(fc="white",ec="none",pad=0.5))
ax.annotate("In m.p.\n156.6 °C",xy=(1,C(TmIn)),xytext=(0.72,135),fontsize=7,ha="left",
            arrowprops=dict(arrowstyle="->",lw=0.8),bbox=dict(fc="white",ec="none",pad=0.5))
def rl(x,y,t,b=True): ax.text(x,y,t,ha="center",va="center",fontsize=9.5,
    fontweight=("bold" if b else "normal"),bbox=dict(fc="white",ec="none",pad=0.5))
rl(0.45,110,"L")
rl(0.045,0,"(Ga)",True); rl(0.96,40,"(In)",True)
rl(0.10,8,"L + (Ga)",False); rl(0.62,70,"L + (In)",False)
rl(0.5,-15,"(Ga) + (In)",False)
ax.set_xlim(0,1); ax.set_ylim(-30,170)
ax.set_xlabel("Composition, mole fraction In", labelpad=4)
ax.set_ylabel("Temperature, °C")
for s in ax.spines.values(): s.set_linewidth(1.1); s.set_color("black")
fig.savefig("Fig_C2_GaIn_computed.png",dpi=600)
fig.savefig("../figures/Fig2.png",dpi=600); print("written")
