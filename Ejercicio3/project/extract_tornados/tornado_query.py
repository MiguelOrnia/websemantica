""" Clase TornadoQuery donde se almacena  la informacion a buscar en la instancia de Wikibase """


class TornadoQuery:
    """ Constructor de la clase TornadoQuery donde se reciben la fecha de inicio, el condado y la duracion """
    def __init__(self, begindate, county, duration):
        self.begindate = begindate
        self.county = self.formatear_mayusculas(county)
        self.duration = duration

    """ Metodo  de la clase TornadoQuery que devuelve la consulta a realizar en la instancia 
    de Wikibase """
    def get_query(self):
        query = "tornado " + self.county + " " + self.begindate.split(" ")[0].split("-")[0]
        return query

    def formatear_mayusculas(self, cadena):
        primera_letra = False
        cadena_formateada = cadena[0]
        for word in cadena:
            if word != cadena[0] or primera_letra:
                cadena_formateada += word.lower()
                primera_letra = True
        return cadena_formateada
