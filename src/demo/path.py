#!/bin/env python
#-*- encoding=utf8 -*-

import os
import sys


'''
os.getcwd() “/home/boot/src/github”，取的是起始执行目录
sys.path[0]  /home/boot/src/github/src/demo 取的是被初始执行的脚本的所在绝对目录
sys.argv[0]  src/demo/path.py 可以看出取的是被初始执行的脚本的所在相对目录，相对于os.getcwd(),后面又增加了文件名称
os.path.split(os.path.realpath(__file__))[0] “D:\python_test”，取的是__file__所在文件test_path.py的所在目录

 

正确获取当前的路径：

    __file__是当前执行的文件  # 获取当前文件__file__的路径
    print "os.path.realpath(__file__)=%s" %os.path.realpath(__file__) # 获取当前文件__file__的所在目录
    print "os.path.dirname(os.path.realpath(__file__))=%s" % os.path.dirname(os.path.realpath(__file__)) 　　
    # 获取当前文件__file__的所在目录

    print "os.path.split(os.path.realpath(__file__))[0]=%s" % os.path.split(os.path.realpath(__file__))[0]　　
'''


if __name__ == "__main__":

    print "__file__=%s" % __file__

    print "os.path.realpath(__file__)=%s" % os.path.realpath(__file__)

    print "os.path.abspath(__file__)=%s" % os.path.abspath(__file__)

    print "os.path.dirname(os.path.realpath(__file__))＝%s" % os.path.dirname(os.path.realpath(__file__))

    print "os.path.split(os.path.realpath(__file__))[0]=%s" % os.path.split(os.path.realpath(__file__))[0]

    print "os.getcwd()=%s" % os.getcwd()

    print "sys.path[0]=%s" % sys.path[0]

    print "sys.argv[0]=%s" % sys.argv[0]
