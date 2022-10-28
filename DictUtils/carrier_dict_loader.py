"""
Module used for importing and using carrier-dict.csv
"""
import csv
import requests
import constants
from DictUtils import dict_checker, dict_reader


def __fetch_carrier_dictionary_local() -> dict:
    """
    Function used for fetching local carrier dictionary file

    :return: dictionary object created by reading the file
    """
    carrier_dict_file = dict_checker.has_csv_dict()
    return dict_reader.read(carrier_dict_file)


def __fetch_carrier_dictionary() -> dict:
    """
    Function used for fetching cell carrier dictionary from GitHub

    :return: Dictionary file newly-stored locally
    """
    # Fetch dictionary of cell carriers from GitHub
    response = requests.get(constants.CARRIER_DICT_URL, timeout=10)
    # Create list object line-by-line from remote dictionary file
    lines = list(response.iter_lines())
    # Iterate through all the lines in the dictionary and convert them to strings
    for i in enumerate(lines):
        lines[i] = str(lines[i])
    # Fetch path to dictionary file from constants
    dict_patch = constants.LOCAL_DICT_PATCH
    # Open dictionary file and write to it
    with open(dict_patch, 'w', encoding='UTF-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        # Format each line and output to csv file
        for line in lines:
            line = line[2:len(line)-1]
            write_list = line.split(',')
            writer.writerow(write_list)
    # Return dictionary object created from locally stored dictionary newly created
    return dict_reader.read(dict_patch)


def carrier_dictionary() -> dict:
    """
    Function used to return carrier dictionary

    :return: Dict object containing cell carriers and their text-to-mail addresses
    """
    # If in DEBUG mode or if local dict does NOT exist, fetch from GitHub
    if constants.DEBUG or (dict_checker.has_csv_dict() == ""):
        _carrier_dictionary = __fetch_carrier_dictionary()
        # Return fetched dict object
        return _carrier_dictionary
    # Local dictionary file already exists, fetch, turn into dict object, and return it
    return __fetch_carrier_dictionary_local()
