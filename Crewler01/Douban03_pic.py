# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 22:46:07 2019

@author: Chen Tian

E-mail: chentianfighting@126.com
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_urls(n):
    '''
    【分页网页url采集】
    n: 网页数量
    return: 分页网页的list
    '''
    lst = []
    for i in range(10):
        lst.append('https://movie.douban.com/subject/20438962/photos?type=S&start=%d&sortby=like&size=a&subtype=a'%(i*30))
    return lst

def get_pic(ui,d_h,d_c):
    '''
    【数据采集】
    ui: 网址信息
    d_h: user-agent信息
    d_c: cookies信息
    return: 存放图片的dic, 包括图片id和图片src
    '''
    ri = requests.get(url=ui,headers=d_h,cookies=d_c)
    soupi = BeautifulSoup(ri.text,'lxml')
    ul = soupi.find('ul',class_='poster-col3 clearfix')
    lis = ul.find_all('li')
    piclst = []
    for li in lis:
        dic = {}
        dic['id'] = li['data-id']
        dic['scr'] = li.find('img')['src']
        piclst.append(dic)
    
    return piclst        
        
def save_src(picdic):
    '''
    【保存图片】函数
    picdic: 图片存储的字典，包括图片id和图片src
    '''
    img = requests.get(url = picdic['scr'])
    # 访问网页
    with open('./src/p' + picdic['id'] + '.jpg', 'ab') as f:
        f.write(img.content)
        f.close()
        # 写入文件
    

if __name__ == "__main__":
    urllst1 = get_urls(10)
    print(urllst1[0])
    
    dic_h = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
    dic_c = {}
    cookies = 'll="118282"; bid=spA8Ql8IWIU; gr_user_id=49b1fe04-d9d4-43a7-a641-a7bdb20ca1ba; _vwo_uuid_v2=D6601ED3AE314CA404003A1666F3A4C9A|1b8f19345eab070dd4fd295d5d688759; trc_cookie_storage=taboola%2520global%253Auser-id%3D9e23c9af-37a4-462b-b937-6bd72219700d-tuct3e383cd; __yadk_uid=7qmgrgSvCqin3V3x5eOAQXCFJt8x8a2z; __gads=ID=4a43458843103a01:T=1559049076:S=ALNI_MYVxvrihqeweKwib_8mtS8WRSOW7g; __utmz=30149280.1568760962.10.6.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; push_doumail_num=0; __utmv=30149280.16067; push_noty_num=0; viewed="1829226_10799984_33399902_30414622"; dbcl2="160674056:3OWICx9sEcU"; __utmz=223695111.1568815364.7.6.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/setting; ck=rcx8; ap_v=0,6.0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1568845751%2C%22https%3A%2F%2Faccounts.douban.com%2Fpassport%2Fsetting%22%5D; _pk_id.100001.4cf6=dbc9f938a49fd7cb.1558838471.9.1568845751.1568818574.; _pk_ses.100001.4cf6=*; __utma=30149280.1907923955.1557837001.1568815341.1568845751.13; __utmb=30149280.0.10.1568845751; __utmc=30149280; __utma=223695111.961235516.1558838472.1568818253.1568845751.9; __utmb=223695111.0.10.1568845751; __utmc=223695111'
    for i in cookies.split('; '):
        dic_c[i.split('=')[0]] = i.split('=')[1]
        # 获取u
    srclst = []
    errlst = []
    for ui in urllst1:
        try:
            imgs = get_pic(ui, dic_h, dic_c)
            srclst.extend(imgs)
            print("图片src获取成功, 总共获取%i 条" % len(srclst))
        except:
            errlst.append(ui)
            print("图片获取失败, 获取网址为：", ui)
            continue
    
    n = 1
    for src in srclst:
        try:
            save_src(src)
            print('图片采集成功, 已采集%i张图片' % n)
            n += 1
        except:
            print('图片采集失败, 图片信息为：' ,src)
            continue
        # 批量采集图片
        
        