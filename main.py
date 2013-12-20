# -*- coding: utf-8 -*-

""" main.py is the top level script.

Return "Hello World" at the root URL.
"""

import os
import sys

# sys.path includes 'server/lib' due to appengine_config.py
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__.split('.')[0])

from utils import Gae

gae = Gae(app)





@app.before_request
def before_request():
	app.logger.info('before_request %s' % request.url)
	app.logger.info(gae.config)
	app.logger.info('end of before_request')
   	


@app.after_request
def after_request(resp):
   	app.logger.info('after_request')
   	return resp

@app.teardown_request
def teardown_request(e=None):
	app.logger.info('teardown_request')

from config import Config


@app.route('/')
@app.route('/<name>')
def hello(name=None):
	""" Return hello template at application root URL."""
	app.logger.info(gae.config)
	return render_template('hello.html', name=name)


@app.route('/setup')
def setup():
	""" Setup default config - TEST """
	config = Config(name='default', options={'url':'http://xxx'})
	config.put()
	return render_template('ok.html', message='default config created.')
