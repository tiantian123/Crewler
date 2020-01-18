# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 21:23:01 2019

@author: Chen Tian

E-mail: chentianfighting@126.com
"""
import pandas as pd
import pymongo
import numpy as np
import re
import warnings
warnings.filterwarnings('ignore')
# 不发出警告

def data_clean1(table, table_new):
    '''
    【列表数据清洗】函数
    table: 源数据mongo集合对象
    table_new: 清洗后数据mongo集合对象
    '''
    dlst = table.find()
    n = 1
    for i in dlst:
        del i['_id']
        i['关注人数'] = int(i['关注人数'])
        i['面积'] = float(re.search(r'([\d.]+)',i['面积']).group(1))
        i['价格_万'] = float(re.search(r'([\d.]+)万',i['价格']).group(1))
        del i['价格']
        i['单价_元'] = float(re.search(r'(\d+)',i['单价']).group(1))
        del i['单价']
        i['发布时间'] = re.search(r'/(.*前)', i['发布时间']).group(1)
        year = re.search(r'(\d+)年',i['房屋信息'])
        if year:
            i['年份'] = year.group(1)
        lc = re.search(r'(\D+)楼层', i['房屋信息'])
        if lc:
            i['楼层'] = lc.group(1)
        cs = re.search(r'(\d+)层',i['房屋信息'])
        if cs:
            i['层数'] = cs.group(1)
        table_new.insert_one(i)
        print('成功清洗%i条数据' % n)
        n += 1

def data_clean2(table,table_new):
    '''
    【详细信息数据清洗】函数
    table: 源数据mongo集合对象
    table_n: 清洗后数据mongo集合对象
    '''
    dlst = table.find()
    n = 1 
    for i in dlst:
        del i['_id']
        i['总价_万'] = float(i['总价_万'])
        i['单价_元'] = float(i['单价_元'])
        i['lng'] = float(i['lng'])
        i['lat'] = float(i['lat'])
        
        area1 = re.search(r'([\d.]+)',i['建筑面积'])
        if area1:
            i['建筑面积'] = float(area1.group(1))
        else:
            del i['建筑面积']
        area2 = re.search(r'([\d.]+)', i['套内面积'])
        if area2:
            i['套内面积'] = float(area2.group(1))
        else:
            del i['套内面积']
        lc = re.search(r'(\D+)楼层', i['所在楼层'])
        if lc:
            i['楼层'] = lc.group(1)
        cs   = re.search(r'(\d+)层', i['所在楼层'])
        if cs:
            i['层数'] = int(cs.group(1))
        table_new.insert_one(i)
        print('成功清洗%i条数据'%n)
        n += 1
            
if __name__=="__main__":
    myClient = pymongo.MongoClient('mongodb://localhost:27017/')
    db = myClient['链家']
    # 链接数据库
    datatable1 = db['长沙岳麓区二手房']
    datatable1_clean = db['长沙岳麓区二手房_clean']
    datatable1_clean.delete_many({})
    data_clean1(datatable1,datatable1_clean)
    # 将清洗后的数据导出
    datadf1 = pd.DataFrame(list(datatable1_clean.find()))
    del datadf1['_id']
    datadf1.to_excel('长沙岳麓区二手房清洗后数据.xlsx',encoding='utf-8',
                     index=True)
    
    datatable2 = db['长沙岳麓区二手房02']
    datatable2_clean = db['长沙岳麓区二手房02_clean']
    datatable2_clean.delete_many({})
    data_clean2(datatable2,datatable2_clean)
    datadf2 = pd.DataFrame(list(datatable2_clean.find()))
    del datadf2['_id']
    datadf2.to_excel('长沙岳麓区二手房清洗后数据02.xlsx',encoding='utf-8',
                     index=True)
    
    
    
    