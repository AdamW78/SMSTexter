"""
Simple module for creating list from .txt file and returning the list
"""
import phonenumbers as phonenumbers


def read(filename: str) -> list:
    """
    Function used to read in a .txt file containing one phone number per line

    :param filename: string path to .txt file to read - supplied by GUI
    :return: list object of 10-digit phone number strings
    """
    # Make sure filename parameter is a string path to a .txt file
    if filename.endswith('.txt'):
        # Open .txt file at filename parameter path
        with open(filename, 'r', encoding='UTF-8') as textfile:
            # Create empty list literal to add lists of phone numbers and attached variables
            phone_number_list = []
            # Iterate line-by-line through .txt file
            for line in textfile.readlines():
                # Strip each line of all space, tab, newline, etc. characters
                line = str(line.strip())
                # Split line into list using ',' as the delimiter
                num_vars = line.split(',')
                # Create a phonenumbers PhoneNumber object to check if number is valid format
                phone_num = phonenumbers.parse("+1" + num_vars[0])
                # Check if number is a valid format
                if phonenumbers.is_possible_number(phone_num):
                    # Number is in a valid format, list with phone number and every variable after
                    # phone number delimited by a ',' in filename is added to phone_number_list
                    phone_number_list.append(num_vars)
                else:
                    raise IOError("Please include ONE 10-digit phone number on each line!")
            return phone_number_list

    else:
        if filename is "":
            raise IOError("No phone number input provided!")
        raise IOError("Only .txt files are accepted!")

