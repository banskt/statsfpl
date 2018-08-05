import numpy as np
import itertools

from utils.containers import RotationCombinations

def rotate(teams, fixtures, startgw, endgw, nteams, ntarget, csprob = 0.7):
    combinations = itertools.combinations(teams, nteams)
    rotations = list()
    for i, combination in enumerate(combinations):
        score = 0
        benchscore = 0
        cleansheets = 0
        for gw in range(startgw, endgw + 1):
            opps = [fixtures[gw - 1][t].gegen for t in combination]
            prob = [fixtures[gw - 1][t].prob  for t in combination]
            probarr = np.array(prob)
            idx = (-probarr).argsort()[:ntarget]
            benchidx = (-probarr).argsort()[ntarget:]
            score += np.sum(probarr[idx])
            benchscore += np.sum(probarr[benchidx])
            cleansheets += np.sum(probarr[idx] > csprob)
        rotations.append(RotationCombinations(teams = combination,
                                              score = score,
                                              benchscore = benchscore,
                                              cleanies = cleansheets))
    return rotations

def predict_cleansheets(teams, home, away, cutoff = 0.7):
    csh = home > cutoff
    csa = away > cutoff
    cs = np.sum(csh, axis = 1) + np.sum(csa, axis = 1)
    row_format ="{:>4} " * (len(teams) + 1)
    print (row_format.format("Teams ", *teams))
    print (row_format.format("# CS  ", *cs))
    return
