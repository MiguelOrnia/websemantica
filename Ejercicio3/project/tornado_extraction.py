""" Clase TornadoExtraction donde se almacena la informacion extraida con NER y KWIC """


class TornadoExtraction:
    def __init__(self, ner, textacy2):
        self.ner = ner
        self.textacy2 = textacy2
