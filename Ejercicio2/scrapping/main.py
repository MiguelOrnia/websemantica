import requests
from bs4 import BeautifulSoup
import numpy as np

url = "https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=950349"

page = requests.get(url);

soup = BeautifulSoup(page.content,'html.parser')

tornado = soup.table.find_all('td')

info=list()

for campo in tornado:
   info.append(campo.text)

info = np.delete(info,(0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40))
print (info)





