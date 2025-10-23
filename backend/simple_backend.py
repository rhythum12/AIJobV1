#!/usr/bin/env python3
"""
Simple Backend Server
Django server without database connections on startup
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    """Start Django server without database connections"""
    print("🚀 Starting Simple Backend Server...")
    print("=" * 50)
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    
    # Initialize Django
    django.setup()
    
    print("✅ Django initialized successfully")
    print("📊 API endpoints available at:")
    print("   • http://localhost:8000/health/")
    print("   • http://localhost:8000/api/users/profile/")
    print("   • http://localhost:8000/api/users/sync/")
    print("   • http://localhost:8000/api/users/activities/")
    print("\n🔄 User sync will work when databases are accessible!")
    print("=" * 50)
    
    # Start Django server
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])

if __name__ == '__main__':
    main()
