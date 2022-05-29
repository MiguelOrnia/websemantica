import re
from numerizer.numerizer import numerize
from analyze_tuits.tuits_analyzer import TuitsAnalyzer
from extract_tuit.tuits_extractor import TuitExtractor
from tuit_extraction import TuitExtraction
from util.date_helper import DateHelper
from util.strings_helper import StringsHelper
from wikibase.api_wikibase import WikibaseApi
from wikibase.api_wikidata import WikidataApi
from geopy.geocoders import Nominatim

""" Rutas para acceder a los ficheros que contienen las palabras clave a emplear """
KEYWORDS_COASTAL_FLOOD_PATH = "keywords_dictionaries/keywords_coastal_flood.txt"
KEYWORDS_FLASH_FLOOD_PATH = "keywords_dictionaries/keywords_flash_flood.txt"
KEYWORDS_FLOOD_PATH = "keywords_dictionaries/keywords_flood.txt"
KEYWORDS_FUNNEL_CLOUD_PATH = "keywords_dictionaries/keywords_funnel_cloud.txt"
KEYWORDS_HAIL_PATH = "keywords_dictionaries/keywords_hail.txt"
KEYWORDS_HURRICANE_PATH = "keywords_dictionaries/keywords_hurricane.txt"
KEYWORDS_SPEED_PATH = "keywords_dictionaries/keywords_speed.txt"
KEYWORDS_THUNDERSTORM_PATH = "keywords_dictionaries/keywords_thunderstorm.txt"
KEYWORDS_THUNDERSTORM_WIND_PATH = "keywords_dictionaries/keywords_thunderstorm_wind.txt"
KEYWORDS_TIME_PATH = "keywords_dictionaries/keywords_time.txt"
KEYWORDS_TORNADO_PATH = "keywords_dictionaries/keywords_tornado.txt"
KEYWORDS_TYPHOON_PATH = "keywords_dictionaries/keywords_typhoon.txt"

""" Constantes con las URL de nuestra instancia de Wikibase y de Wikidata """

WIKIBASE_URL = 'http://156.35.98.119'
WIKIDATA_URL = 'https://www.wikidata.org'

""" Funcion principal del ejercicio 4 """


