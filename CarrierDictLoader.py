import requests
import Constants
from SMSTexter import DictChecker, DictReader
import csv


def fetch_carrier_dictionary_local() -> dict:
    carrier_dict_file = DictChecker.has_csv_dict()
    cr = csv
    return DictReader.read(carrier_dict_file)


def fetch_carrier_dictionary() -> dict:
    # Fetch dictionary of cell carriers from GitHub
    response = requests.get(Constants.CARRIER_DICT_URL)
    # Create list object line-by-line from remote dictionary file
    lines = list(response.iter_lines())
    #
    for i in range(len(lines)):
        lines[i] = str(lines[i])
    with open('carrier-dict.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        for line in lines:
            line = line[2:len(line)-1]
            write_list = line.split(',')
            writer.writerow(write_list)
    return fetch_carrier_dictionary_local()


def carrier_dictionary():
    if Constants.DEBUG or (DictChecker.has_csv_dict() == ""):
        _carrier_dictionary = fetch_carrier_dictionary()
    else:
        return fetch_carrier_dictionary_local()
    return _carrier_dictionary
