from os.path import exists
import os
import json
import constants

exist = exists("cached-carriers.json")


def cache(phone_number: str, cell_carrier: str):
    if not exist or is_cached(phone_number) is None:
        with open('Cache/cached-carriers.json', 'w') as jsonfile:
            json.dump({phone_number: cell_carrier}, jsonfile)
    if constants.DEBUG:
        print("Response cached successfully to \"cached-carriers.json\".")


def is_cached(phone_number) -> str:
    if constants.DEBUG:
        print(f"Checking if phone number {phone_number} is cached:", end=' ')
    if not exist:
        if constants.DEBUG:
            print("Dict-file does not exist!")
        return None
    elif os.stat('cached-carriers.json').st_size == 0:
        if constants.DEBUG:
            print("Dict file is blank!")
        return None
    with open('cached-carriers.json', 'r') as jsonfile:
        file = json.load(jsonfile)
        if list(dict(file).keys()).count(phone_number) != 0:
            if constants.DEBUG:
                print(f"Successfully found locally cached phone number and cell carrier!")
            return file[phone_number]
