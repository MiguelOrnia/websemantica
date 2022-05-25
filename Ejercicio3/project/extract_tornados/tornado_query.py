""" Clase TornadoQuery donde se almacena  la informacion a buscar en la instancia de Wikibase """


class TornadoQuery:
    """ Constructor de la clase TornadoQuery donde se reciben la fecha de inicio, el condado y la duracion """
    def __init__(self, begindate, county, duration):
        self.begindate = begindate
        self.county = county
        self.duration = duration

    """ Metodo  de la clase TornadoQuery que devuelve la consulta a realizar en la instancia 
    de Wikibase """
    def get_query(self):
        query = "tornado " + self.county + " " + self.begindate.split(" ")[0].split("-")[0]
        return query
