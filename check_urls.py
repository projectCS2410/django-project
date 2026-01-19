import os
import sys
import django
from django.conf import settings
from django.urls import get_resolver

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

# Print all URLs
print("\nActive URLs:")
urlconf = settings.ROOT_URLCONF
resolver = get_resolver(urlconf)
for pattern in resolver.url_patterns:
    print(pattern)
    if hasattr(pattern, 'url_patterns'):
        for sub in pattern.url_patterns:
            print(f"  - {sub}")
