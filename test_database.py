# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 15:37:30 2023

@author: gieseking
"""

import sqlite3

# Set up choices for later
filename = 'utils/matches.db'

# Connect to SQL database
conn = sqlite3.connect(filename)
conn.close()
conn = sqlite3.connect(filename)
c = conn.cursor()

print(c.execute('SELECT COUNT(*) FROM matches;').fetchall())

conn.close()