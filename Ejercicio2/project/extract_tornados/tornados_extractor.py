import os
from bs4 import BeautifulSoup

""" Clase TornadoExtractor encargada de obtener la informacion de los HTML relativa a los diferentes 
tornados existentes en la Storms Events Database """


class TornadosExtractor:

    """ Ubicacion de los HTML dentro del proyecto """
    HTML_PATH = "data/"

    """ Constructor de la clase TornadoScrapping """
    def __init__(self):
        self.informes = []

    """ Metodo de la clase TornadoExtractor encargado de cargar los diferentes HTML existentes para
    extraer posteriormente sus narrativas """
    def cargar_documentos(self):
        for fichero in os.listdir(self.HTML_PATH):
            contenido = open(self.HTML_PATH + fichero, "r").read()
            self.informes.append(contenido)
        return self.informes

    """ Metodo de la clase TornadoExtractor encargado de obtener la informacion de la tabla del tornado """
    def get_table_info(self, cotenido):
        soup = BeautifulSoup(cotenido, 'html.parser')
        tornado_info = soup.table.find_all('td')
        return tornado_info

    """ Metodo de la clase TornadoExtractor encargado de obtener la informacion de los eventos relacionados """
    def get_related_events_info(self, contenido):
        soup = BeautifulSoup(contenido, 'html.parser')
        table = soup.find(id="episode_results")
        tornado_info = table.find_all('tr')
        info_events = list()
        tornado_info.pop()
        for i in range(2, len(tornado_info)):
            info_events.append(tornado_info[i].text)
        events = list()
        for i in range(0, len(info_events)):
            events.append(info_events[i].split("\n"))
        return events
