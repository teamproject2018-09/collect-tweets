################################################################################
collect-tweets
################################################################################

Erik Tjong Kim Sang e.tjongkimsang(a)esciencecenter.nl

This directory contains scripts for collecting and processing tweets for the social media analysis of the Netherlands eScience Center of the team sprint of September 2018. The scripts can be found in the subdirectory collect-tweets.

The collect tweets script should be called as follows:

::
  collect-tweets.py [-u|-s] user-name

See the script headings for more information

The script outputs a json file which can be converted to csv like this:

::
  process-json.py infile1.json [infile2.json ...] > outfile.csv

Alternatively, tweets found on the Twitter website can be stored in html files with your webbrowser and the files can then be converted to csv in this way:

::
  process-html.py infile1.html [infile2.html ...] > outfile.csv

Nex, the csv files can be visualized with the notebook in the _visualization section: https://github.com/teamproject2018-09/visualization
