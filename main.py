from sms_texter import SMSTexter
import constants

if __name__ == "__main__":
    texter = SMSTexter(constants.PHONE_NUMBER)
    texter.send_message()
