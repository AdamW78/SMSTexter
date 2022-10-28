"""
File used to read in carrier-dict.csv and convert it to a dict object
"""
import constants


def read(file_data) -> dict:
    """
    Method to create dictionary object from DictUtils/carrier-dict.csv

    :param file_data:
    :param filename: File to create dictionary object from
    :return: Dictionary object created from contents of filename
    """
    if isinstance(file_data, str):
        with open(file_data, 'r', 'UTF-8') as dictfile:
            return read(dictfile)
    # Create empty dictionary to append and return
    carrier_dictionary = {}
    # Use the file readlines to iterate through the file - CSV wasn't working
    for line in file_data.readlines():
        # Convert line to a string
        line = str(line)
        # Form list by splitting line string with delimiter ','
        email_list = line.split(',')
        # Ignore first two rows of file (headers and example)
        if email_list[0] == "b\'Cell Carrier" or email_list[0] == "b'":
            continue
        # Cell carrier is first item in list, pop and store it in cell_carrier
        cell_carrier = email_list.pop(0)
        # Cut off weird extra text at beginning of string
        cell_carrier = cell_carrier[2:]
        # Iterate through email list one at a time and delete empty items
        i = len(email_list)-1
        while i > 0:
            if email_list[i] == '' or email_list[i] == '\\r\\n\'':
                email_list.pop(i)
                i -= 1
            if constants.DEBUG:
                print(f"Adding cell carrier: {cell_carrier} with email list {email_list}!")
        # Update dict object to include value cell_carrier for key phone_number
        carrier_dictionary[cell_carrier] = email_list
    # Return dictionary created above
    return carrier_dictionary
