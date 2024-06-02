import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time

def getCharInfo(name):
    url = 'https://stardewvalleywiki.com/'+name
    driver = webdriver.Chrome()  
    driver.get(url)
    time.sleep(3)

    page_content = driver.page_source
    soup = BeautifulSoup(page_content, 'html.parser')

    gostos = soup.find_all('table', class_=['wikitable roundedborder', 'wikitable sortable roundedborder jquery-tablesorter'])
    types = ['Loved Gifts', 'Liked Gifts', 'Neutral Gifts', 'Disliked Gifts', 'Hated Gifts']
    character = {}

    for i in range(len(types)):
        gostosE = []
        for j in gostos[i].find_all('tr'):
            a = j.find_all('td')
            b = j.find_all('li')
            if(len(a) == 0):
                continue
            elif(len(b) != 0):
                for k in b:
                    gostosE.append(k.text.rstrip())
            else:
                gostosE.append(a[1].text.rstrip())
        character[types[i]] = gostosE        
        


    labels_df = []
    labels = soup.find_all('td', id='infoboxsection')
    labels.pop(0)

    for i in range(len(labels)):
        labels_df.append(labels[i].text.rstrip())

    infos = soup.find_all('td', id='infoboxdetail')
    
    character['Name'] = name
    for i in range(len(labels)):
            
        if(len(infos[i].find_all('span', class_='nametemplate'))):
            continue
            #for j in infos[i].find_all('span', class_='nametemplate'):
            #    loved_gifts.append(j.text.rstrip().replace('\xa0',''))

            #character[labels[i].text.rstrip()] = loved_gifts
        else:
            if(labels[i].text.rstrip() == 'Family'):
                family = []
                for j in infos[i].find_all('a'):
                    family.append(j.text.rstrip().replace('\xa0',''))
                character[labels[i].text.rstrip()] = family
            elif((labels[i].text.rstrip() == 'Birthday') and (labels[i].text.rstrip() != 'Unknown')):
                
                separated_date = infos[i].text.rstrip().replace('\xa0','').split(' ')
                character['Birthday Season'] = separated_date[0]
                character['Birthday Day'] = separated_date[1]

            else:
                character[labels[i].text.rstrip()] = infos[i].text.rstrip().replace('\xa0','')
            
    driver.quit()

    return character
    


def getCharactersInfo():
    personagens = ['Abigail', 'Alex', 'Caroline', 'Clint','Demetrius','Dwarf', 'Elliott', 'Emily', 'Evelyn', 'George', 'Gus', 'Haley', 'Harvey', 'Jas', 'Jodi', 'Kent', 'Leah', 'Lewis', 'Linus', 'Marnie', 'Maru', 'Pam', 'Penny', 'Pierre', 'Robin', 'Sandy','Sam', 'Sebastian', 'Shane', 'Vincent', 'Willy', 'Wizard'] 
    info = []
    
    for i in range(len(personagens)):
        a = getCharInfo(personagens[i])
        info.append(a)
    info_df = pd.DataFrame(info)

    info_df = info_df[['Name','Birthday Season','Birthday Day','Lives In','Address','Family','Marriage','Clinic Visit','Loved Gifts','Liked Gifts','Neutral Gifts','Disliked Gifts','Hated Gifts']]
    info_df.to_csv('characters.csv', index=False)



getCharactersInfo()
