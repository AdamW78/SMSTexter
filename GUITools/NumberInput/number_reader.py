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
    if filename.endswith('.txt'):
        with open(filename, 'r', encoding='UTF-8') as textfile:
            phone_number_list = []
            for line in textfile.readlines():
                line = str(line.strip())
                phone_num = phonenumbers.parse("+1" + line)
                if line.isnumeric() and phonenumbers.is_possible_number(phone_num):
                    phone_number_list.append(line)
                else:
                    raise IOError("Please include ONE 10-digit phone number on each line!")
            return phone_number_list

    else:
        raise IOError("Only .txt files are accepted!")
