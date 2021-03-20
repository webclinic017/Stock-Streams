web: daphne finance_portfolio.asgi:application --port $PORT -b 0.0.0.0 -v2
worker: python manage.py runworker channel_layer --settings=finance_portfolio.settings -v2
