from twilio.rest import Client
from SMSTexter import Constants, CacheCellCarrier


def get_carrier(number):
    cache_result = CacheCellCarrier.is_cached(number)
    if isinstance(cache_result, str):
        return cache_result
    url = f"https://lookups.twilio.com/v2/PhoneNumbers/{number}"
    account_sid = Constants.TWILIO_SID
    auth_token = Constants.AUTH_TOKEN
    client = Client(account_sid, auth_token)
    phone_number = client.lookups \
        .v1 \
        .phone_numbers(number) \
        .fetch(type=['carrier'])
    cell_carrier = phone_number.carrier['name']
    CacheCellCarrier.cache(number, cell_carrier)
    if Constants.DEBUG:
        print(f"Received response from Twilio for {number} - Carrier: {cell_carrier}")
    return cell_carrier
