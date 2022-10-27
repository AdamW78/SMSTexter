from os import listdir
from os.path import isfile
from csv import reader


def is_csv_dict(filename) -> bool:
    """
    Checks whether a given file is a cell carrier dictionary

    :param filename: file to check
    :return: boolean for whether file is a csv dictionary
    """
    if filename.endswith("csv"):
        with open(filename, newline='\n') as csvfile:

            csv_reader = reader(csvfile)
            csv_file_list = list(csv_reader)
            headers = csv_file_list[0]
            if 'Cell Carrier' in headers:
                return True
            else:
                return False


def has_csv_dict() -> str:
    """
    Checks whether user has already written a CSV file from cell carrier dictionary

    :return: string file where carrrier-dict.csv is found
    """
    files = [f for f in listdir('DictUtils') if isfile(f)]
    for f in files:
        if is_csv_dict(f):
            return "DictUtils/" + f
    return ""
