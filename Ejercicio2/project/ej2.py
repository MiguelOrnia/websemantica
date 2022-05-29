import numpy as np
from datetime import datetime
from extract_tornados.tornados_extractor import TornadosExtractor
from util.strings_helper import StringsHelper
from wiki.api_wikibase import WikibaseApi
from wiki.api_wikidata import WikidataApi

""" Constantes con las URL de nuestra instancia de Wikibase y de Wikidata """
WIKIBASE_URL = 'http://156.35.98.119'
WIKIDATA_URL = 'https://www.wikidata.org'


""" Funcion principal con el ejercicio 2 implementado """


def ej2():
    tornados_extractor = TornadosExtractor()
    api_wikibase = WikibaseApi()
    api_wikidata = WikidataApi()
    formatear_cadenas = StringsHelper()
    informes = tornados_extractor.cargar_documentos()

    for i in range(len(informes)):
        contenido = informes[i]
        tabla_info = tornados_extractor.get_table_info(contenido)
        eventos_relacionados = tornados_extractor.get_related_events_info(contenido)
        print(eventos_relacionados)

        info = obtener_info(tabla_info)

        scale = info[1]
        length = round(float(info[2].split(" ")[0]), 2)
        width = round(float(info[3].split(" ")[0]), 2)
        state = info[4]
        state = formatear_cadenas.formatear_mayusculas(state)
        county = info[5]
        county = formatear_cadenas.formatear_mayusculas(county)

        source = info[7]
        anio_begin = info[9].split('-')[0]
        mes_begin = info[9].split('-')[1]
        anio_end = info[12].split('-')[0]
        mes_end = info[12].split('-')[1]
        end_date = info[12]
        begin_date = info[9]
        lat = round(float(info[11].split('/')[0]), 4)
        lon = round(float(info[11].split('/')[1]), 4)
        deaths = info[15].split('/')[0]
        injuries = info[16].split('/')[0]
        property_damage = convert_damage(info[17])
        crop_damage = convert_damage(info[18])

        begin_date_object = obtener_fecha(anio_begin, mes_begin, begin_date)
        end_date_object = obtener_fecha(anio_end, mes_end, end_date)

        duration = (end_date_object - begin_date_object).total_seconds()

        duration_hours = duration / 3600

        movement_speed = length / duration_hours

        initial_content = {"labels": {"en": {"language": "en", "value": "tornado " + county + " " + anio_begin + " "
                                + str(i)}}, "descriptions": {'en': {'language': 'en', 'value': 'weather event'}}}
        tornado = api_wikibase.insert(initial_content)

        id_entity = tornado['entity']['id']
        api_wikibase.add_claim(id_entity, api_wikibase.get_id_by_query('instance of', 'property'),
                               {'entity-type': 'item', 'id': api_wikibase.get_id_by_query('tornado')})
        api_wikibase.add_claim(id_entity, api_wikibase.get_id_by_query('Enhanced Fujita Scale', 'property'),
                               {'entity-type': 'item', 'id': api_wikibase.get_id_by_query(scale)})
        api_wikibase.add_claim(id_entity, api_wikibase.get_id_by_query('length', 'property'),
                               {'amount': length, 'unit': WIKIBASE_URL + '/entity/'
                                                          + api_wikibase.get_id_by_query('mile')})
        api_wikibase.add_claim(id_entity, api_wikibase.get_id_by_query('width', 'property'),
                               {'amount': width, 'unit': WIKIBASE_URL + '/entity/'
                                                          + api_wikibase.get_id_by_query('mile')})
        api_wikibase.add_claim(id_entity, api_wikibase.get_id_by_query('country', 'property'),
                               {'entity-type': 'item', 'id': api_wikibase.get_id_by_query('United States of America')})

        if len(api_wikibase.get_id_by_query(state)) == 0:
            results = api_wikidata.search(state)
            instance_of_result = api_wikidata.search('instance of', 'property')[0]['id']
            state_result = api_wikidata.search('United States state')[0]['id']
            url_wikidata_property = api_wikibase.get_id_by_query('urlWikiData', 'property')
            for result in results:
                result_id = result['id']
                property_instance_of = api_wikidata.get_property_by_item(result_id, instance_of_result)[0]
                instance_of_value_id = property_instance_of['mainsnak']['datavalue']['value']['id']
                if state_result in instance_of_value_id:
                    new_state = api_wikibase.insert({"labels": {"en": {"language": "en", "value": state}}})
                    api_wikibase.add_claim(new_state['entity']['id'], api_wikibase.get_id_by_query('instance of', 'property'),
                                           {'entity-type': 'item', 'id': api_wikibase.get_id_by_query('state')})
                    api_wikibase.add_claim(new_state['entity']['id'], url_wikidata_property, WIKIDATA_URL
                                                                       + '/wiki/Item:' + result_id)
                    api_wikibase.add_claim(id_entity, api_wikibase.get_id_by_query('state', 'property'),
                                           {'entity-type': 'item', 'id': new_state['entity']['id']})
                    break
        else:
            api_wikibase.add_claim(id_entity, api_wikibase.get_id_by_query('state', 'property'),
                                   {'entity-type': 'item', 'id': api_wikibase.get_id_by_query(state)})

        if len(api_wikibase.get_id_by_query(county)) == 0:
            results = api_wikidata.search(county + ' County')
            instance_of_result = api_wikidata.search('instance of', 'property')[0]['id']
            county_result = api_wikidata.search('county of ' + state)[0]['id']
            url_wikidata_property = api_wikibase.get_id_by_query('urlWikiData', 'property')
            for result in results:
                result_id = result['id']
                property_instance_of = api_wikidata.get_property_by_item(result_id, instance_of_result)[0]
                instance_of_value_id = property_instance_of['mainsnak']['datavalue']['value']['id']
                if county_result in instance_of_value_id:
                    new_county = api_wikibase.insert({"labels": {"en": {"language": "en", "value": county}}})
                    api_wikibase.add_claim(new_county['entity']['id'], api_wikibase.get_id_by_query('instance of', 'property'),
                                           {'entity-type': 'item', 'id': api_wikibase.get_id_by_query('county')})
                    api_wikibase.add_claim(new_county['entity']['id'], url_wikidata_property, WIKIDATA_URL + '/wiki/Item:'
                                           + result_id)
                    api_wikibase.add_claim(id_entity, api_wikibase.get_id_by_query('county', 'property'),
                                           {'entity-type': 'item', 'id': new_county['entity']['id']})
                    break
        else:
            api_wikibase.add_claim(id_entity, api_wikibase.get_id_by_query('county', 'property'),
                                   {'entity-type': 'item', 'id': api_wikibase.get_id_by_query(county)})

        api_wikibase.add_claim(id_entity, api_wikibase.get_id_by_query('beginDate', 'property'),
                               begin_date.split(" ")[0] + "T" + begin_date.split(" ")[1] + ":00")
        api_wikibase.add_claim(id_entity, api_wikibase.get_id_by_query('injuries', 'property'),
                               {'amount': injuries, 'unit': '1'})
        api_wikibase.add_claim(id_entity, api_wikibase.get_id_by_query('deaths', 'property'),
                               {'amount': deaths, 'unit': '1'})
        api_wikibase.add_claim(id_entity, api_wikibase.get_id_by_query('propertyDamage', 'property'),
                               {'amount': property_damage, 'unit': WIKIBASE_URL + '/entity/'
                                                            + api_wikibase.get_id_by_query('United States dollar')})
        api_wikibase.add_claim(id_entity, api_wikibase.get_id_by_query('cropDamage', 'property'),
                               {'amount': crop_damage, 'unit': WIKIBASE_URL + '/entity/'
                                                                   + api_wikibase.get_id_by_query('United States dollar')})
        api_wikibase.add_claim(id_entity, api_wikibase.get_id_by_query('source', 'property'), source)
        api_wikibase.add_claim(id_entity, api_wikibase.get_id_by_query('duration', 'property'),
                               {'amount': duration, 'unit': WIKIBASE_URL + '/entity/'
                                                          + api_wikibase.get_id_by_query('second')})
        create_has_events(eventos_relacionados, api_wikibase, id_entity, formatear_cadenas)
        api_wikibase.add_claim(id_entity, api_wikibase.get_id_by_query('latitude', 'property'),
                               {'amount': lat, 'unit': '1'})
        api_wikibase.add_claim(id_entity, api_wikibase.get_id_by_query('longitude', 'property'),
                               {'amount': lon, 'unit': '1'})
        api_wikibase.add_claim(id_entity, api_wikibase.get_id_by_query('movementSpeed', 'property'),
                               {'amount': movement_speed, 'unit': WIKIBASE_URL + '/entity/'
                                                            + api_wikibase.get_id_by_query('Miles Per Hour')})


