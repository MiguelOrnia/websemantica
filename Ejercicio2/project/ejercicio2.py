import numpy as np
from datetime import datetime
from extract_tornados.tornados_extractor import TornadosExtractor
from wikibase.api_wikibase import WikibaseApi
from wikibase.api_wikidata import WikidataApi

WIKIBASE_URL = 'http://156.35.98.119'
WIKIDATA_URL = 'https://www.wikidata.org'


def ej2():
    tornados_extractor = TornadosExtractor()
    api_wikibase = WikibaseApi()
    api_wikidata = WikidataApi()
    informes = tornados_extractor.cargar_documentos()

    for i in range(len(informes)):
        contenido = informes[i]
        tabla_info = tornados_extractor.get_table_info(contenido)
        eventos_relacionados = tornados_extractor.get_related_events_info(contenido)
        print(eventos_relacionados)

        info = obtener_info(tabla_info)

        scale = info[1]
        length = round(float(info[2].split(" ")[0]), 2)
        width = float(info[3].split(" ")[0])
        state = info[4]
        state = formatear_mayusculas(state)
        county = info[5]
        county = formatear_mayusculas(county)

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

        begin_date_object = datetime(int(anio_begin), int(mes_begin), int(begin_date.split(" ")[0].split("-")[2]),
                                   int(begin_date.split(" ")[1].split(":")[0]),
                                   int(begin_date.split(" ")[1].split(":")[1]), 00,
                                   00000)

        end_date_object = datetime(int(anio_end), int(mes_end), int(end_date.split(" ")[0].split("-")[2]),
                                 int(end_date.split(" ")[1].split(":")[0]), int(end_date.split(" ")[1].split(":")[1]), 00,
                                 00000)

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
        create_has_events(eventos_relacionados, api_wikibase, api_wikidata, anio_begin, id_entity)
        api_wikibase.add_claim(id_entity, api_wikibase.get_id_by_query('latitude', 'property'),
                               {'amount': lat, 'unit': '1'})
        api_wikibase.add_claim(id_entity, api_wikibase.get_id_by_query('longitude', 'property'),
                               {'amount': lon, 'unit': '1'})
        api_wikibase.add_claim(id_entity, api_wikibase.get_id_by_query('movementSpeed', 'property'),
                               {'amount': movement_speed, 'unit': WIKIBASE_URL + '/entity/'
                                                            + api_wikibase.get_id_by_query('Miles Per Hour')})


def formatear_mayusculas(cadena):
    primera_letra = False
    cadena_formateada = cadena[0]
    for word in cadena:
        if word != cadena[0] or primera_letra:
            cadena_formateada += word.lower()
            primera_letra = True
    return cadena_formateada


def obtener_info(tornado):
    info = list()
    for campo in tornado:
        info.append(campo.text)
    info = np.delete(info, (0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40))
    return info


def find_events(events, api_wikibase, api_wikidata, anio_begin):
    entities = list()
    i = 0
    for event in events:
        i += 1
        label = event[4].split("/")[2] + " " + formatear_mayusculas(event[1])
        response = api_wikibase.get_id_by_query(label)
        if len(response) != 0:
            entities.append(response)
        else:
            date = event[4].split("/")[2] + "-" + event[4].split("/")[0] + "-" + event[4].split("/")[1] + "T" + event[
                5].strip() + ":00"
            county = formatear_mayusculas(event[2].split(" ")[0])
            id_county = api_wikibase.get_id_by_query(county)
            type_event = api_wikibase.get_id_by_query(event[7])
            initial_content = {"labels": {
                "en": {"language": "en", "value": anio_begin + " " + county + " " + str(i)}},
                "descriptions": {'en': {'language': 'en', 'value': event[7]}}}
            new_event = api_wikibase.insert(initial_content)
            event_id = new_event['entity']['id']

            api_wikibase.add_claim(event_id, api_wikibase.get_id_by_query('beginDate', 'property'), date)

            if len(id_county) == 0:
                results = api_wikidata.search(county + ' County')
                instance_of_result = api_wikidata.search('instance of', 'property')[0]['id']
                county_result = api_wikidata.search('county of United States')[0]['id']
                url_wikidata_property = api_wikibase.get_id_by_query('urlWikiData', 'property')
                for result in results:
                    result_id = result['id']
                    property_instance_of = api_wikidata.get_property_by_item(result_id, instance_of_result)[0]
                    instance_of_value_id = property_instance_of['mainsnak']['datavalue']['value']['id']
                    if county_result in instance_of_value_id:
                        new_county = api_wikibase.insert({"labels": {"en": {"language": "en", "value": county}}})
                        id_county = new_county['entity']['id']
                        api_wikibase.add_claim(new_county['entity']['id'],
                                               api_wikibase.get_id_by_query('instance of', 'property'),
                                               {'entity-type': 'item', 'id': api_wikibase.get_id_by_query('county')})
                        api_wikibase.add_claim(new_county['entity']['id'], url_wikidata_property, WIKIDATA_URL + '/wiki/Item:'
                                               + result_id)
                        api_wikibase.add_claim(event_id, api_wikibase.get_id_by_query('instance of', 'property'),
                                               {'entity-type': 'item', 'id': id_county})
                        break

            if len(type_event) == 0:
                new_type_event = api_wikibase.insert({"labels": {"en": {"language": "en", "value": formatear_mayusculas(event[7])}}})
                type_event = new_type_event['entity']['id']

            api_wikibase.add_claim(event_id, api_wikibase.get_id_by_query('county', 'property'),
                                   {'entity-type': 'item', 'id': id_county})
            api_wikibase.add_claim(event_id, api_wikibase.get_id_by_query('typeEvent', 'property'),
                                   {'entity-type': 'item', 'id': type_event})

            entities.append(new_event["entity"]["id"])

    return entities


def create_has_events(eventos_relacionados, api_wikibase, api_wikidata, anio_begin, id_entity):
    hasevents = find_events(eventos_relacionados, api_wikibase, api_wikidata, anio_begin)

    for e in hasevents:
        api_wikibase.add_claim(id_entity, api_wikibase.get_id_by_query('hasEvents', 'property'),
                               {'entity-type': 'item', 'id': e})


def convert_damage(damage):
    if "M" in damage:
        return float(damage.split("M")[0]) * 1000000
    if "K" in damage:
        return float(damage.split("K")[0]) * 1000
