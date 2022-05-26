from numerizer import numerize
from analyze_tornados.words_analyzer import WordsAnalyzer
from tornado_extraction import TornadoExtraction
from extract_tornados.tornados_extractor import TornadoScrapping
from util.fujita_scale_helper import FujitaScaleHelper

""" Rutas para acceder a los ficheros que contienen las palabras clave a emplear """
KEYWORDS_IN_CONTEXT_SPEED_PATH = "keywords_dictionaries/keywords_in_context_speed.txt"
KEYWORDS_IN_CONTEXT_LAND_PATH = "keywords_dictionaries/keywords_in_context_land.txt"
KEYWORDS_IN_CONTEXT_MARINE_PATH = "keywords_dictionaries/keywords_in_context_marine.txt"


def ej3():
    tornados_scrapping = TornadoScrapping()
    words_analyzer = WordsAnalyzer()
    tornados = []
    informes = tornados_scrapping.cargar_documentos()

    for i in range(len(informes)):
        dic_textacy2 = {}
        contenido = informes[i]
        narrative = tornados_scrapping.extraer_narrativa(contenido)
        scale = tornados_scrapping.extraer_escala(contenido)
        informes[i] = narrative
        print("-------------NER " + str(i + 1) + " --------------")
        # Lista con tipos: {'ORDINAL': OrderedDict([('first', 7), ('second', 3)])... #JSON
        ner_value = words_analyzer.ner(informes[i])

        print("------------TEXTACY " + str(i + 1) + " --------------")

        print("***textacy2 " + str(i + 1) + " ****")
        file = open("keywords_dictionaries/keywords_in_context_speed.txt", "r")
        for line in file:
            textacy2_value = words_analyzer.textacy2(informes[i], line.rstrip())
            if len(textacy2_value) > 0:
                dic_textacy2[line.rstrip()] = textacy2_value
        file = open("keywords_dictionaries/keywords_in_context_land.txt", "r")
        for line in file:
            textacy2_value = words_analyzer.textacy2(informes[i], line.rstrip())
            if len(textacy2_value) > 0:
                dic_textacy2[line.rstrip()] = textacy2_value
        file = open("keywords_dictionaries/keywords_in_context_marine.txt", "r")
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


def extract_with_ner(tornado, tornadoValues):
    if "QUANTITY" in tornado.ner:
        quantity_ner = tornado.ner["QUANTITY"]
        print(quantity_ner)
        for quantity in quantity_ner:
            if "mph" in quantity[0].lower():
                tornadoValues["speedWind"] = numerize(quantity[0])+" mph"
            if "miles per hour" in quantity[0].lower():
                tornadoValues["speedWind"] = numerize(quantity[0])+" mph"

    if "LOC" in tornado.ner:
        location_ner = tornado.ner["LOC"]
        if len(location_ner) > 0:
            tornadoValues["isLand"] = True

    if "FAC" in tornado.ner:
        fac_ner = tornado.ner["FAC"]
        if len(fac_ner) > 0:
            tornadoValues["isLand"] = True
    return tornadoValues


def extract_speed_with_textacy2(tornado, tornado_values, file, scale):
    file = open(file, "r")
    exist_speed = False
    fujita_scale_helper = FujitaScaleHelper()
    for line in file:
        for key in tornado.textacy2:
            max = 0
            value = 0

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
                tornado_values["speedWind"] = str(value) + " mph"
    if not exist_speed:
        tornado_values["speedWind"] = str(fujita_scale_helper.get_speed_by_fujita_scale(scale)) + " mph"

    return tornado_values


def extract_type_with_textacy2(tornado, tornadovalues, file, property):
    file = open(file, "r")
    for line in file:
        for key in tornado.textacy2:
            prueba= tornado.textacy2[key]
            if line.rstrip('\n') in key:
                tornadovalues[property] = True
    return tornadovalues


def search_tornado(tornadoquery):
    # Código de wikibase
    # Items con ids por label (lista de tornados)
    # Obtener id de las propiedades: beginDate, county, duration
    # Recorremos la lista de tornados y comprobamos que coinciden las propiedades
    # Si coindicen actualizamos el tornado con las nuevas propiedades
    return 0
