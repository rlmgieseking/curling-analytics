# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 15:07:18 2023

@author: gieseking
"""

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
    # Header for curling basics
    #html = '<button type="button" class="collapsible">Basics of Curling (click to expand)</button><div class="content">'
    html = '<details><summary>Basics of Curling</summary>'
    # Main text for curling basics
    html += '<p>If you are unfamiliar with curling, the World Curling Federation has a nice 2-minute intro to the sport:</p>'
    html += '''<iframe width="420" height="315"
src="https://www.youtube.com/embed/IOk9SVzqHsk">
</iframe> '''
    html += '<p>In curling, two teams of four players take turns sliding rocks down a sheet of ice toward a target painted on the far end of the ice (called the <b>house</b> or <b>rings</b>), sweeping the ice in from of the rock to control its path. Each match has series of scoring opportunities called <b>ends</b> (similar to innings in baseball), typically 8 or 10 ends, and the team with the most points at the conclusion of the match wins. Unlike most sports, teams often concede early if they are too far behind to have a realistic chance of winning.</p>'
    html += '<p>In each end, the teams take turns sliding rocks until each team has delivered 8 rocks. The team that delivers the last rock (called <b>hammer</b>) has a big advantage in scoring, since they have the last chance to rearrange rocks to maximize their score.</p>'
    html += '<p>The score for the end is based on the placement of the rocks after all rocks are delivered. If no rocks are in the house (at least touching the edge of the outermost 12-foot circle), both teams score zero points. If at least one rock is touching the house, the team with the rock closest to the center of the rings scores one point for each of their rocks that is closer to the center than the nearest opponent rock. For example, if the closest rock to the center is red and the second closest is yellow, red scores 1 point. If the closest three rocks to the center are all yellow and the fourth closest is red, then yellow scores 3 points.</p>'
    html += '<a href="https://kccurling.com/startcurling/curlingexplained/terminology"><img src="https://kccurling.com/images/2018/05/13/scoring-examples.png" alt="Scoring in curling" width="598" height="215"></a>'
    html += '<p>The common types of scores for one end are:</p>'
    html += ''' <ul>
  <li><b>Convert:</b> Team with hammer scores 2 or more points</li>
  <li><b>Force:</b> Team with hammer scores exactly 1 point</li>
  <li><b>Blank:</b> Both teams score 0 points</li>
  <li><b>Steal:</b> Team without hammer scores 1 or more points (I use negative numbers for steals in my analysis)</li>
</ul>'''
    html += '<p>If the end is blanked, the team with hammer keeps it in the next end. If one team scores, the team that did not score gets hammer in the next end. The team with hammer will usually try to convert (maximizing their score) or blank (saving their advantage for a better opportunity later), and the team without hammer will usually try to steal or force.</p>'
    html += '</details>'
    return html

def database():
    # Header for curling basics
    html = '<details><summary>Database Details</summary>'
    # Main text for curling basics
    html += '<p><a href="https://curlingzone.com">CurlingZone</a> maintains a database of the line scores from matches in most major events. Since the website does not allow API access, I used webscraping to construct my own SQL database of the line scores (scores in each end) of over 170,000 matches, along with basic event and team information. The analysis below is based on that database.</p>'
    html += '</details>'
    return html


