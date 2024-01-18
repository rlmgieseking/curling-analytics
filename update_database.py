# Script to update the database of matches stored in utils/matches.db
# 1. Update the events table
# 2. Query the updates table to find when the database was last updated
# 3. Update the matches table for all events since the last update
# 4. Update the teams table to have current rankings
# 5. Update the update table to current date

import utils.webscraper as scraper
import sqlite3
import datetime 

# Set up choices for later
filename = 'utils/matches.db'
update_events = True
update_matches = True
update_teams = True

# Connect to SQL database
conn = sqlite3.connect(filename)
conn.close()
conn = sqlite3.connect(filename)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS updates (
	date VARCHAR PRIMARY KEY
)''')

if len(c.execute('''SELECT * FROM updates;''').fetchall()) == 0:
    c.execute('INSERT INTO updates (date) VALUES ("2023-07-01");')

today = datetime.date.today().strftime('%Y-%m-%d')
last_update = c.execute('''SELECT MAX(date) FROM updates;''').fetchall()[0][0]

# Update the events table
if update_events:
    last_event = c.execute('''SELECT MAX(EID) FROM events;''').fetchall()[0][0]
    print('Last event in old table: ' + str(last_event))
    new_events = scraper.readeventinfo(last_event+1)
    #print(new_events)
    if len(new_events) > 1:
        c.execute('''INSERT INTO events (EID, Event, Date, Type)
                  VALUES
                  ''' + new_events + ';')
    
    last_event = c.execute('''SELECT MAX(EID) FROM events;''').fetchall()[0][0]
    print('Last event in new table: ' + str(last_event))
    conn.commit()

# Update the matches table for all events since the last update
if update_matches:
    print("Matches last updated: ", last_update)
    # Updated matches with start dates later than 14 days before the last update
    # Long events run up to 10-12 days, so this captures events that were running
    # at the time of the last update
    start = (datetime.datetime.strptime(last_update, '%Y-%m-%d') - 
             datetime.timedelta(days=14)).strftime('%Y-%m-%d')
    print("Updating all events with start dates since " + start)

    new_events = c.execute('''SELECT EID FROM events
        WHERE Date BETWEEN "''' + start + '" AND "' + today + '";').fetchall()
    print('Number of events that need matches: '+str(len(new_events)))
    for event in new_events:
        if event[0] >= 7000:
            matches = scraper.readallboxscores(event[0])
        else:
            matches = []
        #print(matches)
        if len(matches) > 0:
            # Check if any matches from this event are already in the database
            # If not, add all
            # If yes, check each one for duplicates
            curr_matches = c.execute('''SELECT * FROM matches 
                                     WHERE EID = '''+str(event[0]) + ';').fetchall()
            if len(curr_matches) == 0:
                values = ''
                for m in matches:
                    if 'Team1' in m.keys() and 'Team2' in m.keys():
                        values += scraper.matchtostring(m) + ',\n'
                values = values[:-2] + ';'
                c.execute('''INSERT INTO matches (EID, Draw, Team1, Team2, 
                              Final1, Final2, Ham1, 
                              End1, End2, End3, End4, End5, End6, 
                              End7, End8, End9, End10, End11, End12)
                    VALUES
                    ''' + values)
            else:
                for m in matches:
                    if 'Team1' in m.keys() and 'Team2' in m.keys():
                        curr = len(c.execute('''SELECT * FROM matches 
                                                 WHERE EID = '''+str(event[0]) + 
                                                 ' AND Draw = "' + str(m['Draw']) + 
                                                 '" AND Team1 = "' + str(m['Team1']) +
                                                 '" AND Team2 = "' + str(m['Team2']) + 
                                                 '";').fetchall())
                        
                        if curr == 0:
                            values = scraper.matchtostring(m) 
                            c.execute('''INSERT INTO matches (EID, Draw, Team1, Team2, 
                                          Final1, Final2, Ham1, 
                                          End1, End2, End3, End4, End5, End6, 
                                          End7, End8, End9, End10, End11, End12)
                                VALUES
                                ''' + values + ';')
                        else:
                            c.execute('''UPDATE matches
                                      SET Final1 = "''' + str(m['Final1']) + '", ' +
                                      'Final2 = "' + str(m['Final2']) + '", ' +
                                      'Ham1 = "' + str(m['Ham1']) + '", ' +
                                      'End1 = "' + str(m['End1']) + '", ' +
                                      'End2 = "' + str(m['End2']) + '", ' +
                                      'End3 = "' + str(m['End3']) + '", ' +
                                      'End4 = "' + str(m['End4']) + '", ' +
                                      'End5 = "' + str(m['End5']) + '", ' +
                                      'End6 = "' + str(m['End6']) + '", ' +
                                      'End7 = "' + str(m['End7']) + '", ' +
                                      'End8 = "' + str(m['End8']) + '", ' +
                                      'End9 = "' + str(m['End9']) + '", ' +
                                      'End10 = "' + str(m['End10']) + '", ' +
                                      'End11 = "' + str(m['End11']) + '", ' +
                                      'End12 = "' + str(m['End12']) + '" \n' +
                                      'WHERE EID = '+str(event[0]) + 
                                      ' AND Draw = "' + str(m['Draw']) + 
                                      '" AND Team1 = "' + str(m['Team1']) +
                                      '" AND Team2 = "' + str(m['Team2']) + '";')
            conn.commit()
            matches = c.execute('''SELECT Team1, Team2 FROM matches 
                        WHERE EID = '''+str(event[0]) + '''
                        AND (Team1 = "Canada" OR Team2 = "Canada"
                            OR Team1 = "Ontario" OR Team2 = "Ontario"
                            OR Team1 = "Alberta" OR Team2 = "Alberta"
                            OR Team1 = "Sweden" OR Team2 = "Sweden"
                            OR Team1 = "Scotland" OR Team2 = "Scotland"
                            OR Team1 = "Norway" OR Team2 = "Norway"
                            OR Team1 = "Japan" OR Team2 = "Japan"
                            OR Team1 = "China" OR Team2 = "China")'''
                        ).fetchall()
            if len(matches) > 0:
                teams = scraper.get_fixed_teams(event[0])
                for key in teams.keys():
                    c.execute('''UPDATE matches
                        SET Team1 = "''' + teams[key] + '''" 
                        WHERE EID = '''+str(event[0]) + '''
                            AND Team1 = "''' + key + '"')
                    c.execute('''UPDATE matches
                        SET Team2 = "''' + teams[key] + '''" 
                        WHERE EID = '''+str(event[0]) + '''
                            AND Team2 = "''' + key + '"')

