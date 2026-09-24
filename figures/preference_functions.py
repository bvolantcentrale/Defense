"""Courbes reprises des cinq TikZ de article LCA MCDM/tables/pref functions.
Vshape.tex : cas q=0. L'état avec indifférence utilise q et p de pref_functions.tex.
Les définitions suivent les courbes TikZ (gaussienne bornée entre 0 et 1).
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).with_name("preferences")
OUT.mkdir(exist_ok=True)
plt.rcParams["svg.fonttype"] = "none"

def curve(name):
    fig, ax = plt.subplots(figsize=(3.0, 1.25), layout="constrained")
    ax.set(xlim=(-.2, 2), ylim=(-.08, 1.14))
    ax.set_yticks([0, 1])
    ax.set_xticks([0])
    ax.set_xlabel("d", loc="right", labelpad=-15)
    ax.text(0, 1.03, "P(d)", transform=ax.transAxes, fontsize=10, ha="left", va="bottom")
    def line(x,y): ax.plot(x,y,color="#222222",linewidth=2)
    def jump(x,y0,y1):
        ax.plot([x,x],[y0,y1],color="#777777",linestyle=":")
        ax.plot(x,y0,"o",color="#222222",markersize=4)
        ax.plot(x,y1,"o",markeredgecolor="#222222",markerfacecolor="white",markersize=4)
    if name=="Usual":
        line([-.2,0],[0,0]); line([0,2],[1,1]); jump(0,0,1)
    elif name=="Ushape":
        line([-.2,1],[0,0]); line([1,2],[1,1]); jump(1,0,1)
        ax.set_xticks([0,1],["0","q"])
    elif name=="Level":
        line([-.2,.7],[0,0]); line([.7,1.4],[.5,.5]); line([1.4,2],[1,1])
        jump(.7,0,.5); jump(1.4,.5,1); ax.set_xticks([0,.7,1.4],["0","q","p"])
        ax.set_yticks([0,.5,1],["0","½","1"])
    elif name=="Gaussian":
        x=np.linspace(0,2,150); line([-.2,0],[0,0]); line(x,1-np.exp(-x*x/(2*.7**2)))
        ax.set_xticks([0,.7],["0","s"])
    else:
        q=0 if name=="Vshape" else .7
        p=1 if name=="Vshape" else 1.4
        line([-.2,q,p,2],[0,0,1,1]); ax.set_xticks([0,p],["0","p"])
        if q: ax.set_xticks([0,q,p],["0","q","p"])
    ax.spines[["top","right"]].set_visible(False)
    ax.tick_params(labelsize=10,length=2)
    ax.grid(axis="y",linestyle=":",alpha=.25)
    fig.savefig(OUT/(name+".svg"),transparent=True)
    plt.close(fig)

if __name__=="__main__":
    for name in ["Usual","Ushape","Level","Gaussian","Vshape","Vshape_indifference"]:
        curve(name)
