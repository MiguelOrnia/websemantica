# Ejercicio 3: Rellenar el grafo de conocimiento con datos en lenguaje natural

## Datos utilizados para la realización del ejercicio
Para llevar a cabo este ejercicio se ha hecho uso de los HTML proporcionados en el dataset siguiente: https://drive.google.com/file/d/17sFuZxT25UIFle1WPrPe7HIwlFUVW6hI/view

Básicamente se han extraído los párrafos informativos de cada tornado para complementar la información extraída en el ejercicio 2.

## Librerías empleadas
A continuación se van a enumerar las librerías utilizadas para desarrollar el ejercicio:
- **BeautifulSoup**: La hemos aplicado para poder hacer scrapping de los HTML citados
- **Wikibase-api**: La hemos aplicado para poder realizar peticiones a nuestra instancia de Wikibase y poder insertar la información de los eventos analizados
- **Numerizer**: La hemos empleado para poder convertir cifras representadas como una cadena de carácteres a un número

## Funcionalidades de extracción de información utilizadas
Para capturar la información requerida hemos aplicado NER y KWIC. En el primer caso nos ha permitido obtener cantidades fundamentalmente (útil para extraer la velocidad del viento de un evento) y en el segundo caso nos ha resultado útil para poder extraer información sobre si el tornado ha sido marino o terrestre, además de poder corroborar la información obtenida con NER.

## Estructura del proyecto
- **data**: Contiene los HTML del dataset empleado
- **keywords_dictionaries**: Palabras clave empleadas KWIC. Se han divido en diferentes ficheros en función de su utilidad
- **extract_tornados**: Contiene una clase para extraer la información de los HTML
- **analyze_tornado**: Contiene una clase para aplicar NER y KWIC sobre el tornado a analizar
- **util**: Contiene una clase para tratar cadenas, para dar formato a la información a guardar
- **wikibase**: Contiene una clase para acceder a Wikibase

## Consideraciones finales
En los casos en los que no hemos obtenido explícitamente en la narrativa del evento la velocidad, se ha optado por calcular la velocidad que ha alcanzado en función de su escala de Fujita ampliada, dado que para cada valor de esta escala tiene asociados un valor máximo y mínimo. Por otro lado, con ambos extremos también hemos podido verificar si la velocidad obtenida del párrafo informativo es adecuada o no para la escala de ese tornado. Fuente utilizada: https://www.weather.gov/tae/ef_scale