def ej4():
    tuits_extractor = TuitExtractor()
    tuits = tuits_extractor.cargar_tuits()
    tuits_analyzer = TuitsAnalyzer()
    date_helper = DateHelper()
    tornados = []

    for i in range(len(tuits)):
        tuit = tuits[i].full_text
        print()
        print("*********** TUIT " + str(i + 1) + " ******************")
        print(tuit)

        print("-------------NER " + str(i + 1) + " --------------")
        ner_value = tuits_analyzer.ner(tuit)

        dic_textacy2 = {}

        print("------------TEXTACY " + str(i + 1) + " --------------")
        print("***textacy2 " + str(i + 1) + " ****")

        file = open(KEYWORDS_COASTAL_FLOOD_PATH, "r")
        for line in file:
            textacy2_value = tuits_analyzer.textacy2(tuit, line.rstrip())
            if len(textacy2_value) > 0:
                dic_textacy2[line.rstrip()] = textacy2_value

        file = open(KEYWORDS_FLASH_FLOOD_PATH, "r")
        for line in file:
            textacy2_value = tuits_analyzer.textacy2(tuit, line.rstrip())
            if len(textacy2_value) > 0:
                dic_textacy2[line.rstrip()] = textacy2_value

        file = open(KEYWORDS_FLOOD_PATH, "r")
        for line in file:
            textacy2_value = tuits_analyzer.textacy2(tuit, line.rstrip())
            if len(textacy2_value) > 0:
                dic_textacy2[line.rstrip()] = textacy2_value

        file = open(KEYWORDS_FUNNEL_CLOUD_PATH, "r")
        for line in file:
            textacy2_value = tuits_analyzer.textacy2(tuit, line.rstrip())
            if len(textacy2_value) > 0:
                dic_textacy2[line.rstrip()] = textacy2_value

        file = open(KEYWORDS_HAIL_PATH, "r")
        for line in file:
            textacy2_value = tuits_analyzer.textacy2(tuit, line.rstrip())
            if len(textacy2_value) > 0:
                dic_textacy2[line.rstrip()] = textacy2_value

        file = open(KEYWORDS_HURRICANE_PATH, "r")
        for line in file:
            textacy2_value = tuits_analyzer.textacy2(tuit, line.rstrip())
            if len(textacy2_value) > 0:
                dic_textacy2[line.rstrip()] = textacy2_value

        file = open(KEYWORDS_SPEED_PATH, "r")
        for line in file:
            textacy2_value = tuits_analyzer.textacy2(tuit, line.rstrip())
            if len(textacy2_value) > 0:
                dic_textacy2[line.rstrip()] = textacy2_value

        file = open(KEYWORDS_THUNDERSTORM_PATH, "r")
        for line in file:
            textacy2_value = tuits_analyzer.textacy2(tuit, line.rstrip())
            if len(textacy2_value) > 0:
                dic_textacy2[line.rstrip()] = textacy2_value

        file = open(KEYWORDS_THUNDERSTORM_WIND_PATH, "r")
        for line in file:
            textacy2_value = tuits_analyzer.textacy2(tuit, line.rstrip())
            if len(textacy2_value) > 0:
                dic_textacy2[line.rstrip()] = textacy2_value

        file = open(KEYWORDS_TIME_PATH, "r")
        for line in file:
            textacy2_value = tuits_analyzer.textacy2(tuit, line.rstrip())
            if len(textacy2_value) > 0:
                dic_textacy2[line.rstrip()] = textacy2_value

        file = open(KEYWORDS_TORNADO_PATH, "r")
        for line in file:
            textacy2_value = tuits_analyzer.textacy2(tuit, line.rstrip())
            if len(textacy2_value) > 0:
                dic_textacy2[line.rstrip()] = textacy2_value

        file = open(KEYWORDS_TYPHOON_PATH, "r")
        for line in file:
            textacy2_value = tuits_analyzer.textacy2(tuit, line.rstrip())
            if len(textacy2_value) > 0:
                dic_textacy2[line.rstrip()] = textacy2_value

        tuit_extraction = TuitExtraction(ner_value, dic_textacy2)
        tornados.append(tuit)

        tuit_values = extract_with_ner(tuit_extraction, {}, date_helper)

        tuit_values = extract_speed_with_textacy2(tuit_extraction, tuit_values, KEYWORDS_SPEED_PATH)
        tuit_values = extract_time_with_textacy2(tuit_extraction, tuit_values, KEYWORDS_TIME_PATH)
        tuit_values = extract_type_events_with_textacy2(tuit_extraction, tuit_values, KEYWORDS_COASTAL_FLOOD_PATH,
                                                        "coastal flood")
        tuit_values = extract_type_events_with_textacy2(tuit_extraction, tuit_values, KEYWORDS_FLASH_FLOOD_PATH,
                                                        "flash flood")
        tuit_values = extract_type_events_with_textacy2(tuit_extraction, tuit_values, KEYWORDS_FLOOD_PATH,
                                                        "flood")
        tuit_values = extract_type_events_with_textacy2(tuit_extraction, tuit_values, KEYWORDS_FUNNEL_CLOUD_PATH,
                                                        "funnel flood")
        tuit_values = extract_type_events_with_textacy2(tuit_extraction, tuit_values, KEYWORDS_HAIL_PATH,
                                                        "hail")
        tuit_values = extract_type_events_with_textacy2(tuit_extraction, tuit_values, KEYWORDS_HURRICANE_PATH,
                                                        "hurricane")
        tuit_values = extract_type_events_with_textacy2(tuit_extraction, tuit_values, KEYWORDS_THUNDERSTORM_PATH,
                                                        "thunderstorm")
        tuit_values = extract_type_events_with_textacy2(tuit_extraction, tuit_values, KEYWORDS_THUNDERSTORM_WIND_PATH,
                                                        "thunderstorm wind")
        tuit_values = extract_type_events_with_textacy2(tuit_extraction, tuit_values, KEYWORDS_TORNADO_PATH,
                                                        "tornado")
        tuit_values = extract_type_events_with_textacy2(tuit_extraction, tuit_values, KEYWORDS_TYPHOON_PATH,
                                                        "typhoon")

        print(tuit_values)

        event = check_event(tuits[i], tuit_values, date_helper)

        if event is not None:
            create_event(event, date_helper)


