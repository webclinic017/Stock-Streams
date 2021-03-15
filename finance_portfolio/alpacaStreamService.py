import os
import websocket
import asyncio
import threading

ALPACA_KEY_ID = os.getenv('ALPACA_KEY_ID')
ALPACA_SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')

ALPACA_STREAM = 'wss://data.alpaca.markets/stream'
API_AUTH = {
	"key_id": ALPACA_KEY_ID,
	"secret_key": ALPACA_SECRET_KEY
}

class AlpacaStreamService:

	def __init__(self, event, symbol):
		self.event = event
		self.symbol = symbol
		self.streamSymbol = f'{event}.{symbol}'
		print("init ass", self.streamSymbol)

		websocket.enableTrace(True)
		self._ws = websocket.WebSocketApp(ALPACA_STREAM, 
			on_open= lambda ws: self.on_open(ws), 
			on_message= lambda ws, msg: self.on_message(ws, msg),
			on_close= lambda ws: self.on_close(ws))

		self.t = threading.Thread(target=self._ws.run_forever, args=(1,))
		self.t.start()
		# self.t.run()

	def on_open(self, ws):
		print("initializing")
		auth_data = {
			"action": "authenticate",
			"data": API_AUTH
		}
		ws.send(json.dumps(auth_data))

		listen_message = {
			"action": "listen",
			"data": { "streams": [self.streamSymbol]}
		}

		ws.send(json.dumps(listen_message))

	def on_close(self, ws):
		self.t.stop()

	def on_message(self, ws, message):
		print('incoming --->')
		message_obj = json.loads(message)
		print(message)
		
		data = message_obj['data']
		event = data['ev']


		#  Trade Channel ===============
		'''
		-ev = T
		-T = Symbol
		-i = Trade ID
		-x = Exchange Code
		-p = Trade Price
		-s = Trade Size (shares)
		-t = Epoch TimeStamp (nanoseconds)
		-c = Condition Flags
		-z = Tape ID

		'''

		if self.event == 'T':
			# symbol = message_obj['stream']
			trade_stream_data_object = {
				'symbol': data['T'],
				'trade_id': data['i'],
				'exchange_code': data['x'],
				'trade_price': data['p'],
				'trade_size': data['s'],
				'timestamp': data['t']//1e9,
				'condition_flag': data['c'],
				'tape_id': data['z']
			}
			stream_data = trade_stream_data_object

		# Minute Channel ================
		'''
		-ev = AM
		-T = Symbol
		-v = Volume (shares)
		-av = Accumulated Volume
		-op = Official Open Price
		-vw = VWAP
		-o = open price 
		-h = high price
		-l = low price
		-c = close price
		-a = average price
		-s = Epoch TimeStamp at beginning of window (milliseconds)
		-e = Epoch TimeStamp at end of window (milliseconds)

		'''

		if self.event == 'AM':
			minute_stream_data_object = {
				'symbol': data['T'],
				'volume': data['v'],
				'accumulated_volume': data['av'],
				'official_open_price': data['op'],
				'VWAP': data['vw'],
				'open_price': data['o'],
				'close_price': data['c'],
				'high_price': data['h'],
				'low_price': data['l'],
				'average_price': data['a'],
				'timestamp_beginning': data['s'],
				'timetstamp_end': data['e'],
				
			}
			stream_data = minute_stream_data_object

		return stream_data

	def receive(self):
		new_message = self.ws.recv()
		print(new_message)
		return 1
		# return await self.ws.recv()

	def close(self):
		self.t.stop()
		


		