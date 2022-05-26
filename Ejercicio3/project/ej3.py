from numerizer import numerize
from analyze_tornados.words_analyzer import WordsAnalyzer
from tornado_extraction import TornadoExtraction
from extract_tornados.tornados_extractor import TornadoScrapping
import itertools


def ej3():
    tornados_scrapping = TornadoScrapping()
    words_analyzer = WordsAnalyzer()
    tornados = []
    informes = tornados_scrapping.cargarDocumentos()

    for i in range(len(informes)):
        dicTextacy2 = {}
        contenido = informes[i]
        narrative = tornados_scrapping.extraer_narrativa(contenido)
        scale = tornados_scrapping.extraer_escala(contenido)
        informes[i] = narrative
        print("-------------NER " + str(i + 1) + " --------------")
        # Lista con tipos: {'ORDINAL': OrderedDict([('first', 7), ('second', 3)])... #JSON
        nerValue = words_analyzer.ner(informes[i])

        print("------------TEXTACY " + str(i + 1) + " --------------")

        print("***textacy1 " + str(i + 1) + " ****")
        textacy1Value = words_analyzer.textacy1(informes[i])

        print("***textacy2 " + str(i + 1) + " ****")
        file = open("keywords_dictionaries/keywords_in_context_speed.txt", "r")
        for line in file:
            textacy2Value = words_analyzer.textacy2(informes[i], line.rstrip())
            if len(textacy2Value)>0:
                dicTextacy2[line.rstrip()] = textacy2Value
        file = open("keywords_dictionaries/keywords_in_context_land.txt", "r")
        for line in file:
            textacy2Value = words_analyzer.textacy2(informes[i], line.rstrip())
            if len(textacy2Value)>0:
                dicTextacy2[line.rstrip()] = textacy2Value
        file = open("keywords_dictionaries/keywords_in_context_marine.txt", "r")
        for line in file:
            textacy2Value = words_analyzer.textacy2(informes[i], line.rstrip())
            if len(textacy2Value)>0:
                dicTextacy2[line.rstrip()] = textacy2Value
        print(dicTextacy2)
        tornado = TornadoExtraction(nerValue, textacy1Value, dicTextacy2)
        tornados.append(tornado)
        print(tornado.textacy1)
        print(tornado.textacy2)

        # Analizar la info obtenida
        # NER
        tornadoValues = extractWithNer(tornado, {})

        # TEXTACY1
        tornadoValues = extractWithTextacy1(tornado, tornadoValues, "keywords_dictionaries/keywords_triples_land.txt",
                                            "isLand")
        tornadoValues = extractWithTextacy1(tornado, tornadoValues, "keywords_dictionaries/keywords_triples_marine.txt",
                                            "isMarine")

        # TEXTACY2
        tornadoValues = extractSpeedWithTextacy2(tornado, tornadoValues,
                                                 "keywords_dictionaries/keywords_in_context_speed.txt", scale)
        tornadoValues = extractTypeWithTextacy2(tornado, tornadoValues,
                                                "keywords_dictionaries/keywords_in_context_land.txt", "isLand")
        tornadoValues = extractTypeWithTextacy2(tornado, tornadoValues,
                                                "keywords_dictionaries/keywords_in_context_marine.txt", "isMarine")

        print(tornadoValues)


def extractWithNer(tornado, tornadoValues):
    if "QUANTITY" in tornado.ner:
        quantityNer = tornado.ner["QUANTITY"]
        print(quantityNer)
        for quantity in quantityNer:
            if "mph" in quantity[0].lower():
                tornadoValues["speedWind"] = numerize(quantity[0])+" mph"
            if "miles per hour" in quantity[0].lower():
                tornadoValues["speedWind"] = numerize(quantity[0])+" mph"

    if "LOC" in tornado.ner:
        locationNer = tornado.ner["LOC"]
        if len(locationNer) > 0:
            tornadoValues["isLand"] = True

    if "FAC" in tornado.ner:
        facNer = tornado.ner["FAC"]
        if len(facNer) > 0:
            tornadoValues["isLand"] = True
    return tornadoValues


def extractWithTextacy1(tornado, tornadovalues, file, property):
    file = open(file, "r")
    for line in file:
        for entity in tornado.textacy1:
            if line.rstrip() in entity.subject:
                tornadovalues[property] = True
            if line.rstrip() in entity.object:
                tornadovalues[property] = True
    return tornadovalues


def extractSpeedWithTextacy2(tornado, tornadovalues, file, scale):
    file = open(file, "r")
    existSpeed = False
    for line in file:
        for key in tornado.textacy2:
            max = 0
            value = 0

            if line.rstrip() in key:
                existSpeed = True
                speedInContext = tornado.textacy2[key]

                if len(speedInContext)>1:
                    for speed in speedInContext:
                        words = speed[0][0].split(" ")
                        value = int(words[len(words) - 2])
                        if checkSpeedByFujitaScale(value, scale):
                            max = value
                    if max == 0:
                        value = getSpeedByFujitaScale(scale)
                    else:
                        value = max
                else:
                    words = speedInContext[0][0].split(" ")
                    value = words[len(words) - 2]
                tornadovalues["speedWind"] = str(value) + " mph"
    if not existSpeed:
        tornadovalues["speedWind"] = str(getSpeedByFujitaScale(scale)) + " mph"

    return tornadovalues

def checkSpeedByFujitaScale(value, scale):
    if scale == "EF0" and 65 <= value <= 85:
        return True
    elif scale == "EF1" and 86 <= value <= 110:
        return True
    elif scale == "EF2" and 111 <= value <= 135:
        return True
    elif scale == "EF3" and 136 <= value <= 165:
        return True
    elif scale == "EF4" and 166 <= value <= 200:
        return True
    elif scale == "EF5" and value>=201:
        return True
    return False

def getSpeedByFujitaScale(scale):
    if scale == "EF0":
        return (65+85)/2
    elif scale == "EF1":
        return (86+110)/2
    elif scale == "EF2":
        return (111+135)/2
    elif scale == "EF3":
        return (136+165)/2
    elif scale == "EF4":
        return (166+200)/2
    elif scale == "EF5":
        return 201

def extractTypeWithTextacy2(tornado, tornadovalues, file, property):
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
