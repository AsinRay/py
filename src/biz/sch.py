import re
from functools import wraps
import MySQLdb
from bs4 import BeautifulSoup
import requests.packages.urllib3.util.ssl_
from flask_apscheduler import APScheduler
from flask import Flask, jsonify, make_response
import logging
logging.basicConfig()

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'

app = Flask(__name__)

scheduler = APScheduler()
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
    if m12_div.has_key(name):
        rtn = {'key': str(m12_div.get(name))}
        # print(json.dumps(rtn, sort_keys=True, indent=4, ensure_ascii=False))
        resp = make_response(jsonify(rtn))
        resp.headers['server'] = 'sffe'
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    else:
        return name


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


def gen_coin_charts(src):
    try:
        for tag in src.select("> a"):
            m12_div[tag['id']] = str(tag.nextSibling.nextSibling)
    except:
        print("error")


# get the data of the github summary
def get_data(key, url):
    req_url = "https://www.cryptomiso.com/" + url
    resp = requests.get(req_url)
    soup = BeautifulSoup(resp.content, "lxml")
    d = soup.select('#miso_barcharts h4.card-title')
    data_result[key] = d
    if key == "m12":
        m12_soup["cache"] = soup


def replace_non_ascii(s):
    rtn = ''
    for i in s:
        if ord(i) < 128:
            rtn = rtn + i
        else:
            rtn = rtn + '|'
    return rtn


def format_data(txt):
    rtn = replace_non_ascii(txt)
    rtn = rtn.replace('\t', '').replace('\n', ' ').replace('commits', 'c ').replace('commit', 'c ')
    rtn = rtn.replace('.', '').replace(',', '').replace('+', ' ').strip()
    spl = rtn.split('|')

    org = ''.join(re.findall(r"[a-zA-Z ]+", spl[0]))
    org = org.strip()

    bspl = spl[1].split()
    repo = bspl[0]
    commit = '0'
    contrib = '0'
    if len(bspl) > 0:
        commit = bspl[1]
    if len(bspl) > 3:
        contrib = bspl[3]
    data = {'org': org, 'repo': repo, 'commit': commit, 'contrib': contrib}
    return data


def get_sql_values(src):
    vals = ''
    for data in src:
        txt = data.text
        i = format_data(txt)
        val = "('" + i["org"] + "','" + i['repo'] + "'," + i['commit'] + "," + i['contrib'] + "),"
        vals = vals + val
    return vals[:-1]


def update_db_m3(data):
    sql = "insert into github_code_commit_summary(`org_name`,`repo_name`,`m3_commit`,`m3_contrib`) values "
    sql = sql + data
    sql = sql + ' on duplicate key update m3_commit = values(m3_commit),m3_contrib = values(m3_contrib)'
    return sql


def update_db_m6(data):
    sql = "insert into github_code_commit_summary(`org_name`,`repo_name`,`m6_commit`,`m6_contrib`) values "
    sql = sql + data
    sql = sql + ' on duplicate key update m6_commit = values(m6_commit),m6_contrib = values(m6_contrib)'
    return sql


def update_db_m12(data):
    sql = "insert into github_code_commit_summary(`org_name`,`repo_name`,`m12_commit`,`m12_contrib`) values "
    sql = sql + data
    sql = sql + ' on duplicate key update m12_commit = values(m12_commit),m12_contrib = values(m12_contrib)'
    return sql


def exec_sql(sql):
    # Open database connection
    db = MySQLdb.connect("47.98.56.206", "root", "123456", "blz")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()


def task0():
    print("task0 started.")
    for (key, value) in mapping.items():
        get_data(key, value['url'])
    print("get_data over!!")

    for (key, value) in data_result.items():
        sql = eval(mapping[key]['f'])(get_sql_values(value))
        exec_sql(sql)
    print("save data to mysql over!!")
    div = m12_soup["cache"].find(id="miso_barcharts").div.div
    gen_coin_charts(div)
    print("task0 ended.")


def init_data():
    print("========== init data start =============")
    for (key, value) in mapping.items():
        get_data(key, value['url'])
    print("get_data over!!")

    for (key, value) in data_result.items():
        sql = eval(mapping[key]['f'])(get_sql_values(value))
        exec_sql(sql)
    print("save data to mysql over!!")
    div = m12_soup["cache"].find(id="miso_barcharts").div.div
    gen_coin_charts(div)
    print("===========init data end ============")


@app.route('/pause')
def pause_task(id):
    scheduler.pause_job(id)
    return "Success!"


@app.route('/resume')
def resume_task(id):
    scheduler.resume_job(id)
    return"Success!"


@app.route('/gettask')
def get_task(id):
    jobs = scheduler.get_jobs()
    print(jobs)
    return '111'


@app.route('/job/add', methods=['GET', 'POST'])
def add_task():
    init_data()
    print(" job will start 50 seconds later.")
    scheduler.add_job(func=task0, id='0', args=(), trigger='interval', seconds=100, max_instances=3, replace_existing=True)
    return 'success'


if __name__ == '__main__':
    #  app.config.from_object('config')
    scheduler.init_app(app=app)
    scheduler.start()
    app.run(host='0.0.0.0', debug=True)
