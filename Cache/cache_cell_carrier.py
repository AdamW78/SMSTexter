from os.path import exists
import os
import json
import constants


def cache(phone_number: str, cell_carrier: str):
    """
    Method used for locally caching phone numbers and their cell carriers to limit Twilio API requests

    :param phone_number: String phone number to cache
    :param cell_carrier: String cell carrier for the phone number to cache
    """
    carrier_json = constants.LOCAL_CACHE_PATH
    # Check if the cache file does NOT exist:
    cache_result = is_cached(phone_number)
    if cache_result == 0:
        if constants.DEBUG:
            print("Local cell phone numbers and cell carriers cache did not exist, creating now...")
        # Create and write entry for phone_number to local cache
        __write_data(carrier_json, {phone_number: cell_carrier})
    # Check if the specific phone number string "phone_number" is NOT already cached:
    elif cache_result == -1:
        # Check if local cache file is blank
        if os.stat(carrier_json).st_size == 0:
            if constants.DEBUG:
                print("Found blank JSON cache, writing to it now...")
            # Create and write entry for phone_number to local cache
            __write_data(carrier_json, {phone_number: cell_carrier})
        # The cache file is NOT blank and the specific phone number response is -1
        # This means the phone number is NOT already cached locally
        else:
            if constants.DEBUG:
                print("Found existing non-empty local cache, appending it with new data now...")
            # Load current local cache into dictionary variable data
            data = __load_data(carrier_json)
            # Add current phone_number and cell_carrier values to end of dictionary
            data[phone_number] = cell_carrier
            # Write updated dictionary to local cache
            __write_data(carrier_json, data)
    # The cache file is exists and is_cached(phone_number) returned a value NOT -1
    # This means phone_number already has a cell carrier cached locally
    else:
        # Check that the local cache is accurate with currently used information
        data = __load_data(carrier_json)
        if data[phone_number] != cell_carrier:
            if constants.DEBUG:
                print("Found outdated local cache information, updating it...", end=' ')
            # If local cache is NOT accurate, update it!
            data[phone_number] = cell_carrier
            __write_data(carrier_json, data)
            if constants.DEBUG:
                print("Complete!")
        # Phone number is already locally cached, cache is up-to-date, do nothing
        else:
            if constants.DEBUG:
                print("Found correct information already cached locally, skipping caching!")


def __load_data(json_file: str) -> dict:
    """
    Helper method used for reading from local json cache file

    :param json_file: json cache file from which to read
    :return: dict object containing phone numbers and their cell carriers loaded from local cache
    """
    # Open the json_file parameter for reading using a with-open-as statement
    with open(json_file, 'r', encoding='UTF-8') as jsonfile:
        # Use the json.load() function to create a dictionary out of the local cache json file
        data = json.load(jsonfile)
    # Return the created dictionary
    return data


def __write_data(json_file: str, data_dict: dict):
    """
    Helper method used for writing a dict object to a json file to locally cache numbers and carriers

    :param json_file: String filename to which the dictionary parameter will be written as JSON
    :param data_dict: dict object containing phone numbers and their corresponding cell carriers
    """
    # Open the json_file parameter for writing using a with-open-as statement
    with open(json_file, 'w', encoding='UTF-8') as jsonfile:
        # Write the data_dict parameter to the json_file parameter
        json.dump(data_dict, jsonfile)


def is_cached(phone_number) -> str or int:
    """
    Method to check whether a phone number is already locally cached or not

    :param phone_number: String phone number to check local cache for
    :return: str cell_carrier if one is found or int -1 if one is not
    """
    carrier_json = constants.LOCAL_CACHE_PATH
    if constants.DEBUG:
        print(f"Checking if phone number {phone_number} is cached:", end=' ')
    # If the local cache file does not exist, return 0
    cache_exists = exists(carrier_json)
    if not cache_exists:
        return 0
    # If the local cache file has a size of 0 (empty file), return 1
    elif os.stat(carrier_json).st_size == 0:
        return -1
    # Local cache exists and is not empty - load it into a dictionary object for checking
    else:
        data = __load_data(carrier_json)
        # Check if the local cache contains the phone number
        if (list(data.keys()).count(phone_number)) != 0:
            # It does - return the cell carrier stored from the phone number
            return data[phone_number]
        # It does not contain the phone number - return -1
        else:
            return -1
