# Ejercicio 1: Crear grafo de conocimiento con información sobre tornados

## Estructura de los directorios empleados
El ejercicio se compone de dos carpetas que se detallan a continuación:
- **graphs**: Incluye los tres grafos de conocimiento (**RDF - ttl**) desarrollados.
- **shex**: Incluye la **shape expression** correspondiente a los grafos de conocimiento creados.

## Tornados utilizados para el modelado y fuente de información usada
Los tornados empleados (obtenidos de la **Storm Events Database**) para la elaboración de los grafos de conocimientos son los siguientes:
- Datos del **grafo de conocimiento 1:** https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=936510
- Datos del **grafo de conocimiento 2:** https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=993011
- Datos del **grafo de conocimiento 3:** https://www.ncdc.noaa.gov/stormevents/eventdetails.jsp?id=943554

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
