#!/usr/bin/python
# -*- coding: utf-8 -*-

from locations import *
from scrapers import *
import json
import time
import pickle
import os
import sys
#start = time.clock()

stash = {}

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

for loc in UVK:
	stash = dict(stash.items() + scrape_uvk(loc).items())


sys.setrecursionlimit(10000)
pickle.dump(stash, open('info.p', 'wb'))