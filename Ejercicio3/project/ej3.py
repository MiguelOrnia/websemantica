from numerizer import numerize
from analyze_tornados.words_analyzer import WordsAnalyzer
from tornado_extraction import TornadoExtraction
from extract_tornados.tornados_extractor import TornadoScrapping


def ej3():
    tornados_scrapping = TornadoScrapping()
    words_analyzer = WordsAnalyzer()
    tornados = []
    informes = tornados_scrapping.cargarDocumentos()

    for i in range(len(informes)):
        dicTextacy2 = {}
        contenido = informes[i]
        narrative = tornados_scrapping.extraer_narrativa(contenido)
        informes[i] = narrative
        print("-------------NER " + str(i + 1) + " --------------")
        # Lista con tipos: {'ORDINAL': OrderedDict([('first', 7), ('second', 3)])... #JSON
        nerValue = words_analyzer.ner(informes[i])

        print("------------TEXTACY " + str(i + 1) + " --------------")

        print("***textacy1 " + str(i + 1) + " ****")
        textacy1Value = words_analyzer.textacy1(informes[i])

        print("***textacy2 " + str(i + 1) + " ****")
        file = open("keywords_in_context_speed.txt", "r")
        for line in file:
            textacy2Value = words_analyzer.textacy2(informes[i], line.rstrip())
            dicTextacy2[line.rstrip()] = textacy2Value
        file = open("keywords_in_context_land.txt", "r")
        for line in file:
            textacy2Value = words_analyzer.textacy2(informes[i], line.rstrip())
            dicTextacy2[line.rstrip()] = textacy2Value
        file = open("keywords_in_context_marine.txt", "r")
        for line in file:
            textacy2Value = words_analyzer.textacy2(informes[i], line.rstrip())
            dicTextacy2[line.rstrip()] = textacy2Value

        tornado = TornadoExtraction(nerValue, textacy1Value, dicTextacy2)
        tornados.append(tornado)
        print(tornado.textacy1)
        print(tornado.textacy2)

        # Analizar la info obtenida
        # NER
        tornadoValues = extractWithNer(tornado, {})

        # TEXTACY1
        tornadoValues = extractWithTextacy1(tornado, tornadoValues, "keywords_triples_land.txt", "isLand")
        tornadoValues = extractWithTextacy1(tornado, tornadoValues, "keywords_triples_marine.txt", "isMarine")

        # TEXTACY2
        tornadoValues = extractSpeedWithTextacy2(tornado, tornadoValues, "keywords_in_context_speed.txt")
        tornadoValues = extractTypeWithTextacy2(tornado, tornadoValues, "keywords_in_context_land.txt", "isLand")
        tornadoValues = extractTypeWithTextacy2(tornado, tornadoValues, "keywords_in_context_marine.txt", "isMarine")


def extractWithNer(tornado, tornadoValues):
    if "QUANTITY" in tornado.ner:
        quantityNer = tornado.ner["QUANTITY"]
        print(quantityNer)
        for quantity in quantityNer:
            if "mph" in quantity[0].lower():
                tornadoValues["speedWind"] = numerize(quantity[0])
            if "miles per hour" in quantity[0].lower():
                tornadoValues["speedWind"] = numerize(quantity[0])

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


def extractSpeedWithTextacy2(tornado, tornadovalues, file):
    file = open(file, "r")
    for line in file:
        for tupla in tornado.textacy2:
            if line.rstrip() in tupla[1]:
                if line.rstrip() == "mph":
                    words = tupla[0].split(" ")
                    tornadovalues["speedWind"] = numerize(words[len(words) - 1]) + " mph"
    return tornadovalues


def extractTypeWithTextacy2(tornado, tornadovalues, file, property):
    file = open(file, "r")
    for line in file:
        for tupla in tornado.textacy2:
            if line.rstrip() in tupla[1]:
                tornadovalues[property] = True
    return tornadovalues

def search_tornado(tornadoquery):
    # Código de wikibase
    # Items con ids por label (lista de tornados)
    # Obtener id de las propiedades: beginDate, county, duration
    # Recorremos la lista de tornados y comprobamos que coinciden las propiedades
    # Si coindicen actualizamos el tornado con las nuevas propiedades
    return 0
