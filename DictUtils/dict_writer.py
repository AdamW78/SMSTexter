"""
Module used to write and locally store dictionary file
"""
import csv


def write(dictionary, filename):
    """
    Writes passed in cell carrier dictionary to csv file to cache locally

    :param dictionary: dict object containing cell carrier keys as strings
    and lists of text-to-email addresses as strings
    :param filename: string name of csv file to write
    :raises IOError: If writing to the CSV file fails, raise an IOError
    """
    csv_columns = ["Cell Carrier", "Email 1", "Email 2", "Email 3", "Email 4", "Email 5", "Email 6"]
    csv_file = "DictUtils/" + filename + ".csv"
    with open(csv_file, 'w', 'UTF-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_columns)
        for key in dictionary:
            write_list = list()
            write_list.append(key)
            for email in list(dictionary[key]):
                write_list.append(email)
            while len(write_list) < 6:
                write_list.append("")
            writer.writerow(write_list)
