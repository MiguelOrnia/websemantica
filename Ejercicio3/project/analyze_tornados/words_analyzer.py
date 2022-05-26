import spacy
import textacy
import itertools
import json
from collections import OrderedDict

""" Clase encargada de analizar los documentos HTML con tornados obtenidos. Implementa dos funcionalidades 
de extraccion de informacion diferentes, estas son las siguientes: NER y KWIC """


class WordsAnalyzer:
    """ Metodo de la clase WordsAnalyzer encargado de aplicar la funcionalidad de extraccion de informacion NER
    (RECONOCIMIENTO DE ENTIDADES CON NOMBRE) """

    def ner(self, informe):
        nlp = spacy.load("en_core_web_lg")

        doc = nlp(informe)

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

        for etiqueta in destilado:
            destilado[etiqueta] = OrderedDict(destilado[etiqueta])
            print(etiqueta)

            entidades = destilado[etiqueta]

            entidades = dict(itertools.islice(entidades.items(), 5))
            print(json.dumps(entidades, sort_keys=False, indent=4))

        return destilado

    """ Metodo de la clase WordsAnalyzer encargado de aplicar la funcionalidad de extraccion de informacion KWIC
    (PALABRA CLAVE EN SU CONTEXTO). En este metodo se obtienen tripletas sujeto-verbo-objeto con textacy """

    def textacy1(self, informe):
        nlp = spacy.load('en_core_web_lg')

        doc = nlp(informe)

        entities = textacy.extract.triples.subject_verb_object_triples(doc)

        contador = 0
        for entity in entities:
            print(entity)
            contador += 1
            if contador > 40:
                break
        return entities

    """ Metodo de la clase WordsAnalyzer encargado de aplicar la funcionalidad de extraccion de informacion KWIC
    (PALABRA CLAVE EN SU CONTEXTO). En este metodo se obtiene una tupla con la palabra clave en su contexto en la 
    posicion central """

    def textacy2(self, informe, keyword):
        nlp = spacy.load("en_core_web_lg")
        doc = nlp(informe)
        entities = textacy.extract.kwic.keyword_in_context(doc, keyword, window_width=30)

        entitiesList = []
        for entity in entities:
            print(entity)
            entitiesList.append(entity)

        return entitiesList




