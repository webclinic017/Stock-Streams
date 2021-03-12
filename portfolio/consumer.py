# import os
# from json import loads

# from kafka import KafkaConsumer

# TOPIC = 'alpaca_stream'
# KAFKA_BOOTSTRAP_SERVER = os.environ.get('KAFKA_BOOTSTRAP_SERVERS')
# KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC')
# consumer = KafkaConsumer(
# 	KAFKA_TOPIC,
# 	bootstrap_servers=[KAFKA_BOOTSTRAP_SERVER],
# 	value_deserializer=lambda x: loads(x.decode('utf-8')),
# 	enable_auto_commit=True
# 	)


# def fromStream():
# 	for m in consumer:
# 		yield m
	# return consumer

# ------------------------------------------------------------------------
# django channels using redis 

import os
import json
import time

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from . import alpaca
from . import alpacaStreamService as alpacaStream



class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

class AlpacaConsumer(WebsocketConsumer):

	def connect(self):
		# self.is_connected = True
		print(alpaca)
		self.symbol = self.scope['url_route']['kwargs']['symbol']
		# ws = alpacaStream.AlpacaStreamService(event, [f'{event}.{s}' for s in symbols])
		print("Websocket is connected as alpaca consumer")
		# print(self.symbol, self.scope)
		# self.ws = alpacaStream.AlpacaStreamService('AM', self.symbol)

		self.stream_name = 'stream_%s' % self.symbol

		async_to_sync(self.channel_layer.group_add)(
			self.stream_name,
			self.channel_name
		)
		self.accept()

	def receive(self, text_data):
		# Send message to room group
		print("websocket receive", text_data)
		minute_update_data = alpaca.get_minute_update(self.symbol)
	
		print(minute_update_data)
		async_to_sync(self.channel_layer.group_send)(
			self.stream_name,
			{
				'type': 'stream_message',
				'message': minute_update_data,
			}
        )
		
	def disconnect(self, event):
		# self.is_connected = False
		print("websocket disconnected", event)
		async_to_sync(self.channel_layer.group_discard)(
            self.stream_name,
            self.channel_name
        )

	def stream_message(self, event):
		message = event['message']
		print('stream message', message)
		self.send(text_data=json.dumps({
			'message': message
		}))














