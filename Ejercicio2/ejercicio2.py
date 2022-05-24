import requests
from bs4 import BeautifulSoup
import numpy as np
from wikibase_api import Wikibase
import json

url = "https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=943554"

page = requests.get(url);

soup = BeautifulSoup(page.content, 'html.parser')

tornado = soup.table.find_all('td')

info = list()

for campo in tornado:
    info.append(campo.text)

credentials = {
    "bot_username": "Admin",
    "bot_password": "bot@9eomjq89fmimaa11t2gilnkh64ed398p",
}

info = np.delete(info, (0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40))

wb = Wikibase(api_url='http://156.35.98.119/w/api.php',
              oauth_credentials=None,
              login_credentials=credentials,
              is_bot=True)

entity = wb.entity.add("item")
año = info[9].split('-')[0]
content = {"labels": {"en": {"language": "en", "value": info[5] + " Tornado " + año}}}
updated = wb.entity.update(entity["entity"]["id"], content=content)
listItems = list()
pos = 0
for i in info:
    print(i)
    r = wb.entity.search(i, 'es')['search']
    pos = pos + 1
    if len(r) > 0:
        listItems.append(r[0].get('id'))
print(listItems)
