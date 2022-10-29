"""
Module used to check if a file is a csv dictionary
"""

from csv import reader
from os.path import exists
import constants


def is_csv_dict(filename) -> bool:
    """
    Checks whether a given file is a cell carrier dictionary

    :param filename: file to check
    :return: boolean for whether file is a csv dictionary
    """
    if filename.endswith("csv"):
        with open(filename, 'r', encoding='UTF-8') as csvfile:
            csv_reader = reader(csvfile)
            csv_file_list = list(csv_reader)
            headers = csv_file_list[0]
            return 'Cell Carrier' in headers
    return False


def has_csv_dict() -> bool:
    """
    Checks whether user has already written a CSV file from cell carrier dictionary

    :return: boolean for whether a local dict file has already been created
    """
    return exists(constants.LOCAL_DICT_PATH)
