#!/usr/bin/env python3
"""
Standalone script to refresh AI jobs
Can be run as a cron job or scheduled task
"""

import os
import sys
import django
import logging
from datetime import datetime

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.core.management import execute_from_command_line

def refresh_ai_jobs():
    """Refresh AI jobs using Django management command"""
    try:
        print(f"[{datetime.now()}] Starting AI job refresh...")
        
        # Run the Django management command
        execute_from_command_line([
            'manage.py', 
            'refresh_ai_jobs',
            '--query=software engineer',
            '--location=Perth',
            '--limit=50',
            '--save-to-csv'
        ])
        
        print(f"[{datetime.now()}] AI job refresh completed successfully!")
        
    except Exception as e:
        print(f"[{datetime.now()}] Error refreshing AI jobs: {e}")
        logging.error(f"Error refreshing AI jobs: {e}")

if __name__ == "__main__":
    refresh_ai_jobs()
