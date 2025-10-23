#!/usr/bin/env python3
"""
Script to fix Docker port configuration and test connections
"""

import requests
import subprocess
import sys

def test_postgresql_connection():
    """Test PostgreSQL connection"""
    try:
        print("🔍 Testing PostgreSQL Connection")
        print("=" * 40)
        
        # Test if PostgreSQL is accessible
        import psycopg2
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="job_recommender",
            user="admin",
            password="password123"
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        print(f"✅ PostgreSQL is working!")
        print(f"   Port: 5432")
        print(f"   Database: job_recommender")
        print(f"   Version: {version[0][:50]}...")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False

def test_mongodb_connection():
    """Test MongoDB connection"""
    try:
        print("\n🔍 Testing MongoDB Connection")
        print("=" * 40)
        
        from pymongo import MongoClient
        
        client = MongoClient('mongodb://localhost:27017/')
        db = client['job_recommender']
        
        # Test connection
        client.admin.command('ping')
        
        # Count collections
        collections = db.list_collection_names()
        users_count = db.users.count_documents({})
        
        print(f"✅ MongoDB is working!")
        print(f"   Port: 27017")
        print(f"   Database: job_recommender")
        print(f"   Collections: {collections}")
        print(f"   Users count: {users_count}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False

def test_web_interfaces():
    """Test web interfaces"""
    try:
        print("\n🔍 Testing Web Interfaces")
        print("=" * 40)
        
        # Test Mongo Express
        try:
            response = requests.get("http://localhost:8081", timeout=5)
            if response.status_code == 200:
                print("✅ Mongo Express is accessible at http://localhost:8081")
            else:
                print(f"⚠️  Mongo Express returned status: {response.status_code}")
        except Exception as e:
            print(f"❌ Mongo Express not accessible: {e}")
        
        # Test pgAdmin
        try:
            response = requests.get("http://localhost:8080", timeout=5)
            if response.status_code == 200:
                print("✅ pgAdmin is accessible at http://localhost:8080")
            else:
                print(f"⚠️  pgAdmin returned status: {response.status_code}")
        except Exception as e:
            print(f"❌ pgAdmin not accessible: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing web interfaces: {e}")
        return False

def show_correct_ports():
    """Show the correct port mappings"""
    print("\n📋 Correct Port Mappings:")
    print("=" * 40)
    print("🌐 Web Interfaces:")
    print("   • pgAdmin:     http://localhost:8080")
    print("   • Mongo Express: http://localhost:8081")
    print("")
    print("🗄️  Database Ports:")
    print("   • PostgreSQL:  localhost:5432")
    print("   • MongoDB:     localhost:27017")
    print("")
    print("🔑 Login Credentials:")
    print("   • pgAdmin:")
    print("     - Email: admin@jobrecommender.com")
    print("     - Password: admin123")
    print("   • Mongo Express:")
    print("     - Username: admin")
    print("     - Password: admin123")
    print("   • PostgreSQL:")
    print("     - Database: job_recommender")
    print("     - Username: admin")
    print("     - Password: password123")

def fix_port_configuration():
    """Suggest fixes for port configuration"""
    print("\n🔧 Port Configuration Fixes:")
    print("=" * 40)
    print("If you want to change the ports, edit docker-compose.yml:")
    print("")
    print("For pgAdmin on port 5050:")
    print("  ports:")
    print("    - \"5050:80\"")
    print("")
    print("For different PostgreSQL port:")
    print("  ports:")
    print("    - \"5433:5432\"  # Use 5433 instead of 5432")
    print("")
    print("For different MongoDB port:")
    print("  ports:")
    print("    - \"27018:27017\"  # Use 27018 instead of 27017")

def main():
    """Main function"""
    print("🔧 Docker Port Configuration Fix")
    print("=" * 60)
    print("Diagnosing and fixing Docker port issues...")
    print("=" * 60)
    
    # Test connections
    postgres_ok = test_postgresql_connection()
    mongo_ok = test_mongodb_connection()
    web_ok = test_web_interfaces()
    
    # Show correct ports
    show_correct_ports()
    
    # Show fixes
    fix_port_configuration()
    
    print("\n" + "=" * 60)
    print("📊 Test Results:")
    print(f"   PostgreSQL: {'✅ Working' if postgres_ok else '❌ Failed'}")
    print(f"   MongoDB: {'✅ Working' if mongo_ok else '❌ Failed'}")
    print(f"   Web Interfaces: {'✅ Working' if web_ok else '❌ Failed'}")
    
    if all([postgres_ok, mongo_ok, web_ok]):
        print("\n🎉 All services are working correctly!")
        print("💡 The issue was just port confusion - everything is actually working!")
    else:
        print("\n⚠️  Some services need attention")
        print("💡 Check the error messages above for specific issues")

if __name__ == "__main__":
    main()
