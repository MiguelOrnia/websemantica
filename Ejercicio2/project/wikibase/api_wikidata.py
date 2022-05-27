import requests

""" Clase WikidataApi encargada de conectar con la API de Wikidata """


class WikidataApi:

    """ ENDPOINT de la API de Wikidata """
    WIKIDATA_API_ENDPOINT = "https://www.wikidata.org/w/api.php"

    """ Metodo de la clase WikidataApi encargado de buscar un item o propiedad en Wikidata """
    def search(self, query, search_type='item'):
        params = {
            'action': 'wbsearchentities',
            'format': 'json',
            'language': 'en',
            'search': query,
            'type': search_type,
            'limit': 50
        }

        response = requests.get(self.WIKIDATA_API_ENDPOINT, params=params)
        return response.json()['search']

    """ Metodo de la clase WikidataApi encargado de obtener una propiedad de un item """
    def get_property_by_item(self, item_id, property_id):
        params = {
            'action': 'wbgetclaims',
            'format': 'json',
            'entity': item_id,
            'property': property_id
        }

        response = requests.get(self.WIKIDATA_API_ENDPOINT, params=params)
        return response.json()['claims'][property_id]
