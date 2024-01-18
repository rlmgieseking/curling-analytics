# -*- coding: utf-8 -*-

import utils.graphs as graphs

def head():
    html = '''<head>
<style>
    h1 {text-align: center; font-family: verdana, arial, sans-serif;}
    h2 {font-family: verdana, arial, sans-serif;}
    h3 {font-family: verdana, arial, sans-serif;}
    h4 {font-family: verdana, arial, sans-serif;}
    h5 {font-family: verdana, arial, sans-serif;}
    p  {font-family: verdana, arial, sans-serif;}
    ul, ol {font-family: verdana, arial, sans-serif;}
    div {font-family: verdana, arial, sans-serif;}
    summary {font-family: verdana, arial, sans-serif; font-size: 1.5em; font-weight: bolder}
    iframe {text-align: center;}
    table, th, td {font-family: verdana, arial, sans-serif; border: 1px solid black; border-collapse: collapse;}
</style>
<title>Curling Sports Analytics</title>
</head>'''
    return html

def header():
    html  = '<h1>'
    html += 'Curling Sports Analytics'
    html += '</h1>\n'
    return html

def curling_basics():
    # Header 
    html = '<details><summary>Basics of Curling</summary>'
    # Main text
    html += '<p>If you are unfamiliar with curling, the World Curling Federation has a nice 2-minute intro to the sport:</p>'
    html += '''<iframe width="420" height="315"
src="https://www.youtube.com/embed/IOk9SVzqHsk">
</iframe> '''
    html += '<p>In curling, two teams of four players take turns sliding rocks down a sheet of ice toward a target painted on the far end of the ice (called the <b>house</b> or <b>rings</b>), sweeping the ice in from of the rock to control its path. Each match has series of scoring opportunities called <b>ends</b> (similar to innings in baseball), typically 8 or 10 ends, and the team with the most points at the conclusion of the match wins. Unlike most sports, teams often concede early if they are too far behind to have a realistic chance of winning.</p>'
    html += '<p>In each end, the teams take turns sliding rocks until each team has delivered 8 rocks. The team that delivers the last rock (called <b>hammer</b>) has a big advantage in scoring, since they have the last chance to rearrange rocks to maximize their score.</p>'
    html += '<p>The score for the end is based on the placement of the rocks after all rocks are delivered. If no rocks are in the house, both teams score zero points. If at least one rock is touching the house, the team with the rock closest to the center of the rings scores one point for each of their rocks that is closer to the center than the nearest opponent rock. For example, if the closest rock to the center is red and the second closest is yellow, red scores 1 point. If the closest three rocks to the center are all yellow and the fourth closest is red, then yellow scores 3 points.</p>'
    html += '<a href="https://kccurling.com/startcurling/curlingexplained/terminology"><img src="https://kccurling.com/images/2018/05/13/scoring-examples.png" alt="Scoring in curling" width="598" height="215"></a>'
    html += '<p>The common types of scores for one end are:</p>'
    html += ''' <ul>
  <li><b>Convert:</b> Team with hammer scores 2 or more points</li>
  <li><b>Force:</b> Team with hammer scores exactly 1 point</li>
  <li><b>Blank:</b> Both teams score 0 points</li>
  <li><b>Steal:</b> Team without hammer scores 1 or more points (I use negative numbers for steals in my analysis)</li>
</ul>'''
    html += '<p>If the end is blanked, the team with hammer keeps it in the next end. If one team scores, the team that did not score gets hammer in the next end. The team with hammer will usually try to convert (maximizing their score) or blank (saving their advantage for a better opportunity later), and the team without hammer will usually try to steal or force.</p>'
    # Closing tag
    html += '</details>'
    return html

