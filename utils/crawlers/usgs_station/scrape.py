from traceback import format_exc
from logging import error as logging_error
from urllib.request import urlopen
from bs4 import BeautifulSoup
from spinner import Spinner
from time import sleep
from re import compile
from os import path, remove
from functools import reduce

WATER_DATA_URL = "https://waterdata.usgs.gov/nwis/current/?type=quality"
WATER_INFO_URL = [
    "https://waterdata.usgs.gov/nwis/inventory/?site_no=", "&agency_cd=USGS"]
FILE_NAME = "stations.csv"
HEADER_ROW = "site_no,url,lat,long,id,county,state,hydrolic_unit_id,id2"
SPINNER = Spinner()


def main():
    SPINNER.start()
    if path.exists(FILE_NAME):
        remove(FILE_NAME)
    try:
        print_status_message("Reading HTML from url:", WATER_DATA_URL)
        html = get_html(WATER_DATA_URL)
        soup = get_soup(html)
        ids = get_station_data_ids(soup)
        print_status_message("Found", len(ids), "station ids")
        process_station_pages(ids)
    except Exception:
        logging_error(format_exc())

    SPINNER.stop()


def get_html(url=""):
    if url is None or url == "":
        raise ValueError("Must provide a valid url")

    return urlopen(url)


def get_soup(html=None):
    if html is None:
        raise ValueError("URL not found")

    return BeautifulSoup(html.read(), features="html.parser")


def get_station_data_table(soup=None):
    if soup is None:
        raise ValueError("BeautifulSoup object not found")

    print_status_message("Getting data table")
    return soup.find("table", attrs={"align": "left"})


def get_station_data_rows(table=None):
    if table is None:
        raise ValueError("BeautifulSoup table not found")

    print_status_message("Getting data rows")
    rows = table.find_all("tr", attrs={"align": "right"})

    if rows is None:
        raise AttributeError("Tag was not found")
    elif len(rows) == 0:
        raise ValueError("Found 0 rows")

    return rows


def get_station_data_ids(soup=None):
    if soup is None:
        raise ValueError("BeautifulSoup object not found")

    table = get_station_data_table(soup)
    rows = get_station_data_rows(table)
    print_status_message("Getting station ids")
    ids = map(get_row_id, rows)
    return list(filter(lambda id: id is not None, ids))


def get_row_id(row=None):
    if row is not None:
        cell = row.find('td', attrs={"align": "left"})
        if cell is not None and cell.a is not None:
            return cell.a.get_text()


def process_station_pages(ids=[]):
    if ids is not None and len(ids):
        idsLen = len(ids)
        for i in range(idsLen):
            url = build_water_info_url(ids[i])
            print_status_message("%.2f" % ((i+1) / idsLen * 100) + "%")
            data = [ids[i]] + get_info_data(url)
            write_to_file(
                list(map(lambda x: (str(x) if x is not None else "").replace(",", ""), data)))


def build_water_info_url(stationId=""):
    if stationId is None or stationId == "":
        raise ValueError("Must supply a valid stationId")

    return WATER_INFO_URL[0] + stationId + WATER_INFO_URL[1]


def get_info_data(url=""):
    data = [url]
    if url is not None and url != "":
        html = get_html(url)
        soup = get_soup(html)
        stationTable = soup.find("div", id="stationTable")

        lines = []
        if stationTable is not None and stationTable.dl is not None:
            # a very inefficient way to obtain the "lines" we are looking for
            # certain pages break different lines into separate dd elements; whereas, others just use line breaks
            # compiling the lines like this guarantees successful parsing in both scenarios
            lines = split(reduce(lambda x, y: x + "\n" + y, map(lambda el: el.get_text()
                                                                if el is not None else "", stationTable.dl.find_all("dd"))), "\n")

        # lat, long, and id are found on line 1
        if len(lines):
            line = lines[0]
            lat = get_value_for_label(line, "Latitude ")
            if lat[-1] == ",":
                lat = lat[:-1]
            long = get_value_for_label(line, "Longitude ")
            id = split(line)[-1]
            data.append(format_coord(lat) if lat is not None else None)
            data.append(format_coord(long) if long is not None else None)
            data.append(id)

        # we should have 4 values by now, fill in the remaining slots (if any) with None
        for _ in range(4 - len(data)):
            data.append(None)

        # county, state, hydrolic unit id found on line 2
        if len(lines) > 1:
            line = lines[1]
            commaSplit = split(line, ",")

            if len(commaSplit):
                data.append(commaSplit[0].strip())
            if len(commaSplit) > 1:
                data.append(commaSplit[1].strip())
            if len(commaSplit) > 2:
                data.append(split(commaSplit[2])[-1])

        # we should have 7 values by now, fill in the remaining slots (if any) with None
        for _ in range(7 - len(data)):
            data.append(None)

        # id2 found on last line
        if len(lines) > 2:
            id2 = split(lines[-1])[-1]
            if id2[-1] == ".":
                id2 = id2.replace(".", "")
            # some pages don't contain id2, in which case the last word found will end up being "miles"
            if "mile" not in id2:
                data.append(id2)

    # we should have 8 values by now, fill in the remaining slots (if any) with None
    for _ in range(8 - len(data)):
        data.append(None)

    return data


def format_coord(coord=""):
    if coord is None or coord == "":
        return coord

    degreeSplit = coord.split("°")
    degree = float(degreeSplit[0])
    minuteSplit = degreeSplit[1].split("\'")
    minute = float(minuteSplit[0])
    second = float(minuteSplit[1][:-1])
    return round(degree + minute/60 + second/3600, 6)


def get_value_for_label(text="", label=None):
    if label is not None and text.find(label) != -1:
        words = split(text[text.find(label):])
        if len(words) > 1:
            return words[1]
    return None


def split(str="", char_delim=" "):
    return list(filter(lambda str: str != "", str.strip().split(char_delim)))


def write_to_file(data=[]):
    if data is not None and len(data):
        file = open_file()
        file.write(",".join(data) + "\n")


def open_file():
    try:
        file = open(FILE_NAME, "r")
    except FileNotFoundError:
        create_file()
        return open_file()

    isEmpty = file.read() == ""
    file.close()
    file = open(FILE_NAME, "a+")
    if isEmpty:
        # first time opening this file
        # we need to write the CSV headings first
        file.write(HEADER_ROW + "\n")

    return file


def create_file():
    file = open(FILE_NAME, "w+")
    file.close()


def print_status_message(*args):
    if len(args) and args[0] is not None and args[0] != "":
        SPINNER.stop()
        sleep(0.01)
        print(*args, "\n")
        SPINNER.start()


main()