""" Funcion encargada de devolver la informacion del tornado estructurada """


def obtener_info(tornado):
    info = list()
    for campo in tornado:
        info.append(campo.text)
    info = np.delete(info, (0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40))
    return info


""" Funcion encargada de devolver los eventos relacionados correspondientes """


def find_events(events, api_wikibase, formatear_cadenas):
    entities = list()
    i = 0
    for event in events:
        i += 1
        location = formatear_cadenas.formatear_localizacion(event[1], formatear_cadenas)
        label = event[4].split("/")[2] + " " + location + ' ' + event[4] + ' ' + event[5].strip()
        response = api_wikibase.get_id_by_query(label)
        if len(response) != 0:
            entities.append(response)
        else:
            date = event[4].split("/")[2] + "-" + event[4].split("/")[0] + "-" + event[4].split("/")[1] + "T" + event[
                5].strip() + ":00"
            county = formatear_cadenas.formatear_mayusculas(event[2].split(" ")[0])
            id_county = api_wikibase.get_id_by_query(county)
            type_event = api_wikibase.get_id_by_query(event[7])
            initial_content = {"labels": {
                "en": {"language": "en", "value": label}},
                "descriptions": {'en': {'language': 'en', 'value': event[7]}}}
            new_event = api_wikibase.insert(initial_content)
            event_id = new_event['entity']['id']

            api_wikibase.add_claim(event_id, api_wikibase.get_id_by_query('beginDate', 'property'), date)

            if len(id_county) == 0:
                new_county = api_wikibase.insert({"labels": {"en": {"language": "en", "value": county}}})
                id_county = new_county['entity']['id']
                api_wikibase.add_claim(new_county['entity']['id'], api_wikibase.get_id_by_query('instance of', 'property'),
                                       {'entity-type': 'item', 'id': api_wikibase.get_id_by_query('county')})

            if len(type_event) == 0:
                new_type_event = api_wikibase.insert({"labels": {"en": {"language": "en", "value":
                    formatear_cadenas.formatear_minusculas(event[7])}}})
                type_event = new_type_event['entity']['id']
                api_wikibase.add_claim(new_type_event['entity']['id'],
                                api_wikibase.get_id_by_query('instance of', 'property'),
                                {'entity-type': 'item', 'id': api_wikibase.get_id_by_query('atmospheric phenomenon')})

            api_wikibase.add_claim(event_id, api_wikibase.get_id_by_query('county', 'property'),
                                   {'entity-type': 'item', 'id': id_county})
            api_wikibase.add_claim(event_id, api_wikibase.get_id_by_query('typeEvent', 'property'),
                                   {'entity-type': 'item', 'id': type_event})

            entities.append(new_event["entity"]["id"])

    return entities


""" Funcion encargada de crear los eventos relacionados """


def create_has_events(eventos_relacionados, api_wikibase, id_entity, formatear_cadenas):
    has_events = find_events(eventos_relacionados, api_wikibase, formatear_cadenas)
    for e in has_events:
        api_wikibase.add_claim(id_entity, api_wikibase.get_id_by_query('hasEvents', 'property'),
                               {'entity-type': 'item', 'id': e})


""" Funcion encargada de formatear los danios acontecidos """


def convert_damage(damage):
    if "M" in damage:
        return float(damage.split("M")[0]) * 1000000
    if "K" in damage:
        return float(damage.split("K")[0]) * 1000


""" Funcion encargada de calcular la fecha de un tornado"""


def obtener_fecha(anio, mes, date):
    return datetime(int(anio), int(mes), int(date.split(" ")[0].split("-")[2]),
                                 int(date.split(" ")[1].split(":")[0]),
                                 int(date.split(" ")[1].split(":")[1]), 00,
                                 00000)
