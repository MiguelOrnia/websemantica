import re
from datetime import datetime

from numerizer.numerizer import numerize

from analyze_tuits.tuits_analyzer import TuitsAnalyzer
from extract_tuit.tuits_extractor import TuitExtractor
from tuit_extraction import TuitExtraction


def ej4():
    tuits_extractor = TuitExtractor()
    tuits = tuits_extractor.cargarTuits()
    tuits_analyzer = TuitsAnalyzer()
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

        file = open("dictionaries/keywords_coastal_flood.txt", "r")
        for line in file:
            textacy2_value = tuits_analyzer.textacy2(tuit, line.rstrip())
            if len(textacy2_value) > 0:
                dic_textacy2[line.rstrip()] = textacy2_value

        file = open("dictionaries/keywords_flash_flood.txt", "r")
        for line in file:
            textacy2_value = tuits_analyzer.textacy2(tuit, line.rstrip())
            if len(textacy2_value) > 0:
                dic_textacy2[line.rstrip()] = textacy2_value

        file = open("dictionaries/keywords_flood.txt", "r")
        for line in file:
            textacy2_value = tuits_analyzer.textacy2(tuit, line.rstrip())
            if len(textacy2_value) > 0:
                dic_textacy2[line.rstrip()] = textacy2_value

        file = open("dictionaries/keywords_funnel_cloud.txt", "r")
        for line in file:
            textacy2_value = tuits_analyzer.textacy2(tuit, line.rstrip())
            if len(textacy2_value) > 0:
                dic_textacy2[line.rstrip()] = textacy2_value

        file = open("dictionaries/keywords_hail.txt", "r")
        for line in file:
            textacy2_value = tuits_analyzer.textacy2(tuit, line.rstrip())
            if len(textacy2_value) > 0:
                dic_textacy2[line.rstrip()] = textacy2_value

        file = open("dictionaries/keywords_hurricane.txt", "r")
        for line in file:
            textacy2_value = tuits_analyzer.textacy2(tuit, line.rstrip())
            if len(textacy2_value) > 0:
                dic_textacy2[line.rstrip()] = textacy2_value

        file = open("dictionaries/keywords_speed.txt", "r")
        for line in file:
            textacy2_value = tuits_analyzer.textacy2(tuit, line.rstrip())
            if len(textacy2_value) > 0:
                dic_textacy2[line.rstrip()] = textacy2_value

        file = open("dictionaries/keywords_thunderstorm.txt", "r")
        for line in file:
            textacy2_value = tuits_analyzer.textacy2(tuit, line.rstrip())
            if len(textacy2_value) > 0:
                dic_textacy2[line.rstrip()] = textacy2_value

        file = open("dictionaries/keywords_thunderstorm_wind.txt", "r")
        for line in file:
            textacy2_value = tuits_analyzer.textacy2(tuit, line.rstrip())
            if len(textacy2_value) > 0:
                dic_textacy2[line.rstrip()] = textacy2_value

        file = open("dictionaries/keywords_time.txt", "r")
        for line in file:
            textacy2_value = tuits_analyzer.textacy2(tuit, line.rstrip())
            if len(textacy2_value) > 0:
                dic_textacy2[line.rstrip()] = textacy2_value

        file = open("dictionaries/keywords_tornado.txt", "r")
        for line in file:
            textacy2_value = tuits_analyzer.textacy2(tuit, line.rstrip())
            if len(textacy2_value) > 0:
                dic_textacy2[line.rstrip()] = textacy2_value

        file = open("dictionaries/keywords_typhoon.txt", "r")
        for line in file:
            textacy2_value = tuits_analyzer.textacy2(tuit, line.rstrip())
            if len(textacy2_value) > 0:
                dic_textacy2[line.rstrip()] = textacy2_value

        tuit_extraction = TuitExtraction(ner_value, dic_textacy2)
        tornados.append(tuit)

        # NER
        tuit_values = extract_with_ner(tuit_extraction, {})

        # TEXTACY 2
        tuit_values = extract_speed_with_textacy2(tuit_extraction, tuit_values, "dictionaries/keywords_speed.txt")
        tuit_values = extract_time_with_textacy2(tuit_extraction, tuit_values, "dictionaries/keywords_time.txt")
        tuit_values = extract_type_events_with_textacy2(tuit_extraction, tuit_values,
                                                        "dictionaries/keywords_coastal_flood.txt",
                                                        "coastal flood")
        tuit_values = extract_type_events_with_textacy2(tuit_extraction, tuit_values,
                                                        "dictionaries/keywords_flash_flood.txt",
                                                        "flash flood")
        tuit_values = extract_type_events_with_textacy2(tuit_extraction, tuit_values,
                                                        "dictionaries/keywords_coastal_flood.txt",
                                                        "flood")
        tuit_values = extract_type_events_with_textacy2(tuit_extraction, tuit_values,
                                                        "dictionaries/keywords_funnel_cloud.txt",
                                                        "funnel flood")
        tuit_values = extract_type_events_with_textacy2(tuit_extraction, tuit_values, "dictionaries/keywords_hail.txt",
                                                        "hail")
        tuit_values = extract_type_events_with_textacy2(tuit_extraction, tuit_values,
                                                        "dictionaries/keywords_hurricane.txt",
                                                        "huricane")
        tuit_values = extract_type_events_with_textacy2(tuit_extraction, tuit_values,
                                                        "dictionaries/keywords_thunderstorm.txt",
                                                        "thunderstorm")
        tuit_values = extract_type_events_with_textacy2(tuit_extraction, tuit_values,
                                                        "dictionaries/keywords_thunderstorm_wind.txt",
                                                        "thunderstorm wind")
        tuit_values = extract_type_events_with_textacy2(tuit_extraction, tuit_values,
                                                        "dictionaries/keywords_tornado.txt",
                                                        "tornado")
        tuit_values = extract_type_events_with_textacy2(tuit_extraction, tuit_values,
                                                        "dictionaries/keywords_typhoon.txt",
                                                        "typhoon")

        print(tuit_values)

        event = check_event(tuits[i], tuit_values)


