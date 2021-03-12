from django.shortcuts import render, reverse
from django.http import HttpResponse, Http404, JsonResponse, StreamingHttpResponse

from django.core import serializers

import json
# Create your views here.

from . import alpaca 

# from .consumer import fromStream

def old_home(request):
	portfolio = alpaca.get_portfolio()
	positions = alpaca.get_positions()
	# positions = ['AMZN', 'AAPL', 'GOOG', 'AMD']
	position_status = []
	for p in positions:
		asset = {}
		gain_loss = float(p.current_price) - (float(p.cost_basis)/float(p.qty))
		# asset['x'] = p.x
		asset['name'] = alpaca.get_name(p.symbol)
		asset['symbol'] = p.symbol
		asset['current_price'] = (float(p.current_price))
		asset['cost_basis'] = float(p.cost_basis)/int(p.qty)
		asset['Gain/Loss($)'] = "{:.2f}".format(gain_loss)
		# asset['unrealized_pl'] = "{:.4f}".format(float(p.unrealized_pl))
		asset['unrealized_pl'] = p.unrealized_pl
		asset['lastday_price'] = float(p.lastday_price)
		asset['qty'] = int(p.qty)

		position_status.append(asset)

	keys = [
		'asset_id',
		'symbol',
		'exchange',
		'asset_class',
		'qty',
		'avg_entry_price',
		'side',
		'market_value',
		'cost_basis',
		'unrealized_pl',
		'unrealized_plpc',
		'unrealized_intraday_pl',
		'unrealized_intraday_plpc',
		'current_price',
		'lastday_price',
		'change_today'
	]
	print(position_status)
	bp = portfolio.buying_power
	# print(type(bp))
	market_status = alpaca.market_status()

	context = {
		'positions': positions,
		'assets': position_status,
		'bp': "{:.2f}".format(float(bp)),
		'cash': "{:.2f}".format(float(portfolio.cash)),
		'returns': float(portfolio.portfolio_value),
		'market_status': market_status
	}
	return render(request=request, template_name="portfolio/home.html", context=context)

def buy(request, symbol):
	return HttpResponse("Buy Here!")

def sell(request, symbol):
	return HttpResponse("Sell Here!")

def stock(request, symbol):

	order_msg = ''
	if request.method == 'POST':
		# order_request = json.dumps(request.body)
		params = request.POST
		print(params)
		order_side = params['orderside']
		share = request.POST.getlist('shares')
		order_type = params['ordertype']
		print(f'{order_side} {share[(len(order_side)+1)%2]} shares of {symbol}')
		order_success = alpaca.submit_order(
			symbol=symbol,
			qty=share[(len(order_side)+1)%2],
			side=order_side,
			type=order_type
			)
		if order_success:
			order_msg = 'Success!'
		else:
			order_msg = 'Sorry, insufficient buying power'
		# if order_type == 'buy':
		# 	print(f'{order_type} {share[len]} shares of {symbol}')
		# elif order_type == 'sell':
		# 	print(f'{order_type} {share[1]} shares of {symbol}')
		# print(params['ordertype'])
		# print(f'shares: {share}')
	context = {
		'symbol': symbol,
		'price': 13.00,
		'is_holding': True,
		'order_msg': order_msg
	}


	return render(request, template_name="portfolio/stock.html", context=context)


def testchat(request):
	return render(request, template_name="chat/chat.html")

def testroom(request, room_name):
	return render(request, template_name='chat/room.html', context={'room_name': room_name})

def home(request):
	return render(request, template_name="portfolio/newhome.html", context={})

def stream(request, symbol):
	symbol_data_month = alpaca.populate_historical(symbol).df
	symbol_data_month_close = symbol_data_month[(symbol.upper(), 'close')]
	chart_data = [{'t': t.strftime('%m-%d-%Y'), 'y': float(c)} for t, c in zip(symbol_data_month_close.index, symbol_data_month_close)]
	# print(chart_data)

	symbol_data = alpaca.get_asset_info(symbol)
	# print(symbol_data, symbol_data_month)

	context = {
		'symbol': symbol,
		'asset_info': symbol_data,
		'stock_data': json.dumps({'data': chart_data})
	}
	return render(request, template_name="portfolio/stock_data.html", context=context)































