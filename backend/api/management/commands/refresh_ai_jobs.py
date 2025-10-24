"""
Django management command to refresh AI jobs from the scraper
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
import os
import sys
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Refresh AI jobs by running the job scraper'

    def add_arguments(self, parser):
        parser.add_argument(
            '--query',
            type=str,
            default='software engineer',
            help='Job search query'
        )
        parser.add_argument(
            '--location',
            type=str,
            default='Perth',
            help='Job search location'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=50,
            help='Maximum number of jobs to fetch'
        )
        parser.add_argument(
            '--save-to-csv',
            action='store_true',
            help='Save results to CSV file'
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Starting AI job refresh...')
        )

        try:
            # Add AI folder to Python path
            ai_folder_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'AI')
            if ai_folder_path not in sys.path:
                sys.path.append(ai_folder_path)

            # Import AI modules
            from job_scraper import load_job_data

            query = options['query']
            location = options['location']
            limit = options['limit']

            self.stdout.write(f'Fetching jobs for: "{query}" in {location} (limit: {limit})')

            # Fetch jobs from AI scraper
            job_df = load_job_data(query, location, results_per_page=limit)

            if job_df.empty:
                self.stdout.write(
                    self.style.WARNING('No jobs found for the given criteria')
                )
                return

            self.stdout.write(
                self.style.SUCCESS(f'Successfully fetched {len(job_df)} jobs')
            )

            # Save to CSV if requested
            if options['save_to_csv']:
                csv_path = os.path.join(ai_folder_path, 'jobs.csv')
                job_df.to_csv(csv_path, index=False)
                self.stdout.write(
                    self.style.SUCCESS(f'Jobs saved to CSV: {csv_path}')
                )

            # Display sample jobs
            self.stdout.write('\nSample jobs found:')
            for i, (index, row) in enumerate(job_df.head(3).iterrows()):
                self.stdout.write(f'{i+1}. {row.get("Job Title", "Unknown")} at {row.get("Company", "Unknown")}')

            self.stdout.write(
                self.style.SUCCESS('AI job refresh completed successfully!')
            )

        except Exception as e:
            logger.error(f"Error refreshing AI jobs: {e}")
            self.stdout.write(
                self.style.ERROR(f'Error refreshing AI jobs: {e}')
            )
