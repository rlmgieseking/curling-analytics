# Utilities to set up SQLite queries for curling database

get_hammer_scores = ''' CASE WHEN CAST(CAST(End1 AS INTEGER) AS TEXT) <> End1 
           OR CAST(CAST(Ham1 AS INTEGER) AS TEXT) <> Ham1 THEN NULL
         ELSE CAST(End1*Ham1 AS INTEGER) END AS S1,
    CASE WHEN CAST(CAST(End2 AS INTEGER) AS TEXT) <> End2 
           OR CAST(CAST(Ham2 AS INTEGER) AS TEXT) <> Ham2 THEN NULL
         ELSE End2*Ham2 END AS S2,
    CASE WHEN CAST(CAST(End3 AS INTEGER) AS TEXT) <> End3 
           OR CAST(CAST(Ham3 AS INTEGER) AS TEXT) <> Ham3 THEN NULL
         ELSE End3*Ham3 END AS S3,
    CASE WHEN CAST(CAST(End4 AS INTEGER) AS TEXT) <> End4 
           OR CAST(CAST(Ham4 AS INTEGER) AS TEXT) <> Ham4 THEN NULL
         ELSE End4*Ham4 END AS S4,
    CASE WHEN CAST(CAST(End5 AS INTEGER) AS TEXT) <> End5 
           OR CAST(CAST(Ham5 AS INTEGER) AS TEXT) <> Ham5 THEN NULL
         ELSE End5*Ham5 END AS S5,
    CASE WHEN CAST(CAST(End6 AS INTEGER) AS TEXT) <> End6 
           OR CAST(CAST(Ham6 AS INTEGER) AS TEXT) <> Ham6 THEN NULL
         ELSE End6*Ham6 END AS S6,
    CASE WHEN CAST(CAST(End7 AS INTEGER) AS TEXT) <> End7 
           OR CAST(CAST(Ham7 AS INTEGER) AS TEXT) <> Ham7 THEN NULL
         ELSE End7*Ham7 END AS S7,
    CASE WHEN CAST(CAST(End8 AS INTEGER) AS TEXT) <> End8 
           OR CAST(CAST(Ham8 AS INTEGER) AS TEXT) <> Ham8 THEN NULL
         ELSE End8*Ham8 END AS S8,
    CASE WHEN CAST(CAST(End9 AS INTEGER) AS TEXT) <> End9 
           OR CAST(CAST(Ham9 AS INTEGER) AS TEXT) <> Ham9 THEN NULL
         ELSE End9*Ham9 END AS S9,
    CASE WHEN CAST(CAST(End10 AS INTEGER) AS TEXT) <> End10 
           OR CAST(CAST(Ham10 AS INTEGER) AS TEXT) <> Ham10 THEN NULL
         ELSE End10*Ham10 END AS S10,
    CASE WHEN CAST(CAST(End11 AS INTEGER) AS TEXT) <> End11 
           OR CAST(CAST(Ham11 AS INTEGER) AS TEXT) <> Ham11 THEN NULL
         ELSE End11*Ham11 END AS S11,
    CASE WHEN CAST(CAST(End12 AS INTEGER) AS TEXT) <> End12 
           OR CAST(CAST(Ham12 AS INTEGER) AS TEXT) <> Ham12 THEN NULL
         ELSE End12*Ham12 END AS S12 '''

