import itertools
import json
from collections import OrderedDict, Counter
from random import random

import spacy
import textacy
from numerizer.numerizer import nlp
from tqdm import tqdm


class TuitsAnalyzer:
    def ner(self, tuit):
        nlp = spacy.load("en_core_web_lg")

        destilado = {}

        # Recordad, no se pasa a minúsculas puesto que la capitalización es muy
        # importante para reconocer entidades con nombre

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

    # TEXTACY

    """Extracción de keywords in context (palabras clave en su contexto)"""

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

    """YAKE método utilizado para obtener terminología de interés (palabras clave)"""

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
