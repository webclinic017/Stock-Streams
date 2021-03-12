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

def get_asset_info(symbol):
	symbol_data = client.get_asset(symbol.upper())
	# print(symbol_data, symbol_data_month)
	asset_info = {
	    'name': symbol_data.name,
	    'symbol': symbol_data.symbol,
	    'status': symbol_data.status,
		'class': 'us_equity',
		'exchange': symbol_data.exchange,
	    'easy to borrow': symbol_data.easy_to_borrow,
	    'fractionable': symbol_data.fractionable,
	    'id': symbol_data.id,
	    'marginable': symbol_data.marginable,
	    'shortable': symbol_data.shortable,
	    'tradable': symbol_data.tradable
	}
	return asset_info

def get_symbol_dataframe(symbol):
	df = populate_historical(symbol, "1Min", limit=10, end=client.get_clock().timestamp)
	return df

def validate_symbol(symbol):
	try:
		symbol = client.get_asset(symbol)
		return True
	except:
		return False
def get_minute_update(symbol):
	minute_update = populate_historical(symbol, '1Min', 1, end=client.get_clock().timestamp)[symbol][0]
	minute_update_object = {
		'timestamp': minute_update.t.strftime('%Y-%m-%d %H:%M:%S'),
		'open': minute_update.o,
		'close': minute_update.c,
		'high': minute_update.h,
		'low': minute_update.l,
		'volume': minute_update.v

	}
	return minute_update_object

def return_df(alpaca_entity):
	return alpaca_entity.df

def populate_historical(symbol, timeframe="day", limit=30, start=None, end=None, after=None, until=None):
	
	symbol = symbol.upper()
	name = get_name(symbol)
	limit = limit
	timeframe = timeframe

	return client.get_barset(symbol, timeframe, limit)

	# postition = Positions(name=name, symbol=symbol)
	# return df


def market_status():
	return client.get_clock().is_open == True


def submit_order(symbol, qty, side, type, time_in_force='day'):
	print(f'{symbol} {side} {qty} {type} {time_in_force}')
	try:
		# client.submit_order(symbol.upper(), qty, side, type, time_in_force)
		return True
	except:
		return False