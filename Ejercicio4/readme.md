# Ejercicio 4: Rellenar el grafo de conocimiento con datos de Twitter
## Datos utilizados para la realización del ejercicio
Para llevar a cabo este ejercicio se ha hecho uso de los tweets proporcionados en el dataset siguiente: https://drive.google.com/file/d/1RY32b2ucUhIibd1OCkhTL2kluAeE8puI/view

Básicamente se han extraído los tweets más completos (debían tener localización, fecha, tipo de evento y en algunos casos velocidad del viento) para crear eventos en nuestra instancia de Wikibase.

## Librerías empleadas
A continuación se van a enumerar las librerías utilizadas para desarrollar el ejercicio:
- **Geopy**: La hemos aplicado para obtener una ciudad y estado dadas unas coordenadas
- **Wikibase-api**: La hemos aplicado para poder realizar peticiones a nuestra instancia de Wikibase y poder insertar la información de los eventos analizados
- **Numerizer**: La hemos empleado para poder convertir cifras representadas como una cadena de carácteres a un número

## Estructura del proyecto
- **data**: Contiene los HTML del dataset empleado
- **keywords_dictionaries**: Palabras clave empleadas en KWIC. Se han divido en diferentes ficheros en función del tipo de evento
- **extract_tuits**: Contiene una clase para extraer la información de los tweets
- **analyze_tuits**: Contiene una clase para aplicar NER y KWIC sobre el tweet a analizar
- **util**: Contiene una clase para tratar cadenas, para dar formato a la información a guardar, y otra para formatear fechas
- **wikibase**: Contiene una clase para acceder a Wikibase

## Enlace a la instancia de Wikibase
Este es el enlace para acceder a la instancia de Wikibase utilizada: http://156.35.98.119/wiki/Main_Page

## Consideraciones finales
Como se mencionaba previamente, para que un tweet se considerase relevante y completo para crear el evento se han establecido las siguientes condiciones: Debe tener localización, debe tener una fecha asociada para poder trazar cuando se ha producido el evento, debe conocerse el tipo de evento acontecido y por último, aunque no es de aplicación en todos los casos, debe poderse conocer la velocidad del viento asociada al evento.

Por otra parte, cabe destacar que en algunos casos se ha detectado que, aún teniendo coordenadas, su ubicación era imprecisa apuntando a localizaciones no trazables (veáse un océano), por lo que en esos casos también se ha descartado el tweet.

Por último, no se ha podido aplicar sobre la totalidad del dataset, pero se ha podido realizar sobre un subconjunto de este. Esto se debe a que nuestra instancia de Wikibase emitía un error de no permitir más peticiones HTTP seguidas, por lo que se ha realizado sobre un subconjunto de 2000 tweets.
