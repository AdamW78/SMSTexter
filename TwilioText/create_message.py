from twilio.rest import Client

import constants


def text(number: str, message: str):

    account_sid = constants.TWILIO_SID
    auth_token = constants.AUTH_TOKEN
    client = Client(account_sid, auth_token)
    text_message = client.messages.create(
        from_=constants.TWILIO_PHONE_NUMBER,
        messaging_service_sid='MG2168ce1be1b55e05579770f61e7ccbd8',
        body=message,
        provide_feedback=True,
        to=number
    )
    if text_message.status != 'accepted':
        raise IOError("Could not send text using Twilio API")


