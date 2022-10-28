"""
File used to read in carrier-dict.csv and convert it to a dict object
"""
import csv

import constants


def read(file_data) -> dict:
    """
    Method to create dictionary object from DictUtils/carrier-dict.csv

    :param file_data:
    :param filename: File to create dictionary object from
    :return: Dictionary object created from contents of filename
    """
    if isinstance(file_data, str):
        with open(file_data, 'r', encoding='UTF-8') as dictfile:
            return read(dictfile)
    # Create empty dictionary to append and return
    carrier_dictionary = {}
    # Use the file readlines to iterate through the file - CSV wasn't working
    reader = csv.reader(file_data)
    for line in reader:
        # Ignore first two rows of file (headers and example)
        if line[0] == "Cell Carrier" or line[0] == "":
            continue
        # Cell carrier is first item in list, pop and store it in cell_carrier
        cell_carrier = line.pop(0)
        # Iterate through email list one at a time and delete empty items
        index = len(line)-1
        while index > 0:
            if line[index] == '':
                line.pop(index)
            index -= 1
        if constants.DEBUG:
            print(f"Adding cell carrier: {cell_carrier} with email list {line}!")
        # Update dict object to include value cell_carrier for key phone_number
        carrier_dictionary[cell_carrier] = line
    # Return dictionary created above
    return carrier_dictionary