def database():
    # Header 
    html = '<details><summary>Database Details</summary>'
    # Main text 
    html += '<p><a href="https://curlingzone.com">CurlingZone</a> maintains a database of the line scores from matches in most major events. Since the website does not allow API access, I used webscraping to construct my own SQL database of the line scores (scores in each end) of over 170,000 matches, along with basic event and team information. The analysis below is based on that database.</p>'
    html += '<p>The database contains four tables:</p>'
    html += '''<ol>
   <li>Matches: This is the main table that stores information about each match, including when it happened, who played, and the line scores.</li>
   <li>Events: This table includes names and dates of each curling event. Events vary in size, but most include ~10-100 matches.</li>
   <li>Teams: This table includes the world ranking points for mens and womens teams for each season from 2011-2024, as well as whether the team is a mens or womens team. (Curling also has formats like mixed doubles, wheelchair, junior men/women, etc., which are not currently included in this table.)</li>
   <li>Updates: This table lists when the update_database script has been run, which lets that script only update matches in events that happened since the last update.</li>
 </ol>'''
    html += '<p>The detailed structure of each table is listed below:</p>' 
    html += ''' <table>
    <tr>
        <th>Column</th>
        <th>Description</th>
    </tr>
    <tr><th colspan="2">Matches</th></tr>
    <tr>
        <td>EID</td>
        <td>ID number of event that the match was part of (foreign key for events)</td>
    </tr>
    <tr>
        <td>Draw</td>
        <td>Time slot (draw) of the match within the event</td>
    </tr>
    <tr>
        <td>Team1</td>
        <td>Name of first team playing in the match (foreign key for teams)</td>
    </tr>
    <tr>
        <td>Team2</td>
        <td>Name of second team playing in the match (foreign key for teams)</td>
    </tr>
    <tr>
        <td>Final1</td>
        <td>Final score of team 1</td>
    </tr>
    <tr>
        <td>Final2</td>
        <td>Final score of team 2</td>
    </tr>
    <tr>
        <td>Ham1</td>
        <td>Indicates which team had hammer in End 1 to start the game. 1 for Team 1, -1 for Team 2, Null for unknown.</td>
    </tr>
    <tr>
        <td>End1</td>
        <td>Score in End 1. Positive means Team 1 scored, negative means Team 2 scored, zero means neither team scored, X or Null means the game was over or the score is unknown.</td>
    </tr>
    <tr>
        <td>End2, End3, ...</td>
        <td>Columns for Ends 1-12 are included, analogous to End1.</td>
    </tr>
    <tr><th colspan="2">Events</th></tr>
    <tr>
        <td>EID</td>
        <td>ID number of the event</td>
    </tr>
    <tr>
        <td>Name</td>
        <td>Name of the event, in words</td>
    </tr>
    <tr>
        <td>Date</td>
        <td>Start date of the event. Events usually last 1-12 days.</td>
    </tr>
    <tr>
        <td>Type</td>
        <td>Identifies the events as mens, womens, etc.</td>
    </tr>
    <tr><th colspan="2">Teams</th></tr>
    <tr>
        <td>Name</td>
        <td>Name of the team, usually the name of the team's skip (captain).</td>
    </tr>
    <tr>
        <td>Type</td>
        <td>Identifies the team as mens, womens, etc.</td>
    </tr>
    <tr>
        <td>Location</td>
        <td>Country, state, or province where the team was most recently based.</td>
    </tr>
    <tr>
        <td>World2011</td>
        <td>World ranking points the team earned in the 2010-2011 season.</td>
    </tr>
    <tr>
        <td>World2012, World 2013, ...</td>
        <td>Same as above, for seasons through 2023-2024.</td>
    </tr>
    <tr><th colspan="2">Updates</th></tr>
    <tr>
        <td>date</td>
        <td>Date when the update_database script was run.</td>
    </tr>
    </table> '''
    html += '<p>Because CurlingZone has become more popular over time, 94% of the matches in my webscraped database happened since the 2010-2011 season. In my analyses, I chose to focus mainly on data aggregated from the 2010-2011 season to the present. The rules and strategy in curling have undergone some minor changes since 2010, but the changes have generally not dramatically changed the balance of the game.</p>'
    html += '<p>As a webscraped database, the data is naturally messy due to data entry errors, inconsistencies in formatting from year to year, etc. I chose to leave the raw webscraped data in the database and perform cleaning before each analysis run, rather than permanently altering the table to only include cleaned data. When running the analysis, I temporarily remove matches with the following errors:</p>'
    html += '''<ul>
   <li>No final score or line score is available (~2900 matches).</li>
   <li>A final score is available, but no line score is available (~1700 matches).</li>
   <li>Scores are only reported in one or two ends (~1400 matches). While it is possible for one team to concede early in a match, visual inspection suggests that the majority of these matches had the end scores entered as placeholders, not as the actual scores of the first one or two ends.</li>
   <li>The final score is a tie (~150 matches). In most events, the match continues until a tie is broken, so these are most likely data entry errors.</li>
   <li>Scores of > 8 in a single end (1 match). This is impossible in curling because a team scores one point per rock, and each team only has 8 rocks.</li>
   <li>One team’s final score does not match the sum of their scores for all ends (~760 matches).</li>
   <li>The final score is a tie (~150 matches). In most events, the match continues until a tie is broken, so these are most likely data entry errors.</li>
    </ul>'''
    html += '<p>This removes ~6200 matches from the databases, out of >178,000. That means the rate of incomplete or obviously incorrect data is ~3.5%, with the majority of the matches that are removed being because of incomplete data.</p>'
    html += '<p>Much of the analysis below categorizes the matches by mens/womens, match length, and team rankings. Since none of those features are stored permanently in matches, they need to be computed by joining with other tables. For example, finding matches between two top-25 womens teams requires one join with the events table to find the season for each match, one join with teams to find the gender and season rank of Team 1, and a second join with teams to find the gender and season rank of Team 2. This is possible to do, but in practice collecting the results over 14 seasons for ~30 combinations of gender, match length, and rank is slow to run.</p>'
    html += '<p>To speed up the calculations, I chose to use joins to pre-compute the features needed to categorize the matches and temporarily add those features to the matches table. To minimize the permanent size of the database, I chose not to store those features permanently. The pre-computed features are:</p>'
    html += '''<ul>
   <li>Ham2, Ham3, ... Ham12. Identity of the tean that has hammer in each end (1 for Team 1, -1 for Team 2), similar to Ham1.</li>
   <li>Ends. Scheduled length of the match, in ends. Since curling has a culture of teams conceding early if they have no chance of winning, just using the number of ends played will not give accurate results.</li>
   <li>Season. Season when the match was played. 2011 means the 2010-2011 season, etc.</li>
   <li>Category. Indicates whether the match was mens, womens, or other/unknown.</li>
   <li>Rank1, Rank2. Ranks of Team 1 and Team 2 in their category during the season when the match occurred.</li>
    </ul>'''
    # Closing tag
    html += '</details>'
    return html

