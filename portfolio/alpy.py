import os
from dotenv import load_dotenv
load_dotenv()

ALPACA_KEY_ID = os.environ['ALPACA_KEY_ID']
ALPACA_SECRET_KEY = os.environ['ALPACA_SECRET_KEY']
HEADERS = {'APCA-API-KEY-ID': ALPACA_KEY_ID, 'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY}
ALPACA_ENDPOINT = 'https://paper-api.alpaca.markets'

get_positions = f'{ALPACA_ENDPOINT}/v2/positions'

import requests, json

r = requests.get(get_positions, headers=HEADERS)

content = json.loads(r.content)

for c in content[0]:
	print(c)