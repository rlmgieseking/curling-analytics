# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 08:35:21 2023

@author: gieseking
"""

import utils.webscraper as scraper
import utils.queries as queries
import utils.graphs as graphs
import utils.htmlgen as htmlgen
import sqlite3

filename = 'utils/matches.db'
conn = sqlite3.connect(filename)
conn.close()
conn = sqlite3.connect(filename)
c = conn.cursor()
'''
# Clean the data
text = queries.clean_data()
text.extend(queries.add_hammer())
text.extend(queries.add_season())
text.extend(queries.add_ends())
text.extend(queries.add_category_rank())
print('Cleaning up database')
for t in text:
    c.execute(t)
'''

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

combos = [[None, None, None, None, 'All matches'],
          ['Men', 8,  (  1,500), (  1,500), 'Men, 8 ends, all ranks'],
          ['Men', 8,  (  1, 25), (101,500), 
           'Men, 8 ends, rank 1-25 vs. 101-500'],
          ['Men', 10, (  1,500), (  1,500), 'Men, 10 ends, all ranks']]

out = open('test.html','w', encoding="utf-8")
out.write("<html>")
out.write(htmlgen.head())
out.write("<body>\n")
out.write(htmlgen.header())
out.write(htmlgen.curling_basics())
out.write(htmlgen.database())
#out.write(graphs.matches_month(c, season, combos, True))
#out.write(graphs.final_scores(c, season, combos, False))
#out.write(graphs.end_scores(c, season, combos, False))
out.write("</body></html>\n")
out.close()



'''
graphs.plot_end_scores(c, season=list(range(2011,2025)), category='Men', ends=8,
                                 rank1=(1,25), rank2=(100,500), plot_end=list(range(1,10)))
'''
'''    
graph = graphs.plot_final_scores(c, season=list(range(2011,2025)), category='Men', ends=8,
                                 rank1=(1,25), rank2=(1,25))
graph = graphs.plot_final_scores(c, season=list(range(2011,2025)), category='Women', ends=8,
                                 rank1=(1,25), rank2=(1,25))
'''
'''
count = queries.count_final_scores(category='Men', ends=8, 
                                    rank1 = None, rank2 = None, 
                                    season=list(range(2015, 2021)))

for q in count:
    print(q)
    months = c.execute(q).fetchall()
    print(months)
'''
"""
print(c.execute('''SELECT EID, COUNT(*) FROM events
                GROUP BY EID
                ORDER BY COUNT(*)''').fetchall())

print(c.execute('''SELECT events.EID, COUNT(*) FROM matches
                INNER JOIN events ON matches.EID = events.EID
                WHERE Date BETWEEN "2012-11-00" AND "2012-11-31"
                GROUP BY events.EID
                ORDER BY COUNT(*)''').fetchall())
"""
conn.close()