def matches_month(c, season, combos, js=False):
    # Header 
    html = '<details><summary>Timing of Matches</summary>'
    # Main text 
    html += '<p>The graph below shows the number of curling matches that took place each month, and can be filtered by mens/womens, match length in ends, and ranks of the two teams.</p>'
    html += graphs.matches_month(c, season, combos, js)
    html += '<p>This graph shows the following trends:</p>'
    html += '''<ul>
   <li>Curling is mainly a fall/winter sport, with most matches taking place between September and February. Many of the late-season events (February-April) are national and world championships.</li>
   <li>The number of curling matches dropped sharply in the 2020-2021 season because of COVID, and has mostly but not fully recovered to its pre-COVID levels since then.</li>
   <li>Most fall matches are 8 ends. Starting around December/January, a higher proportion of events are provincial/national/world championships, which are typically 10 ends.</li>
   <li>Higher-ranked teams are more likely to play late-season matches (February-April).</li>
 </ul>'''
    # Closing tag
    html += '</details>'
    return html

def final_scores(c, season, combos, js=False):
   # Header 
   html = '<details><summary>Distribution of Final Scores</summary>'
   # Main text 
   html += '<p>The graph below shows the number of curling matches with a given final score since the start of the 2010-2011 season, and can be filtered by mens/womens, match length in ends, and ranks of the two teams.</p>'
   html += graphs.final_scores(c, season, combos, js)
   html += '<p>This graph shows the following trends:</p>'
   html += '''<ul>
  <li>Across the full database, the most common final scores are 6-5 for 8-end matches and 7-6 for 10-end matches.</li>
  <li>Low-scoring matches (fewer than 5 total points scored) are very rare. If one team has a very low-scoring game (0-2 points), it usually means the other team has a fairly high-scoring game (5-10 points). Even though blank ends are not extremely rare, it is rare for teams to blank most of the ends in a match.</li>
  <li>It is fairly rare for a team to score more than 9 points in an 8-end game, or more than 11 points in a 10-end game. There are several reasons for this:
      <ul>
        <li>Scores of more than 2-3 points in one end are fairly rare, so it is rare for the total number of points scored to be much more than twice the number of ends.</li>
        <li>Win margin is not used in any common curling statistics or ranking, so teams that are far ahead often play conservatively, aiming to maintain their margin but not take risks to increase it.</li>
        <li>Teams usually concede if they are so far behind that they do not have a realistic chance of winning, so a lopsided match will often end early before the winning team has a chance to build up a higher score.</li>
      </ul>
      </li>
  <li>If the ranges of ranks for Team 1 and Team 2 are the same, the score distribution is of course symmetric across the diagonal. </li>
  <li>If Team 1 outranks Team 2, then Team 1 has a high chance of winning, as expected. The bigger the difference in rank, the more likely the match will have a very lopsided final score.</li>
</ul>'''
   # Closing tag
   html += '</details>'
   return html

