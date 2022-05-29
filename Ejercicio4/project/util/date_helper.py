""" Clase DateHelper encargada de cuestiones relacionadas con fechas """


class DateHelper:
    def __init__(self):
        pass

    """ Metodo de la clase DateHelper encargado de formatear la fecha adecuadamente (mm/dd/yy)"""

    def format_date(self, date):
        words = date.split(" ")
        new_date = str(self.__get_month(words[1])) + "/" + words[2] + "/" + words[5]
        return new_date

    """ Metodo de la clase DateHelper encargado de formatear un tiempo dado """
    def format_time(self, time):
        words = time.split(" ")
        new_time = words[3]
        return new_time

    """ Metodo auxiliar de la clase DateHelper encargado de obtener el mes (int) para una cadena dada """
    def __get_month(self, month_name):
        if month_name == "Jan":
            return 1
        elif month_name == "Feb":
            return 2
        elif month_name == "Mar":
            return 3
        elif month_name == "Apr":
            return 4
        elif month_name == "May":
            return 5
        elif month_name == "Jun":
            return 6
        elif month_name == "Jul":
            return 7
        elif month_name == "Aug":
            return 8
        elif month_name == "Sep":
            return 9
        elif month_name == "Oct":
            return 10
        elif month_name == "Nov":
            return 11
        else:
            return 12

    """ Metodo de la clase DateHelper que comprueba si una cadena tiene el formato mm/dd/yy de fecha """
    def check_date_by_slash(self, date):
        try:
            datetime.strptime(date, "%m/%d/%y")
            return True
        except ValueError as err:
            return False

    """ Metodo de la clase DateHelper que comprueba si una cadena tiene el formato mm-dd-yy de fecha """
    def check_date_by_middle_dash(self, date):
        try:
            datetime.strptime(date, "%m-%d-%y")
            return True
        except ValueError as err:
            return False

    """ Metodo que formatea la fecha para incluirla en Wikibase """
    def format_wikibase_date(self, date, time):
        date_fragmentada = date.split('/')
        date_formateada = date_fragmentada[2] + '-' + date_fragmentada[0]+ '-' + date_fragmentada[1] + 'T'
        time_formateado = time + ':00'
        return date_formateada + time_formateado
