"""
WSGI config for getgig project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'getgig.settings')

# Initialize standard Django WSGI application
application = get_wsgi_application()

# Wrap application with WhiteNoise for server-level asset delivery
application = WhiteNoise(application, root=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'))