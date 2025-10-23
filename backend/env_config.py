"""
Environment configuration for backend
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database Configuration
MONGODB_URL = os.getenv('MONGODB_URL', 'mongodb://admin:password123@localhost:27017/job_recommender?authSource=admin')
MONGODB_DATABASE = os.getenv('MONGODB_DATABASE', 'job_recommender')

POSTGRES_DB = os.getenv('POSTGRES_DB', 'job_recommender')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'admin')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'password123')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')

# Firebase Configuration
FIREBASE_PROJECT_ID = os.getenv('FIREBASE_PROJECT_ID', 'ai-powered-job-recommend-4250d')
FIREBASE_PRIVATE_KEY_ID = os.getenv('FIREBASE_PRIVATE_KEY_ID', '')
FIREBASE_PRIVATE_KEY = os.getenv('FIREBASE_PRIVATE_KEY', '')
FIREBASE_CLIENT_EMAIL = os.getenv('FIREBASE_CLIENT_EMAIL', '')
FIREBASE_CLIENT_ID = os.getenv('FIREBASE_CLIENT_ID', '')

# Django Configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-your-secret-key-here')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,0.0.0.0').split(',')
