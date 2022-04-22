# imdbdownloader.py
This program allows you to download the information of the movies in IMDb into the database.

# imdb.db
If you don't want to wait, you can use the ready database.

# Builth With
- Python 3.10 
- requests
- from bs4 import BeautifulSoup
- sqlite3
- datetime
- concurrent.futures

  if not exists this modules you have to install modules,
- pip3 install requests
- pip3 install beautifulsoup4
# Help Me
This program can download all movie data from IMDb at the same time (depends on the number of cores in the processor) \
but cannot add it to the database at the same time as it gives a 'database locked' error.This causes it to run longer. 
# Contact Me
- suakbenli@gmail.com
