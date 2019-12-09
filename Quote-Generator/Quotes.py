#/usr/bin/env python2
#This is done in Python 2 and requires the beautiful soup library

from bs4 import BeautifulSoup
from urllib2 import urlopen
import re

quotes=[]
doc = open('q.txt', 'w')
how_many = 100

def main():
    while len(quotes) < how_many:
        soup = urlfetch() #fetching random page
        stuff = soup.findAll('a',{"href" : re.compile("view.php\?id\=\d+")}) #this gets the quotes      
        for link,tag in enumerate(stuff):
            quotes.append(str(tag.get_text()))#this converts the quotes into universal strings
        print len(quotes)
    doc.write(str(quotes))
    doc.close()
    print "Done!"     

def urlfetch():
    url = "http://epicquotes.org/?filter=random" #source of quotes
    response = urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup
 
main()
