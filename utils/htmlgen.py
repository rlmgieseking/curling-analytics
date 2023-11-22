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
    ul {font-family: verdana, arial, sans-serif;}
    div {font-family: verdana, arial, sans-serif;}
    summary {font-family: verdana, arial, sans-serif; font-size: 1.5em; font-weight: bolder}
    iframe {text-align: center;}
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
    html += '<p>Because CurlingZone has become more popular over time, 94% of the matches in my webscraped database happened since the 2010-2011 season. In my analyses, I chose to focus mainly on data aggregated from the 2010-2011 season to the present. The rules and strategy in curling have undergone some minor changes since 2010, but the changes have generally not dramatically changed the balance of the game.</p>'
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

def template():
   # Header 
   html = '<details><summary>Title</summary>'
   # Main text 
   html += '<p></p>'
   # Closing tag
   html += '</details>'
   return html
