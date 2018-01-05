# -*- coding: utf-8 -*-
# import libraries
import urllib2
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import pandas as pd

# specify the url
months = ['January_2018','February_2018','March_2018','April_2018','May_2018','June_2018','July_2018','August_2018','September_2018','October_2018','November_2018','December_2018']
urls = []
for i in months:
    urls.append('http://ports.cruisett.com/schedule/United_States_Of_America/534-Port_Canaveral_Florida/'+i+'/')

# query the website and return the html to the variable ‘page’
all_links = []
for pg in urls:
    page = urllib2.urlopen(pg)

# parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(page, 'html.parser')

    rows = soup.find_all('a')

    for html in rows:
        try:
            if html.find_all('a') is not None:
                x = html['title']
                all_links.append(x)
        except KeyError:
            pass

# query saved links and get cruises and dates from link title
cruise = []
dates = []

for a in all_links:
    b = a.rsplit(' to',1)[0]
    c = a.rsplit(' to',1)[1]

    #arrival date
    d = b.rsplit(' from ')[1]
    e = d[:-6].strip()

    #depart date
    f = c[:-7].strip()

    g = b.replace(' is in the port ', ' ')
    h = g[:-6]

    #cruise ship name
    i = h.rsplit(' from ',1)[0]

    cruise.append(i)
    dates.append(e)

    #if arrival is not equal to depart, add depart date to list
    if e != f:
        cruise.append(i)
        dates.append(f)

#add Royal Caribbean and remove Of The Seas from all RC cruise ships 
for x in range(len(cruise)):
    if "Of The Seas" in cruise[x]:
        y = cruise[x].rsplit(' Of',1)[0]
        z = 'Royal Caribbean ' + y
        cruise[x] = z
    if 'of the Seas' in cruise[x]:
        y = cruise[x].rsplit(' of',1)[0]
        z = 'Royal Caribbean ' + y
        cruise[x] = z

#format date
for l in range(len(dates)):
    m = dates[l].replace('-', ' ')
    n = m + ' 2018'
    o = datetime.strptime(n, '%d %b %Y').date()
    dates[l] = o

#generate csv
df = pd.DataFrame({'cruise': cruise, 'dates': dates})
df.to_csv('cruise_dates_t.csv')
