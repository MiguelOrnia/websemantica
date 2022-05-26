import os
from datetime import datetime
from bs4 import BeautifulSoup
from extract_tornados.tornado_query import TornadoQuery
from util.date_helper import DateHelper

""" Clase TornadoExtractor encargada de obtener la informacion de los HTML relativa a los diferentes 
tornados existentes en la Storms Events Database """


class TornadoExtractor:
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

    """ Metodo privado de la clase TornadoExtractor encargado de extraer cierta informacion de los HTML """
    def __extraer_informacion(self, contenido, elemento):
        soup = BeautifulSoup(contenido, 'html.parser')
        todos_tds = soup.find_all("td")

        dato = ""

        for i in range(len(todos_tds)):
            contenidos_td = todos_tds[i].contents
            if elemento in contenidos_td:
                dato = todos_tds[i + 1].get_text()
                break

        return dato

    """ Metodo de la clase TornadoExtractor encargado de extraer el texto correspondiente a la narrativa 
    de un tornado """
    def extraer_narrativa(self, contenido):
        return self.__extraer_informacion(contenido, 'Event Narrative')

    """ Metodo de la clase TornadoScrapping encargado de extraer la escala de un tornado. 
     Este dato es necesario para obtener la velocidad del viento de un tornado en caso de que 
     no se pueda determinar mendiante la narrativa existente """
    def extraer_escala(self, contenido):
        return self.__extraer_informacion(contenido, '-- Scale')

    """ Metodo de la clase TornadoExtractor encargado en obtener la consulta a realizar en la API de Wikibase """
    def buscar_info(self, contenido):
        date_helper = DateHelper()
        soup = BeautifulSoup(contenido, 'html.parser')
        todos_tds = soup.find_all("td")

        for i in range(len(todos_tds)):
            contenidos_td = todos_tds[i].contents
            if 'County/Area' in contenidos_td:
                county = todos_tds[i + 1].get_text()
            if 'Begin Date' in contenidos_td:
                begin_date = todos_tds[i + 1].get_text()
            if 'End Date' in contenidos_td:
                end_date = todos_tds[i + 1].get_text()
                break

        year_begin = date_helper.calcular_anio(begin_date)
        month_begin = date_helper.calcular_mes(begin_date)
        day_begin = date_helper.calcular_dia(begin_date)
        minutes_begin = date_helper.calcular_minutos(begin_date)
        seconds_begin = date_helper.calcular_segundos(begin_date)

        year_end = date_helper.calcular_anio(end_date)
        month_end = date_helper.calcular_mes(end_date)
        day_end = date_helper.calcular_dia(end_date)
        minutes_end = date_helper.calcular_minutos(end_date)
        seconds_end = date_helper.calcular_segundos(end_date)

        begin_date_object = datetime(int(year_begin), int(month_begin), int(day_begin),
                                   int(minutes_begin), int(seconds_begin),
                                   00,
                                   00000)
        end_date_object = datetime(int(year_end), int(month_end), int(day_end),
                                 int(minutes_end), int(seconds_end),
                                 00,
                                 00000)
        scale = self.extraer_escala(contenido)
        duration = "+" + str(int((end_date_object - begin_date_object).total_seconds()))
        tornado_query = TornadoQuery(begin_date, county, duration, scale)
        return tornado_query
