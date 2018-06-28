import re
import json
from functools import wraps

from flask import Flask, jsonify, make_response
import logging
logging.basicConfig()


app = Flask(__name__)

# TODO try this for test! '@_@"

mapping = {"m12": {"url": "", "f": "update_db_m12"},
           "m6": {"url": "months_6.html", "f": "update_db_m6"},
           "m3": {"url": "months_3.html", "f": "update_db_m3"}}
data_result = {}
m12_div = {}
m12_soup = {}


@app.route("/")
@app.route('/<name>')
def github_section(name='Hey guys, the server is ready, please query the coin! e.g. /bitcoin '):
    rtn = name
    if name.lower() == "stub":
        f = open("/home/boot/Downloads/5690501.json")
        rtn = f.read()
    resp = make_response(jsonify(rtn))
    resp.headers['server'] = 'sffe'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/stub')
def stub_section():
    f = open("/home/boot/Downloads/5690501.json")
    rtn = f.read()
    resp = app.response_class(
        response=json.dumps(rtn),
        status=200,
        mimetype='application/json'
    )
    resp = make_response(jsonify(rtn))
    resp.headers['server'] = 'sffe'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/summary')
def summary():
    data = {"k": "v", "x": "y"}
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst
    return wrapper_fun


@app.route('/hosts/')
@allow_cross_domain
def domains():
    pass


if __name__ == '__main__':
    #  app.config.from_object('config')
    app.run(host='0.0.0.0', debug=True)
