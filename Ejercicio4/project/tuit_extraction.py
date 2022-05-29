""" Clase TuitExtraction donde se almacena la informacion extraida con NER y KWIC """


class TuitExtraction:
    def __init__(self, ner, textacy2):
        self.ner = ner
        self.textacy2 = textacy2
