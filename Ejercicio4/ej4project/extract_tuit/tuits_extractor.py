import json

from extract_tuit.tuit_info import TuitInfo


class TuitExtractor:
    def __init__(self):
        self.tuits = []

    def cargarTuits(self):
        lineas = open("data/tweets-tornadoes-high_accuracy-expanded.ndjson", encoding="utf8").readlines()


        for linea in lineas:
            tuit = json.loads(linea)

            # Si el tuit tiene localización lo agregmos a tuits
            if tuit["place"] is not None:
                full_text = tuit["full_text"]
                created_at = tuit["created_at"]
                if tuit["place"]["bounding_box"] is not None:
                    longitude = tuit["place"]["bounding_box"]["coordinates"][0][0][0]
                    latitude = tuit["place"]["bounding_box"]["coordinates"][0][0][1]
                    tuit_info = TuitInfo(full_text, created_at, longitude, latitude)
                    self.tuits.append(tuit_info)

        return self.tuits