""" Clase StringsHelper para formatear cadenas de caracteres """


class StringsHelper:

    """ Metodo de la clase StringsHelper encargado de formatear una cadena de caracteres
    para que su primera letra sea mayuscula y las siguientes minusculas """
    def formatear_mayusculas(self, cadena):
        primera_letra = False
        cadena_formateada = cadena[0]
        for word in cadena:
            if word != cadena[0] or primera_letra:
                cadena_formateada += word.lower()
                primera_letra = True
        return cadena_formateada

    """ Metodo de la clase StringsHelper encargado de formatear una cadena de caracteres
    para que su todas sus letras sean minusculas """
    def formatear_minusculas(self, cadena):
        return cadena.lower()
