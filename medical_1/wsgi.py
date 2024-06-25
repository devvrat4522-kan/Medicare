"""
WSGI config for medical_1 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.core.management.commands.runserver import Command as runserver

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medical_1.settings')

application = get_wsgi_application()



runserver.default_port = os.getenv('PORT', '8000')

