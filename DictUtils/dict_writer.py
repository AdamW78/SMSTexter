"""
Module used to write and locally store dictionary file
"""
import csv

import constants


def write(dictionary):
    """
    Writes passed in cell carrier dictionary to csv file to cache locally

    :param dictionary: dict object containing cell carrier keys as strings
    and lists of text-to-email addresses as strings
    """
    # CSV Column Headers to Use
    csv_columns = ["Cell Carrier", "Email 1", "Email 2", "Email 3", "Email 4", "Email 5", "Email 6"]
    # Path to CSV file
    csv_file = constants.LOCAL_DICT_PATCH
    with open(csv_file, 'w', encoding='UTF-8') as csvfile:
        # Create CSV Writer object
        writer = csv.writer(csvfile)
        # Write column headers to CSV file
        writer.writerow(csv_columns)
        # For writing each line to the file
        for key in dictionary:
            # Instantiate a list containing just the key - store this in write_list
            write_list = [key]
            # Make sure lists are uniform length and contain emails for each cell carrier
            for email in list(dictionary[key]):
                write_list.append(email)
            while len(write_list) < 6:
                write_list.append("")
            # Write a row of CSV
            writer.writerow(write_list)