def check_event(tuit_info, tuit_values, date_helper):
    file = open("keywords_dictionaries/type_events.txt", "r")
    info = {}

    for line in file:
        has_event_type = False
        for key in tuit_values:
            if line.rstrip('\n') == key:
                info["type_event"] = line.rstrip()
                has_event_type = True
                break
        if has_event_type:
            break

    if "type_event" not in info:
        return None

    if "date" in tuit_values:
        date = tuit_values["date"]
        if date.lower() == 'today':
            info["date"] = date_helper.format_date(tuit_info.created_at)
        else:
            info["date"] = date
    else:
        info["date"] = date_helper.format_date(tuit_info.created_at)

    if "time" in tuit_values:
        time = tuit_values["time"]
        info["time"] = time
    else:
        time = date_helper.format_time(tuit_info.created_at)
        info["time"] = time

    info["longitude"] = tuit_info.longitude
    info["latitude"] = tuit_info.latitude

    if "speedWind" in tuit_values:
        info["speed_wind"] = tuit_values["speedWind"]
    else:
        if info["type_event"] == "tornado":
            return None

    return info


""" Funcion encargada de recoger los valores obtenidos con NER """


def extract_with_ner(tuit, tuit_values,date_helper):
    if "TIME" in tuit.ner:
        time_ner = tuit.ner["TIME"]
        for time in time_ner:
            if "am" in time.lower() or "pm" in time.lower() or "a.m" in time.lower() or "p.m" in time.lower():
                tuit_values["time"] = time

    if "DATE" in tuit.ner:
        date_ner = tuit.ner["DATE"]
        for date in date_ner:
            if date.lower() == "today" or date_helper.check_date_by_slash(date) \
                    or date_helper.check_date_by_middle_dash(date):
                tuit_values["date"] = date

    if "QUANTITY" in tuit.ner:
        quantity_ner = tuit.ner["QUANTITY"]
        for quantity in quantity_ner:
            file = open(KEYWORDS_SPEED_PATH, "r")
            for line in file:
                if line.rstrip() in quantity:
                    tuit_values["speedWind"] = numerize(quantity)

    return tuit_values


""" Funcion encargada de recoger la velocidad obtenida con KWIC """


def extract_speed_with_textacy2(tuit, tuit_values, file):
    file = open(file, "r")
    for line in file:
        for key in tuit.textacy2:
            if line.rstrip() in key:
                speed_in_context = tuit.textacy2[key]
                value = None
                if len(speed_in_context) > 1:
                    for speed in speed_in_context:
                        speed_new = speed[0].strip()
                        words = speed_new.split(" ")
                        if calculate_number(words[len(words) - 1]) is not None:
                            value = float(calculate_number(words[len(words) - 1]))
                        else:
                            value = calculate_number(words[len(words) - 1])

                else:
                    speed_new = speed_in_context[0][0].strip()
                    words = speed_new.split(" ")
                    if calculate_number(words[len(words) - 1]) is not None:
                        value = float(calculate_number(words[len(words) - 1]))
                    else:
                        value = calculate_number(words[len(words) - 1])

                if value is not None:
                    tuit_values["speedWind"] = value
    return tuit_values


""" Funcion que calcula el numero correspondiente a una cadena dada. Se utiliza para calculo de velocidades"""


def calculate_number(value):
    try:
        return float(value)
    except ValueError as err:
        if re.search('^([a-zA-Z]|@|\+)+[0-9]+.*[0-9]*', value):
            return value[1:]
        elif re.search('^[0-9]+.*[0-9]*([a-zA-Z]|@|\+)+', value):
            return value[:-1]
        elif re.search('^([a-zA-Z]|@|\+)+[0-9]+.*[0-9]*([a-zA-Z]|@|\+)+', value):
            return value[1:-1]
        else:
            return None


