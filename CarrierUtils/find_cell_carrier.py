from twilio.rest import Client
import constants
from Cache import cache_cell_carrier


def get_carrier(number):
    cache_result = cache_cell_carrier.is_cached(number)
    if isinstance(cache_result, str):
        return cache_result
    url = f"https://lookups.twilio.com/v2/PhoneNumbers/{number}"
    account_sid = constants.TWILIO_SID
    auth_token = constants.AUTH_TOKEN
    client = Client(account_sid, auth_token)
    phone_number = client.lookups \
        .v1 \
        .phone_numbers(number) \
        .fetch(type=['carrier'])
    cell_carrier = phone_number.carrier['name']
    cache_cell_carrier.cache(number, cell_carrier)
    if constants.DEBUG:
        print(f"Received response from Twilio for {number} - Carrier: {cell_carrier}")
    return cell_carrier
