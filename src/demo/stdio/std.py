# ! /usr/bin/python
# -*- coding: utf-8 -*-
import sys
from subprocess import Popen, PIPE

name = raw_input()
if len(name) < 3:
    print >> sys.stderr, "Name is too short"
else:
    print "Hello %s" % name

# 接下來試著使用 subprocess 調用這個程式吧！

# 首先是 input 長度正常的結果


p = Popen(['python', 'test.py'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
stdout, stderr = p.communicate(input='aweimeow\n')
stdout = 'Hello aweimeow\n'


# 再來是 input 長度過短的結果

from subprocess import Popen, PIPE
p = Popen(['python', 'test.py'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
stdout, stderr = p.communicate(input='aweimeow\n')
# stderr = 'Name is too short\n'
# 如此一來便可以輕鬆的接到 stdout 及 stderr 了！
