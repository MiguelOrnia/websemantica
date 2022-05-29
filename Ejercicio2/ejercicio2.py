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


wb = createWikiBase()


def findEntity(label):
    r = wb.entity.search(label, 'es')['search']
    if len(r) > 0:
        return r[0].get('id')
    else:
        newEntity = wb.entity.add("item")
        entityContent = {"labels": {"en": {"language": "en", "value": label}}}
        wb.entity.update(newEntity["entity"]["id"], content=entityContent)
        return newEntity["entity"]["id"]


info = obtenerInfo(tornado)

instanceOf = info[0]
scale = info[1]
length = float(info[2].split(" ")[0])
width = float(info[3].split(" ")[0])
country = "United States"
state = info[4]
county = info[5]
source = info[7]
añoBegin = info[9].split('-')[0]
mesBegin = info[9].split('-')[1]
añoEnd = info[12].split('-')[0]
mesEnd = info[12].split('-')[1]
endDate = info[12]
beginDate = info[9 ]
lat = info[11].split('/')[0]
lon = info[11].split('/')[1]
duration = ""
deaths = info[15].split('/')[0]
injuries = info[16].split('/')[0]
propertyDamage = float(info[17].split("M")[0])
print(propertyDamage)
cropDamage = float(info[18].split("K")[0])

beginDateObject = datetime(int(añoBegin), int(mesBegin), int(beginDate.split(" ")[0].split("-")[2]),
                           int(beginDate.split(" ")[1].split(":")[0]), int(beginDate.split(" ")[1].split(":")[1]), 00,
                           00000)

endDateObject = datetime(int(añoEnd), int(mesEnd), int(endDate.split(" ")[0].split("-")[2]),
                         int(endDate.split(" ")[1].split(":")[0]), int(endDate.split(" ")[1].split(":")[1]), 00, 00000)

duration = (endDateObject - beginDateObject).total_seconds()

duration_hours = duration / 3600

movementSpeed = length / duration_hours

idState = findEntity(state)
idCounty = findEntity(county)
idState.split('Q')[1]

entity = wb.entity.add("item")

content = {"labels": {"en": {"language": "en", "value": info[5] + " Tornado " + añoBegin}},
           "descriptions": {'en': {'language': 'en', 'value': 'weather event'}},
           "claims": {'P3': [{'mainsnak': {'snaktype': 'value', 'property': 'P3',
                                           'datavalue': {'value': {'entity-type': 'item', 'numeric-id': 5, 'id': 'Q5'},
                                                         'type': 'wikibase-entityid'}, 'datatype': 'wikibase-item'},
                              'type': 'statement', 'rank': 'normal'}],
                      'P18': [{'mainsnak': {'snaktype': 'value', 'property': 'P18',
                                            'datavalue': {'value': {'entity-type': 'item', 'numeric-id': 7, 'id': 'Q7'},
                                                          'type': 'wikibase-entityid'}, 'datatype': 'wikibase-item'},
                               'type': 'statement', 'rank': 'normal'}],
                      'P9': [{'mainsnak': {'snaktype': 'value', 'property': 'P9', 'datavalue': {
                          'value': {'amount': length, 'unit': 'http://156.35.98.119/entity/Q8'}, 'type': 'quantity'},
                                           'datatype': 'quantity'}, 'type': 'statement', 'rank': 'normal'}],
                      'P10': [{'mainsnak': {'snaktype': 'value', 'property': 'P10', 'datavalue': {
                          'value': {'amount': width, 'unit': 'http://156.35.98.119/entity/Q9'}, 'type': 'quantity'},
                                            'datatype': 'quantity'}, 'type': 'statement', 'rank': 'normal'}],
                      'P5': [{'mainsnak': {'snaktype': 'value', 'property': 'P5', 'datavalue': {
                          'value': {'entity-type': 'item', 'numeric-id': 10, 'id': 'Q10'}, 'type': 'wikibase-entityid'},
                                           'datatype': 'wikibase-item'}, 'type': 'statement', 'rank': 'normal'}],
                      'P6': [{'mainsnak': {'snaktype': 'value', 'property': 'P6', 'datavalue': {
                          'value': {'entity-type': 'item', 'numeric-id': idState.split('Q')[1], 'id': idState},
                          'type': 'wikibase-entityid'},
                                           'datatype': 'wikibase-item'}, 'type': 'statement', 'rank': 'normal'}],
                      'P8': [{'mainsnak': {'snaktype': 'value', 'property': 'P8', 'datavalue': {
                          'value': {'entity-type': 'item', 'numeric-id': idCounty.split('Q')[1], 'id': idCounty},
                          'type': 'wikibase-entityid'},
                                           'datatype': 'wikibase-item'}, 'type': 'statement', 'rank': 'normal'}],
                      'P16': [{'mainsnak': {'snaktype': 'value', 'property': 'P16',
                                            'datavalue': {'value': source, 'type': 'string'},
                                            'datatype': 'string'}, 'type': 'statement', 'rank': 'normal'}],
                      'P15': [{'mainsnak': {'snaktype': 'value', 'property': 'P15', 'datavalue': {
                          'value': {'amount': duration, 'unit': 'http://156.35.98.119/entity/Q13'}, 'type': 'quantity'},
                                            'datatype': 'quantity'}, 'type': 'statement', 'rank': 'normal'}],
                      'P21': [{'mainsnak': {'snaktype': 'value', 'property': 'P21',
                                            'datavalue': {'value': {'amount': injuries, 'unit': '1'}, 'type': 'quantity'},
                                            'datatype': 'quantity'}, 'type': 'statement', 'rank': 'normal'}],
                      'P22': [{'mainsnak': {'snaktype': 'value', 'property': 'P22',
                                            'datavalue': {'value': {'amount': deaths, 'unit': '1'}, 'type': 'quantity'},
                                            'datatype': 'quantity'}, 'type': 'statement', 'rank': 'normal'}],
                      'P23': [{'mainsnak': {'snaktype': 'value', 'property': 'P23', 'datavalue': {
                          'value': {'amount': propertyDamage, 'unit': 'http://156.35.98.119/entity/Q14'}, 'type': 'quantity'},
                                            'datatype': 'quantity'}, 'type': 'statement', 'rank': 'normal'}],
                      'P24': [{'mainsnak': {'snaktype': 'value', 'property': 'P24', 'datavalue': {
                          'value': {'amount': cropDamage, 'unit': 'http://156.35.98.119/entity/Q14'}, 'type': 'quantity'},
                                            'datatype': 'quantity'}, 'type': 'statement', 'rank': 'normal'}],

                      }}

updated = wb.entity.update(entity["entity"]["id"], content=content)

print(entity["entity"]["id"])