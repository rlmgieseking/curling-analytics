# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 14:46:40 2023

@author: gieseking
"""

import utils.webscraper as scraper
import utils.api as api
import sqlite3

# Connect to SQL database
filename = 'utils/matches.db'
conn = sqlite3.connect(filename)
conn.close()
conn = sqlite3.connect(filename)
c = conn.cursor()

matches = c.execute('''SELECT EID, Team1, Team2 FROM matches 
            WHERE (Team1 = "United States" OR Team2 = "United States"
                OR Team1 = "Manitoba" OR Team2 = "Manitoba"
                OR Team1 = "Italy" OR Team2 = "Italy"
                OR Team1 = "Nunavut" OR Team2 = "Nunavut"
                OR Team1 = "Russia" OR Team2 = "Russia"
                OR Team1 = "England" OR Team2 = "England"
                OR Team1 = "Latvia" OR Team2 = "Latvia"
                OR Team1 = "Korea" OR Team2 = "Korea"
                OR Team1 = "Australia" OR Team2 = "Australia"
                OR Team1 = "New Zealand" OR Team2 = "New Zealand")'''
            ).fetchall()
print(matches)
print(len(matches))

"""
for event in range(1000,8100):
    matches = c.execute('''SELECT Team1, Team2 FROM matches 
                WHERE EID = '''+str(event) + '''
                AND (Team1 = "United States" OR Team2 = "United States"
                    OR Team1 = "Manitoba" OR Team2 = "Manitoba"
                    OR Team1 = "Italy" OR Team2 = "Italy"
                    OR Team1 = "Nunavut" OR Team2 = "Nunavut"
                    OR Team1 = "Russia" OR Team2 = "Russia"
                    OR Team1 = "England" OR Team2 = "England"
                    OR Team1 = "Latvia" OR Team2 = "Latvia"
                    OR Team1 = "Korea" OR Team2 = "Korea"
                    OR Team1 = "Australia" OR Team2 = "Australia"
                    OR Team1 = "New Zealand" OR Team2 = "New Zealand")'''
                ).fetchall()
    #print(matches)
    if len(matches) > 0:
        teams = scraper.get_fixed_teams(event)
        print(event)
        for key in teams.keys():
            #print(key, teams[key])
            c.execute('''UPDATE matches
                SET Team1 = "''' + teams[key] + '''" 
                WHERE EID = '''+str(event) + '''
                    AND Team1 = "''' + key + '"')
            c.execute('''UPDATE matches
                SET Team2 = "''' + teams[key] + '''" 
                WHERE EID = '''+str(event) + '''
                    AND Team2 = "''' + key + '"')
        #print(c.execute('SELECT EID, Team1, Team2 FROM matches WHERE EID = '+str(event)).fetchall())
        conn.commit()
"""
conn.close()