#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Asin Liu


class Person(object):

    def __init__(self, name, lang, website):
        self.name = name
        self.lang = lang
        self.website = website


'''
未实例化时，运行程序，构造方法没有运行
'''

p = Person('Tim', 'English', 'www.universal.com')