# Update the teams table to have current rankings
if update_teams:
    curr_season = (datetime.date.today() + datetime.timedelta(days=180)).year
    print('Updating world points for season '+str(curr_season))
    try:
        c.execute('SELECT World'+str(curr_season)+' FROM teams;')
    except:
        c.execute('''ALTER TABLE teams
                  ADD COLUMN World'''+str(curr_season) + ' REAL;')
    # Clear world points from current season
    c.execute('''UPDATE Teams
              SET World'''+str(curr_season) + ' = Null;')
    # Get world points for current season
    teams = scraper.readteamrankings(curr_season)
    #print(teams)
    for t in teams:
        try:
            c.execute('''UPDATE teams SET 
                      Location = "''' + t['Location'] + '''", 
                      World'''+str(curr_season)+' = "'+t['Points']+'''"
                      WHERE Name = "''' + t['Team'] + '";')
        except:
            c.execute('INSERT INTO teams (Name, Type, Location, World'+str(curr_season)+''')
                      VALUES ("''' + t['Team'] + '", "' + t['Type'] + '", "' +
                      t['Location'] + '"", "' + t['Points'] + '");')

# Update the 'last update' date
if last_update != today:
    c.execute('''INSERT INTO updates (date) VALUES ("''' + today + '");')

# Commit updates
conn.commit()
conn.close()