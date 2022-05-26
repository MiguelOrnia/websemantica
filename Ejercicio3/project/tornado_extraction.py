""" Clase TornadoExtraction donde se almacena la informacion extraida con NER y KWIC """


class TornadoExtraction:
    def __init__(self, ner, textacy1, textacy2):
        self.ner = ner
        self.textacy1 = textacy1
        self.textacy2 = textacy2