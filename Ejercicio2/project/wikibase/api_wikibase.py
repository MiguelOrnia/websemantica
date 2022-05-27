from wikibase_api import Wikibase

""" Clase WikibaseApi encargada de conectar con la API de nuestra instancia de Wikibase """


class WikibaseApi:
    """ Constantes de la clase WikibaseApi. INSTANCE_URL se corresponde con la URL de la instancia
    de Wikibase. BOT_USERNAME se corresponde con el nombre de usuario del bot creado en la instancia de
    Wikibase utilizada. BOT_PASSWORD se corresponde con la clave del bot creado """
    INSTANCE_URL = 'http://156.35.98.119'
    INSTANCE_URL_API = INSTANCE_URL + '/w/api.php'
    BOT_USERNAME = 'Admin'
    BOT_PASSWORD = 'bot@9eomjq89fmimaa11t2gilnkh64ed398p'

    """ Constructor de la clase WikibaseApi. En el se inicializan las credenciales del bot de la instancia yç
     el objeto correspondiente a la conexion con la API """

    def __init__(self):
        self.credentials = {
            'bot_username': self.BOT_USERNAME,
            'bot_password': self.BOT_PASSWORD,
        }

        self.wb = Wikibase(
            api_url=self.INSTANCE_URL_API,
            oauth_credentials={},
            login_credentials=self.credentials,
            is_bot=True
        )

    """ Metodo de la clase WikibaseApi encargado en realizar una busqueda en Wikibase obteniendo el id buscado. 
    Si no se establece el tipo (propiedad o item), realiza una busqueda como item"""
    def get_id_by_query(self, query, query_type='item'):
        if len(self.wb.entity.search(query, 'en', query_type)['search']) == 0:
            return []
        return self.wb.entity.search(query, 'en', query_type)['search'][0]['id']

    """ Metodo de la clase WikibaseApi encargado en realizar una busqueda en Wikibase. Obtiene las propiedades
    asociadas a un item concreto """
    def get_item_claims_by_query(self, query):
        tornado_id = self.wb.entity.search(query, 'en')['search'][0]['id']
        return list(self.wb.entity.get(tornado_id, ['claims'], ['en'])['entities'][tornado_id]['claims'].keys())

    """ Metodo privado de la clase WikibaseApi encargado de obtener el claim id de una propiedad de un item """
    def __get_claim_id(self, id_entity, id_property):
        return self.wb.entity.get(id_entity)['entities'][id_entity]['claims'][id_property][0]['id']

    """ Metodo de la clase WikibaseApi encargado de modificar una propiedad de un item dado """
    def update_claim(self, id_entity, id_property, value):
        claim_id = self.__get_claim_id(id_entity, id_property)
        self.wb.claim.update(claim_id, value)

    """ Metodo de la clase WikibaseApi encargado de crear una propiedad """
    def add_claim(self, id_entity, id_property, value):
        self.wb.claim.add(id_entity, id_property, value)

    """ Metodo de la clase WikibaseApi encargado de poner un valor de velocidad maxima a un tornado """
    def set_max_wind_speed(self, tornado_query, speed):
        id_property = self.get_id_by_query('maxWindSpeed', 'property')
        id_entity = self.get_id_by_query(tornado_query)
        id_units = self.get_id_by_query('Miles Per Hour')
        speed_value = {"amount": speed, "unit": self.INSTANCE_URL + '/entity/' + id_units}
        if id_property in self.get_item_claims_by_query(tornado_query):
            self.update_claim(id_entity, id_property, speed_value)
        else:
            self.add_claim(id_entity, id_property, speed_value)

    """ Metodo de la clase WikibaseApi encargado de indicar si es terrestre o marino un tornado """
    def set_land_or_marine(self, tornado_query, tornado_type):
        id_property = self.get_id_by_query('landOrMarine', 'property')
        id_entity = self.get_id_by_query(tornado_query)
        if id_property in self.get_item_claims_by_query(tornado_query):
            self.update_claim(id_entity, id_property, tornado_type)
        else:
            self.add_claim(id_entity, id_property, tornado_type)

    """ Metodo de la clase WikibaseApi encargado de crear un item o propiedad """
    def insert(self, content, insert_type='item'):
        return self.wb.entity.add(insert_type, content)

    """ Metodo de la clase WikibaseApi encargado de actualizar un item """
    def update(self, content, update_type='item'):
        self.wb.entity.update(update_type, content)
