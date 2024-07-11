import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re

url = 'https://stardewvalleywiki.com/Crops'
driver = webdriver.Chrome()  
driver.get(url)
time.sleep(3)

page_content = driver.page_source
soup = BeautifulSoup(page_content, 'html.parser')
allCrops = []

crops = soup.find_all('table', class_=['wikitable roundedborder'])
for i in range(len(crops)-7):
    crop = {}

    headers = crops[i].find_all('th')
    headers = [header.get_text() for header in headers]
    sell_index = headers.index('Sells For\n')
    
    a = crops[i].find_all('tr')
    toplevel_tr = [tr for tr in a if tr.find_parent('tr') is None]

    line1 = toplevel_tr[1]
    line1 = line1.find_all('td')

    line2 = toplevel_tr[2]
    line2 = line2.find_all('td')

    ### Managing crop name ###

    crop['Seed'] = line1[0].get_text().rstrip()
    crop['Seed'] = crop['Seed'].split('\n')[0]

    ### Managing prices ###

    sell_prices = line1[sell_index].find_all('td')
    for j in range(len(sell_prices)):
        sell_prices[j] = sell_prices[j].get_text().rstrip().replace('g','')

    if len(sell_prices) > 0:
        crop['Price (Regular)'] = int(sell_prices[1].replace(',',''))
        crop['Price (Silver)'] = int(sell_prices[3].replace(',',''))
        crop['Price (Gold)'] = int(sell_prices[5].replace(',',''))
        crop['Price (Iridium)'] = int(sell_prices[7].replace(',',''))
    else:
        sell_prices = line1[sell_index+1].find_all('td')
        for j in range(len(sell_prices)):
            sell_prices[j] = sell_prices[j].get_text().rstrip().replace('g','')
        
        crop['Price (Regular)'] = int(sell_prices[1].replace(',',''))
        crop['Price (Silver)'] = int(sell_prices[3].replace(',',''))
        crop['Price (Gold)'] = int(sell_prices[5].replace(',',''))
        crop['Price (Iridium)'] = int(sell_prices[7].replace(',',''))

    ### Managing growth time ###
    growth_time_index = headers.index('Harvest\n')
    growth_time = line2[growth_time_index-1].get_text().rstrip()

    if 'Regrowth' in line2[growth_time_index].get_text().rstrip():
        crop['Regrowth Time (In Days)'] = line2[growth_time_index].get_text().rstrip().split(':')[1].rstrip().split(' ')[0]


    ### Managing regrowth time ###  
    crop['Growth Time (In Days)'] = int(growth_time.split(' ')[1])

    ### Managing Selling ###

    selling = line1[0].find('div', class_='no-wrap')
    selling = selling.find_all('a')
    for i in range(len(selling)):
        selling[i] = selling[i].get_text().rstrip()
    
    crop['Purchase Source'] = selling


    crop_url = line1[0].find_all('a')
    url = 'https://stardewvalleywiki.com' + crop_url[1].get('href')
    driver = webdriver.Chrome()  
    driver.get(url)
    time.sleep(3)

    content_crop = driver.page_source
    soup_content = BeautifulSoup(content_crop, 'html.parser')
    tabela = soup_content.find('table', id='infoboxtable')

    linhas = tabela.find_all('tr')
    for linha in linhas:
        
        if 'Crop' in linha.get_text():
            crop_type = linha.find_all('td')[1].get_text().rstrip()
            crop['Name'] = crop_type

        if 'Season' in linha.get_text():
            season = linha.find_all('td')[1].get_text().rstrip()
            crop['Season'] = re.sub(r'[^A-Za-z0-9 ]+', '', season)
            crop['Season'] = crop['Season'].split(' ')

        
        if 'XP' in linha.get_text():
            xp = linha.find_all('td')[1].get_text().rstrip()
            crop['XP'] = xp
        
        if 'Sell Price' in linha.get_text():
            sell_price = linha.find_all('td')[1].get_text().rstrip()
            if '>' in sell_price:
                sell_price = sell_price.split('>')[1].replace('g','')
                if len(sell_price) <10:
                    crop['Sell Price (Seed)'] = int(sell_price)
                else:
                    crop['Sell Price (Seed)'] = "edit"

        
        ### Managing Purchase Prices ###
                

    print(crop)
    allCrops.append(crop)


df = pd.DataFrame(allCrops)
df.to_csv('crops.csv', index=False)



