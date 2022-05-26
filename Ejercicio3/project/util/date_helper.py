""" Clase encargada de realizar calculos relativos a fechas """


class DateHelper:

    """ Metodo de la clase DateHelper encargado de calcular el anio de un fecha """
    def calcular_anio(self, date):
        return date.split(" ")[0].split("-")[0]

    """ Metodo de la clase DateHelper encargado de calcular el mes de un fecha """
    def calcular_mes(self, date):
        return date.split(" ")[0].split("-")[1]

    """ Metodo de la clase DateHelper encargado de calcular el dia de un fecha """
    def calcular_dia(self, date):
        return date.split(" ")[0].split("-")[2]

    """ Metodo de la clase DateHelper encargado de calcular los minutos de un fecha """
    def calcular_minutos(self, date):
        return date.split(" ")[1].split(":")[0]

    """ Metodo de la clase DateHelper encargado de calcular los segundos de un fecha """
    def calcular_segundos(self, date):
        return date.split(" ")[1].split(":")[1]
