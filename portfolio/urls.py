from django.urls import path, include

from . import views

urlpatterns = [
	path('', views.home, name="home"),
	path('buy/<symbol>', views.buy, name="buy"),
	path('sell/<symbol>', views.sell, name="sell"),
	path('stock/<symbol>', views.stock, name="stock")
]