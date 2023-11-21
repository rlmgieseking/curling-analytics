import utils.api as api
#import pandas as pd

def matchtostring(m):
    values = ''
    values += '(' + str(m['EID']) + ', '
    if type(m['Draw']) == int:
        values += str(m['Draw']) + ', "'
    else:
        values += '"' + str(m['Draw']) + '", "'
    values += m['Team1'] + '", "' + m['Team2'] 
    values += '", ' + str(m['Final1']) + ', ' + str(m['Final2'])
    values += ', ' + str(m['Ham1'])
    for i in range(1,13):
        if type(m['End'+str(i)]) == int:
            values += ', ' + str(m['End'+str(i)]) 
        elif type(m['End'+str(i)]) == str:
            values += ', "' + str(m['End'+str(i)]) + '"'
        else:
            values += ', Null'
    values += ')'
    return values

# For a given event, read all boxscores
def readallboxscores(event: int, startdraw: int = 1) -> list:
    allboxscores = []
    draw = startdraw
    # Some events (like mixed mens/womens) have empty draws in between active draws
    # Keep looking for new draws until we see 3 consecutive empty draws
    # Most mixed mens/womens events alternate, so usually 2 consecutive is enough
    # 3 consecutive accounts for mismatched numbers of tiebreakers, etc.
    empty = 0
    while empty < 3:
        #print('Event', event, 'Draw', draw)
        boxscores = readboxscores(event, draw)
        allboxscores.extend(boxscores)
        if len(boxscores) == 0:
            empty += 1
        else:
            empty = 0
            print('  Event', event, 'Draw', draw, 'Matches', len(boxscores))
        draw += 1
    '''
    scorelist = ''
    for score in allboxscores:
        if 'Team1' in score.keys():
            scorelist += '(' + str(score['EID']) + ', '
            if type(score['Draw']) == int:
                scorelist += str(score['Draw']) + ', "'
            else:
                scorelist += '"' + str(score['Draw']) + '", "'
            scorelist += score['Team1'] + '", "' + score['Team2'] 
            scorelist += '", ' + str(score['Final1']) + ', ' + str(score['Final2'])
            scorelist += ', ' + str(score['Hammer'])
            for i in range(1,13):
                if 'End'+str(i) in score.keys():
                    if type(score['End'+str(i)]) == int:
                        scorelist += ', ' + str(score['End'+str(i)]) 
                    else:
                        scorelist += ', "' + str(score['End'+str(i)]) + '"'
                else:
                    scorelist += ', Null'
            scorelist += '),\n'
    scorelist = scorelist[:-2] + ';'
    '''
    return allboxscores

# Read boxscores for one draw
def readboxscores(event: int, draw: int) -> list:
    linescorepage = api.LinescorePage(cz_event_id = event, cz_draw_id = draw)
    boxscores = linescorepage.boxscores
    reformat = []
    for i in range(len(boxscores)):
        #print(boxscores[i])
        if len([key for key in boxscores[i]]) > 0:
            reformat.append(reformatboxscore(boxscores[i]))
            #reformat[-1]['Event'] = linescorepage.event_name
            reformat[-1]['EID'] = event
            #reformat[-1]['Date'] = linescorepage.event_date
            try:
                draw = linescorepage.draw
                if 'Draw: ' in draw:
                    draw = draw.replace('Draw: ', '')
                reformat[-1]['Draw'] = draw
            except: 
                reformat[-1]['Draw'] = None
    return reformat

# Reformat box scores from the czapi format into form used in .csv output
def reformatboxscore(boxscore: dict) -> dict:
    #print(boxscore)
    teams = [key for key in boxscore]
    if len(teams) < 2:
        return {}

