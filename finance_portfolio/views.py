from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, Http404, JsonResponse, StreamingHttpResponse

from django.core import serializers

import json
# Create your views here.

from . import alpaca 

# from .consumer import fromStream

def testchat(request):
	return render(request, template_name="chat/chat.html")

def testroom(request, room_name):
	return render(request, template_name='chat/room.html', context={'room_name': room_name})

def home(request):
	if request.method == 'POST':
		print(request.POST, request.POST['search'])
		stock_symbol = request.POST['search'].upper()

		return redirect(f'/stream/{stock_symbol}')
	return render(request, template_name="finance_portfolio/home.html", context={})

def stream(request, symbol):
	symbol_data_month = alpaca.populate_historical(symbol).df
	symbol_data_month_close = symbol_data_month[(symbol.upper(), 'close')]
	chart_data = [{'t': t.strftime('%m-%d-%Y'), 'y': float(c)} for t, c in zip(symbol_data_month_close.index, symbol_data_month_close)]
	# print(chart_data)

	# symbol_data_day = alpaca.populate_historical(symbol, timeframe='1Min', start=alpaca.get_clock)

	symbol_data = alpaca.get_asset_info(symbol)
	# print(symbol_data, symbol_data_month)
	market_status = alpaca.market_status();

	context = {
		'symbol': symbol,
		'asset_info': symbol_data,
		'stock_data_month': json.dumps({'data': chart_data}),
		'stock_data_day': json.dumps({}),
		'market_status': market_status,
	}
	return render(request, template_name="finance_portfolio/stock_data.html", context=context)































