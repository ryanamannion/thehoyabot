"""
sitescraper.py

Ryan A. Mannion
twitter: @ryanamannion
github: ryanamannion

This script uses BeautifulSoup to scrape titles from the online archives of thehoya.com,
Georgetown University's student newspaper. 

The URLs for the archives are built in the following manner: http://www.thehoya.com/[year]/[page number] 

The script cycles through the pages and with the help of HTML picks out and writes the titles to a file.

"""

import os
import sys

import requests
from bs4 import BeautifulSoup

page_counts = {}

# page_counts[1998] = 26
# page_counts[1999] = 82
# page_counts[2000] = 101
# page_counts[2001] = 110
# page_counts[2002] = 112
# page_counts[2003] = 118
# page_counts[2004] = 125
# page_counts[2005] = 141
# page_counts[2006] = 146
# page_counts[2007] = 143
# page_counts[2008] = 144
# page_counts[2009] = 140
# page_counts[2010] = 164
# page_counts[2011] = 315
# page_counts[2012] = 190
# page_counts[2013] = 211
# page_counts[2014] = 212
# page_counts[2015] = 218
# page_counts[2016] = 189
# page_counts[2017] = 160
# page_counts[2018] = 131
page_counts[2019] = 83

file = open(os.path.join(sys.path[0], "hoyatitles.txt"), "w")

count = 0

for year, pages in page_counts.items():
    page_list = range(pages)
    counter = 0
    for page in page_list:

        url = 'http://www.thehoya.com/' + str(year) + '/page/' + str(page) + '/'

        source = requests.get(url).text  # read the html source text of page one, feed to BeautifulSoup
        start_soup = BeautifulSoup(source, 'html')

        for article in start_soup.find_all('div', class_='post-content'):       # skim the first page

            headline = article.h2.a.text

            file.write(headline+'\n')
            count += 1
        counter += 1
        print("Printed " + str(year) + " page number " + str(counter))

    print("Finished with " + str(year))
    print(str(count) + " articles total")

file.close()