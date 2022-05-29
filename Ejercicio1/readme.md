# Ejercicio 1: Crear grafo de conocimiento con información sobre tornados

## Estructura de los directorios empleados
El ejercicio se compone de dos carpetas que se detallan a continuación:
- **graphs**: Incluye los tres grafos de conocimiento (**RDF - ttl**) desarrollados.
- **shex**: Incluye la **shape expression** correspondiente a los grafos de conocimiento creados y el Entity Schema creado para nuestra instancia de Wikibase.

## Tornados utilizados para el modelado y fuente de información usada
Los tornados empleados (obtenidos de la **Storm Events Database**) para la elaboración de los grafos de conocimientos son los siguientes:
- Datos del **grafo de conocimiento 1:** https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=936510
- Datos del **grafo de conocimiento 2:** https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=993011
- Datos del **grafo de conocimiento 3:** https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=943554

## Marcadores empleados para los grafos de conocimiento

Para almacenar información sobre los eventos y episodios nos hemos basado en los marcadores primarios y secundarios proporcionados en la asignatura:
- **enhancedFujitaScale**: Escala de Fujita Ampliada que sirve para medir la intensidad de un tornado 
- **length**: Longitud del evento (medido en **millas**)
- **width**: Ancho del evento (medido en **millas**)
- **beginDate**: Fecha de inicio del evento
- **location**: Ubicación donde ha acontecido el evento. En el se indican país, estado, condado y coordenadas
- **personalDamage**: Daños personales ocasionados (medido en **doláres estadounidenses**)
- **materialDamage**: Daños materiales ocasionados (medido en **doláres estadounidenses**)
- **source**: Fuente de información de la que proviene el evento
- **duration**: Duración del evento (medido en **segundos**)
- **movementSpeed**: Velocidad de movimiento del evento alcanzada (medida en **millas por hora**)
- **maxWindSpeed**: Máxima velocidad registrada por el evento (medida en **millas por hora**)
- **isLand**: Determina si el evento es marino o terrestre
- **hasEvents**: Eventos relacionados

## Ontologías,tipos de datos y uso de Wikidata en los grafos de conocimiento

En los tres grafos de conocimiento creados en este repositorio se han hecho uso de las siguientes ontologías, además de Wikidata. Por otro lado, para completar
los tipos se han utilizado Schema.org y XML Schema:
- Ontología **Sweet** de eventos metereológicos: Hemos empleado esta ontología para los tipos de eventos y la escala de Fujita Ampliada
- Ontología **OM** para unidades: Hemos empleado esta ontología para indicar las unidades de los diferentes marcadores mencionados previamente
- **Schema.org**: Se utiliza para el tipo de localización y estado
- **XML Schema**: Se emplea para tipos como decimales, enteros, fecha y duración (en segundos)
- **Wikidata**: Hemos empleado Wikidata para referenciar a algunos tipos como por ejemplo condado y país

## Instancia de Wikibase creada y rellenada con los tornados
En nuestra instancia de **Wikibase** se introdujeron manualmente los tres tornados citados previamente. Los enlaces para acceder a dichos tornados son los siguientes:
- **Tornado de Leon (Florida, EEUU)** acontecido en 2021 correspondiente con el **grafo de conocimiento 1**: http://156.35.98.119/wiki/Item:Q4
- **Tornado de Bradford (Florida, EEUU)** acontecido en 2021 correspondiente con el **grafo de conocimiento 2**: http://156.35.98.119/wiki/Item:Q19
- **Tornado de Manatee (Florida, EEUU)** acontencido en 2021 correspondiente con el **grafo de conocimiento 3**: http://156.35.98.119/wiki/Item:Q24

Por otro lado, para realizar consultas **SPARQL** se debe utilizar el siguiente endpoint: http://156.35.98.119:8834/

Ejemplo de consulta con **SPARQL** para obtener todos los tornados existentes en nuestra instancia de Wikibase mostrando cierta información sobre ellos:
```
SELECT DISTINCT ?tornadoName ?scaleValue ?source ?countryName ?stateName ?countyName WHERE {
  ?tornado  wdt:P3 wd:Q5 .
  ?tornado  wdt:P18 ?scale .
  ?tornado  wdt:P16 ?source .
  ?tornado  wdt:P5 ?country .
  ?tornado  wdt:P6 ?state .
  ?tornado  wdt:P8 ?county .
  ?tornado  rdfs:label ?tornadoName .
  ?scale  rdfs:label ?scaleValue .
  ?country  rdfs:label ?countryName .
  ?state  rdfs:label ?stateName .
  ?county  rdfs:label ?countyName 
}
```

## Despliegue de Apache Jena Fuseki
Se ha desplegado un Apache Jena Fuseki (versión **4.5.0**) y se han cargado los tres grafos de conocimiento en este. A continuación, se muestran los endpoints necesarios para acceder a dicho despliegue: 
- Enlace para acceder al Apache Jena Fuseki desplegado: http://156.35.98.116:3030/#/
- Enlace para realizar consultas **SPARQL**: http://156.35.98.116:3030/#/dataset/tornados/query

Ejemplo de consulta con **SPARQL** para obtener todos los tornados existentes en nuestro despliegue de Apache Jena Fuseki mostrando cierta información sobre ellos:
  ```
  PREFIX : <http://example.com/>
  PREFIX schema: <http://schema.org/>
  PREFIX st: <http://sweetontology.net/phenAtmoPrecipitation/>
  PREFIX sostst: <http://sweetontology.net/stateStorm/>
  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

  SELECT DISTINCT ?tornado ?scale ?beginDate ?source WHERE {
    ?tornado  rdf:type st:Tornado .  
    ?tornado  sostst:EnhancedFujitaScale ?scale .
    ?tornado  :beginDate ?beginDate .
    ?tornado  :source ?source .
  }
  ORDER BY ?beginDate
  ```
