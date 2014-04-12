from app import app
import pickle
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    dat = pickle.load( open('info.p','rb'))
    return render_template('bytheater.html', dat=dat)