calculate_hammer = ''' (SELECT *,
    CASE WHEN CAST(CAST(End12 AS INTEGER) AS TEXT) <> End12 THEN NULL
         WHEN CAST(End11 AS INTEGER) > 0 THEN -1
         WHEN CAST(End11 AS INTEGER) < 0 THEN  1
         ELSE Ham11 END AS Ham12
FROM 
(SELECT *, 
    CASE WHEN CAST(CAST(End11 AS INTEGER) AS TEXT) <> End11 THEN NULL
         WHEN CAST(End10 AS INTEGER) > 0 THEN -1
         WHEN CAST(End10 AS INTEGER) < 0 THEN  1
         ELSE Ham10 END AS Ham11
FROM 
(SELECT *, 
    CASE WHEN CAST(CAST(End10 AS INTEGER) AS TEXT) <> End10 THEN NULL
         WHEN CAST(End9 AS INTEGER) > 0 THEN -1
         WHEN CAST(End9 AS INTEGER) < 0 THEN  1
         ELSE Ham9 END AS Ham10
FROM 
(SELECT *, 
    CASE WHEN CAST(CAST(End9 AS INTEGER) AS TEXT) <> End9 THEN NULL
         WHEN CAST(End8 AS INTEGER) > 0 THEN -1
         WHEN CAST(End8 AS INTEGER) < 0 THEN  1
         ELSE Ham8 END AS Ham9
FROM 
(SELECT *, 
    CASE WHEN CAST(CAST(End8 AS INTEGER) AS TEXT) <> End8 THEN NULL
         WHEN CAST(End7 AS INTEGER) > 0 THEN -1
         WHEN CAST(End7 AS INTEGER) < 0 THEN  1
         ELSE Ham7 END AS Ham8
FROM 
(SELECT *, 
    CASE WHEN CAST(CAST(End7 AS INTEGER) AS TEXT) <> End7 THEN NULL
         WHEN CAST(End6 AS INTEGER) > 0 THEN -1
         WHEN CAST(End6 AS INTEGER) < 0 THEN  1
         ELSE Ham6 END AS Ham7 
FROM 
(SELECT *, 
    CASE WHEN CAST(CAST(End6 AS INTEGER) AS TEXT) <> End6 THEN NULL
         WHEN CAST(End5 AS INTEGER) > 0 THEN -1
         WHEN CAST(End5 AS INTEGER) < 0 THEN  1
         ELSE Ham5 END AS Ham6 
FROM 
(SELECT *,
    CASE WHEN CAST(CAST(End5 AS INTEGER) AS TEXT) <> End5 THEN NULL
         WHEN CAST(End4 AS INTEGER) > 0 THEN -1
         WHEN CAST(End4 AS INTEGER) < 0 THEN  1
         ELSE Ham4 END AS Ham5
FROM 
(SELECT *,
    CASE WHEN CAST(CAST(End4 AS INTEGER) AS TEXT) <> End4 THEN NULL
         WHEN CAST(End3 AS INTEGER) > 0 THEN -1
         WHEN CAST(End3 AS INTEGER) < 0 THEN  1
         ELSE Ham3 END AS Ham4
FROM 
(SELECT *, 
    CASE WHEN CAST(CAST(End3 AS INTEGER) AS TEXT) <> End3 THEN NULL
         WHEN CAST(End2 AS INTEGER) > 0 THEN -1
         WHEN CAST(End2 AS INTEGER) < 0 THEN  1
         ELSE Ham2 END AS Ham3
FROM 
(SELECT *, 
    CASE WHEN CAST(CAST(End2 AS INTEGER) AS TEXT) <> End2 THEN NULL
         WHEN CAST(End1 AS INTEGER) > 0 THEN -1
         WHEN CAST(End1 AS INTEGER) < 0 THEN  1
         ELSE Ham1 END AS Ham2
    FROM matches ))))))))))) AS matches '''

