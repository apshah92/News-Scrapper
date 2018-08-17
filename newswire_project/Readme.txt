
This project is tested on Windows and Linux System.

To Run this project make sure you have python 3 installed on your system and "python3" (without quotes) is recognized command in your terminal.

Enter following commands at terminal prompt in Linux or Windows cmd. On windows it can be executed in any IDE also by running solution.py

On windows you need to have Visual C++ 14.0 to before running this.

1. cd newswire_project/

2. ls

/* you should see following contents */

  -newswire_project
  -Readme.txt
  -runscripts.bat
  -scrapy.cfg
  -solution.py

3. python3 solution.py  

all the required scripts will be installed first.

after a while you will be prompted to provide a date in YYYY-MM-DD format. 
This will be the starting date to fetch news. End date is by default today's date. solution will analyze all news between these dates

If no date is provided then date prior to 7 days is take by default. 


4. At the end of execution you should see 3 tables of top 10 trends by locations, categories and tags .
