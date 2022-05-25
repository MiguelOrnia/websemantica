import os
from datetime import datetime
from bs4 import BeautifulSoup
from extract_tornados.tornado_query import TornadoQuery

""" Clase TornadoScrapping encargada de obtener la informacion de los HTML relativa a los diferentes 
tornados existentes en la Storms Events Database """


class TornadoScrapping:

    HTML_PATH = "data/"

    """ Constructor de la clase TornadoScrapping """
    def __init__(self):
        self.informes = []

    """ Metodo de la clase TornadoScrapping encargado de cargar los diferentes HTML existentes para
    extraer posteriormente sus narrativas """
    def cargarDocumentos(self):
        for fichero in os.listdir(self.HTML_PATH):
            contenido = open(self.HTML_PATH + fichero, "r").read()
            self.informes.append(contenido)
        return self.informes

    """ Metodo de la clase TornadoScrapping encargado de extraer el texto correspondiente a la narrativa 
    de un tornado """
    def extraer_narrativa(self, contenido):
        soup = BeautifulSoup(contenido, 'html.parser')
        todos_tds = soup.find_all("td")

        narrative = ""

        for i in range(len(todos_tds)):
            contenidos_td = todos_tds[i].contents
            if 'Event Narrative' in contenidos_td:
                narrative = todos_tds[i + 1].get_text()
                break

        return narrative

    """ Metodo encargado en obtener la consulta a realizar en la API de Wikibase """
    def buscar_info(self, contenido):
        # Extraer info del html
        soup = BeautifulSoup(contenido, 'html.parser')
        todos_tds = soup.find_all("td")

        for i in range(len(todos_tds)):
            contenidos_td = todos_tds[i].contents
            if 'County/Area' in contenidos_td:
                county = todos_tds[i + 1].get_text()
            if 'Begin Date' in contenidos_td:
                beginDate = todos_tds[i + 1].get_text()
            if 'End Date' in contenidos_td:
                endDate = todos_tds[i + 1].get_text()
                break

        yearBegin = beginDate.split(" ")[0].split("-")[0]
        monthBegin = beginDate.split(" ")[0].split("-")[1]
        dayBegin = beginDate.split(" ")[0].split("-")[2]
        minutesBegin = beginDate.split(" ")[1].split(":")[0]
        secondsBegin = beginDate.split(" ")[1].split(":")[1]

        yearEnd = endDate.split(" ")[0].split("-")[0]
        monthEnd = endDate.split(" ")[0].split("-")[1]
        dayEnd = endDate.split(" ")[0].split("-")[2]
        minutesEnd = endDate.split(" ")[1].split(":")[0]
        secondsEnd = endDate.split(" ")[1].split(":")[1]

        # Calcular duración (end date - begin date)
        beginDateObject = datetime(int(yearBegin), int(monthBegin), int(dayBegin),
                                   int(minutesBegin), int(secondsBegin),
                                   00,
                                   00000)
        endDateObject = datetime(int(yearEnd), int(monthEnd), int(dayEnd),
                                 int(minutesEnd), int(secondsEnd),
                                 00,
                                 00000)
        duration = "+" + str(int((endDateObject - beginDateObject).total_seconds()))
        tornadoQuery = TornadoQuery(beginDate, county, duration)
        return tornadoQuery
