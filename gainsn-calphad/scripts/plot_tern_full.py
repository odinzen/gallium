# -*- coding: utf-8 -*-
import numpy as np, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.tri as mtri
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":13,"axes.linewidth":1.3,
 "axes.edgecolor":"black","figure.facecolor":"white","axes.facecolor":"white"})
P=np.load("tern_full_grid.npy"); m=np.isfinite(P[:,3])
xGa,xIn,xSn,T=P[m,0],P[m,1],P[m,2],P[m,3]; TC=T-273.15
Ga=np.array([0.5,np.sqrt(3)/2]); In=np.array([0,0]); Sn=np.array([1,0])
X=xGa*Ga[0]+xIn*In[0]+xSn*Sn[0]; Y=xGa*Ga[1]+xIn*In[1]+xSn*Sn[1]
tri=mtri.Triangulation(X,Y)
fig,ax=plt.subplots(figsize=(7.2,6.7)); fig.subplots_adjust(left=0.04,right=0.97,top=0.83,bottom=0.17)
ax.set_aspect('equal'); ax.axis('off')
lv=[20,40,60,80,100,120,160,200,240,280,320,360,400]
cs=ax.tricontour(tri,TC,levels=lv,colors='black',linewidths=1.2)
ax.clabel(cs,fmt="%d°C",fontsize=8.5,inline=True)
# shade coolest region lightly
ax.tricontourf(tri,TC,levels=[0,20,40],colors=['0.80','0.90'],alpha=0.6)
tr=np.array([Ga,In,Sn,Ga]); ax.plot(tr[:,0],tr[:,1],'k-',lw=1.3)
ax.text(Ga[0],Ga[1]+0.03,"Ga",ha='center',va='bottom',fontsize=12,fontweight='bold')
ax.text(In[0]-0.02,In[1]-0.03,"In",ha='right',va='top',fontsize=12,fontweight='bold')
ax.text(In[0]-0.02,In[1]-0.075,"indium",ha='right',va='top',fontsize=7.5)
ax.text(Sn[0]+0.02,Sn[1]-0.03,"Sn",ha='left',va='top',fontsize=12,fontweight='bold')
ax.text(Sn[0]+0.02,Sn[1]-0.075,"tin",ha='left',va='top',fontsize=7.5)
ax.text(Ga[0]+0.075,Ga[1]+0.0,"gallium",ha='left',va='center',fontsize=7.5)
def tp(g,i,s): return g*Ga+i*In+s*Sn
eu=tp(0.84,0.12,0.04); ax.plot(eu[0],eu[1],'o',ms=8,mfc='white',mec='black',mew=1.5,zorder=7)
gp=tp(0.685,0.215,0.10); ax.plot(gp[0],gp[1],'^',ms=9,mfc='0.2',mec='black',mew=1.0,zorder=7)
fig.text(0.5,0.918,"with In–Sn intermediate phases β and γ (David et al. 2004)",ha='center',va='top',fontsize=8,style='italic',color='0.3')
fig.savefig("Fig_C4_GaInSn_full.png",dpi=600)
fig.savefig("../figures/Fig4.png",dpi=600); print("written")