# Queries required to clean up the matches table before analysis
# Delete matches with invalid scores (end scores do not sum to final score,
#   ends with scores > 8, matches with no scores or ties, matches of 1-2 ends,
#   one specific case with known bad data)
# Add number of ends to the events table
def clean_data():
    query = ['''UPDATE matches
SET End1 = COALESCE(End1,""),
    End2 = COALESCE(End2,""),
    End3 = COALESCE(End3,""),
    End4 = COALESCE(End4,""),
    End5 = COALESCE(End5,""),
    End6 = COALESCE(End6,""),
    End7 = COALESCE(End7,""),
    End8 = COALESCE(End8,""),
    End9 = COALESCE(End9,""),
    End10 = COALESCE(End10,""),
    End11 = COALESCE(End11,""),
    End12 = COALESCE(End12,"")''',
    '''DELETE 
FROM matches 
WHERE CAST(Final1 AS INTEGER) <> MAX(CAST(End1 AS INTEGER), 0)
       + MAX(CAST(End2 AS INTEGER), 0)
       + MAX(CAST(End3 AS INTEGER), 0)
       + MAX(CAST(End4 AS INTEGER), 0)
       + MAX(CAST(End5 AS INTEGER), 0)
       + MAX(CAST(End6 AS INTEGER), 0)
       + MAX(CAST(End7 AS INTEGER), 0)
       + MAX(CAST(End8 AS INTEGER), 0)
       + MAX(CAST(End9 AS INTEGER), 0)
       + MAX(CAST(End10 AS INTEGER), 0)
       + MAX(CAST(End11 AS INTEGER), 0)
       + MAX(CAST(End12 AS INTEGER), 0) 
    OR CAST(Final2 AS INTEGER) <> ABS(MIN(CAST(End1 AS INTEGER), 0)
       + MIN(CAST(End2 AS INTEGER), 0)
       + MIN(CAST(End3 AS INTEGER), 0)
       + MIN(CAST(End4 AS INTEGER), 0)
       + MIN(CAST(End5 AS INTEGER), 0)
       + MIN(CAST(End6 AS INTEGER), 0)
       + MIN(CAST(End7 AS INTEGER), 0)
       + MIN(CAST(End8 AS INTEGER), 0)
       + MIN(CAST(End9 AS INTEGER), 0)
       + MIN(CAST(End10 AS INTEGER), 0)
       + MIN(CAST(End11 AS INTEGER), 0)
       + MIN(CAST(End12 AS INTEGER), 0))''',
    '''DELETE 
FROM matches 
WHERE  ABS(CAST(End1 AS INTEGER)) > 8
    OR ABS(CAST(End2 AS INTEGER)) > 8
    OR ABS(CAST(End3 AS INTEGER)) > 8
    OR ABS(CAST(End4 AS INTEGER)) > 8
    OR ABS(CAST(End5 AS INTEGER)) > 8
    OR ABS(CAST(End6 AS INTEGER)) > 8
    OR ABS(CAST(End7 AS INTEGER)) > 8
    OR ABS(CAST(End8 AS INTEGER)) > 8
    OR ABS(CAST(End9 AS INTEGER)) > 8
    OR ABS(CAST(End10 AS INTEGER)) > 8
    OR ABS(CAST(End11 AS INTEGER)) > 8
    OR ABS(CAST(End12 AS INTEGER)) > 8''',
    '''DELETE 
FROM matches 
WHERE (CAST(Final1 AS INTEGER) = 0
    AND CAST(Final2 AS INTEGER) = 0)
    OR Final1 IS NULL
    OR Final2 IS NULL''',
    '''DELETE 
FROM matches 
WHERE Final1 = Final2''',
    '''DELETE FROM matches
WHERE (CASE WHEN CAST(CAST(End1 AS INTEGER) AS TEXT)  <> End1  THEN 0
            WHEN CAST(CAST(End2 AS INTEGER) AS TEXT)  <> End2  THEN 1
            WHEN CAST(CAST(End3 AS INTEGER) AS TEXT)  <> End3  THEN 2
            ELSE 3 END) < 3''',
    '''DELETE FROM matches
    WHERE EID = 2820 AND Draw = 8 AND Team1 LIKE "%Koltun"''',
    '''ALTER TABLE events
   ADD Ends''',
    '''UPDATE matches
    SET End1 = REPLACE(End1,"None",""),
        End2 = REPLACE(End2,"None",""),
        End3 = REPLACE(End3,"None",""),
        End4 = REPLACE(End4,"None",""),
        End5 = REPLACE(End5,"None",""),
        End6 = REPLACE(End6,"None",""),
        End7 = REPLACE(End7,"None",""),
        End8 = REPLACE(End8,"None",""),
        End9 = REPLACE(End9,"None",""),
        End10 = REPLACE(End10,"None",""),
        End11 = REPLACE(End11,"None",""),
        End12 = REPLACE(End12,"None","")''',
    '''UPDATE events
    SET Ends = temp.Ends
    FROM (SELECT events.EID, 
          ROUND(AVG(CASE WHEN End1 = "" THEN 0
               WHEN End2 = ""  THEN 1
               WHEN End3 = ""  THEN 2
               WHEN End4 = ""  THEN 3
               WHEN End5 = ""  THEN 4
               WHEN End6 = ""  THEN 5
               WHEN End7 = ""  THEN 6
               WHEN End8 = ""  THEN 7
               WHEN End9 = ""  THEN 8
               WHEN End10 = "" THEN 9
               WHEN End11 = "" THEN 10
               WHEN End12 = "" THEN 11
               ELSE 12 END)/2) * 2 AS Ends
        FROM events
        INNER JOIN matches ON matches.EID = events.EID
        WHERE CAST(CAST(End1 AS INTEGER) AS TEXT) = End1
        GROUP BY events.EID) AS temp
    WHERE events.EID = temp.EID''']
    return query

