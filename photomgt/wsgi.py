"""
WSGI config for photomgt project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
import webbrowser
from django.core.wsgi import get_wsgi_application
from .settings import DEFAULT_IP_PORT

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'photomgt.settings')
application = get_wsgi_application()
webbrowser.open("http://"+DEFAULT_IP_PORT) # Open browser immediately after startup of server.

