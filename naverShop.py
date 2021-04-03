import os
import sys
import requests
import re
from bs4 import BeautifulSoup as bs
import time
import random
import pandas as pd
from tqdm import tqdm
def search(product):
    purAll = 0
    url = 'https://shopping.naver.com/search/all'
    s = requests.Session()
    for i in range(8):
        index = i+1
        params = {'frm':'NVSHOVS','origQuery':product,'pagingIndex':index,'pagingSize':5,\
          'productSet':'overseas','query':product,'sort':'rel','viewType':'list'}
#         print('page : '+repr(params['pagingIndex']))
        try:
            r = s.get(url, params = params)
        except:
            pass
        res = requests.post(url, params=params)
        time.sleep(random.uniform(1,2))
        soup = bs(res.text,'html.parser')
        area = soup.find('ul',{'class':'list_basis'}).find_all('div',{'class':"basicList_info_area__17Xyo"})
        for part in area:
            check = part.find_all('a',{'class':'basicList_etc__2uAYO'})
            for elem in check:
        #         print(elem.get_text())
                if '구매건수' in elem.get_text():
                    pur = int(elem.get_text()[4:].replace(',',''))
                    purAll += pur
        if index==1 and purAll==0:
            break
    return purAll
def crawl_headless(date):
    year = date[:4]
    month = date[4:6]
    day = date[6:]
    saveDate = year+'-'+month+'-'+day
    data = pd.read_excel(saveDate + '_new.xlsx')
    data = data[:10]
    keyword = data['키워드'].values
    count = []
    for word in tqdm(keyword):
        try:
            pur = search(word)
        except AttributeError:
            pur = 0
            pass
        count.append(pur)
    if len(data) == len(count):
        data['구매건수'] = count
    else:
        print("count Wrong!")
    data.to_excel(saveDate+'_newCount.xlsx', index=False)
if __name__ == '__main__':
    date = input("date : ")
    crawl_headless(date)


