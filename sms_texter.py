"""
Main module used for sending texts
Contains SMSTexter class
"""
import smtplib
from os.path import exists

import constants
from DictUtils import dict_loader
from CarrierUtils import carrier_setup
from GUITools.NumberInput import number_reader


class SMSTexter:
    """
    Class used for automated sending of texts
    """

    @staticmethod
    def __text_to_email_send(phone_number: str, cell_carrier: str,
                             carrier_dictionary: dict, server: smtplib.SMTP):
        """
        Static helper method used for actually sending an SMS message

        :param server: SMTP object used to send email
        :param carrier_dictionary: Dict containing cell carriers and their text-to-email addresses
        :param cell_carrier: String cell carrier to use to build text-to-email address
        :param phone_number: String phone number to which SMS message is sent
        """
        # Build text-to-email address for phone_number parameter
        recipient = f"{phone_number}{list(carrier_dictionary[cell_carrier])[0]}"
        # Check if performing dry run
        if constants.DRY_RUN:
            # Print success messages
            print("DRY RUN COMPLETED - NO TEXT MESSAGE SENT!")
            SMSTexter.__success_message(cell_carrier, recipient)
        else:
            try:
                # Send SMS text and print success messages
                server.sendmail(constants.EMAIL, recipient, constants.MESSAGE)
                SMSTexter.__success_message(cell_carrier, recipient)
            except smtplib.SMTPRecipientsRefused:
                print("Error: Could not send to that address")

    @staticmethod
    def __start_server(mail_server="smtp.gmail.com", port=587, email=constants.EMAIL,
                       app_password=constants.PASSWORD):
        server = smtplib.SMTP(mail_server, port)
        server.starttls()
        server.login(email, app_password)
        return server

    @staticmethod
    def __success_message(cell_carrier: str, recipient: str):
        print(f"Using Cell Carrier info for Carrier: {cell_carrier}")
        print(f"Recipient Mail Address: {recipient}")
        print("SUCCESS!")

    def __init__(self, phone_number):
        """
        Method called on SMSTexter instantiation

        :param phone_number: string or path to list
        containing phone_number or phone_numbers to run
        """
        # Fetch CSV file containing cell carriers and their text-to-email
        # addresses. Convert the CSV file into a dictionary containing string
        # cell carriers and lists of string text-to-email addresses
        self.carrier_dictionary = carrier_dict_loader.carrier_dictionary()
        # Determine whether phone number string or path string to file was supplied
        # If a phone number, multi is False
        # If a path to a file, multi is true
        self.multi = exists('/' + phone_number)
        # Supplied with path to file
        if self.multi:
            # Update path string to be an absolute path rather than a relative one
            phone_number = '/' + phone_number
            # If true, create an empty list object, carrier_list, to fill with cell carrier strings
            carrier_list = []
            # Replace string in self.phone_number with list object returned by number_reader
            # List object is created from the path supplied iff path is to .txt file
            # Otherwise, raises exception
            # Additionally verifies line-by-line that each string is a number
            # and exactly 10 characters long
            self.phone_number = number_reader.read(phone_number)
            # Iterate through every provided phone number
            for number in self.phone_number:
                # Add the cell carrier string from each phone number to carrier_list
                carrier_list.append(carrier_setup.setup(number, self.carrier_dictionary))
            # Set cell_carrier object variable to carrier_list filled with cell carrier strings
            self.cell_carrier = carrier_list
            if constants.DEBUG:
                print("Using more than one phone number - ready to send multiple messages...")
        # Supplied with single number
        else:
            # Set cell_carrier object variable to cell carrier string for phone_number
            self.phone_number = phone_number
            self.cell_carrier = carrier_setup.setup(phone_number, self.carrier_dictionary)
        if constants.DEBUG:
            print("Phone Number:", self.phone_number)
        if constants.DEBUG_HARD:
            print("Cell Carrier Dictionary Contents:\n", self.carrier_dictionary)

    def send_message(self):
        """
        Main method for class, calls helper method that actually sends text message
        """
        # Check if using multiple phone numbers
        if self.multi:
            # If true, iterate through every supplied phone number
            for number in range(len(self.phone_number)):
                # Send text to phone number using helper method
                self.__text_to_email_send(self.phone_number[number],
                                          self.cell_carrier[number],
                                          self.carrier_dictionary,
                                          self.__start_server())
        # Using a single phone number
        else:
            # Send text to phone number using helper method
            self.__text_to_email_send(self.phone_number,
                                      self.cell_carrier,
                                      self.carrier_dictionary,
                                      self.__start_server())
