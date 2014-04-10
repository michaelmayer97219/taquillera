#!/usr/bin/python


from locations import *
from scrapers import *
import json
import time
#start = time.clock()

def nicePrint(data):
	print(json.dumps((data), indent=3))

#for loc in cinemark:
	#scrape_cinemark(loc)

#print(scrape_cinemark('san-miguel'))

#print(scrape_cineplanet('02'))

#print(scrape_cinepolis())

"""for loc in cinerama:
	nicePrint(scrape_cinerama(loc))

for loc in cinestar:
	nicePrint(scrape_cinestar(loc))"""

nicePrint(scrape_cinestar('Metro-San-Juan'))

#end = time.clock()
#print(end - start)