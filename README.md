# Curling sports analytics

This repository contains analytics for a database of match scores from the sport of curling, webscraped from <a href="https://www.curlingzone.com/">CurlingZone</a>. As of November 2023, the database contains line scores for > 170,000 matches.

## Quick Link to Analytics Results

<a href=https://htmlpreview.github.io/?https://github.com/rlmgieseking/curling-analytics/blob/main/analytics.html">Click here</a> to view the results of my analyses.

## Database

The SQLite database is stored in `utils/matches.db`. The database contains 4 tables:

1. events - Curling events, with names and start dates
2. matches - Curling match results, including the event ID, the teams who played, and scores from each end (segment) of the match.
3. teams - Team names, ranking points from each season (2011-2024), and category (men/women)
4. updates - List of when the database was updated

The script `update_database.py` checks when the database was last updated, looks for new events to add to the database, updates matches for all events since the last database, updates team ranking points for the current season, and adds the current date as the date of the latest update.

## Analytics

The script `create_analytics.py` uses a combination of SQL and pandas to generate analytics, printed to `analytics.html`. The latest version of the analytics is viewable <a href="https://htmlpreview.github.io/?https://github.com/rlmgieseking/curling-analytics/blob/main/analytics.html">here</a>. This document also includes a short summary of the basics of curling so you can understand the terms used in the analytics.

The analytics script first performs data cleaning, removing matches with invalid results from the data set. Also, to minimize the size of the database, columns that can be calculated from other data are not permanently stored. However, because finding matches where teams had certain ranks requires multiple joins (join matches with events to get the season when the match took place, then join with teams twice to get the ranking of team 1 and team 2 during that season), calculating that information on the fly for every query is possible to do but fairly time-consuming to run. Because the database is moderate in size, I chose to pre-compute the season when each match took place and the ranks of each team during data cleaning, but not permanently store those results.

The analytics script then uses SQL queries to extract the necessary data from the database for the graphs, creates interactive graphs using Plotly, and writes the results to an HTML file. I have included my observations from these graphs in the HTML output document.
