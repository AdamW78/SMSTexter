"""
Main module  - should actually be run
"""

import constants
from sms_texter import SMSTexter

if __name__ == "__main__":
    texter = SMSTexter(constants.PHONE_NUMBER)
    texter.send_message()
