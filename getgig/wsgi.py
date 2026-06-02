import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'getgig.settings')

application = get_wsgi_application()

# Target root folder binding fallback
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
application = WhiteNoise(application, root=os.path.join(base_dir, 'static'))

# Vercel app object declaration signature mapping
app = application