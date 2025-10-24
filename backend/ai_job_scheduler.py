#!/usr/bin/env python3
"""
AI Job Scheduler - Runs AI job refresh periodically
"""

import time
import threading
import logging
from datetime import datetime
import os
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

import django
django.setup()

from django.core.management import execute_from_command_line

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_job_scheduler.log'),
        logging.StreamHandler()
    ]
)

class AIJobScheduler:
    def __init__(self, interval_minutes=30):
        self.interval_minutes = interval_minutes
        self.running = False
        self.thread = None

    def refresh_jobs(self):
        """Refresh AI jobs"""
        try:
            logging.info("Starting scheduled AI job refresh...")
            
            execute_from_command_line([
                'manage.py', 
                'refresh_ai_jobs',
                '--query=software engineer',
                '--location=Perth',
                '--limit=50',
                '--save-to-csv'
            ])
            
            logging.info("Scheduled AI job refresh completed successfully!")
            
        except Exception as e:
            logging.error(f"Error in scheduled AI job refresh: {e}")

    def run_scheduler(self):
        """Run the scheduler in a loop"""
        while self.running:
            try:
                self.refresh_jobs()
                logging.info(f"Next refresh in {self.interval_minutes} minutes...")
                
                # Sleep for the specified interval
                time.sleep(self.interval_minutes * 60)
                
            except Exception as e:
                logging.error(f"Error in scheduler loop: {e}")
                time.sleep(60)  # Wait 1 minute before retrying

    def start(self):
        """Start the scheduler"""
        if self.running:
            logging.warning("Scheduler is already running!")
            return
            
        self.running = True
        self.thread = threading.Thread(target=self.run_scheduler)
        self.thread.daemon = True
        self.thread.start()
        logging.info(f"AI Job Scheduler started (interval: {self.interval_minutes} minutes)")

    def stop(self):
        """Stop the scheduler"""
        self.running = False
        if self.thread:
            self.thread.join()
        logging.info("AI Job Scheduler stopped")

def main():
    """Main function"""
    scheduler = AIJobScheduler(interval_minutes=30)  # Refresh every 30 minutes
    
    try:
        scheduler.start()
        
        # Keep the main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logging.info("Received interrupt signal, stopping scheduler...")
        scheduler.stop()

if __name__ == "__main__":
    main()