def add_hammer():
    all_queries = []
    for end in range(2,13):
        all_queries.append('ALTER TABLE matches ADD Ham'+str(end)+';')
        all_queries.append('''UPDATE matches
SET Ham'''+str(end)+' = (CASE WHEN CAST(CAST(End'+str(end)+' AS INTEGER) AS TEXT) <> End'+str(end)+''' THEN NULL
     WHEN CAST(End'''+str(end-1)+''' AS INTEGER) > 0 THEN -1
     WHEN CAST(End'''+str(end-1)+''' AS INTEGER) < 0 THEN  1
     ELSE Ham'''+str(end-1)+' END);')

    return all_queries

def add_ends():
    all_queries = ['ALTER TABLE matches ADD Ends;']
    all_queries.append('''UPDATE matches
SET Ends = tmp.Ends
FROM (SELECT EID, Ends
              FROM events) AS tmp
WHERE tmp.EID = matches.EID;''')
    return all_queries

def add_season():
    all_queries = ['ALTER TABLE matches ADD Season;']
    all_queries.append('''UPDATE matches
SET Season = tmp.Season
FROM (SELECT EID, (CASE WHEN CAST(substr(Date, 6, 2) AS INTEGER) > 6 
                          THEN CAST(substr(Date, 1, 4) AS INTEGER) + 1
                          ELSE CAST(substr(Date, 1, 4) AS INTEGER)
                  END) AS Season
              FROM events) AS tmp
WHERE tmp.EID = matches.EID;''')
    return all_queries

def add_category_rank():
    all_queries = ['ALTER TABLE matches ADD Type;',
                   'ALTER TABLE matches ADD Rank1;',
                   'ALTER TABLE matches ADD Rank2;']
    all_queries.append('''UPDATE matches
SET Type = tmp.Type
FROM (SELECT Name, Type FROM teams) as tmp
WHERE tmp.Name = matches.Team1;''')
    all_queries.append('''UPDATE matches
SET Type = tmp.Type
FROM (SELECT Name, Type FROM teams) as tmp
WHERE tmp.Name = matches.Team2
    AND matches.Type IS NULL''')
    for season in range(2011,2025):
        all_queries.append('''UPDATE matches
SET Rank1 = MIN(tmp.Rank, 500)
FROM (SELECT Name, Type, 
          RANK() OVER (ORDER BY World'''+str(season)+''' DESC) AS Rank
      FROM teams
      WHERE Type = "Men") AS tmp
WHERE tmp.Name = matches.Team1
    AND Season = '''+str(season)+';')
        all_queries.append('''UPDATE matches
SET Rank1 = MIN(tmp.Rank, 500)
FROM (SELECT Name, Type, 
          RANK() OVER (ORDER BY World'''+str(season)+''' DESC) AS Rank
      FROM teams
      WHERE Type = "Women") AS tmp
WHERE tmp.Name = matches.Team1
    AND Season = '''+str(season)+';')
        all_queries.append('''UPDATE matches
SET Rank2 = MIN(tmp.Rank, 500)
FROM (SELECT Name, Type, 
          RANK() OVER (ORDER BY World'''+str(season)+''' DESC) AS Rank
      FROM teams
      WHERE Type = "Men") AS tmp
WHERE tmp.Name = matches.Team2
    AND Season = '''+str(season)+';')
        all_queries.append('''UPDATE matches
SET Rank2 = MIN(tmp.Rank, 500)
FROM (SELECT Name, Type, 
          RANK() OVER (ORDER BY World'''+str(season)+''' DESC) AS Rank
      FROM teams
      WHERE Type = "Women") AS tmp
WHERE tmp.Name = matches.Team2
    AND Season = '''+str(season)+';')
    return all_queries

