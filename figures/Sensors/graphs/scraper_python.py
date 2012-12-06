import urllib
import urllib2
import string
import sys
from bs4 import BeautifulSoup

url='https://play.google.com/store/apps/details?id=com.music.psy'
page = urllib2.urlopen(url).read()
soup = BeautifulSoup(page)


for link in soup.find_all('a'):
	 	l=str(link.get('href'))
		if("category" in l):
    			print (str(link.contents)[2:-1])
			
