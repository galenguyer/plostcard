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

recipients = [
    {
        "address_name": os.environ["ADDRESS_NAME_1"],
        "address_line_1": os.environ["ADDRESS_LINE_1_1"],
        "address_line_1": os.environ.get("ADDRESS_LINE_2_1"),
        "address_city": os.environ["ADDRESS_CITY_1"],
        "address_state": os.environ["ADDRESS_STATE_1"],
        "address_postal_code": int(os.environ["ADDRESS_POSTAL_CODE_1"]),
        "address_country": os.environ["ADDRESS_COUNTRY_1"],
        "return_address_id": int(os.environ["RETURN_ADDRESS_ID"]),
        "schedule": int(time.time())+(1*60*60)
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

r = requests.post(' https://rest.clicksend.com/v3/post/letters/send', json=data, headers=headers)
print(json.dumps(r.json(), indent=4))