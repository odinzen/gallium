# -*- coding: utf-8 -*-
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":13,"axes.linewidth":1.1,
  "axes.edgecolor":"black","axes.facecolor":"white","figure.facecolor":"white","axes.grid":False})

ph=np.load("pbsn_grid_phase.npy", allow_pickle=True)   # (nT,nX,vertex)
Tmin,Tmax,nT,Xmin,Xmax,nX=np.load("pbsn_grid_axes.npy")
nT=int(nT); nX=int(nX)
Ts=np.linspace(Tmin,Tmax,nT); Xs=np.linspace(Xmin,Xmax,nX)
liq=np.load("pbsn_liquidus.npy")  # [Xs; liqT]
def pset(cell): return frozenset(p for p in cell if p)

# boundary points: where stable phase-set changes along X (for each T) and along T (for each X)
bx,by=[],[]
for i in range(nT):
    for j in range(nX-1):
        if pset(ph[i,j])!=pset(ph[i,j+1]):
            bx.append((Xs[j]+Xs[j+1])/2); by.append(Ts[i]-273.15)
for j in range(nX):
    for i in range(nT-1):
        if pset(ph[i,j])!=pset(ph[i+1,j]):
            bx.append(Xs[j]); by.append((Ts[i]+Ts[i+1])/2-273.15)
bx=np.array(bx); by=np.array(by)

fig,ax=plt.subplots(figsize=(7.0,5.0))
fig.subplots_adjust(left=0.12,right=0.90,top=0.85,bottom=0.16)
ax.scatter(bx,by,s=1,c="black",marker="o",linewidths=0,zorder=3)

# eutectic
eutX=0.740; eutT=181.9
ax.plot([eutX],[eutT],marker="o",ms=7,mfc="white",mec="black",mew=1.4,zorder=5)
# eutectic horizontal tie line at eutectic T between solid solubility limits (approx visual)
ax.hlines(eutT, 0.02, 0.99, color="black", lw=0.9, linestyles=(0,(5,3)), zorder=2)
# region labels
def rl(x,y,t,b=True): ax.text(x,y,t,ha="center",va="center",fontsize=9,fontweight=("bold" if b else "normal"),
                              bbox=dict(facecolor="white",edgecolor="none",pad=0.5))
rl(0.5,300,"L")
rl(0.12,170,"(Pb)\nfcc",b=True)
rl(0.93,180,"(Sn)\nbct",b=True)
rl(0.34,150,"L + (Pb)",False)
rl(0.88,215,"L + (Sn)",False)
rl(0.55,120,"(Pb) + (Sn)",False)

ax.set_xlim(0,1); ax.set_ylim(100,330)
ax.set_xlabel("Composition, mole fraction Sn")
ax.set_ylabel("Temperature, °C")
for s in ax.spines.values(): s.set_linewidth(1.1); s.set_color("black")
# top axis: weight percent Sn
def mole2wt(x): 
    MSn,MPb=118.71,207.2; return x*MSn/(x*MSn+(1-x)*MPb)*100
secx=ax.secondary_xaxis('top', functions=(mole2wt, lambda w:(w/118.71)/((w/118.71)+(100-w)/207.2)))
secx.set_xlabel("Composition, weight percent Sn", fontsize=8)
secx.tick_params(labelsize=7)

import os
_here = os.path.dirname(os.path.abspath(__file__))
_fig  = os.path.join(_here, "..", "..", "figures")
fig.savefig(os.path.join(_here, "Fig_C1_PbSn_computed.png"), dpi=600)
fig.savefig(os.path.join(_fig,  "Fig1.png"), dpi=600)
print("figure written")
