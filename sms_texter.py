import smtplib
import constants
from DictUtils import carrier_dict_loader
from CarrierUtils import carrier_setup


class SMSTexter:
    @staticmethod
    def __text_to_email_send(phone_number: str, cell_carrier: str, carrier_dictionary: dict, server: smtplib.SMTP):
        """
        Static helper method used for actually sending an SMS message

        :param server: SMTP object used to send email
        :param carrier_dictionary: Dictionary containing cell carriers and their text-to-email addresses
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

        :param phone_number: string or list containing phone_number or phone_numbers to run
        """
        # Set object variables
        self.carrier_dictionary = carrier_dict_loader.carrier_dictionary()
        self.multi = isinstance(phone_number, list)
        self.phone_number = phone_number
        # Check if supplied with using multiple phone numbers
        if self.multi:
            # If true, create an empty list object, carrier_list, to fill with cell carrier strings
            carrier_list = []
            # Iterate through every provided phone number
            for number in phone_number:
                # Add the cell carrier string from each phone number to carrier_list
                carrier_list.append(carrier_setup.setup(number, self.carrier_dictionary))
            # Set cell_carrier object variable to carrier_list filled with cell carrier strings
            self.cell_carrier = carrier_list
        # Supplied with single number
        else:
            # Set cell_carrier object variable to cell carrier string for phone_number
            self.cell_carrier = carrier_setup.setup(phone_number, self.carrier_dictionary)

    def send_message(self):
        """
        Main method for class, calls helper method that actually sends text message
        """
        # Check if using multiple phone numbers
        if self.multi:
            # If true, iterate through every supplied phone number
            for number in range(len(self.phone_number)):
                # Send text to phone number using helper method
                self.__text_to_email_send(self.phone_number[number], self.cell_carrier[number], self.carrier_dictionary, self.__start_server())
        # Using a single phone number
        else:
            # Send text to phone number using helper method
            self.__text_to_email_send(self.phone_number, self.cell_carrier, self.carrier_dictionary, self.__start_server())
