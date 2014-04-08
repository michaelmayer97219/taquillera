#!/usr/bin/python

from bs4 import BeautifulSoup
import requests


def cinemark(location):
	url = 'http://www.cinemark-peru.com/cines/'+location
	r = requests.get(url).text
	page = BeautifulSoup(r)
	blocks = page.find_all('div', {'class':"item-block-details3"})
	for thing in blocks:
		titleblock = thing.find_all('a', {'class':"red"})
		for title in titleblock:
			print(title.contents[0])
		sblock = thing.find_all('div', {'class':"tabbody"})
		for record in sblock:
			flavor = record.find_all('span', {'class': "red"})
			times = record.find_all('li')
			numflav = len(flavor)
			numtimes = len(times)
			
			for i in range(0,numflav):
				print(flavor[i].contents[0])
				print(times[i].contents[0])
			

			"""for kind in flavor:
													print(kind.contents[0])
												print(len(flavor))
												times = record.find_all('li')
												for r in times:
													print(r.contents[0])"""

cinemark('jockey-plaza')