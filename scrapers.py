#!/usr/bin/python

from bs4 import BeautifulSoup
import requests
import time
import re



def scrape_cinemark(theater):
	url = 'http://www.cinemark-peru.com/cines/'+theater
	r = requests.get(url).text
	page = BeautifulSoup(r)
	representation = {theater: {}}
	#find movie blocks
	blocks = page.find_all('div', {'class':"item-block-details3"})
	#iterate through movies
	for thing in blocks:
		#find titles
		titleblock = thing.find_all('a', {'class':"red"})
		#iterate through titles
		for title in titleblock:
			righttitle = title.contents[0]
			representation[theater][righttitle] = {}

			#print(title.contents[0])
		#find info blocks
		sblock = thing.find_all('div', {'class':"tabbody"})
		#iterate through info blocks
		for record in sblock:
			#find versions
			flavor = record.find_all('span', {'class': "red"})
			#find times 
			times = record.find_all('li')
			#use type of versions to iterate through info
			numflav = len(flavor)
			for i in range(0,numflav):
				rightflavor = flavor[i].contents[0]
				representation[theater][righttitle][rightflavor] = {}			
				timestring = times[i].contents[0]

				#process string of times into individual times
				timelist = timestring.split('|')
				for t in timelist:
					tt = t.encode('utf8')
					time.strptime(tt, "  %I:%M %p   ")
				representation[theater][righttitle][rightflavor] = timelist

	return representation

def scrape_cineplanet(theater_code):
	url = 'http://www.cineplanet.com.pe/nuestroscines.php?complejo='+theater_code
	r = requests.get(url).decode('latin-1').text
	page = BeautifulSoup(r, from_encoding='latin-1')
	theatername = page.find_all('td', {'class', "titulo_pelicula2"})[0].contents[0]
	#site gives garbage so split at first word then add back in
	cleanname = theatername.split('CinePlanet')[-1] + 'CinePlanet'
	#dictionary that will hold theater info
	rep = {cleanname: {}}
	records = page.find_all('a', {'class', 'titulo_pelicula5'})
	for rec in records:
		item = rec.contents[0]
		cleaneditem = item.lstrip().rstrip()
		#print(cleaneditem)
		#isolating movie names from times
		if cleaneditem[0] != '(':
			moviename = cleaneditem.encode('utf8')
			rep[cleanname][moviename] = {}
		else: 
			rep[cleanname][moviename] = cleaneditem



	#return rep


#function for scraping cinepolis. all theaters on same page
def scrape_cinepolis():
	url = 'http://www.cinepolis.com.pe/_CARTELERA/cartelera.aspx?ic=100'
	r = requests.get(url).text
	page = BeautifulSoup(r)

	bigcontainer = page.find('span', {'class', 'TitulosBlanco'}).find_parent('div')
	#print(bigcontainer)
	containers = bigcontainer.findChildren('table')
	print(len(containers))
	payload = {}
	for container in containers:
		
		istheatername = container.find('span', {'class', 'TitulosBlanco'})
		ismoviename = container.find('a', {'class', 'peliculaCartelera'})
		ismovietime = container.find('span', {'class', 'horariosCarteleraUnderline'})
		if istheatername:
			theater = istheatername.contents[0]
			payload[theater] = {}
		elif ismoviename:
			movie = ismoviename.contents[0]
			#mov = movie.split(' Dig ', '4DX')[0]
			mov = re.split(' Dig | 4DX', movie)[0]
			try:
				flav = re.split(' Dig | 4DX', movie)[1]
				print(flav)
			except IndexError:
				print('indexerror '+flav)
				continue
			
			try:
				#payload[theater][mov] = {}
				payload[theater][mov][flav] = []
			except KeyError:
				payload[theater][mov] = {}
				payload[theater][mov][flav] = []

			#print(ismoviename.contents[0])
		elif ismovietime:
			time = ismovietime.contents[0]
			try:
				if time in payload[theater][mov][flav]:
					pass
				else:
					payload[theater][mov][flav].append(time)
			except KeyError:
				continue
			#print(ismovietime.contents)
		
	print(payload)
	#theaters = page.find_all('span', {'class', 'TitulosBlanco'})
	#for theater in theaters:
	#	holder = theater.find_parent('table')
	#	print(holder)
	#return theaters



