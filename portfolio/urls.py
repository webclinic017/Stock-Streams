from django.urls import path, include

from . import views

urlpatterns = [
	path('old', views.old_home, name="old_home"),
	path('buy/<symbol>', views.buy, name="buy"),
	path('sell/<symbol>', views.sell, name="sell"),
	path('stock/<symbol>', views.stock, name="stock"),
	# path('portfolio/<id>')
	path('', views.home, name="home"),
	path('stream/<str:symbol>/', views.stream, name="stream"),
	path('chat', views.testchat, name="chattest"),
	path('chat/<str:room_name>/', views.testroom, name="chatroom"),
	# path('stream/<str:symbol>/', views.teststream, name="stream")
	# path('aux_test', views.auxillary_test, name="aux_test")
]