# Generate reusable SQL to get matches for a given category (men/women), season,
# and ranking range for each team
def sort_matches(ends=None, category=None, 
                 rank1=None, rank2=None, season=None, month=False, 
                 ordered=False):
    query = ''
    if month:
        query = '    INNER JOIN events ON matches.EID = events.EID\n'
    if category or rank1 or rank2 or ends or season:
        query += 'WHERE   '
    if ends:
        query += 'matches.Ends = '+str(ends)+'\n'
        if category or season:
            query += '    AND '
    if category:
        query += 'matches.Type = "' + category + '"\n'
        if rank1 or rank2 or season:
            query += '\n    AND '
    if rank1 and rank2 and not ordered:
        query += '((Rank1 BETWEEN '+str(rank1[0])+' AND '+str(rank1[1])+'\n'
        query += 'AND Rank2 BETWEEN '+str(rank2[0])+' AND '+str(rank2[1])+')\n'
        query += 'OR (Rank1 BETWEEN '+str(rank2[0])+' AND '+str(rank2[1])+'\n'
        query += 'AND Rank2 BETWEEN '+str(rank1[0])+' AND '+str(rank1[1])+'))\n'
        if season:
            query += '    AND '
    elif rank1 and rank2:
        query += '(Rank1 BETWEEN '+str(rank1[0])+' AND '+str(rank1[1])+'\n'
        query += 'AND Rank2 BETWEEN '+str(rank2[0])+' AND '+str(rank2[1])+')\n'
        if season:
            query += '    AND '
    elif rank1 or rank2 and not ordered:
        r = rank1 if rank1 else rank2
        query += '(Rank1 BETWEEN ' + str(r[0]) + ' AND ' +str(r[1]) + '\n'
        query += 'OR Rank2 BETWEEN ' + str(r[0]) + ' AND ' +str(r[1]) + ')\n'
        if season:
            query += '    AND '
    elif rank1:
        query += 'Rank1 BETWEEN ' + str(rank1[0]) + ' AND ' +str(rank1[1]) + '\n'
        if season:
            query += '    AND '
    elif rank2:
        query += 'Rank2 BETWEEN ' + str(rank2[0]) + ' AND ' +str(rank2[1]) + '\n'
        if season:
            query += '    AND '
    if season:
        if type(season) == list:
            query += 'Season BETWEEN '+str(season[0])+' AND '+str(season[-1])
        else:
            query += 'Season = '+str(season)
    return query

