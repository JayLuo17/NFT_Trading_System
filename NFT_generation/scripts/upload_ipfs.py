import os
from pathlib import Path
import requests
import json

PINATA_BASE_URL = "https://api.pinata.cloud/"
endpoint = "pinning/pinJSONToIPFS"

print(os.getenv("PINATA_API_KEY"))
print(os.getenv("PINATA_APT_SECRET"))
headers = {
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_APT_SECRET"),
    "Content-Type": "application/json",
}


def upload(data):
    response = requests.post(
        PINATA_BASE_URL + endpoint,
        headers=headers,
        data=json.dumps(data),
    )
    if response.status_code != 200:
        print(f"Error uploading to Pinata: {response.content}")
    else:
        print(f"Successfully uploaded to Pinata. Hash: {response.json()['IpfsHash']}")


if __name__ == "__main__":
    data = {
        "name": "testing",
        "pinataMetadata": {
            "name": "testing",
            "keyvalues": {"k1": "blabla1", "k2": "blabla2"},
        },
        "pinataContent": {"somekey": "somevalue1111"},
    }
    upload(data)
