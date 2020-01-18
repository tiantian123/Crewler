# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 06:54:40 2019

@author: Chen Tian

E-mail: chentianfighting@126.com
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
print('导入成功')

def get_urls(n):
    '''
    【分页网页url采集】
    n：页数参数
    结果：得到一个分页网页的list
    '''
    lst = []
    for i in range(10):
        ui = 'https://book.douban.com/tag/%%E7%%94%%B5%%E5%%BD%%B1?start=%i&type=T'%(i*20)
        # % 需要改成 %%
        lst.append(ui)
    return lst

def get_dataurls(ui, d_h, d_c):
    """
    【数据信息网页url采集】
    ui：分页网址
    d_h：user-agent信息
    d_c：cookies信息
    结果：得到一个数据信息网页的list
    """
    ri = requests.get(url=ui,headers = d_h, cookies = d_c)
        # 访问页面
    soupi = BeautifulSoup(ri.text,'lxml')
        # 解析页面
    ul = soupi.find('ul',class_="subject-list")
    lis = ul.find_all('li')
    
    lst = []
    for li in lis:
        lst.append(li.find('a')['href'])
    return lst

def get_data(ui,d_h,d_c):
    """
    【数据采集】函数
    ui：数据信息网页
    d_h：user-agent信息
    d_c：cookies信息
    """
    ri = requests.get(ui, headers=d_h, cookies=d_c)
    soupi = BeautifulSoup(ri.text,'lxml')
    dic = {} # 构建空字典，用于存储数据
    dic['书名'] = soupi.find('div',id='wrapper').h1.text
    dic['评分'] = soupi.find('div',class_='rating_self clearfix').strong.text
    dic['评价人数'] = soupi.find('a',class_='rating_people').text
    infors = soupi.find('div',id='info').text.replace(' ','').split('\n')
    for i in infors:
        if ':' in i:
            dic[i.split(':')[0]] = i.split(':')[1]
        else:
            continue
    
    return dic

if __name__ == '__main__':
    u0 = 'https://book.douban.com/tag/%E7%94%B5%E5%BD%B1?start=20&type=T'
    urllst1 = get_urls(10)
    ul = urllst1[0]
    
    dic_h = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
    dic_c = {}
    cookies = '''ll="118282"; bid=spA8Ql8IWIU; gr_user_id=49b1fe04-d9d4-43a7-a641-a7bdb20ca1ba; _vwo_uuid_v2=D6601ED3AE314CA404003A1666F3A4C9A|1b8f19345eab070dd4fd295d5d688759; __yadk_uid=Rgc4QJjq3Ihton0VFjFqDvR3gfe6qEI5; __gads=ID=4a43458843103a01:T=1559049076:S=ALNI_MYVxvrihqeweKwib_8mtS8WRSOW7g; viewed="10799984_33399902_30414622"; __utma=30149280.1907923955.1557837001.1568677770.1568760962.10; __utmc=30149280; __utmz=30149280.1568760962.10.6.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=e18c17f5-4a97-4d32-8fda-54bb94a4e7d6; gr_cs1_e18c17f5-4a97-4d32-8fda-54bb94a4e7d6=user_id%3A0; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1568760981%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.3ac3=*; __utma=81379588.1971464942.1557837032.1568677771.1568760981.5; __utmc=81379588; __utmz=81379588.1568760981.5.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; ap_v=0,6.0; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_e18c17f5-4a97-4d32-8fda-54bb94a4e7d6=true; dbcl2="160674056:j5XXu+/XSaE"; ck=TJE_; __utmt_douban=1; __utmt=1; push_doumail_num=0; __utmt=1; __utmv=30149280.16067; _pk_id.100001.3ac3=d91c0c45250231da.1557836976.5.1568761657.1568677784.; __utmb=30149280.9.10.1568760962; __utmb=81379588.6.10.1568760981; push_noty_num=0'''
    for i in cookies.split('; '):
        dic_c[i.split('=')[0]] = i.split('=')[1]
        # 获取useragent,cookies
    urllst2 = []
    for u in urllst1:
        try:
            urllst2.extend(get_dataurls(u,dic_h,dic_c))
            print("成功获取数据信息页面网址，总共获取%i条信息" % len(urllst2))
        except:
            print("获取数据信息失败, 分页网址为%s" % u)
            
    datalst = []
    errorlst = []
    for u in urllst2:
        try:
            datalst.append(get_data(u,dic_h,dic_c))
            print('数据采集成功，总共采集%i条数据' % len(datalst))
        except:
            errorlst.append(u)
            print('数据采集失败，数据网址为：',u)
    #print(datalst)
    datadf = pd.DataFrame(datalst)
    datadf['评分'] = datadf['评分'].astype('float')
    datadf['评分人数'] = datadf['评价人数'].str.split('人').str[0].astype('int')
    datadf['页数'] = datadf['页数'].str.replace('页','').astype('float')
    datadf.to_excel('豆瓣电影信息爬取结果.xlsx')

    
    

        