import csv

import constants


def read(file_data) -> dict:
    """
    Method to create dictionary object from DictUtils/carrier-dict.csv

    :param filename: File to create dictionary object from
    :return: Dictionary object created from contents of filename
    """
    if isinstance(file_data, str):
        file = open(file_data, 'rb')
        return read(file)
    else:
        # Create empty dictionary to append and return
        carrier_dictionary = {}
        for line in file_data.readlines():
            line = str(line)
            email_list = line.split(',')
            if email_list[0] == "b\'Cell Carrier" or email_list[0] == "b'":
                continue
            else:
                cell_carrier = email_list.pop(0)
                cell_carrier = cell_carrier[2:]
                i = len(email_list)-1
                while i > 0:
                    if email_list[i] == '' or email_list[i] == '\\r\\n\'':
                        email_list.pop(i)
                    i -= 1
                if constants.DEBUG:
                    print(f"Adding entry for cell carrier: {cell_carrier} with email list {email_list}!")
                carrier_dictionary[cell_carrier] = email_list
    # Return dictionary created above
    return carrier_dictionary
