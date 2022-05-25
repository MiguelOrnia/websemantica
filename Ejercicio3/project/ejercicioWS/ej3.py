import os
from datetime import datetime

from bs4 import BeautifulSoup
import spacy
import itertools
import json
import textacy
from collections import OrderedDict

from numerizer import numerize

from ejercicioWS.tornadoinfo import TornadoInfo
from ejercicioWS.tornadoquery import TornadoQuery

ruta = "StormEventsDatabase-Dayton-tornado/"


def ej3():
    informes = []
    tornados = []
    cargarDocumentos(informes)
    for i in range(len(informes)):
        dicTextacy2 = {}
        contenido = informes[i]
        narrative = extraer_narrativa(contenido)
        informes[i] = narrative
        print("-------------NER " + str(i + 1) + " --------------")
        nerValue = ner(informes[i])  # Lista con tipos: {'ORDINAL': OrderedDict([('first', 7), ('second', 3)])... #JSON

        print("------------TEXTACY " + str(i + 1) + " --------------")

        print("***textacy1 " + str(i + 1) + " ****")
        textacy1Value = textacy1(informes[i])

        print("***textacy2 " + str(i + 1) + " ****")
        file = open("keywordsInContextSpeed.txt", "r")
        for line in file:
            textacy2Value = textacy2(informes[i], line.rstrip())
            dicTextacy2[line.rstrip()] = textacy2Value
        file = open("keywordsInContextLand.txt", "r")
        for line in file:
            textacy2Value = textacy2(informes[i], line.rstrip())
            dicTextacy2[line.rstrip()] = textacy2Value
        file = open("keywordsInContextMarine.txt", "r")
        for line in file:
            textacy2Value = textacy2(informes[i], line.rstrip())
            dicTextacy2[line.rstrip()] = textacy2Value

        tornado = TornadoInfo(nerValue, textacy1Value, dicTextacy2)
        tornados.append(tornado)
        print(tornado.textacy1)
        print(tornado.textacy2)

        # Analizar la info obtenida
        # NER
        tornadoValues = extractWithNer(tornado, {})

        # TEXTACY1
        tornadoValues = extractWithTextacy1(tornado, tornadoValues, "")
        tornadoValues = extractWithTextacy1(tornado, tornadoValues, "")

        # TEXTACY2
        tornadoValues = extractWithTextacy2(tornado, tornadoValues, "")
        tornadoValues = extractWithTextacy2(tornado, tornadoValues, "")
        tornadoValues = extractWithTextacy2(tornado, tornadoValues, "")


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


# RECONOCIMIENTO DE ENTIDADES CON NOMBRE (NER)
def ner(informes):
    """Reconocimiento de entidades con nombre (NER)"""
    nlp = spacy.load("en_core_web_lg")  # Modelo utilizado

    # ¡Atención! No pasamos el texto a minúsculas pues la capitalización aquí es crucial

    doc = nlp(informes)

    destilado = {}

    for entidad in doc.ents:

        etiqueta = entidad.label_

        texto = entidad.text

        if etiqueta in destilado:
            if texto in destilado[etiqueta]:
                destilado[etiqueta][texto] += 1
            else:
                destilado[etiqueta][texto] = 1
        else:
            destilado[etiqueta] = {}

    # Las etiquetas dependen del modelo que se este utilizando
    for etiqueta in destilado:
        destilado[etiqueta] = OrderedDict(destilado[etiqueta])
        print(etiqueta)

        entidades = destilado[etiqueta]

        entidades = dict(itertools.islice(entidades.items(), 5))
        print(json.dumps(entidades, sort_keys=False, indent=4))

    return destilado


# EXTRACCIÓN DE INFORMACIÓN CON TEXTACY
def textacy1(informes):
    """Obtención de tripletas sujeto-verbo-objeto con textacy"""
    nlp = spacy.load('en_core_web_lg')

    doc = nlp(informes)

    entities = textacy.extract.triples.subject_verb_object_triples(doc)

    contador = 0
    for entity in entities:
        print(entity)
        contador += 1
        if contador > 40:
            break
    return entities


def textacy2(informes, keyword):
    """Extracción de keywords in context (palabra clave en su contexto)"""
    nlp = spacy.load("en_core_web_lg")  # Modelo utilizado
    doc = nlp(informes)
    entities = textacy.extract.kwic.keyword_in_context(doc, keyword, window_width=30)

    for entity in entities:
        print(entity)
    return entities


# CARGAR DOCUMENTOS Y EXTRAER NARRATIVA
def cargarDocumentos(informes):
    for fichero in os.listdir(ruta):
        contenido = open(ruta + fichero, "r").read()
        informes.append(contenido)


def extraer_narrativa(contenido):
    soup = BeautifulSoup(contenido, 'html.parser')
    todos_tds = soup.find_all("td")

    narrative = ""

    for i in range(len(todos_tds)):
        contenidos_td = todos_tds[i].contents
        if 'Event Narrative' in contenidos_td:
            narrative = todos_tds[i + 1].get_text()
            break

    return narrative


def buscar_info(contenido):
    # Extraer info del html
    soup = BeautifulSoup(contenido, 'html.parser')
    todos_tds = soup.find_all("td")

    for i in range(len(todos_tds)):
        contenidos_td = todos_tds[i].contents
        if 'County/Area' in contenidos_td:
            county = todos_tds[i + 1].get_text()
        if 'Begin Date' in contenidos_td:
            beginDate = todos_tds[i + 1].get_text()
        if 'End Date' in contenidos_td:
            endDate = todos_tds[i + 1].get_text()
            break

    yearBegin = beginDate.split(" ")[0].split("-")[0]
    monthBegin = beginDate.split(" ")[0].split("-")[1]
    dayBegin = beginDate.split(" ")[0].split("-")[2]
    minutesBegin = beginDate.split(" ")[1].split(":")[0]
    secondsBegin = beginDate.split(" ")[1].split(":")[1]

    yearEnd = endDate.split(" ")[0].split("-")[0]
    monthEnd = endDate.split(" ")[0].split("-")[1]
    dayEnd = endDate.split(" ")[0].split("-")[2]
    minutesEnd = endDate.split(" ")[1].split(":")[0]
    secondsEnd = endDate.split(" ")[1].split(":")[1]

    # Calcular duración (end date - begin date)
    beginDateObject = datetime(int(yearBegin), int(monthBegin), int(dayBegin),
                               int(minutesBegin), int(secondsBegin),
                               00,
                               00000)
    endDateObject = datetime(int(yearEnd), int(monthEnd), int(dayEnd),
                             int(minutesEnd), int(secondsEnd),
                             00,
                             00000)
    duration = "+" + str(int((endDateObject - beginDateObject).total_seconds()))
    tornadoQuery = TornadoQuery(beginDate, county, duration)


def search_tornado(tornadoquery):
    # Código de wikibase
    # Items con ids por label (lista de tornados)
    # Obtener id de las propiedades: beginDate, county, duration
    # Recorremos la lista de tornados y comprobamos que coinciden las propiedades
    # Si coindicen actualizamos el tornado con las nuevas propiedades
    return 0
