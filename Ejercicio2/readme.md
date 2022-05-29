# Ejercicio 2: Rellenar el grafo de conocimiento con datos estructurados

## Datos utilizados para la realización del ejercicio
Para llevar a cabo este ejercicio se ha hecho uso de los HTML proporcionados en el dataset siguiente: https://drive.google.com/file/d/17sFuZxT25UIFle1WPrPe7HIwlFUVW6hI/view

Básicamente se han analizado estos HTML y se ha extraído de ellos la información almacenada en la tabla de cada evento, de acuerdo a la estructura mencionada en el ejercicio 1.

## Librerías empleadas
A continuación se van a enumerar las librerías utilizadas para desarrollar el ejercicio:
- **BeautifulSoup**: La hemos aplicado para poder hacer scrapping de los HTML citados
- **Wikibase-api**: La hemos aplicado para poder realizar peticiones a nuestra instancia de Wikibase y poder insertar la información de los eventos analizados
- **Requests**: La hemos utilizado para realizar peticiones HTTP a la API de Wikidata

## Vinculación de la información con Wikidata
Para mantener una relación entre los eventos y sus propiedades (creados en nuestra instancia de Wikibase) y las entidades ya existentes en Wikidata, se ha creado una propiedad específica que muestra una URL de ese mismo contenido pero en Wikidata. De esta forma permite consultar dicha información y relacionarla con nodos ya existentes en el grafo de conocimiento de Wikidata. Cabe destacar que no en todos los casos ha sido viable enlazar los contenidos con Wikidata pero si se ha conseguido en ciertas ocasiones.

## Estructura del proyecto
- **data**: Contiene los HTML del dataset empleado
- **extract_tornados**: Contiene una clase para extraer la información de los HTML
- **util**: Contiene una clase para tratar cadenas, para dar formato a la información a guardar
- **wiki**: Contiene dos clases, una para acceder a Wikibase y otra para acceder a Wikidata
