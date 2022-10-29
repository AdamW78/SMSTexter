"""
Used to obtain the correct cell carrier information for a given cell phone number
"""
import difflib
import sys
from time import sleep
from CarrierUtils import find_carrier


def __search_carriers(phone_number: str, carrier_dictionary: dict) -> str or list:
    """
    Method to find close matches or exact match for cell carrier from find_cell_carrier.find(number)

    :return: List close_matches of most similar to supplied carrier or correct carrier
    """
    # Perform cell carrier lookup for inputted phone_number from find_cell_carriers.find() method
    # Store in user_carrier
    user_carrier = find_carrier.get_carrier(phone_number)
    print(f"Performed cell carrier lookup for {phone_number} and found {user_carrier}!")
    # Fetches all keys from carrier_dictionary object
    keys = list(carrier_dictionary.keys())
    # Close matches is returned in more than one case - instantiate it to empty list here
    close_matches = []
    # Iterating through every cell carrier in the carrier dictionary
    for key in keys:
        # Compare user_carrier string to current cell carrier string (key)
        if user_carrier == key:
            # If they are the same string, return the string
            # We have found the correct cell carrier in our dict
            return user_carrier
        # Check if the current carrier string (key) and user_carrier contain each other
        if (key.find(user_carrier) != -1) or (user_carrier.find(key) != -1):
            # If they do, return the current cell carrier string (key)
            return key
        # Checks if either the current carrier string (key),
        # user_carrier, OR both contain a space
        if (key.find(' ') != -1) or (user_carrier.find(' ') != -1):
            # If they do, we want to check if they contain any of the same words
            # Create sets from strings by splitting them using SPACE as a delimiter
            key_words = set(key.split(' '))
            user_carrier_words = set(user_carrier.split(' '))
            # Use the built-in set .intersection() method to return values in BOTH sets
            # word_matches is the new set return by this method
            word_matches = key_words.intersection(user_carrier_words)
            # Checks that word_matches is NOT the null set
            # AND that it is NOT a set just containing "Wireless"
            if (word_matches != set()) and (word_matches != {'Wireless'}):
                # If true, check our current cell carrier string (key)
                # in order to see if it contains "Wireless" or "PCS"
                if key.find('PCS') != -1 or key.find('Wireless') != -1:
                    # If our current cell carrier string contains one of these, it is most likely
                    # the main entry for the cell carrier in carrier-dict.csv
                    # If true, return the current cell carrier string (key)
                    return key
                # Otherwise, append the current cell carrier string (key) to close_matches to return
                close_matches.append(key)
    # Add each of the 5 closest matches lexicographically to close_matches
    for match in difflib.get_close_matches(user_carrier,
                                           list(carrier_dictionary.keys()),
                                           n=5, cutoff=0.2):
        close_matches.append(match)
    # Return close_matches
    return close_matches


def setup(phone_number: str, carrier_dictionary: dict) -> str:
    """
    Function used for performing necessary cell carrier setup for a given phone number

    :param phone_number: String phone number used when searching for a cell carrier
    :param carrier_dictionary: Dict object with cell carriers and their text-to-email addresses
    :return: User's cell carrier as a string findable in the carrier dictionary
    """
    # Fetch list of cell carriers or cell carrier string by running __search_carriers function
    # Stores returned value in carrier_list
    carrier_list = __search_carriers(phone_number, carrier_dictionary)
    # Check if carrier_list is a string
    if isinstance(carrier_list, str):
        # If true, return carrier_list
        return carrier_list
    # In this case carrier_list is NOT a string - this means it is a list
    # Getting user's carrier selection from carrier_list can raise multiple exception
    # Return the selected carrier from __get_carrier_selection
    return __get_carrier_selection(carrier_list)


def __get_carrier_selection(close_matches: list) -> str:
    """
    Takes user input to obtain selection from close_matches

    :param close_matches: List of close matches returned from __search_carriers() - list of strings
    :return: User carrier selection as string
    :raises TypeError Asks for a numerical input choice, this is raised if the input (string)
    cannot be converted to an int (usually means user did not input a number)
    :raises IndexError If the numerical input provided is out of bounds, this is raised
    :raises ValueError Asks for a yes/no user input, raised if user input is NOT: "Y"/"y" or "N"/"n"
    """
    # Method is only called when automated carrier search fails
    # Send messages to user to notify them of what is going on
    print("We're having some trouble determining your cell carrier in our databases...")
    print("Is one of the below your cell carrier?")
    # Iterate through each cell carrier string in close_matches
    for i in enumerate(close_matches):
        # Check if we are on the first iteration of the loop
        if i == 0:
            # Print the closest cell carrier match found
            print(f"Closest match was: \"{close_matches[0]}\"")
        # Every other iteration of the loop besides the first one
        else:
            # Print the next closest cell carrier match
            print(f"Next closest match was: \"{close_matches[i]}\"")
    # Get input from user - was one of the printed cell carrier's theirs?
    yes_no = input("Is one of these correct? Yes/No)").casefold()
    # Check if input received was no
    if yes_no in set('n', 'no'):
        # Exit the program
        print("Unable to find your cell carrier. Exiting...")
        sleep(3)
        sys.exit(0)
    # Check if input received was yes
    if yes_no in set('y', 'ye', 'yes'):
        # Print matches as a numerical list
        for k in enumerate(close_matches):
            print(f"{k + 1}. {close_matches[k]}")
        # Ask for numerical input from user selecting cell carrier from list
        number_choice = input("Please select the number of your cell carrier: ")
        num = int(number_choice)
        # Check if user input is out of bounds
        if num > len(close_matches) or num <= 0:
            # Raise IndexError
            print(f"Error: Input \"{number_choice}\" is not a listed carrier. Exiting...")
            raise IndexError(f"User input \"{number_choice}\" was out of bounds.")
        # Fetch the user's choice from close_matches and return cell carrier string
        carrier_choice = close_matches[num - 1]
        print(f"Chosen carrier: {carrier_choice}")
        return carrier_choice
    # Input received was invalid
    print(f"Error: Input \"{yes_no}\" is invalid. Exiting...")
    raise ValueError("User input \"{yes_no}\" was invalid. Please enter \"y\" or \"n\".")
