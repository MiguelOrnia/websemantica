from wikibase_api import Wikibase

""" Clase WikibaseApi encargada de conectar con la API de nuestra instancia de Wikibase """


class WikibaseApi:
    """ Constantes de la clase WikibaseApi. INSTANCE_URL se corresponde con la URL de la instancia
    de Wikibase. BOT_USERNAME se corresponde con el nombre de usuario del bot creado en la instancia de
    Wikibase utilizada. BOT_PASSWORD se corresponde con la clave del bot creado """
    INSTANCE_URL = 'http://156.35.98.119/w/api.php'
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
            api_url=self.INSTANCE_URL,
            oauth_credentials=None,
            login_credentials=self.credentials,
            is_bot=True
        )

    """ Metodo de la clase WikibaseApi encargado en crear un nuevo item en Wikibase """
    def insert(self, content):
        r = self.wb.entity.add("item")
        # content = {"labels": {"en": {"language": "en", "value": "Updated label"}}}
        updated = self.wb.entity.update(r["entity"]["id"], content=content)
        print(updated)
