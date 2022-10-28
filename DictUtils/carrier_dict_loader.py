import csv
import requests
import constants
from DictUtils import dict_checker, dict_reader


def fetch_carrier_dictionary_local() -> dict:
    carrier_dict_file = dict_checker.has_csv_dict()
    return dict_reader.read(carrier_dict_file)


def fetch_carrier_dictionary() -> dict:
    # Fetch dictionary of cell carriers from GitHub
    response = requests.get(constants.CARRIER_DICT_URL)
    # Create list object line-by-line from remote dictionary file
    lines = list(response.iter_lines())
    #
    for i in range(len(lines)):
        lines[i] = str(lines[i])
    dict_patch = constants.LOCAL_DICT_PATCH
    with open(dict_patch, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        for line in lines:
            line = line[2:len(line)-1]
            write_list = line.split(',')
            writer.writerow(write_list)
    return dict_reader.read(dict_patch)


def carrier_dictionary():
    if constants.DEBUG or (dict_checker.has_csv_dict() == ""):
        _carrier_dictionary = fetch_carrier_dictionary()
    else:
        return fetch_carrier_dictionary_local()
    return _carrier_dictionary
