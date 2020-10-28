import os

ALPACA_KEY_ID = os.getenv('ALPACA_KEY_ID')
ALPACA_SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
HEADERS = {'APCA-API-KEY-ID': ALPACA_KEY_ID, 'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY}
ALPACA_ENDPOINT = 'https://paper-api.alpaca.markets'

import alpaca_trade_api as tradeapi

from .models import Positions
from .models import Account

client = tradeapi.REST(ALPACA_KEY_ID, ALPACA_SECRET_KEY, base_url=ALPACA_ENDPOINT, api_version='v2')


def get_portfolio():
	account = client.get_account()
	# print(account, account.status)
	return account

def get_positions():
	return client.list_positions()

def get_name(symbol):
	return client.get_asset(symbol.upper()).name

def get_symbol_dataframe(symbol):
	df = populate_historical(symbol, "1Min", limit=10, end=alpaca.client.get_clock().timestamp)
	return df

def validate_symbol(symbol):
	try:
		symbol = client.get_asset(symbol)
		return True
	except:
		return False

def populate_historical(symbol, timeframe="day", limit=300, start=None, end=None, after=None, until=None):
	
	symbol = symbol.upper()
	name = get_name(symbol)
	limit = 300
	timeframe = timeframe

	df = client.get_barset(symbol, timeframe, limit).df

	# postition = Positions(name=name, symbol=symbol)


def market_status():
	return client.get_clock().is_open == True