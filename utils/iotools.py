import numpy as np
import collections
import csv

from utils.containers import FixtureInfo

def get_fixtures(filename, scores):
    fixtures = [{} for x in range(38)]
    with open(filename) as csvfile:
        instream = csv.reader(csvfile, delimiter = ',')
        for row in instream:
            team = row[0].strip()
            teamscores = scores[team]
            for gw in range(1, 39):
                opp = row[gw].split()[0].strip()
                loc = row[gw].split()[1].strip()[1]
                athome = False
                if loc == 'H':
                    athome = True
                score = teamscores[opp][loc]
                fixtures[gw - 1][team] = FixtureInfo(gegen = opp, athome = athome, prob = score)
    return fixtures

def convert_scores_mat(sdict, teams, nanval = 0.5):
    n = len(teams)
    home = np.zeros((n, n))
    away = np.zeros((n, n))
    for i, t1 in enumerate(teams):
        for j, t2 in enumerate(teams):
            home[i, j] = sdict[t1][t2]['H']
            away[i, j] = sdict[t1][t2]['A']

    vmin = min(np.min(home), np.min(away))
    vmax = max(np.max(home), np.max(away))
    delta = vmax - vmin
    home = (home - vmin) / delta
    away = (away - vmin) / delta

    home[np.diag_indices_from(home)] = nanval
    away[np.diag_indices_from(away)] = nanval
    return home, away

def get_scores(filename, nanval = 0.5):
    scores = {}
    points = {}
    teams = list()
    ATTACKH = 0
    ATTACKA = 1
    DEFENDH = 2
    DEFENDA = 3
    with open(filename) as csvfile:
        instream = csv.reader(csvfile, delimiter = ',')
        next(instream, None)
        for row in instream:
            team = row[0].strip()
            teams.append(team)
            points[team] = [float(x.strip()) for x in row[1:]]
    for team in teams:
        scores[team] = {}
        for opp in teams:
            scores[team][opp] = {}
            if opp == team:
                scores[team][opp]['H'] = 0
                scores[team][opp]['A'] = 0
            else:
                scores[team][opp]['H'] = points[team][DEFENDH] - points[opp][ATTACKA]
                scores[team][opp]['A'] = points[team][DEFENDA] - points[opp][ATTACKH]
                
    home, away = convert_scores_mat(scores, teams, nanval = nanval)
    for i, team in enumerate(teams):
        for j, opp in enumerate(teams):
            scores[team][opp]['H'] = home[i, j]
            scores[team][opp]['A'] = away[i, j]

    return teams, scores
