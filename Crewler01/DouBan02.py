# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 20:12:33 2019

@author: Chen Tian

E-mail: chentianfighting@126.com
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_url(n):
    '''
    【分页网页url采集】函数
    n：页数参数
    '''
    lst = []
    for i in range(n):
        lst.append('https://book.douban.com/tag/%%E7%%94%%B5%%E5%%BD%%B1?start=%i&type=T'%(i*20))
    return lst

def get_data(ui, d_h, d_c):
    """
    """
    ri = requests.get(url=ui,headers=d_h,cookies=d_c)
    soupi = BeautifulSoup(ri.text,'lxml')
    ul = soupi.find('ul',class_="subject-list")
    lis = ul.find_all('li')
    lst = []
    for li in lis:
        dic = {}
        dic['书名'] = li.find('div',class_='info').h2.text.replace(' ','').replace('\n','') 
        #dic['评分']= li.find('div',class_="star clearfix").find('span',class_="rating_nums").text
        #dic['评价人数'] = li.find('div',class_="star clearfix").find('span',class_="pl").text.split('人')[0].replace(' ','').replace('\n','')[1:]
        dic['评价'] = li.find('div',class_="star clearfix").text.replace('\n','').replace(' ','')
        dic['简介'] = li.find('p').text
        dic['其他'] = li.find('div',class_="pub").text.replace(' ','').replace('\n','')
        lst.append(dic)
    #print(dic)   
    return lst
        


if __name__ == "__main__":
    urllst1 = get_url(10)
    dic_h = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
    #dic_h = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
    dic_c = {}
    cookies = '''ll="118282"; bid=spA8Ql8IWIU; gr_user_id=49b1fe04-d9d4-43a7-a641-a7bdb20ca1ba; _vwo_uuid_v2=D6601ED3AE314CA404003A1666F3A4C9A|1b8f19345eab070dd4fd295d5d688759; __yadk_uid=Rgc4QJjq3Ihton0VFjFqDvR3gfe6qEI5; __gads=ID=4a43458843103a01:T=1559049076:S=ALNI_MYVxvrihqeweKwib_8mtS8WRSOW7g; __utmz=30149280.1568760962.10.6.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; push_doumail_num=0; __utmv=30149280.16067; push_noty_num=0; ap_v=0,6.0; __utmc=30149280; __utmc=81379588; viewed="1829226_10799984_33399902_30414622"; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1568815029%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.3ac3=*; dbcl2="160674056:3OWICx9sEcU"; ck=rcx8; __utma=30149280.1907923955.1557837001.1568810350.1568815341.12; __utmt=1; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=c51a328a-e1df-47f8-92f8-d07e0cb4cc9c; gr_cs1_c51a328a-e1df-47f8-92f8-d07e0cb4cc9c=user_id%3A1; __utmt_douban=1; __utma=81379588.1971464942.1557837032.1568810350.1568815374.7; __utmz=81379588.1568815374.7.4.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/setting; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_c51a328a-e1df-47f8-92f8-d07e0cb4cc9c=true; _pk_id.100001.3ac3=d91c0c45250231da.1557836976.7.1568815401.1568811231.; __utmb=30149280.6.10.1568815341; __utmb=81379588.2.10.1568815374'''
    #cookies = '''ll="118282"; bid=spA8Ql8IWIU; gr_user_id=49b1fe04-d9d4-43a7-a641-a7bdb20ca1ba; _vwo_uuid_v2=D6601ED3AE314CA404003A1666F3A4C9A|1b8f19345eab070dd4fd295d5d688759; __yadk_uid=Rgc4QJjq3Ihton0VFjFqDvR3gfe6qEI5; __gads=ID=4a43458843103a01:T=1559049076:S=ALNI_MYVxvrihqeweKwib_8mtS8WRSOW7g; viewed="10799984_33399902_30414622"; __utma=30149280.1907923955.1557837001.1568677770.1568760962.10; __utmc=30149280; __utmz=30149280.1568760962.10.6.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=e18c17f5-4a97-4d32-8fda-54bb94a4e7d6; gr_cs1_e18c17f5-4a97-4d32-8fda-54bb94a4e7d6=user_id%3A0; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1568760981%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.3ac3=*; __utma=81379588.1971464942.1557837032.1568677771.1568760981.5; __utmc=81379588; __utmz=81379588.1568760981.5.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; ap_v=0,6.0; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_e18c17f5-4a97-4d32-8fda-54bb94a4e7d6=true; dbcl2="160674056:j5XXu+/XSaE"; ck=TJE_; __utmt_douban=1; __utmt=1; push_doumail_num=0; __utmt=1; __utmv=30149280.16067; _pk_id.100001.3ac3=d91c0c45250231da.1557836976.5.1568761657.1568677784.; __utmb=30149280.9.10.1568760962; __utmb=81379588.6.10.1568760981; push_noty_num=0'''
    for i in cookies.split('; '):
        dic_c[i.split('=')[0]] = i.split('=')[1]
        # 获取useragent,cookies
        
    datalst = []
    errorlst  = []
    for ui in urllst1:
        try:
            datalst.extend(get_data(ui,dic_h,dic_c))
            print('数据采集成功，总共采集%i条数据' % len(datalst))
        except:
            errorlst.append(ui)
            print("数据采集失败，数据网址为：",ui)
    #print(datalst)
    datadf = pd.DataFrame(datalst)
    datadf['评分'] = datadf['评价'].str.split('(').str[0]
    datadf['评价数量'] = datadf['评价'].str.split('(').str[1].str.split('人').str[0]  
    datadf['评分'].fillna(0,inplace=True)
    
    del datadf['评价']
    datadf['价格'] = datadf['其他'].str.split('/').str[-1]
        # 数据清洗
        # 对于价格由于噪音较多，后续通过正则提取数字
    
    datadf.to_excel('豆瓣电影信息爬取结果2.xlsx')
        # 导出excel