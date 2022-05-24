import requests
from bs4 import BeautifulSoup
import numpy as np
from wikibase_api import Wikibase
from datetime import datetime


def scrapping():
    url = "https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=943554"
    page = requests.get(url);
    soup = BeautifulSoup(page.content, 'html.parser')
    tornadoInfo = soup.table.find_all('td')
    return tornadoInfo


tornado = scrapping()


def obtenerInfo(tornado):
    info = list()
    for campo in tornado:
        info.append(campo.text)
    info = np.delete(info, (0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40))
    return info;


def createWikiBase():
    credentials = {
        "bot_username": "Admin",
        "bot_password": "bot@9eomjq89fmimaa11t2gilnkh64ed398p",
    }

    wikibase = Wikibase(api_url='http://156.35.98.119/w/api.php',
                  oauth_credentials=None,
                  login_credentials=credentials,
                  is_bot=True)

    return wikibase


info = obtenerInfo(tornado)

instanceOf = info[0]
scale = info[1]
length = info[2]
width = info[3]
country = "United States"
state = info[4]
county = info[5]
source = info[7]
añoBegin = info[9].split('-')[0]
mesBegin = info[9].split('-')[1]
añoEnd = info[12].split('-')[0]
mesEnd = info[12].split('-')[1]
endDate = info[12]
beginDate = info[9]
lat = info[11].split('/')[0]
lon = info[11].split('/')[1]
duration = ""
deaths = info[15].split('/')[0]
injuries = info[16].split('/')[0]
propertyDamage = info[18] + " United States dollar"
cropDamage = info[19] + " United States dollar"

beginDateObject = datetime(int(añoBegin), int(mesBegin), int(beginDate.split(" ")[0].split("-")[2]),
                           int(beginDate.split(" ")[1].split(":")[0]), int(beginDate.split(" ")[1].split(":")[1]), 00,
                           00000)

endDateObject = datetime(int(añoEnd), int(mesEnd), int(endDate.split(" ")[0].split("-")[2]),
                         int(endDate.split(" ")[1].split(":")[0]), int(endDate.split(" ")[1].split(":")[1]), 00, 00000)

duration = (endDateObject - beginDateObject).total_seconds()

duration_hours = duration / 3600

movementSpeed = float(length.split(" ")[0]) / duration_hours

wb = createWikiBase()

entity = wb.entity.add("item")

content = {"labels": {"en": {"language": "en", "value": info[5] + " Tornado " + añoBegin}}}
updated = wb.entity.update(entity["entity"]["id"], content=content)
wb.claim.add(entity["entity"]["id"], "P9", length, snak_type='value')


def obtenerItemsExistentes():
    listItems = list()
    pos = 0
    for i in info:
        print(i)
        r = wb.entity.search(i, 'es')['search']
        pos = pos + 1
        if len(r) > 0:
            listItems.append(r[0].get('id'))
        return listItems


print(obtenerItemsExistentes())
