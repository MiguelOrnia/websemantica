""" Clase TuitInfo donde se almacena la informacion extraida de un tuit concreto """


class TuitInfo:
    def __init__(self, full_text, created_at, longitude, latitude):
        self.full_text = full_text
        self.created_at = created_at
        self.longitude = longitude
        self.latitude = latitude
