
# -*- coding: utf-8 -*-
from app import app
import pickle
from flask import render_template
from utils import convert_strings_to_unicode



@app.route('/')
@app.route('/index')
def index():
	dat = pickle.load( open('info.p','rb'))
	#convert_strings_to_unicode(dat)
	return render_template('bytheater.html', dat=dat)
