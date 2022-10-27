import csv


def read(filename: str) -> dict:
    """
    Method to create dictionary object from carrier-dict.csv

    :param filename: File to create dictionary object from
    :return: Dictionary object created from contents of filename
    """
    # Create empty dictionary to append and return
    carrier_dictionary = {}
    with open(filename, 'r') as csvfile:
        for csv_row in csv.reader(csvfile, delimiter=','):
            # Skip useless lines of file (first 2)
            if csv_row[0] == '' or csv_row[0] == 'Cell Carrier':
                continue
            # Create list out of current row
            email_list = list(csv_row)
            # Pop carrier (always at index 0) from list
            carrier = email_list.pop(0)
            # Remove blank entries from list
            formatted_email_list = [email for email in email_list if email != '']
            # Update carrier dictionary entry for carrier with formatted list of text-to-email emails
            carrier_dictionary[carrier] = formatted_email_list
    # Return dictionary created above
    return carrier_dictionary

