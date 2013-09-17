Careermap
=========

Goal: For any given astronomer, track their location as a function of time via their publication record.

Long term goal: do this for a large # of astronomers and find out the typical time spent at a given location

Tools
-----
`scrape_cities`: Get lat/lon for a given city name from wikipedia or other database

`ads_name_query`: Get a dict of {year: affiliation} for a given author name.  Examples:
```
dan = get_author_locations('Foreman-Mackey')
adam = get_author_locations('Ginsburg, A')
```
