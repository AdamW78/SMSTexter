"""
Module used for importing and using carrier-dict.csv
"""
import csv
import os
from os.path import exists
import requests
import constants
from DictUtils import dict_checker, dict_reader


def __fetch_carrier_dictionary() -> dict:
    """
    Function used for fetching cell carrier dictionary from GitHub

    :return: Dictionary file newly-stored locally
    """
    # Check if Cache directory exists or not
    if not exists(os.getcwd()+"/Documents/SMS Texter/"):
        # Cache directory does not exist, create it
        print(os.mkdir(os.getcwd()+"/Documents/SMS Texter/"))
    return __fetch_remote_dict()


def __fetch_remote_dict() -> dict:
    # Fetch dictionary of cell carriers from GitHube
    response = requests.get(constants.CARRIER_DICT_URL, timeout=10)
    # Create list object line-by-line from remote dictionary file
    lines = list(response.iter_lines())
    # Fetch path to dictionary file from constants
    dict_path = constants.LOCAL_DICT_PATH

    # Open dictionary file and write to it
    with open(dict_path, 'w', encoding='UTF-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        # Format each line and output to csv file
        for line in lines:
            line = str(line)
            line = line[2:len(line) - 1]
            write_list = line.split(',')
            writer.writerow(write_list)
    # Return dictionary object created from locally stored dictionary newly created
    return dict_reader.read(dict_path)


def carrier_dictionary() -> dict:
    """
    Function used to return carrier dictionary

    :return: Dict object containing cell carriers and their text-to-mail addresses
    """
    # If in DEBUG mode or if local dict does NOT exist, fetch from GitHub
    if constants.DEBUG or (not dict_checker.has_csv_dict()):
        return __fetch_carrier_dictionary()
    # Local dictionary file already exists, fetch, turn into dict object, and return it
    return dict_reader.read(constants.LOCAL_DICT_PATH)
