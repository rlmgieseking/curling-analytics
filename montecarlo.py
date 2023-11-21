# -*- coding: utf-8 -*-
"""
Created on Mon May  1 08:56:50 2023

@author: gieseking
"""

import numpy as np

def end(scores, t0prob, t1prob, hammer, score=[0,0]):
    if hammer == 0:
        endscore = np.random.choice(scores, p=t0prob)
    else: 
        endscore = np.random.choice(scores, p=t1prob)
    if endscore > 0:
        score[hammer] += endscore
        hammer = 1 - hammer
    else:
        score[1-hammer] -= endscore
    #print('Team ',hammer,' scores ',endscore, 'result', score, hammer)
    return score, hammer, endscore

def game(scores, t0prob, t1prob, ends, hammer=None, score=[0,0]):
    # Assign hammer randomly to team 0 or 1, if not assigned
    if hammer == None:
        hammer = np.random.randint(0,2)
    # Simulate regular ends
    for i in range(ends):
        score, hammer, endscore = end(scores, t0prob, t1prob, hammer, score)
    # Simulate extra ends
    while score[0] == score[1]:
        score, hammer, endscore = end(scores, t0prob, t1prob, hammer, score)
    winner = 0 if score[0] > score[1] else 1
    return score, winner
    
                


scores = [-8, -7, -6, -5, -4, -3,   -2,   -1,    0,    1,    2,    3,    4,     5,  6,  7,  8]
t0prob = [ 0,  0,  0,  0,  0,  0, 0.02, 0.12, 0.25, 0.20, 0.25, 0.10, 0.05,  0.01,  0,  0,  0]
t1prob = [ 0,  0,  0,  0,  0,  0, 0.02, 0.12, 0.00, 0.45, 0.25, 0.10, 0.05,  0.01,  0,  0,  0]
#t1prob = [0.5,0,0.5,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

wcount = [0,0]
scount = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

for i in range(10000):
    #score, hammer, endscore = end(scores, t0prob, t1prob, 1)
    #scount[scores.index(endscore)] += 1
    score, winner = game(scores, t0prob, t1prob, 8, score=[0,0])
    #print(score, winner)
    wcount[winner] += 1 
print(wcount)