def end_scores(c, season, combos, js=False):
   # Header 
   html = '<details><summary>Distribution of Scores in Each End</summary>'
   # Main text 
   html += '<p>The graph below shows the distribution of scores in each end of a curling match, and can be filtered by mens/womens, match length in ends, and ranks of the two teams. Positive scores mean that the team with hammer scored, and negative scores mean that the team without hammer scored (stole).</p>'
   html += graphs.end_scores(c, season, combos, js)
   html += '<p>This graph shows the following trends:</p>'
   html += '''<ul>
  <li>The left graph shows the distribution of scores if Team 1 has hammer in a given end, and the right graph shows the distribution if Team 2 has hammer. The distributions are only different if Team 1 and Team 2 have different ranks.</li>
  <li>In the later ends, the probabilities of scores do not sum to 100%. This is because some in some matches, one team concedes early. If matches that ended early were included, the probabilities would sum to 100%</li>
  <li>If a match is tied after the planned number of ends, it goes to an extra end as a tiebreaker (End 9 of an 8-end game, or End 11 of a 10-end game).</li>
  <li>In general, the most common outcome of an end is a score of 1 for the team with hammer. A score of 2 or a steal of 1 (shown as -1) are also fairly common.</li>
  <li>Blank ends (score = 0) are relatively common early in the match, but become less common as the match progresses. Blank ends are slightly more common in 10-end matches than in 8-end matches, especially in the first couple ends.</li>
  <li>When playing against similar-ranked teams, top-tier teams are slightly more likely to blank or convert (score 2+) and less likely to steal.</li>
  <li>When two teams of different ranks play each other, the higher-ranked team is more likely to convert, less likely to be forced (score 1 when they have hammer), and less likely to give up a steal when they have hammer. The higher-ranked team is also more likely to have hammer in the final scheduled end of the match, helping their odds of winning a close match.</li>
</ul>'''
   # Closing tag
   html += '</details>'
   return html

