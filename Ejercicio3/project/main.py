from ej3 import ej3
from wikibase.api_wikibase import WikibaseApi

""" Se rellena la instancia de Wikibase a partir 
de informacion obtenida en las narrativas de tornados 
proporcionados por la Storm Events Database. 
Previamente se han cargado los tornados en Wikibase 
y ahora se completa su informacion """
if __name__ == '__main__':
    #ej3()
    apiwikibase = WikibaseApi()
    id = apiwikibase.search("tornado Leon 2021")[0]
    print(id)
    apiwikibase.update(id, 50.0)