def sort_matches_old(ends=None, category=None, 
                 rank1=None, rank2=None, season=None, 
                 ordered=False):
    query = '    INNER JOIN events ON matches.EID = events.EID\n'
    if category or rank1 or rank2:
        query += '''    INNER JOIN teams AS t1 ON matches.Team1 = t1.Name
    INNER JOIN teams AS t2 ON matches.Team2 = t2.Name\n'''
    if category or rank1 or rank2 or ends or season:
        query += 'WHERE   '
    if ends:
        query += 'Ends = '+str(ends)+'\n'
        if category or season:
            query += '    AND '
    if category:
        query += '(t1.Type = "' + category + '"\n    OR t2.Type = "' + category + '")'
        if rank1 or rank2 or season:
            query += '\n    AND '
    
    if rank1 and rank2 and not ordered:
        query += '''((t1.Name IN (SELECT Name from teams
        WHERE Type = "''' + category + '''"
        ORDER BY World'''+str(season) + ''' DESC
        LIMIT ''' + str(rank1[1]-rank1[0]+1) + ' OFFSET '+str(rank1[0]-1)+''')
    AND t2.Name IN (SELECT Name from teams
        WHERE Type = "''' + category + '''"
        ORDER BY World'''+str(season) + ''' DESC
        LIMIT ''' + str(rank2[1]-rank2[0]+1) + ' OFFSET '+str(rank2[0]-1)+'''))
    OR (t2.Name IN (SELECT Name from teams
        WHERE Type = "''' + category + '''"
        ORDER BY World'''+str(season) + ''' DESC
        LIMIT ''' + str(rank1[1]-rank1[0]+1) + ' OFFSET '+str(rank1[0]-1)+''')
    AND t1.Name IN (SELECT Name from teams
        WHERE Type = "''' + category + '''"
        ORDER BY World'''+str(season) + ''' DESC
        LIMIT ''' + str(rank2[1]-rank2[0]+1) + ' OFFSET '+str(rank2[0]-1)+''')))\n'''
        if season:
            query += '    AND '
    elif rank1 and rank2:
        query += '''(t1.Name IN (SELECT Name from teams
        WHERE Type = "''' + category + '''"
        ORDER BY World'''+str(season) + ''' DESC
        LIMIT ''' + str(rank1[1]-rank1[0]+1) + ' OFFSET '+str(rank1[0]-1)+''')
    AND t2.Name IN (SELECT Name from teams
        WHERE Type = "''' + category + '''"
        ORDER BY World'''+str(season) + ''' DESC
        LIMIT ''' + str(rank2[1]-rank2[0]+1) + ' OFFSET '+str(rank2[0]-1)+'''))\n'''
        if season:
            query += '    AND '
    elif rank1 or rank2 and not ordered:
        r = rank1 if rank1 else rank2
        query += '''(t1.Name IN (SELECT Name from teams
        WHERE Type = "''' + category + '''"
        ORDER BY World'''+str(season) + ''' DESC
        LIMIT ''' + str(r[1]-r[0]+1) + ' OFFSET '+str(r[0]-1)+''')
    OR t2.Name IN (SELECT Name from teams
        WHERE Type = "''' + category + '''"
        ORDER BY World'''+str(season) + ''' DESC
        LIMIT ''' + str(r[1]-r[0]+1) + ' OFFSET '+str(r[0]-1)+'''))\n'''
        if season:
            query += '    AND '
    elif rank1:
        query +='''t1.Name IN (SELECT Name from teams
        WHERE Type = "''' + category + '''"
        ORDER BY World'''+str(season) + ''' DESC
        LIMIT ''' + str(rank1[1]-rank1[0]+1) + ' OFFSET '+str(rank1[0]-1)+')\n'
        if season:
            query += '    AND '
    elif rank2:
        query +='''t2.Name IN (SELECT Name from teams
        WHERE Type = "''' + category + '''"
        ORDER BY World'''+str(season) + ''' DESC
        LIMIT ''' + str(rank2[1]-rank2[0]+1) + ' OFFSET '+str(rank1[0]-1)+')\n'
        if season:
            query += '    AND '
    if season:
        query += 'Date BETWEEN "'+str(season-1)+'-07-00" AND "'+str(season)+'-06-31"'
    return query
    

# Count matches by month
def count_matches_month(ends = None, category = None, 
                        rank1 = None, rank2 = None, season = [None]):
    if (rank1 or rank2) and (not category or not season):
        print('Error: Sorting by team rank is only available within a team category (men or women)')
        print('    and with a season or range of seasons specified')
        return []
    if type(rank1) == int:
        rank1 = (1, rank1)
    if type(rank2) == int:
        rank2 = (1, rank2)
    if type(season) == int:
        season = [season]
    
    # Do one query for each season
    # This enables selecting the appropriate range of ranks for each season
    all_queries = []
    query = '''SELECT CAST(substr(Date, 1, 4) AS INTEGER) AS Year, 
        CAST(substr(Date, 6, 2) AS INTEGER) AS Month, COUNT(*) 
FROM matches 
'''
    if category or ends or season or rank1 or rank2:
        query += sort_matches(category = category, ends = ends,
                              season = season, rank1 = rank1, rank2 = rank2, 
                              ordered = False, month=True)
    query += '\nGROUP BY substr(Date, 1, 4), substr(Date, 6, 2);'
    all_queries.append(query)
    return all_queries


# Count events by month
def count_events_month(ends = None):
    query = '''SELECT substr(Date, 1, 4) AS Year, substr(Date, 6, 2) AS Month, COUNT(*) 
FROM events '''
    if ends:
        query += '\nWHERE Ends = '+str(ends)+'\n'

    query += 'GROUP BY substr(Date, 1, 4), substr(Date, 6, 2);'
    return query


