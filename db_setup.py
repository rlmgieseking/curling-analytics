# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 15:08:15 2023

@author: gieseking
"""

import sqlite3
import pandas as pd

# Connect to a SQL database
filename = 'curlingmatches.db'
conn = sqlite3.connect(filename)

# Convert data from csv into sql database
'''
scores = pd.read_csv('scores_0-4000.csv')
print(scores.head())
scores.to_sql('matches', conn, if_exists='replace', index=False)
print('scores_0-4000.csv done')

scorefiles = ['scores_4000-5000.csv',
              'scores_5000-6000.csv',
              'scores_6000-7000.csv',
              'scores_7000-8000.csv',
              'scores_8000-9000.csv']
for f in scorefiles:
    scores = pd.read_csv(f)
    print(scores.head())
    scores.to_sql('matches', conn, if_exists='append', index=False)
    print(f + ' done')
'''

# Add event table to database

events = pd.read_csv('events.csv', encoding_errors='replace')
events.to_sql('events', conn, index=False, if_exists='replace')
print('events done')


# Add teams to database
'''
mteams = pd.read_csv('mens_teams.csv')
mteams.to_sql('teams', conn, if_exists='replace', index=False)
print('men done')
wteams = pd.read_csv('womens_teams.csv')
wteams.to_sql('teams', conn, if_exists='append', index=False)
print('women done')
'''