# Set up reformatted dictionary: team names, final scores, and winner
# If hammer = 1, team 1 starts with hammer; if hammer = None, first hammer not known
    reformat = {'Team1': teams[0], 'Team2': teams[1],  
            'Final1': int(boxscore.get(teams[0]).get('finalscore')),
            'Final2': int(boxscore.get(teams[1]).get('finalscore'))}

    # Make sure only teams[0] has hammer
    if (boxscore.get(teams[0]).get('hammer') == True 
          and boxscore.get(teams[1]).get('hammer') == False):
        reformat['Ham1'] = 1
    elif (boxscore.get(teams[1]).get('hammer') == True 
          and boxscore.get(teams[0]).get('hammer') == False):
        teams[0], teams[1] = teams[1], teams[0]
        reformat['Ham1'] = 1
    else:
        reformat['Ham1'] = 'Null'
    
    # Set up scores by end
    # Positive score is a score for team 1, negative is team 2, zero is blank
    team1scores = boxscore.get(teams[0]).get('score')
    team2scores = boxscore.get(teams[1]).get('score')
    
    ends = min(len(team1scores), len(team2scores))
    if len(team1scores) != len(team2scores):
        #reformat['Error'] = True
        print('Error: Teams have scores from different numbers of ends')
        print('   ', team1scores)
        print('   ', team2scores)
    for i in range(ends):
        key = 'End' + str(i+1)
        #hkey = 'Ham' + str(i+1)
        if team1scores[i].isdigit() and team2scores[i].isdigit():
            score = int(team1scores[i]) - int(team2scores[i])
            if int(team1scores[i]) != 0 and int(team2scores[i]) != 0:
                print('Error: Both teams scored in end ', str(i+1))
                print('   ', team1scores)
                print('   ', team2scores)
                #reformat['Error'] = True
        else:
            score = 'X'
        reformat[key] = score
    for i in range(ends,13):
        key = 'End' + str(i+1)
        reformat[key] = None
    
    return reformat

# Get name, date, and type for new events since a given start point
def readeventinfo(event, maxlen = 1000):
    valid = True
    event_info = ''
    e = event
    while valid:
        eventpage = api.EventPage(cz_event_id = e)
        if not eventpage.event_name or e - event == maxlen:
            valid = False
        else:
            #print(eventpage.event_name,eventpage.event_date,eventpage.event_type)
            if len(event_info) > 0:
                event_info += ',\n'
            event_info += '(' + str(e) + ', "' + eventpage.event_name + '", "'
            event_info += eventpage.event_date + '", ' + eventpage.event_type  + ')'
        #print(str(e))
        e += 1
    return event_info


# Get team ranking points for a given season
def readteamrankings(season):
    import requests
    
    def clean(t):
        #print(t)
        t1 = t[t.index('>')+1:]
        while len(t1) > 0 and t1[0] == '<':
            t1 = t1[t1.index('>')+1:]
        if '<' in t1:
            t1 = t1[:t1.index('<')]
        if '&nbsp;' in t1:
            t1 = t1[:t1.index('&nbsp;')]
        return t1
    
    # Get the parsed HTML content
    men_url = 'https://www.curlingzone.com/rankings.php?task=week&oomid=81&eventyear='+str(season)
    wom_url = 'https://www.curlingzone.com/rankings.php?task=week&oomid=82&eventyear='+str(season)
    teams = []
    for url in [men_url,wom_url]:
        response = requests.get(url)
        #soup = BeautifulSoup(response.content, "html.parser")
        text = str(response.content).split("<td data-th=")
        for t in text[1:]:
            if '"Team">' in t:
                #print('t',t)
                team = clean(t)
                teams.append({'Team': team})
                if url == men_url:
                    teams[-1]['Type'] = 'Men'
                else:
                    teams[-1]['Type'] = 'Women'
            elif '"Location">' in t:
                loc = clean(t)
                teams[-1]['Location'] = loc
            elif '"Total" align="right">' in t:
                pts = clean(t)
                teams[-1]['Points'] = pts

    return teams

def get_fixed_teams(event):
    page = api.TeamsPage(cz_event_id=event)
    return page.team_dict
