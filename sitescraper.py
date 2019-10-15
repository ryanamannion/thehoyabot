"""
sitescraper.py

This script uses BeautifulSoup to scrape titles from the online archives of thehoya.com,
Georgetown University's student newspaper. 

The URLs for the archives are built in the following manner: http://www.thehoya.com/[year]/[page number] 

The script cycles through the pages and with the help of HTML picks out and writes the titles to a file.

Ryan A. Mannion
ram321@georgetown.edu
twitter @ryanamannion
ryanamannion.com

"""

import os
import sys
import argparse

import requests
from bs4 import BeautifulSoup


parser = argparse.ArgumentParser()
parser.add_argument('--begin', action="store", dest="begin", default="1998", help="year to begin scraping at")
parser.add_argument('--end', action="store", dest="end", default="2019", help="year to end scraping at")
parser.add_argument('--start', action="store", dest="start", default="1", help="page number to start scraping at")

options = parser.parse_args()
begin = int(options.begin)
end = int(options.end)
start = int(options.start)

page_counts = {}

page_counts[1998] = 26
page_counts[1999] = 82
page_counts[2000] = 101
page_counts[2001] = 110
page_counts[2002] = 112
page_counts[2003] = 118
page_counts[2004] = 125
page_counts[2005] = 141
page_counts[2006] = 146
page_counts[2007] = 143
page_counts[2008] = 144
page_counts[2009] = 140
page_counts[2010] = 164
page_counts[2011] = 315
page_counts[2012] = 190
page_counts[2013] = 211
page_counts[2014] = 212
page_counts[2015] = 218
page_counts[2016] = 189
page_counts[2017] = 160
page_counts[2018] = 131
page_counts[2019] = 92

file = open(os.path.join(sys.path[0], "hoyatitlestest.txt"), "a+")

count = 0       # establish count for titles per page
counter = 0     # establish counter for page numbers

real_end = end + 1

years = list(range(begin, real_end))    # create list of specified years

for year in years:      # loop through specified years
    end_page = page_counts.get(year) + 1
    pages = list(range(start, end_page))    # create range of pages

    for page in pages:      # loop through specified pages

        url = 'http://www.thehoya.com/' + str(year) + '/page/' + str(page) + '/'

        source = requests.get(url).text  # read the html source text of page one, feed to BeautifulSoup
        start_soup = BeautifulSoup(source, features="html.parser")

        for article in start_soup.find_all('div', class_='post-content'):       # skim the first page

            headline = article.h2.a.text

            file.write(headline+'\n')
            count += 1
        counter += 1
        print("Printed " + str(year) + " page number " + str(counter))

    print("Finished with " + str(year))
    print(str(count) + " articles total")

file.close()
