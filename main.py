#
# Originally Sourced from:
# Author D3ISM3
# Edited by Adam W
# https://gist.github.com/D3ISM3/743d2119562c3e01d9e09baf8c5df328#file-sendtextmessage-py
# Modified to support multiple senders
# Modified to simplify for specific use-case (Sending rush text-messages)
#
import smtplib
import Constants
import CarrierDictLoader
import difflib

from SMSTexter import FindCellCarrier


def get_carrier_selection(close_matches: list) -> str:
    """
    Takes in a list of close matches for a cell carrier and gets the user to select the one they would like to text

    Prints "Could not find your exact input in our carrier list.", iterates through close_matches and prints each string
    Asks for yes/no input ("Is one of these correct? Enter \"y\" for yes or \"n\" for no: ") - is one of the printed values desired cell carrier
    If no, exit the program
    If yes, iterate through and print a numbered version of each string in list close_matches
    Asks for user input (numerical) to select the desired cell carrier
    Returns selected carrier
    :param close_matches: List of close matches returned from search_carriers() - list of strings
    :return: User carrier selection as string
    :raises TypeError Asks for a numerical input choice, this is raised if the input (string) cannot be converted to an int (usuallu means user did not input a number)
    :raises IndexError If the numerical input provided is out of bounds of list of options provided, this is raised
    :raises ValueError Asks for a yes/no user input, raised if user input is NOT: "Y"/"y" or "N"/"n"
    :
    """

    print("Could not find your exact input in our carrier list.")
    for i in range(len(close_matches)):
        if i == 0:
            print(f"Closest match was: \"{close_matches[0]}\"")
        else:
            print(f"Next closest match was: \"{close_matches[i]}\"")
    yes_no = input("Is one of these correct? Enter \"y\" for yes or \"n\" for no: ").casefold()
    if yes_no == "n":
        print("Unable to find your cell carrier. Exiting...")
        exit(0)
    elif yes_no == "y":
        for k in range(len(close_matches)):
            print(f"{k + 1}. {close_matches[k]}")
        number_choice = input("Please select the number of your cell carrier: ")
        try:
            num = int(number_choice)
        except ValueError:
            print(f"Error: Input \"{number_choice}\" is invalid. Exiting...")
            raise TypeError(f"User input \"{number_choice}\" failed to convert from string to integer.")
        if num > len(close_matches) or num <= 0:
            print(f"Error: Input \"{number_choice}\" is not a listed carrier. Exiting...")
            raise IndexError(f"User input \"{number_choice}\" was out of bounds for cell carrier list.")
        else:
            print(len(close_matches))
            carrier_choice = close_matches[num - 1]
            print(f"Chosen carrier: {carrier_choice}")
            return carrier_choice
    else:
        print(f"Error: Input \"{yes_no}\" is invalid. Exiting...")
        raise ValueError("User input \"{yes_no}\" was invalid. Please enter \"y\" or \"n\".")


def start_server(mail_server="smtp.gmail.com", port=587, email=Constants.EMAIL,
                 app_password=Constants.PASSWORD):
    server = smtplib.SMTP(mail_server, port)
    server.starttls()
    server.login(email, app_password)
    return server


class SMSTexter:

    def __init__(self, phone_number: str, multi=False):
        self.carrier_dictionary = CarrierDictLoader.carrier_dictionary()
        self.multi = multi
        self.phone_number = phone_number
        self.server = start_server()
        if multi:
            carrier_list = list()
            for number in phone_number:
                try:
                    carrier_list.append(self.carrier_setup(number))
                except:
                    raise Exception(f"Failed to initialize SMSTexter for {number}")
            self.cell_carrier = carrier_list
        else:
            try:
                self.cell_carrier = self.carrier_setup(phone_number)
            except:
                raise Exception(f"Failed to initialize SMSTexter for {phone_number}")

    def send_message(self):
        """
        Main method for class, calls helper methods and actually sends text message

        Calls setup() and stores email from which to send text
        Fetches user's desired cell carrier to text on from carrier_setup()
        Creates recipient string email address by concatenating inputted phone number
        and the found email address for texting for selected cell carrier
        Ex: 1234567890@txt.att.net
        """
        if self.multi:
            for phone_number in self.phone_numbers:
                self.text_to_email_send(phone_number)
        else:
            self.text_to_email_send(self.phone_number)

    def text_to_email_send(self, phone_number: str):
        recipient = f"{phone_number}{list(self.carrier_dictionary[self.cell_carrier])[0]}"
        if not Constants.DRY_RUN:
            try:
                self.server.sendmail(Constants.EMAIL, recipient, Constants.MESSAGE)
            except smtplib.SMTPRecipientsRefused:
                print("Error: Could not send to that address")
        else:
            print("DRY RUN COMPLETED - NO TEXT MESSAGE SENT!")
            print(f"Using Cell Carrier info for Carrier: {self.cell_carrier}")
            print(f"Recipient Mail Address: {recipient}")
            print("SUCCESS!")
            exit(0)

    def search_carriers(self, phone_number: str) -> str or list:
        """
        Method to search dictionary of cell carriers to find close matches or exact match for cell carrier from FindCellCarrier.find(number)

        Fetches cell carrier as a string using FindCellCarrier's find method
        Fetches list of cell carriers in carrier_dictionary
        Iterate through carriers in the carrier dictionary carrier-by-carrier
        If current cell carrier string is in carrier_dictionary, return the current carrier string
        Else, check if the current carrier string and the found carrier contain each other - if so, add it to close matches
        Then, return a list of the 5 most lexicographically similar strings to user_carrier from carrier_dictionary
        :return: List close_matches of 5 most lexicographically similar strings to user_carrier OR exact match
        """
        user_carrier = FindCellCarrier.get_carrier(phone_number)
        keys = list(self.carrier_dictionary.keys())
        close_matches = list()
        word_match = False
        for key in keys:
            if user_carrier == key:
                return user_carrier
            elif (key.find(user_carrier) != -1) or (user_carrier.find(key) != -1):
                return key
            if (key.find(' ') != -1) or (user_carrier.find(' ') != -1):
                key_words = set(key.split(' '))
                user_carrier_words = set(user_carrier.split(' '))
                word_matches = key_words.intersection(user_carrier_words)
                if (word_matches != set()) and (word_matches != {'Wireless'}):
                    close_matches.append(key)
                    word_match = True
        if word_match:
            for match in close_matches:
                if match.find('PCS') != -1 or match.find('Wireless') != -1:
                    return match
            return close_matches
        return difflib.get_close_matches(user_carrier, list(self.carrier_dictionary.keys()), n=5, cutoff=0.2)

    def carrier_setup(self, phone_number: str) -> str:
        """
        Calls search_carriers() to return either the found carrier or list of close matches to Constants.CARRIER
        Checks to see if search_carriers() returned a list or a single carrier
        If a single carrier, returns just that carrier
        :return: User's cell carrier as a string findable in the carrier dictionary

        """
        carrier_list = self.search_carriers(phone_number)
        if isinstance(carrier_list, str):
            return carrier_list
        else:
            try:
                carrier_selection = get_carrier_selection(carrier_list)
            except ValueError or IndexError or TypeError:
                raise Exception(f"Carrier setup was unsuccessful for {phone_number}.")
            return carrier_selection


if __name__ == "__main__":
    o = SMSTexter(Constants.PHONE_NUMBER)
    o.send_message()
