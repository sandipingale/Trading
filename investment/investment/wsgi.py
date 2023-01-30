"""
WSGI config for investment project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv
project_home = '/home/sandipingale/Trading/investment'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

project_folder = os.path.expanduser('~')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investment.settings')

application = get_wsgi_application()
