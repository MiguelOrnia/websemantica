import itertools
import json
import spacy
import textacy
from collections import OrderedDict, Counter
from random import random
from numerizer.numerizer import nlp
from tqdm import tqdm

""" Clase encargada de analizar los tuits disponibles en el dataset. Implementa dos funcionalidades 
de extraccion de informacion diferentes, estas son las siguientes: NER y KWIC """


class TuitsAnalyzer:
    """ Metodo de la clase TuitsAnalyzer encargado de aplicar la funcionalidad de extraccion de informacion NER
    (RECONOCIMIENTO DE ENTIDADES CON NOMBRE) """

    def ner(self, tuit):
        nlp = spacy.load("en_core_web_lg")

        destilado = {}

        doc = nlp(tuit)

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

        for etiqueta in destilado:
            print(etiqueta)

            entidades = destilado[etiqueta]

            entidades = dict(itertools.islice(entidades.items(), 10))
            print(json.dumps(entidades, sort_keys=False, indent=4))

        return destilado

    """ Metodo de la clase WordsAnalyzer encargado de aplicar la funcionalidad de extraccion de informacion KWIC
    (PALABRA CLAVE EN SU CONTEXTO). En este metodo se obtiene una tupla con la palabra clave en su contexto en la 
    posicion central """

    def textacy2(self, tuit, keyword):
        kwics = []

        doc = nlp(tuit)

        entities = textacy.extract.kwic.keyword_in_context(doc, keyword, window_width=30)
        entities_list = []
        for entity in entities:
            kwics.append(entity)
            entities_list.append(entity)

        for kwic in Counter(kwics).most_common(50):
            print(kwic)

        return entities_list

    """ Metodo de la clase WordsAnalyzer utilizado para obtener terminología de interes (palabras clave). Se ha 
    empleado para rellenar los diccionarios de palabras clave empleados """

    def yake(self, tuits):
        random.shuffle(tuits)
        concatenacion_tuits = ""

        with tqdm(total=len(tuits)) as barra:
            for tuit in tuits:
                concatenacion_tuits += (tuit + " ")
                if len(concatenacion_tuits) > 1000000:
                    break

                barra.update(1)

        concatenacion_tuits = concatenacion_tuits[0:1000000]

        doc = nlp(concatenacion_tuits.lower())

        rank = textacy.extract.keyterms.yake(doc, topn=40)

        for item in rank:
            print(item)
