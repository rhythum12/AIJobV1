import os
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
import logging
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PostgreSQLConnection:
    def __init__(self):
        self.connection_pool = None
        self.connected = False
        # Don't connect on init, connect when needed

    def connect(self):
        """Create connection pool to PostgreSQL"""
        if self.connected:
            return True
            
        try:
            # PostgreSQL connection parameters - use correct password
            db_config = {
                'host': os.getenv('POSTGRES_HOST', 'localhost'),
                'port': os.getenv('POSTGRES_PORT', '5432'),
                'database': os.getenv('POSTGRES_DB', 'job_recommender'),
                'user': os.getenv('POSTGRES_USER', 'admin'),
                'password': os.getenv('POSTGRES_PASSWORD', 'password123'),  # Correct password
                'cursor_factory': RealDictCursor
            }
            
            # Create connection pool
            self.connection_pool = psycopg2.pool.ThreadedConnectionPool(
                minconn=1,
                maxconn=20,
                **db_config
            )
            
            # Test the connection
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT version();")
                    version = cursor.fetchone()
                    logger.info(f"Successfully connected to PostgreSQL: {version['version']}")
            
            self.connected = True
            return True
            
        except Exception as e:
            logger.warning(f"PostgreSQL connection failed: {e}")
            self.connected = False
            return False

    @contextmanager
    def get_connection(self):
        """Get a connection from the pool"""
        if not self.connected:
            self.connect()
        if not self.connection_pool:
            raise Exception("PostgreSQL connection not established")
            
        conn = None
        try:
            conn = self.connection_pool.getconn()
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Database connection error: {e}")
            raise
        finally:
            if conn:
                self.connection_pool.putconn(conn)

    @contextmanager
    def get_cursor(self):
        """Get a cursor from a connection"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                yield cursor

    def execute_query(self, query, params=None):
        """Execute a SELECT query and return results"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"Query execution error: {e}")
            raise

    def execute_insert(self, query, params=None):
        """Execute an INSERT query and return the inserted ID"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    conn.commit()
                    return cursor.fetchone()[0] if cursor.description else None
        except Exception as e:
            logger.error(f"Insert execution error: {e}")
            raise

    def execute_update(self, query, params=None):
        """Execute an UPDATE query and return affected rows count"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    conn.commit()
                    return cursor.rowcount
        except Exception as e:
            logger.error(f"Update execution error: {e}")
            raise

    def execute_delete(self, query, params=None):
        """Execute a DELETE query and return affected rows count"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    conn.commit()
                    return cursor.rowcount
        except Exception as e:
            logger.error(f"Delete execution error: {e}")
            raise

    def close_pool(self):
        """Close the connection pool"""
        if self.connection_pool:
            self.connection_pool.closeall()
            logger.info("PostgreSQL connection pool closed")

    def health_check(self):
        """Check if the database connection is healthy"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("SELECT 1;")
                return True
        except Exception as e:
            logger.error(f"PostgreSQL health check failed: {e}")
            return False

# Global PostgreSQL connection instance
postgresql_connection = PostgreSQLConnection()

def get_postgresql():
    """Get PostgreSQL connection instance"""
    return postgresql_connection

def get_postgresql_cursor():
    """Get PostgreSQL cursor context manager"""
    return postgresql_connection.get_cursor()
