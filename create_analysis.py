# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 08:35:21 2023

@author: gieseking
"""

import utils.queries as queries
import utils.htmlgen as htmlgen
import sqlite3

database = 'utils/matches.db'
html_file = 'analytics.html'

# Connect to database
conn = sqlite3.connect(database)
conn.close()
conn = sqlite3.connect(database)
c = conn.cursor()

# Clean the data
text = queries.clean_data()
text.extend(queries.add_hammer())
text.extend(queries.add_season())
text.extend(queries.add_ends())
text.extend(queries.add_category_rank())
print('Cleaning up database')
for t in text:
    c.execute(t)


# Range of seasons to use for statistics
season = [2011,2024]

# Combinations of category, ends, rank1, and rank2 to use, along with menu item for each
combos = [[None, None, None, None, 'All matches'],
          ['Men', 8,  (  1,500), (  1,500), 
           'Men, 8 ends, all ranks'],
          ['Men', 8,  (  1, 25), (  1, 25), 
           'Men, 8 ends, rank 1-25 vs. 1-25'],
          ['Men', 8,  (  1, 25), ( 26,100), 
           'Men, 8 ends, rank 1-25 vs. 26-100'],
          ['Men', 8,  (  1, 25), (101,500), 
           'Men, 8 ends, rank 1-25 vs. 101-500'],
          ['Men', 8,  ( 26,100), ( 26,100), 
           'Men, 8 ends, rank 26-100 vs. 26-100'],
          ['Men', 8,  ( 26,100), (101,500), 
           'Men, 8 ends, rank 26-100 vs. 101-500'],
          ['Men', 8,  (101,500), (101,500), 
           'Men, 8 ends, rank 101-500 vs. 101-500'],
          ['Men', 10, (  1,500), (  1,500), 
           'Men, 10 ends, all ranks'],
          ['Men', 10, (  1, 25), (  1, 25), 
           'Men, 10 ends, rank 1-25 vs. 1-25'],
          ['Men', 10, (  1, 25), ( 26,100), 
           'Men, 10 ends, rank 1-25 vs. 26-100'],
          ['Men', 10, (  1, 25), (101,500), 
           'Men, 10 ends, rank 1-25 vs. 101-500'],
          ['Men', 10, ( 26,100), ( 26,100), 
           'Men, 10 ends, rank 26-100 vs. 26-100'],
          ['Men', 10, ( 26,100), (101,500), 
           'Men, 10 ends, rank 26-100 vs. 101-500'],
          ['Men', 10, (101,500), (101,500), 
           'Men, 10 ends, rank 101-500 vs. 101-500'],
          ['Women', 8,  (  1,500), (  1,500), 
           'Women, 8 ends, all ranks'],
          ['Women', 8,  (  1, 25), (  1, 25), 
           'Women, 8 ends, rank 1-25 vs. 1-25'],
          ['Women', 8,  (  1, 25), ( 26,100), 
           'Women, 8 ends, rank 1-25 vs. 26-100'],
          ['Women', 8,  (  1, 25), (101,500), 
           'Women, 8 ends, rank 1-25 vs. 101-500'],
          ['Women', 8,  ( 26,100), ( 26,100), 
           'Women, 8 ends, rank 26-100 vs. 26-100'],
          ['Women', 8,  ( 26,100), (101,500), 
           'Women, 8 ends, rank 26-100 vs. 101-500'],
          ['Women', 8,  (101,500), (101,500), 
           'Women, 8 ends, rank 101-500 vs. 101-500'],
          ['Women', 10, (  1,500), (  1,500), 
           'Women, 10 ends, all ranks'],
          ['Women', 10, (  1, 25), (  1, 25), 
           'Women, 10 ends, rank 1-25 vs. 1-25'],
          ['Women', 10, (  1, 25), ( 26,100), 
           'Women, 10 ends, rank 1-25 vs. 26-100'],
          ['Women', 10, (  1, 25), (101,500), 
           'Women, 10 ends, rank 1-25 vs. 101-500'],
          ['Women', 10, ( 26,100), ( 26,100), 
           'Women, 10 ends, rank 26-100 vs. 26-100'],
          ['Women', 10, ( 26,100), (101,500), 
           'Women, 10 ends, rank 26-100 vs. 101-500'],
          ['Women', 10, (101,500), (101,500), 
           'Women, 10 ends, rank 101-500 vs. 101-500']]

out = open(html_file,'w', encoding="utf-8")
out.write("<html>")
out.write(htmlgen.head())
out.write("<body>\n")
out.write(htmlgen.header())
out.write(htmlgen.curling_basics())
out.write(htmlgen.database())
out.write(htmlgen.matches_month(c, season, combos, True))
out.write(htmlgen.final_scores(c, season, combos, False))
out.write(htmlgen.end_scores(c, season, combos, False))
out.write("</body></html>\n")
out.close()

conn.close()