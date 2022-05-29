import requests

query = """  prefix : <http://example.com/> 
prefix st: <http://sweetontology.net/phenAtmoPrecipitation/>
prefix sostst: <http://sweetontology.net/stateStorm/>
prefix sophatmoc: <http://sweetontology.net/phenAtmoCloud/>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix xsd: <http://www.w3.org/2001/XMLSchema#>
prefix schema: <http://schema.org/>
prefix wikidata: <http://www.wikidata.org/entity/>
prefix om: <http://www.ontology-of-units-of-measure.org/resource/om-2/>

INSERT DATA
{
:tornado rdf:type st:Tornado ;
    sostst:EnhancedFujitaScale sostst:EF1 ;
    :length [ rdf:type om:Measure; om:hasNumericalValue "0.85"^^xsd:decimal; om:hasUnit om:mile-Statute ] ;
    :width  [ rdf:type om:Measure; om:hasNumericalValue "50.0"^^xsd:decimal; om:hasUnit om:yard-International ] ;
    schema:location :location ;
    :beginDate     "2021-01-27T11:30:00"^^xsd:dateTime ;
    :personalDamage :personalDamage ; 
    :materialDamage :materialDamage ;
    :source :NWSStormSurvey ;
    :duration "PT60S"^^xsd:duration ;
    :movementSpeed [ rdf:type om:Measure; om:hasNumericalValue "50.0"^^xsd:decimal; om:hasUnit om:mile-StatutePerHour ] ; 
    :maxWindSpeed [ rdf:type om:Measure; om:hasNumericalValue "90.0"^^xsd:decimal; om:hasUnit om:mile-StatutePerHour ] ; 
    :isLand true ;
    :hasEvents   :ocheessee, :andrew .

:materialDamage rdf:type :Damage;
    :propertyDamage [ rdf:type om:Measure; om:hasNumericalValue "5000.0"^^xsd:decimal; om:hasUnit om:UnitedStatesDollar ] ;
    :cropDamage [ rdf:type om:Measure; om:hasNumericalValue "0.0"^^xsd:decimal; om:hasUnit om:UnitedStatesDollar ] .
    
:personalDamage rdf:type :Damage;
    :injuries 0 ;
    :deaths 0 .

:location rdf:type schema:location;
    :country :US ;
    :state :Florida ;
    :county :Leon ;
    :lat 30.4182 ;
    :long -84.5522 .

:ocheessee rdf:type :Event ;
    :beginDate "2021-01-27T08:36:00"^^xsd:dateTime ;
    :eventCounty :Calhoun ;
    :typeEvent sophatmoc:FunnelCloud .
    
:andrew rdf:type :Event ;
    :beginDate "2021-01-27T11:37:00"^^xsd:dateTime ;
    :eventCounty :Leon ;
    :typeEvent st:Tornado .

:US rdf:type wikidata:Q6256 .
:Florida rdf:type schema:state .
:Calhoun rdf:type wikidata:Q28575 .
:Leon rdf:type wikidata:Q28575 .

}   """

response = requests.post('http://156.35.98.116:3030/tornados/update',
                         data={'query': query})
print(response)
