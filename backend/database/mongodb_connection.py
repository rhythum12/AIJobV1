import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDBConnection:
    def __init__(self):
        self.client = None
        self.db = None
        self.connected = False
        # Don't connect on init, connect when needed

    def connect(self):
        """Establish connection to MongoDB"""
        if self.connected:
            return True
            
        try:
            # MongoDB connection string - connect to Docker MongoDB on localhost
            mongodb_url = os.getenv('MONGODB_URL', 'mongodb://localhost:27018/job_recommender')
            database_name = os.getenv('MONGODB_DATABASE', 'job_recommender')
            
            # Create MongoDB client
            self.client = MongoClient(
                mongodb_url,
                serverSelectionTimeoutMS=10000,  # 10 second timeout
                connectTimeoutMS=10000,
                socketTimeoutMS=10000,
                retryWrites=True
            )
            
            # Test the connection
            self.client.admin.command('ping')
            
            # Get database
            self.db = self.client[database_name]
            self.connected = True
            
            logger.info(f"Successfully connected to MongoDB database: {database_name}")
            return True
            
        except Exception as e:
            logger.warning(f"MongoDB connection failed: {e}")
            self.connected = False
            return False

    def get_collection(self, collection_name):
        """Get a specific collection from the database"""
        if not self.connected:
            self.connect()
        if self.db is None:
            raise Exception("Database connection not established")
        return self.db[collection_name]

    def get_database(self):
        """Get the database instance"""
        return self.db

    def close_connection(self):
        """Close the MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

    def health_check(self):
        """Check if the database connection is healthy"""
        try:
            self.client.admin.command('ping')
            return True
        except Exception as e:
            logger.error(f"MongoDB health check failed: {e}")
            return False

# Global MongoDB connection instance
mongodb_connection = MongoDBConnection()

def get_mongodb():
    """Get MongoDB connection instance"""
    return mongodb_connection

def get_mongodb_collection(collection_name):
    """Get a specific MongoDB collection"""
    return mongodb_connection.get_collection(collection_name)
