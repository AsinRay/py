#!/usr/bin/env python
# coding: utf-8
# 一直在想怎么测试输出64K的数据，发现dd这个思路很棒，是见过最优雅的例子了，精确控制输出的长度

import subprocess

def test(size):
    print 'start'

    cmd = 'dd if=/dev/urandom bs=1 count=%d 2>/dev/null' % size
    p = subprocess.Popen(args=cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    #p.communicate()
    p.wait()  # 这里超出管道限制，将会卡住子进程

    print 'end'

# 64KB
test(64 * 1024)

# 64KB + 1B
test(64 * 1024 + 1)

# output :
'''

start
end
start 


'''
#  然后就阻塞了。


