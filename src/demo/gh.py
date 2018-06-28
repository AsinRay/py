from flask import Flask
import re
import MySQLdb
from bs4 import BeautifulSoup, Comment
import requests.packages.urllib3.util.ssl_
from flask_apscheduler import APScheduler

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'

# TODO try this for test! '@_@"
mapping = {"m12": {"url": "", "f": "update_db_m12"},
           "m6": {"url": "months_6.html", "f": "update_db_m6"},
           "m3": {"url": "months_3.html", "f": "update_db_m3"}}
div_map = {}
data_result = {}
m12_div = {}

app = Flask(__name__)


@app.route("/")
@app.route('/<name>')
def github_section(name='Hey guys, the server is ready, please query the coin! e.g. /bitcoin '):
    if mapping.has_key(name):
        return str(mapping.get(name))
    else:
        return name


if __name__ == '__main__':
    app.run(debug=True)

