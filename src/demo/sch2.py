from flask import Flask
import re
import MySQLdb
from bs4 import BeautifulSoup, Comment
import requests.packages.urllib3.util.ssl_
from flask_apscheduler import APScheduler

#Schduler config
JOBS = [
    {
        'id': 'createschuler_job',
        'func': 'module:func',
        'args': None,
        'trigger': 'interval',
        'seconds': 5*60
    }
]
scheduler = APScheduler()

app = Flask(__name__)

app.config.from_object('config')

scheduler.init_app(app)

#trigger schduler
scheduler.start()


app.run(debug=True)