#========#========#========#========#
# write 
# 	230411
# writer 
# 	BiZak
# content
# 	- 명일방주 위키 크롤링
#========#========#========#========#

from bs4 import BeautifulSoup
import urllib.request
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# [CODE 1]
def getOperator(result):
    getUrl = "https://arknights.fandom.com/wiki/Operator/"
    parameter = "-star"
    # [Window]
    wd = webdriver.Chrome('./chromedriver.exe')
    
    # 1~6성 오퍼레이터 목록 페이지 순회 반복
    # for star in range(3,4):
    for star in range(1,7):
        try:
            url = getUrl + str(star) + parameter 
            wd.get(url)
            # print('[Magpie]>> Create Url + Parameter')
            print('[Magpie]>> '+str(star)+'-Star Operator')
            print(url)
            print()
            time.sleep(3)
            
            html = wd.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            # 3성과 5성은 임시 모집으로 인해 테이블 경로가 다름
            if(star==3) or (star == 5):
                table_seletor = '#mw-content-text > div.mw-parser-output > div > div.wds-tab__content.wds-is-current > table'
            else:
                table_seletor = '#mw-content-text > div.mw-parser-output > table.mrfz-wtable.sortable.jquery-tablesorter'
            
            table = soup.select_one(table_seletor)
            tbody = table.select_one('tbody')
            for row in tbody.find_all('tr'):
                cols = row.find_all('td')
                
                a = cols[1].select('a')
                op_codename = a[0].string
                
                op_class = cols[2].select_one('div > a')['title']
                op_branch = cols[3].select_one('div > div > a')['title']
                op_faction = cols[4].select_one('a')['title']
                
                
                op_star = str(star)
                
                result.append([op_codename]+[op_class]+[op_branch]+[op_faction]+[op_star])
        except:
            print()
            print("[Magpie]>> "+str(star)+"-star Exeption!")
            print()
            time.sleep(3)
            continue
        
    return result

# [CODE 2]
def getData(operator_list):
    getWikiUrl = "https://arknights.fandom.com/wiki/"
    for parameter in operator_list:
        url = getWikiUrl + parameter
        print(url)
        
        
    return

# [CODE 0]
def main():
    result = []
    operator_list = []
    print('\n\n[Magpie]>> Arknoghts crawling\n\n\n')

    print('[Magpie]>> Get Operator List\n')
    getOperator(operator_list)    # [CODE 1]
    # print(operator_list)
    print("\n[Magpie]>> Operator Count :: " + str(len(operator_list)))
    
    # Save CSV
    ListData = pd.DataFrame(operator_list, columns=('Codename', 'Class', 'Branch', 'Faction', 'Star'))
    ListData.to_csv('./Operator_list.csv', encoding='utf-8', mode='w', index= True)
    print('[Magpie]>> Create File  |  ./Operator_list.csv')
    
    # ======== # ======== # ======== # ======== # ======== # ======== # ======== # ======== #
    
    # getData(operator_list)  # [CODE 2]
    
    # op_data = pd.DataFrame(result, columns=('Codename', 'Class', 'Branch', 'Faction', 'Star'))
    # op_data.to_csv('./Operator_Data.csv', encoding='utf-8', mode='w', index= True)
    # print('[Magpie]>> Create File  |  ./Operator_Data.csv')
    

if __name__ == '__main__':
    main()
