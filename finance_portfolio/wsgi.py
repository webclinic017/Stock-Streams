"""
WSGI config for finance_portfolio project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_portfolio.settings')

# SECRET_KEY = os.environ.get('SECRET_KEY')

# try:
# 	from .local_settings import *
# except Exception as e:
# 	pass

application = get_wsgi_application()
