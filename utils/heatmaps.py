import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from utils import mpl_stylesheet
from utils.annotate_heatmap import annotate_heatmap

mpl_stylesheet.banskt_presentation(fontfamily = 'latex', fontsize = 20)
matplotlib.rcParams['xtick.major.size'] = 0
matplotlib.rcParams['ytick.major.size'] = 0

def rotation(teams, startgw, endgw, eplfix, annotate = True):

    prob = np.zeros((len(teams), endgw - startgw + 1))
    opps = np.zeros((len(teams), endgw - startgw + 1)).astype(str)
    for i, t in enumerate(teams):
        prob[i, :] = [eplfix[gw - 1][t].prob  for gw in range(startgw, endgw + 1)]
        if annotate:
            opps[i, :] = [eplfix[gw - 1][t].gegen for gw in range(startgw, endgw + 1)]
            locs = [eplfix[gw - 1][t].athome for gw in range(startgw, endgw + 1)]
            for k in range(endgw - startgw + 1):
                if not locs[k]: opps[i, k] = opps[i, k].lower()

    height = 2 + len(teams) * 0.5
    
    fig = plt.figure(figsize = (16, height))
    ax1 = fig.add_subplot(111)
    
    im1 = ax1.imshow(prob, cmap=plt.get_cmap("RdYlGn", 50), interpolation='None', vmin = 0.0, vmax = 1.0)
    
    myticks = [x for x in range(len(teams))]
    mxticks = [x for x in range(endgw - startgw + 1)]
    gameweeks = ['GW{:d}'.format(x) for x in range(startgw, endgw + 1)]
    ax1.set_xticks(mxticks)
    ax1.set_xticklabels(gameweeks, rotation='90')
    ax1.set_yticks(myticks)
    ax1.set_yticklabels(teams)
    
    if annotate:
        texts = annotate_heatmap(im1, opps, data = prob, threshold = 0.35)

    plt.tight_layout()
    plt.show()
    return

def score(teams, home, away):

    fig, axarr = plt.subplots(1,2, figsize = (12, 6))

    ax1 = axarr[0]
    ax2 = axarr[1]
    ax_cbar = fig.add_axes([1.1, 0.15, .02, 0.7])

    vmin = min(np.min(home), np.min(away))
    vmax = max(np.max(home), np.max(away))
    im1 = ax1.imshow(home, cmap=plt.get_cmap("RdYlGn", 50), interpolation='None', vmin = vmin, vmax = vmax)
    im2 = ax2.imshow(away, cmap=plt.get_cmap("RdYlGn", 50), interpolation='None', vmin = vmin, vmax = vmax)

    mticks = [x for x in range(len(teams))]
    ax1.set_xticks(mticks)
    ax1.set_xticklabels(teams, rotation='90')
    ax1.set_yticks(mticks)
    ax1.set_yticklabels(teams)

    ax2.yaxis.tick_right()
    ax2.set_xticks(mticks)
    ax2.set_xticklabels([t.lower() for t in teams], rotation='90')
    ax2.set_yticks(mticks)
    ax2.set_yticklabels(teams)

    plt.colorbar(im1, cax=ax_cbar)

    plt.subplots_adjust(wspace=0, hspace=0, left=0, right=1, bottom=0, top=1)
    #plt.tight_layout()
    plt.show()
    return
