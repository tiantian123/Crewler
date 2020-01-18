# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 20:05:35 2019

@author: Chen Tian

E-mail: chentianfighting@126.com
"""
import re

lst = ['小红的成绩为98分',
       '小王的成绩为92分',
       '老李今天没上班',
       '小明的成绩为88分',]

m = r'(\D*)的成绩为(\d*)分'

data = []
for i in lst:
    matchob = re.match(m, i)
    dic = {}
    if matchob:
        print('匹配成功')
        dic['姓名'] = matchob.group(1)
        dic['成绩'] = matchob.group(2)
        data.append(dic)
    else:
        print('匹配失败')