def count_final_scores(ends = 8, category = None, 
                       rank1 = None, rank2 = None, season = [None], ordered=True):
    if (rank1 or rank2) and (not category or not season):
        print('Error: Sorting by team rank is only available within a team category (men or women)')
        print('    and with a season or range of seasons specified')
        return []
    if type(rank1) == int:
        rank1 = (1, rank1)
    if type(rank2) == int:
        rank2 = (1, rank2)
    if type(season) == int:
        season = [season]
    
    # Do one query for each season
    # This enables selecting the appropriate range of ranks for each season
    all_queries = []
    query = '''SELECT Final1, Final2, COUNT(*) 
FROM matches 
'''
    if category or ends or season or rank1 or rank2:
        query += sort_matches(category = category, ends = ends,
                              season = season, rank1 = rank1, rank2 = rank2,
                              ordered = ordered)
    query += '\nGROUP BY Final1, Final2;'
    all_queries.append(query)
    query = '''SELECT Final2, Final1, COUNT(*) 
FROM matches 
'''
    if category or ends or season or rank1 or rank2:
        query += sort_matches(category = category, ends = ends,
                              season = season, rank1 = rank2, rank2 = rank1,
                              ordered = ordered)
    query += '\nGROUP BY Final2, Final1;'
    all_queries.append(query)
    return all_queries

def get_end_scores(ends = 8, category = None,
                     rank1 = None, rank2 = None, season = [None], ordered=True):
    all_queries = []
    query = '''SELECT CAST(End1 AS INTEGER), CAST(Ham1 AS INTEGER), 
                      CAST(End2 AS INTEGER), CAST(Ham2 AS INTEGER),
                      CAST(End3 AS INTEGER), CAST(Ham3 AS INTEGER),
                      CAST(End4 AS INTEGER), CAST(Ham4 AS INTEGER),
                      CAST(End5 AS INTEGER), CAST(Ham5 AS INTEGER),
                      CAST(End6 AS INTEGER), CAST(Ham6 AS INTEGER),
                      CAST(End7 AS INTEGER), CAST(Ham7 AS INTEGER),
                      CAST(End8 AS INTEGER), CAST(Ham8 AS INTEGER),
                      CAST(End9 AS INTEGER), CAST(Ham9 AS INTEGER),
                      CAST(End10 AS INTEGER), CAST(Ham10 AS INTEGER),
                      CAST(End11 AS INTEGER), CAST(Ham11 AS INTEGER),
                      CAST(End12 AS INTEGER), CAST(Ham12 AS INTEGER)
FROM matches\n'''
    query += sort_matches(category = category, ends = ends,
                          season = season, rank1 = rank1, rank2 = rank2,
                          ordered = ordered)
    query += ';'
    all_queries.append(query)
    query = '''SELECT -CAST(End1 AS INTEGER), -CAST(Ham1 AS INTEGER), 
                      -CAST(End2 AS INTEGER), -CAST(Ham2 AS INTEGER),
                      -CAST(End3 AS INTEGER), -CAST(Ham3 AS INTEGER),
                      -CAST(End4 AS INTEGER), -CAST(Ham4 AS INTEGER),
                      -CAST(End5 AS INTEGER), -CAST(Ham5 AS INTEGER),
                      -CAST(End6 AS INTEGER), -CAST(Ham6 AS INTEGER),
                      -CAST(End7 AS INTEGER), -CAST(Ham7 AS INTEGER),
                      -CAST(End8 AS INTEGER), -CAST(Ham8 AS INTEGER),
                      -CAST(End9 AS INTEGER), -CAST(Ham9 AS INTEGER),
                      -CAST(End10 AS INTEGER), -CAST(Ham10 AS INTEGER),
                      -CAST(End11 AS INTEGER), -CAST(Ham11 AS INTEGER),
                      -CAST(End12 AS INTEGER), -CAST(Ham12 AS INTEGER)
FROM ''' + calculate_hammer + '\n'
    query += sort_matches(category = category, ends = ends,
                          season = season, rank1 = rank2, rank2 = rank1,
                          ordered = ordered)
    query += ';'
    all_queries.append(query)
    return all_queries
