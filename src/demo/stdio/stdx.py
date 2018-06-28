# ! /usr/bin/python
# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE

sh = '''docker logs -f webqq'''


def run_it(cmd):
    # _PIPE = subprocess.PIPE
    p = Popen(cmd, stdout=PIPE, shell=True, stderr=PIPE) #, close_fds=True)

    print('running:%s' % cmd)
    out, err = p.communicate()
    print(out)
    if p.returncode != 0:
        print("Non zero exit code:%s executing: %s" % (p.returncode, cmd))
    return p.stdout


p = Popen(sh.split(), stdout=PIPE, stderr=PIPE, stdin=PIPE)
stdout, stderr = p.communicate(input='aweimeow\n')

so = run_it(sh.split())
while True:
    line = p.stdout.readline()
    if line:
        print(line)
