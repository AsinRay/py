import re
import MySQLdb
from bs4 import BeautifulSoup, Comment
import requests.packages.urllib3.util.ssl_

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'

# TODO try this for test! '@_@"
mapping = {"m12": {"url": "", "f": "update_db_m12"},
           "m6": {"url": "months_6.html", "f": "update_db_m6"},
           "m3": {"url": "months_3.html", "f": "update_db_m3"}}
div_map = {}
data_result = {}
m12_div = {}
# return the div element of the html dom


def get_div(key, url):
    req_url = "https://www.cryptomiso.com/" + url
    resp = requests.get(req_url)
    soup = BeautifulSoup(resp.content, "lxml")
    for element in soup(text=lambda text: isinstance(text, Comment)):
        element.extract()
    div = str(soup.find(id="miso_barcharts"))
    div_map[key] = div


def get_m12_div():
    req_url = "https://www.cryptomiso.com"
    resp = requests.get(req_url)
    soup = BeautifulSoup(resp.content, "lxml")
    for element in soup(text=lambda text: isinstance(text, Comment)):
        element.extract()
    div = str(soup.find(id="miso_barcharts div div.col-lg-8"))
    return str(div[0].contents)


def get_m12_div_from_local():
    soup = BeautifulSoup(open("index.html"), "lxml")
    for element in soup(text=lambda text: isinstance(text, Comment)):
        element.extract()
    # div = soup.select("#miso_barcharts div div.col-lg-8")[0]
    div = soup.find(id="miso_barcharts").div.div
    return div


def get_coin_chart(div, coin):
    return div.find(id=coin).nextSibling.nextSibling


def bs_preprocess(html):
    """remove distracting whitespaces and newline characters"""
    pat = re.compile('(^[\s]+)|([\s]+$)', re.MULTILINE)
    html = re.sub(pat, '', html)       # remove leading and trailing whitespaces
    html = re.sub('\n', ' ', html)     # convert newlines to spaces
                                        # this preserves newline delimiters
    html = re.sub('[\s]+<', '<', html)  # remove whitespaces before opening tags
    html = re.sub('>[\s]+', '>', html)  # remove whitespaces after closing tags
    return html


def gen_coin_charts(src):
    for tag in src.select("> a"):
       m12_div[tag['id']] = str(tag.nextSibling.nextSibling)


def print_m12_div():
    for k, v in m12_div.items():
        print(v)


# get the data of the github summary
def get_data(key, url):
    req_url = "https://www.cryptomiso.com/" + url
    resp = requests.get(req_url)
    soup = BeautifulSoup(resp.content, "lxml")
    d = soup.select('#miso_barcharts h4.card-title')
    data_result[key] = d


def append_to_file(msg):
    try:
        f = open("index.html", 'w')
        f.write(msg)
        f.close()
    except IOError:
        print("IOError!!")


def remove_non_ascii(s):
    return "|".join(i for i in s if ord(i) < 128)


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


for (key, value) in mapping.items():
    get_data(key, value['url'])

for (key, value) in data_result.items():
    sql = eval(mapping[key]['f'])(get_sql_values(value))
    print(sql)
    exec_sql(sql)


div = get_m12_div_from_local()
gen_coin_charts(div)



