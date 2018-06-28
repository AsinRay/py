#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from subprocess import Popen, PIPE

'''
subprocess module introduction

subprocess.call
subprocess.check_call
subprocess.check_output
subprocess.Popen


subprocess.call
Run the command described by args. Wait for command to complete, then return the returncode attribute.

也就是說，我們的 code 會等到指令執行結束才回傳結果，用這個例子來試試看：

'''
import subprocess

subprocess.call(['sleep', '1'])

'''
結果會在 1 秒後回傳 0，這個 0 有著特殊意義，他代表著 return code

這邊需要注意的是，arg 代入的參數是 list 型態，
如果需要帶入字串的話，可以加上一個參數，像以下例子：
'''

subprocess.call('sleep 1', shell=True)

'''
shell=True 表示會呼叫一個 /bin/sh 來執行這條指令，
不過因為有 Command Injection 的問題，所以並不是推薦的方法。
https://www.owasp.org/index.php/Command_Injection
當然，你也可以使用這種方式來執行指令：
'''

# 利用 str 的 split 把 str 以空白做區隔切成一個 List
subprocess.call('sleep 1'.split())

'''
subprocess.check_call
Run command with arguments. Wait for command to complete. If the return code was zero then return, 
otherwise raise CalledProcessError.

也就是說，如果 return code 為 0 才回傳 return code，否則拋出例外。
通常 return code 為 0 表示正常執行，因為 return code 又稱為 Exit Status，
如果不為零，則代表執行程式的錯誤代碼。
這個 function 在不需執行結果，只需要執行狀態的時候適用。

舉個例子：
'''

if subprocess.check_call(['ls']) == 0:
    print('Command Success Execute')
else:
    print('Oops, something error')

'''
subprocess.check_output
Run command with arguments and return its output as a byte string.

這個則是很實用的 function 了，他會把輸出直接回傳給你，
不過值得注意的一點是，與上一個 function 相同，如果 return code 不是 0 也會拋出例外。

舉個例子，先試著讓他拋出例外：
'''
try:
    output = subprocess.check_output('exit 1', shell=True)
except subprocess.CalledProcessError:
    print('Exception handled')

# 然後則是在 return code 是 0 的狀態：

try:
    output = subprocess.check_output(['ls'])
except subprocess.CalledProcessError:
    print('Exception handled')
# 然後試著印出 output 吧

'''
subprocess.Popen
Execute a child program in a new process. On Unix, the class uses os.execvp()-like behavior to execute the child program.

這是我最常使用的 function，因為有時候我會需要接收來自 stderr 的訊息。

舉個例子，先寫段 code 來達成一個簡易的功能，
如果輸入過短則把錯誤訊息輸出到 stderr，
否則便把 'Hello name' 輸出到 stdout
'''