def check_event(tuit_info, tuit_values):
    file = open("dictionaries/type_events.txt", "r")
    info = {}

    # Tipo de evento
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

    # Fecha
    if "date" in tuit_values:
        date = tuit_values["date"]
        if date.lower() == 'today':
            info["date"] = format_date(tuit_info.created_at)
        else:
            info["date"] = date
    else:
        info["date"] = format_date(tuit_info.created_at)

    # Hora
    if "time" in tuit_values:
        time = tuit_values["time"]
        info["time"] = time
    else:
        time = format_time(tuit_info.created_at)
        info["time"] = time

    # Localización
    info["longitude"] = tuit_info.longitude
    info["latitude"] = tuit_info.latitude

    # Velocidad del viento
    if "speedWind" in tuit_values:
        info["speed_wind"] = tuit_values["speedWind"]
    else:
        if info["type_event"] == "tornado":
            return None
    print("TUIT FINAL")
    print(info)
    return info


def format_date(date):
    words = date.split(" ")
    newDate = str(get_month(words[1])) + "/" + words[2] + "/" + words[5]
    return newDate


def format_time(time):
    words = time.split(" ")
    newTime = words[3]
    return newTime


def get_month(month_name):
    if month_name == "Jan":
        return 1
    elif month_name == "Feb":
        return 2
    elif month_name == "Mar":
        return 3
    elif month_name == "Apr":
        return 4
    elif month_name == "May":
        return 5
    elif month_name == "Jun":
        return 6
    elif month_name == "Jul":
        return 7
    elif month_name == "Aug":
        return 8
    elif month_name == "Sep":
        return 9
    elif month_name == "Oct":
        return 10
    elif month_name == "Nov":
        return 11
    else:
        return 12


def extract_with_ner(tuit, tuit_values):
    if "TIME" in tuit.ner:
        time_ner = tuit.ner["TIME"]
        for time in time_ner:
            if "am" in time.lower() or "pm" in time.lower() or "a.m" in time.lower() or "p.m" in time.lower():
                tuit_values["time"] = time

    if "DATE" in tuit.ner:
        date_ner = tuit.ner["DATE"]
        for date in date_ner:
            if date.lower() == "today" or check_date_by_slash(date) or check_date_by_middle_dash(date):
                tuit_values["date"] = date

    if "QUANTITY" in tuit.ner:
        quantity_ner = tuit.ner["QUANTITY"]
        for quantity in quantity_ner:
            file = open("dictionaries/keywords_speed.txt", "r")
            for line in file:
                if line.rstrip() in quantity:
                    tuit_values["speedWind"] = numerize(quantity)

    return tuit_values


def check_date_by_slash(date):
    try:
        datetime.strptime(date, "%m/%d/%y")
        return True
    except ValueError as err:
        return False


def check_date_by_middle_dash(date):
    try:
        datetime.strptime(date, "%m-%d-%y")
        return True
    except ValueError as err:
        return False


def extract_speed_with_textacy2(tuit, tuit_values, file):
    file = open(file, "r")
    for line in file:
        for key in tuit.textacy2:
            if line.rstrip() in key:
                speed_in_context = tuit.textacy2[key]
                value = None
                if len(speed_in_context) > 1:
                    for speed in speed_in_context:
                        speedNew = speed[0].strip()
                        words = speedNew.split(" ")
                        print((words[len(words) - 1]))
                        if calculate_number(words[len(words) - 1]) is not None:
                            value = float(calculate_number(words[len(words) - 1]))
                        else:
                            value = calculate_number(words[len(words) - 1])

                else:
                    speedNew = speed_in_context[0][0].strip()
                    words = speedNew.split(" ")
                    if calculate_number(words[len(words) - 1]) is not None:
                        value = float(calculate_number(words[len(words) - 1]))
                    else:
                        value = calculate_number(words[len(words) - 1])

                if value is not None:
                    tuit_values["speedWind"] = value
    return tuit_values


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


def extract_type_events_with_textacy2(tuit, tuit_values, file, type_event):
    file = open(file, "r")
    for line in file:
        for key in tuit.textacy2:
            if line.rstrip('\n') in key:
                tuit_values[type_event] = True
    return tuit_values


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
                            value = str(words[len(words) - 2]) + " " + time[1]  # Nos quedamos con el ultimo
                else:
                    words = time_in_context[0][0].split(" ")
                    if re.search('^([0-9]+:[0-9]+|[0-9]+-[0-9]+)', words[len(words) - 2]):
                        value = str(words[len(words) - 2]) + " " + time_in_context[0][1]
                if value is not None:
                    tuit_values["time"] = value
    return tuit_values
