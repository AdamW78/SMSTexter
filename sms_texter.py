#
# Originally Sourced from:
# Author D3ISM3
# Edited by Adam W
# https://gist.github.com/D3ISM3/743d2119562c3e01d9e09baf8c5df328#file-sendtextmessage-py
# Modified to support multiple senders
# Modified to simplify for specific use-case (Sending rush text-messages)
#

import smtplib
import sys
import constants
from DictUtils import carrier_dict_loader
import difflib
from CarrierUtils import find_cell_carrier


def start_server(mail_server="smtp.gmail.com", port=587, email=constants.EMAIL,
                 app_password=constants.PASSWORD):
    server = smtplib.SMTP(mail_server, port)
    server.starttls()
    server.login(email, app_password)
    return server


class SMSTexter:

    def __init__(self, phone_number, multi=False):
        self.carrier_dictionary = carrier_dict_loader.carrier_dictionary()
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
        Fetches user's desired cell carrier to text on from setup()
        Creates recipient string email address by concatenating inputted phone number
        and the found email address for texting for selected cell carrier
        Ex: 1234567890@txt.att.net
        """
        if self.multi:
            for number in self.phone_number:
                self.text_to_email_send(number)
        else:
            self.text_to_email_send(self.phone_number)

    def text_to_email_send(self, phone_number: str):
        """
        Helper method used for actually sending a
        :param phone_number:
        :return:
        """
        recipient = f"{phone_number}{list(self.carrier_dictionary[self.cell_carrier])[0]}"
        if not constants.DRY_RUN:
            try:
                self.server.sendmail(constants.EMAIL, recipient, constants.MESSAGE)
            except smtplib.SMTPRecipientsRefused:
                print("Error: Could not send to that address")
        else:
            print("DRY RUN COMPLETED - NO TEXT MESSAGE SENT!")
            print(f"Using Cell Carrier info for Carrier: {self.cell_carrier}")
            print(f"Recipient Mail Address: {recipient}")
            print("SUCCESS!")
            sys.exit(0)