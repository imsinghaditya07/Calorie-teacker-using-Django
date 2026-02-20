import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Tell Django it's running on Vercel (enables Vercel-specific settings)
os.environ.setdefault('VERCEL', '1')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calorie_counter.settings')

# Bootstrap Django
import django
django.setup()

from calorie_counter.wsgi import application

# Vercel expects the WSGI callable to be named 'app'
app = application
