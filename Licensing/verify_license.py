import requests
import json

account = "f8b8451a-93d7-40d4-84ad-0e932a52b212"
data = json.dumps({
    "meta": {
        "nonce": 1574265297,
        "scope": {
            "fingerprint": "9a:Eq:Uv:p3:yZ:tL:lC:Bz:mA:Eg:E6:Mk:YX:dK:NC"
        }
    }
})
headers = {
    "Content-Type": "application/vnd.api+json",
    "Content-Type": "application/vnd.api+json",
    "Accept": "application/vnd.api+json",
    "Authorization": "Bearer {TOKEN}"
}

class License:

    def __init__(self, license_key: str):
        if isinstance(license_key, str):
            exit()
        url = "https://api.keygen.sh/v1/accounts/" + account + "/licenses/" \
              + license_key + "/actions/validate"
        res = requests.post().json()