def win_probability(c, season, combos, js=False, win_probs=None):
    # Header 
    html = '<details><summary>Testing the Common Wisdom: Having hammer in even ends is a big advantage</summary>'
    # Main text 
    html += '<p>In high-level curling, most players and commentators think that having the advantage of hammer (last rock) in even ends is a big advantage late in the game. The team with hammer has more control over the outcome of the end and is much more likely to score. </p>'
    html += '<p>For example, a team that is down 2 points with hammer in end 8 of 10 could score 2 in end 8 (tieing the score), force their opponent to score 1 point in end 9 (going down by one), and then score 2 in end 10 to win by 1 point. In contrast, a team that is down by even 1 point without hammer in end 8 of 10 has a trickier route to winning the game: they need to either score 3 points when they have hammer or steal at least 1 point to have a chance of winning.</p>'
    html += '<p>The graph below shows the probability of Team 1 winning a curling match, and can be filtered by mens/womens, match length in ends, and ranks of the two teams. Positive margins mean that Team 1 is ahead, and negative margins means that Team 1 is behind.</p>'
    html += graphs.win_probability(c, season, combos, js, win_probs)
    html += '<p>This graph shows the following trends:</p>'
    html += '''<ul>
   <li>If the range of ranks is the same for Team 1 and Team 2, the left and right graphs essentially mirror each other (because both graphs use Team 1's points margin on the x axis), with their color scales reversed (because the color scale shows Team 1's chance of winning in both graphs).</li>
   <li>Situations that are impossible or have not occurred in any actual games in the database are shown as white boxes. For example, during End 1, no one has had an opportunity to score, so the only possible points margin is 0. The team that scores in End 1 loses hammer in End 2, so a positive margin (Team 1 scored) must mean that Team 2 has hammer and vice versa. An extra end (End 9 in an 8-end match, or End 11 in a 10-end match) only happens if the match is tied at the end of regular play.</li>
   <li>Some of the graphs, especially the ones sorted by team rank, have very few matches within certain ranges of margins - especially for margins where the lower-ranked team is ahead. The small sample size creates a lot of noise in the win probabilities, so the exact percentages should not be over-interpreted. You can hover the mouse over a box in the graph to see how many matches in the database fit that situation.</li>
   <li>There are fewer 10-end matches than 8-end matches in the database, and fewer women's matches than men's matches. I will focus mostly on 8-end men's games, since the larger number means that subset is the least noisy.</li>
   <li>If Team 1 and Team 2 have similar ranks:
       <ul><li>As expected, the team that is currently ahead on the scoreboard has a >50% chance of winning, and if the game is tied, the team with hammer has a >50% chance of winning.</li>
       <li>Even relatively small deficits on the scoreboard are hard to overcome in curling: a team up by 1 or more points with hammer has >70% chance of winning in almost all scenarios, and a team down by 2 or more points with hammer has a <30% chance of winning. This is not surprising because scores of >2 points in an end are fairly rare.</li>
       <li>For a given score margin, the fewer ends remain, the more likely it is that the team currently ahead on the scoreboard will go on to win the game in most cases (the colors generally get darker as you go up in the plot toward higher current end numbers).</li>
   </ul>
   <li>If Team 1 outranks Team 2:
       <ul><li>The higher-ranked team has a higher chance of winning even if they are not currently ahead. For example, for men's 8-end games where Team 1 is ranked 1-25 and Team 2 is ranked 101-500, Team 1 has a >50% chance of winning if they are down 1 point with hammer, or tied without hammer in End 7 or earlier.</li>
       <li>This suggests that even if a higher-ranked team makes a mistake early in a match to put themselves at a disadvantage, they are more likely to outplay their opponent later in the match and regain the advantage.</li>
   </ul>
   <li>Does the common wisdom match the data?
       <ul><li>If having hammer in even ends is actually a big advantage, I would expect the likelihood of Team 1 winning when they have hammer at a given score margin to be noticeably higher in End 6 of an 8-end match (of End 8 of a 10-end match) than in the surrounding ends.</li>
       <li>For teams of all ranks, that pattern is <b>not</b> clearly present: the probability of winning based on a given scenario in End 6 is not significantly different than during the nearby ends. This means that <b>the common wisdom is not quite accurate.</b></li>
       <li>Instead, for a team that is down 1-2 points with hammer, their odds of winning are a few percentage points lower in End 7 than in End 6 or 8 of an 8-end match. Instead of having hammer in even ends being an advantage, <b>having hammer in the next-to-last end is a small disadvantage in close matches.</b> Aiming to have hammer in even ends helps teams avoid this disadvantage, instead of giving them a direct advantage.</li>
       <li>Looking only at the top-ranked teams, there are hints that <b>the common wisdom may be more accurate for the best teams.</b> However, the data is sparse enough that these hints may just be noise.</li>
   </ul> 
 </ul>'''
    # Closing tag
    html += '</details>'
    return html

def template(c, season, combos, js=False):
   # Header 
   html = '<details><summary>Title</summary>'
   # Main text 
   html += '<p></p>'
   # Closing tag
   html += '</details>'
   return html
