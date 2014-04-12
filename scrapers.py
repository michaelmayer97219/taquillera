#!/usr/bin/python

from bs4 import BeautifulSoup
import requests
import time
import re
import datetime



def scrape_cinemark(theater):
	url = 'http://www.cinemark-peru.com/cines/'+theater
	r = requests.get(url).text.encode('latin-1')
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
	r = requests.get(url).text.encode('latin-1')
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
	r = requests.get(url).text.encode('latin-1')
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
		
	return payload

def scrape_cinerama(cinemacode): #accepts 1-7 as character
	url = 'http://www.cinerama.com.pe/detalle-cine.php?fk='+cinemacode
	r = requests.get(url).text.encode('latin-1')
	page = BeautifulSoup(r)
	payload = {}
	day = datetime.datetime.now().weekday()
	theater = page.find('p',{'class', 'dtit'}).contents[0]
	payload[theater] = {}
	containers = page.find_all('div', {'class', 'programa-des'})
	for cont in containers:
		title = cont.find('p',{'class','ptit2'}).find('a').contents[0]
		payload[theater][title] = []
		times = cont.find_all('tr')
		for t in times:
			if t.find_all('span'):
				pass
			elif t.find_all('td')[day].contents[0] == u'\xa0':
				pass
			else:
				show = t.find_all('td')[day].contents
				payload[theater][title].append(show[0])

	return payload

def scrape_cinestar_or_movietime(chain,location):
	if chain == 'cinestar':
		url = 'http://www.cinestar.com.pe/multicines/cine/'+location
	elif chain == 'movietime':
		url = "http://www.movietime.com.pe/multicines/cine/"+location
	r = requests.get(url).text.encode('latin-1')
	page = BeautifulSoup(r)
	payload = {}
	theater = page.find('span', {'class','titley'}).contents[0]
	payload[theater] = {}
	theateradd = page.find('div', {'id','content-internas'}).find('p').contents[0]
	theaterphone = page.find('div', {'id','content-internas'}).find_all('p')[1].contents[0]
	payload[theater]['address'] = theateradd
	payload[theater]['phone'] = theaterphone
	payload[theater]['movies'] = {}
	flavors = {" (Doblada)": '(DOB)',
				" (Subtitulada)": "(SUB)",
				" 3D (Doblada)": "3D (DOB)",
				" 3D (Subtitulada)": "3D (SUB)",
				" (HD - Subtitulada)": "(SUB)",
				" (HD - Doblada)": "(DOB)"}
	container = page.find_all('div',{'class','programacion_'})[1]
	movies = container.find_all('a')
	for movie in movies:
		mtitle = movie.contents[0]

		times = movie.findParent('tr').find_all('td')[1].contents[0]

		for key in flavors:
			if key in mtitle:
				fixtitle = mtitle.split(key)[0]
				payload[theater]['movies'][fixtitle] = {}
				payload[theater]['movies'][fixtitle][flavors[key]] = times.split('/')

	return payload

def scrape_uvk(location):
	url = 'http://www.uvkmulticines.com/multicines/cine/'+location
	r = requests.get(url).text
	page = BeautifulSoup(r, from_encoding='UTF-8')
	
	payload = {}
	theateradd = page.find_all('p')[2].renderContents()
	theaterphone = page.find_all('p')[3].contents[0].renderContents('latin-1')
	flavors = {" (Doblada)": '(DOB)',
				" (Subtitulada)": "(SUB)",
				" 3D (Doblada)": "3D (DOB)",
				" 3D (Subtitulada)": "3D (SUB)",
				" (HD - Subtitulada)": "(SUB)",
				" (HD - Doblada)": "(DOB)"}
	container = page.find('div', {'class','highslide-body'})
	theater = container.find('h3').contents[0].split('-')[0]
	payload[theater] = {}
	payload[theater]['address'] = theateradd
	payload[theater]['phone'] = theaterphone
	payload[theater]['movies'] = {}
	movies = container.find_all('a')
	for movie in movies:
		mtitle = movie.contents[0].replace('Estreno - ','')
		times = movie.findParent('tr').find_all('td')[1].contents[0].split('/')
		possibletitle = []
		for key in flavors:
			if key in mtitle:
				fixtitle = mtitle.split(key)[0]
				possibletitle.append([fixtitle,flavors[key]])
		if len(possibletitle) == 0:
			possibletitle.append([mtitle,''])
		for candidate in possibletitle:
			if len(possibletitle) > 1:
				possibletitle = [possibletitle[len(possibletitle)-1]]
		try:
			payload[theater]['movies'][possibletitle[0][0]][possibletitle[0][1]] = times
		except KeyError:
			payload[theater]['movies'][possibletitle[0][0]] = {}
			payload[theater]['movies'][possibletitle[0][0]][possibletitle[0][1]] = times
	#return payload
	return payload



