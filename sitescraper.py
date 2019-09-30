from bs4 import BeautifulSoup
import requests
from string import digits

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

file = open("hoyatitles.txt","w")

count = 0

for year, pages in page_counts.items():
    page_list = range(pages)
    counter = 0
    for page in page_list:

        url = 'http://www.thehoya.com/' + str(year) + '/page/' + str(page) + '/'

        source = requests.get(url).text  # read the html source text of page one, feed to BeautifulSoup
        start_soup = BeautifulSoup(source, 'lxml')

        for article in start_soup.find_all('div', class_='post-content'):       # skim the first page

            headline = article.h2.a.text

            file.write(headline+'\n')
            count += 1
        counter += 1
        print("Printed " + str(year) + " page number " + str(counter))

    print("Finished with " + str(year))
    print(str(count) + " articles total")

file.close()