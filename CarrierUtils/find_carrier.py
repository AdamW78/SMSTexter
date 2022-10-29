"""
Uses either Twilio API or locally cached cell carrier value to return cell carrier
"""
from twilio.rest import Client
import constants
from CarrierUtils import cache_carrier


def get_carrier(number):
    """
    Method used for fetching cell carrier for supplied number

    :param number: String phone number for which cell carrier will be returned
    :return: String cell carrier found either locally or using Twilio API
    """
    # Check if String number is cached locally
    cache_result = cache_cell_carrier.is_cached(number)
    # Check if the cache lookup result is a string
    if isinstance(cache_result, str):
        # It is a string, found cell carrier locally, return cell carrier string
        return cache_result
    # Values below stored in constants.py - untracked file
    account_sid = constants.TWILIO_SID
    auth_token = constants.AUTH_TOKEN
    # Code below sourced directly from Twilio documentation
    client = Client(account_sid, auth_token)
    phone_number = client.lookups \
        .v1 \
        .phone_numbers(number) \
        .fetch(type=['carrier'])
    cell_carrier = phone_number.carrier['name']
    # Cache cell carrier Twilio returns locally in JSON file
    cache_cell_carrier.cache(number, cell_carrier)
    if constants.DEBUG:
        print(f"Received response from Twilio for {number} - Carrier: {cell_carrier}")
    # Return the cell carrier found by the Twilio API
    return cell_carrier
