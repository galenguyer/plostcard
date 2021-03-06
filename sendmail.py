from posix import environ
import time
import os
import base64
import requests
from dotenv import load_dotenv
import time

import json

load_dotenv()

def get_auth_header():
    username = os.environ.get("CLICKSEND_USERNAME")
    password = os.environ.get("CLICKSEND_PASSWORD")
    creds = username+":"+password
    bytes = creds.encode('ascii')
    base64_bytes = base64.b64encode(bytes)
    encoded = base64_bytes.decode("ascii")
    return "Basic " + encoded

headers = {
    'Authorization': get_auth_header(),
    'Content-Type': 'application/json'
}

if os.environ.get("GALEN_ADDRESS_NAME") == "":
    print("Missing GALEN_ADDRESS_NAME")
if os.environ.get("GALEN_ADDRESS_LINE_1") == "":
    print("Missing GALEN_ADDRESS_LINE_1")
if os.environ.get("GALEN_ADDRESS_LINE_2") == "":
    print("Missing GALEN_ADDRESS_LINE_2")
if os.environ.get("GALEN_ADDRESS_CITY") == "":
    print("Missing GALEN_ADDRESS_CITY")
if os.environ.get("GALEN_ADDRESS_STATE") == "":
    print("Missing GALEN_ADDRESS_CITY")
if os.environ.get("GALEN_ADDRESS_POSTAL_CODE") == "":
    print("Missing GALEN_ADDRESS_POSTAL_CODE")
if os.environ.get("GALEN_ADDRESS_COUNTRY") == "":
    print("Missing GALEN_ADDRESS_COUNTRY")
if os.environ.get("RETURN_ADDRESS_ID") == "":
    print("Missing RETURN_ADDRESS_ID")

recipients = [
    {
        "address_name": os.environ["GALEN_ADDRESS_NAME"],
        "address_line_1": os.environ["GALEN_ADDRESS_LINE_1"],
        "address_line_2": os.environ.get("GALEN_ADDRESS_LINE_2"),
        "address_city": os.environ["GALEN_ADDRESS_CITY"],
        "address_state": os.environ["GALEN_ADDRESS_STATE"],
        "address_postal_code": int(os.environ["GALEN_ADDRESS_POSTAL_CODE"]),
        "address_country": os.environ["GALEN_ADDRESS_COUNTRY"],
        "return_address_id": int(os.environ["RETURN_ADDRESS_ID"]),
        "schedule": int(time.time())+(24*60*60)
    }
]

data = {
    "file_url": "https://plostcard.galenguyer.workers.dev",
    "template_used": 0,
    "colour": 0,
    "duplex": 0,
    "priority_post": 0,
    "recipients": recipients
}

#requests.post(' https://rest.clicksend.com/v3/post/letters/send', json=data, headers=headers)