""" Funcion encargada de recoger el tipo de evento con KWIC """


def extract_type_events_with_textacy2(tuit, tuit_values, file, type_event):
    file = open(file, "r")
    for line in file:
        for key in tuit.textacy2:
            if line.rstrip('\n') in key:
                tuit_values[type_event] = True
    return tuit_values


""" Funcion encargada de recoger el tiempo obtenido con KWIC """


def extract_time_with_textacy2(tuit, tuit_values, file):
    file = open(file, "r")
    for line in file:
        for key in tuit.textacy2:
            if line.rstrip('\n') in key:
                time_in_context = tuit.textacy2[key]
                value = None
                if len(time_in_context) > 1:
                    for time in time_in_context:
                        words = time[0].split(" ")
                        if re.search('^([0-9]+:[0-9]+|[0-9]+-[0-9]+)', words[len(words) - 2]):
                            value = str(words[len(words) - 2]) + " " + time[1]
                else:
                    words = time_in_context[0][0].split(" ")
                    if re.search('^([0-9]+:[0-9]+|[0-9]+-[0-9]+)', words[len(words) - 2]):
                        value = str(words[len(words) - 2]) + " " + time_in_context[0][1]
                if value is not None:
                    tuit_values["time"] = value
    return tuit_values


""" Funcion encargada de crear un evento """


def create_event(event_info, date_helper):
    wikibase_api = WikibaseApi()
    wikidata_api = WikidataApi()
    strings_helper = StringsHelper()

    id_property_instance_of = wikibase_api.get_id_by_query('instance of', 'property')
    id_property_state = wikibase_api.get_id_by_query('state', 'property')
    id_property_latitude = wikibase_api.get_id_by_query('latitude', 'property')
    id_property_longitude = wikibase_api.get_id_by_query('longitude', 'property')
    id_property_begin_date = wikibase_api.get_id_by_query('eventDate', 'property')
    id_property_wiki_data = wikibase_api.get_id_by_query('urlWikiData', 'property')

    coordinates = str(event_info['latitude']) + ' , ' + str(event_info['longitude'])
    geolocator = Nominatim(user_agent="Wikibase")
    location = geolocator.reverse(coordinates)
    if location is not None:
        address = location.raw['address']
        county = address.get('county', '')

        event_name = event_info['date'].split("/")[2] + " " + county + ' ' + event_info['date'] + ' ' + event_info['time']
        event = wikibase_api.insert({"labels": {
            "en": {"language": "en", "value": event_name}}})

        type_event = wikibase_api.get_id_by_query(event_info['type_event'])

        if len(type_event) == 0:
            new_type_event = wikibase_api.insert({"labels": {"en": {"language": "en", "value":
                strings_helper.formatear_minusculas(event_info['typeEvent'])}}})
            type_event = new_type_event['entity']['id']
            wikibase_api.add_claim(new_type_event['entity']['id'], id_property_instance_of,
                                   {'entity-type': 'item',
                                    'id': wikibase_api.get_id_by_query('atmospheric phenomenon')})

        wikibase_api.add_claim(event['entity']['id'], wikibase_api.get_id_by_query('typeEvent', 'property'),
                               {'entity-type': 'item', 'id': type_event})

        wikibase_api.add_claim(event['entity']['id'], id_property_latitude,
                               {'amount': event_info['latitude'], 'unit': '1'})
        wikibase_api.add_claim(event['entity']['id'], id_property_longitude,
                               {'amount': event_info['longitude'], 'unit': '1'})

        begin_date = date_helper.format_wikibase_date(event_info['date'], event_info['time'])
        wikibase_api.add_claim(event['entity']['id'], id_property_begin_date, begin_date)

        if "speed_wind" in event_info:
            id_property_max_wind_speed_event = wikibase_api.get_id_by_query('maxWindSpeed', 'property')
            wikibase_api.add_claim(event['entity']['id'], id_property_max_wind_speed_event,
                                   {'amount': event_info['speed_wind'], 'unit': WIKIBASE_URL + '/entity/'
                                                                                + wikibase_api.get_id_by_query(
                                       'Miles Per Hour')})
