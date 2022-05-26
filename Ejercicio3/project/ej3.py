from numerizer import numerize
from analyze_tornados.words_analyzer import WordsAnalyzer
from tornado_extraction import TornadoExtraction
from extract_tornados.tornados_extractor import TornadoExtractor
from util.fujita_scale_helper import FujitaScaleHelper
from wikibase.api_wikibase import WikibaseApi

""" Rutas para acceder a los ficheros que contienen las palabras clave a emplear """
KEYWORDS_IN_CONTEXT_SPEED_PATH = "keywords_dictionaries/keywords_in_context_speed.txt"
KEYWORDS_IN_CONTEXT_LAND_PATH = "keywords_dictionaries/keywords_in_context_land.txt"
KEYWORDS_IN_CONTEXT_MARINE_PATH = "keywords_dictionaries/keywords_in_context_marine.txt"

""" Funcion principal del ejercicio 3 """


def ej3():
    tornados_scrapping = TornadoExtractor()
    words_analyzer = WordsAnalyzer()
    api_wikibase = WikibaseApi()
    tornados = []
    informes = tornados_scrapping.cargar_documentos()

    for i in range(len(informes)):
        dic_textacy2 = {}
        contenido = informes[i]
        narrative = tornados_scrapping.extraer_narrativa(contenido)
        scale = tornados_scrapping.extraer_escala(contenido)
        informes[i] = narrative
        tornado_query = tornados_scrapping.buscar_info(contenido)

        print("-------------NER " + str(i + 1) + " --------------")
        # Lista con tipos: {'ORDINAL': OrderedDict([('first', 7), ('second', 3)])... #JSON
        ner_value = words_analyzer.ner(informes[i])

        print("------------TEXTACY " + str(i + 1) + " --------------")

        print("***textacy2 " + str(i + 1) + " ****")
        file = open(KEYWORDS_IN_CONTEXT_SPEED_PATH, "r")
        for line in file:
            textacy2_value = words_analyzer.textacy2(informes[i], line.rstrip())
            if len(textacy2_value) > 0:
                dic_textacy2[line.rstrip()] = textacy2_value
        file = open(KEYWORDS_IN_CONTEXT_LAND_PATH, "r")
        for line in file:
            textacy2_value = words_analyzer.textacy2(informes[i], line.rstrip())
            if len(textacy2_value) > 0:
                dic_textacy2[line.rstrip()] = textacy2_value
        file = open(KEYWORDS_IN_CONTEXT_MARINE_PATH, "r")
        for line in file:
            textacy2_value = words_analyzer.textacy2(informes[i], line.rstrip())
            if len(textacy2_value) > 0:
                dic_textacy2[line.rstrip()] = textacy2_value
        print(dic_textacy2)
        tornado = TornadoExtraction(ner_value, dic_textacy2)
        tornados.append(tornado)
        print(tornado.textacy2)

        # Analizar la info obtenida
        # NER
        tornado_values = extract_with_ner(tornado, {})

        # TEXTACY2
        tornado_values = extract_speed_with_textacy2(tornado, tornado_values, KEYWORDS_IN_CONTEXT_SPEED_PATH, scale)
        tornado_values = extract_type_with_textacy2(tornado, tornado_values, KEYWORDS_IN_CONTEXT_LAND_PATH, "isLand")
        tornado_values = extract_type_with_textacy2(tornado, tornado_values, KEYWORDS_IN_CONTEXT_MARINE_PATH, "isMarine")

        print(tornado_values)
        api_wikibase.set_tornado_values(tornado_query, int(tornado_values['speedWind']), get_land_or_marine(tornado_values))


""" Funcion encargada de comprobar si es marino o terrestre """


def get_land_or_marine(tornado_values):
    if tornado_values['isLand']:
        return 'Land'
    elif tornado_values['isMarine']:
        return 'Marine'
    return None


""" Funcion encargada de recoger los valores obtenidos con NER """


def extract_with_ner(tornado, tornado_values):
    if "QUANTITY" in tornado.ner:
        quantity_ner = tornado.ner["QUANTITY"]
        print(quantity_ner)
        for quantity in quantity_ner:
            if "mph" in quantity[0].lower():
                tornado_values["speedWind"] = numerize(quantity[0])
            if "miles per hour" in quantity[0].lower():
                tornado_values["speedWind"] = numerize(quantity[0])

    if "LOC" in tornado.ner:
        location_ner = tornado.ner["LOC"]
        if len(location_ner) > 0:
            tornado_values["isLand"] = True

    if "FAC" in tornado.ner:
        fac_ner = tornado.ner["FAC"]
        if len(fac_ner) > 0:
            tornado_values["isLand"] = True
    return tornado_values


""" Funcion encargada de recoger la velocidad obtenida con KWIC """


def extract_speed_with_textacy2(tornado, tornado_values, file, scale):
    file = open(file, "r")
    exist_speed = False
    fujita_scale_helper = FujitaScaleHelper()
    for line in file:
        for key in tornado.textacy2:
            max = 0

            if line.rstrip() in key:
                exist_speed = True
                speed_in_context = tornado.textacy2[key]

                if len(speed_in_context) > 1:
                    for speed in speed_in_context:
                        words = speed[0].split(" ")
                        value = int(words[len(words) - 2])
                        if fujita_scale_helper.check_speed_by_fujita_scale(value, scale):
                            max = value
                    if max == 0:
                        value = fujita_scale_helper.get_speed_by_fujita_scale(scale)
                    else:
                        value = max
                else:
                    words = speed_in_context[0][0].split(" ")
                    value = words[len(words) - 2]
                tornado_values["speedWind"] = value
    if not exist_speed:
        tornado_values["speedWind"] = str(fujita_scale_helper.get_speed_by_fujita_scale(scale))

    return tornado_values


""" Funcion encargada de recoger si es marino o terrestre con KWIC """


def extract_type_with_textacy2(tornado, tornado_values, file, property_name):
    file = open(file, "r")
    for line in file:
        for key in tornado.textacy2:
            if line.rstrip('\n') in key:
                tornado_values[property_name] = True
    return tornado_values
