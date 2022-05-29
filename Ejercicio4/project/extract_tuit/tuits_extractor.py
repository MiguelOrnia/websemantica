import json
from extract_tuit.tuit_info import TuitInfo

""" Clase TuitExtractor encargada de obtener la informacion de los tuits existentes en el dataset """


class TuitExtractor:
    """ Constante que almacena la ruta al dataset con tuis """
    TUITS_FILE_PATH = "data/tweets-tornadoes-high_accuracy-expanded.ndjson"

    def __init__(self):
        self.tuits = []

    """ Metodo de la clase TornadoExtractor encargado de cargar los diferentes tuits. En primer lugar, 
     para agregar un tuit debe tener una localizacion, sino no se tiene en consideracion la informacion
     que puede almacenar """
    def cargar_tuits(self):
        lineas = open(self.TUITS_FILE_PATH, encoding="utf8").readlines()

        for linea in lineas:
            tuit = json.loads(linea)

            if tuit["place"] is not None:
                full_text = tuit["full_text"]
                created_at = tuit["created_at"]
                if tuit["place"]["bounding_box"] is not None:
                    longitude = tuit["place"]["bounding_box"]["coordinates"][0][0][0]
                    latitude = tuit["place"]["bounding_box"]["coordinates"][0][0][1]
                    tuit_info = TuitInfo(full_text, created_at, longitude, latitude)
                    self.tuits.append(tuit_info)

        return self.tuits
