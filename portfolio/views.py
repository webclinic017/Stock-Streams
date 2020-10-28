from django.shortcuts import render
from django.http import HttpResponse, Http404

# Create your views here.

from . import alpaca 

def home(request):
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
		asset['cost_basis'] = float(p.cost_basis)
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