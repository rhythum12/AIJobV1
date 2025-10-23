#!/usr/bin/env python3
"""
Fix Mongo Express connection to show users
"""

import subprocess
import time

def check_mongodb_connection():
    """Check MongoDB connection and databases"""
    try:
        print("🔍 Checking MongoDB Connection")
        print("=" * 50)
        
        # Connect to MongoDB and list databases
        cmd = [
            'docker', 'exec', 'job_recommender_mongodb',
            'mongosh', '--eval', 'db.adminCommand("listDatabases")'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ MongoDB is accessible")
            print("Databases:")
            print(result.stdout)
            return True
        else:
            print(f"❌ MongoDB connection failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking MongoDB: {e}")
        return False

def check_users_collection():
    """Check users collection directly"""
    try:
        print("\n🔍 Checking Users Collection")
        print("=" * 50)
        
        # Connect to job_recommender database and check users collection
        cmd = [
            'docker', 'exec', 'job_recommender_mongodb',
            'mongosh', 'job_recommender', '--eval', 'db.users.countDocuments({})'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Users collection accessible")
            print(f"User count: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Users collection failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking users collection: {e}")
        return False

def restart_mongo_express():
    """Restart Mongo Express with correct configuration"""
    try:
        print("\n🔧 Restarting Mongo Express")
        print("=" * 50)
        
        # Stop Mongo Express
        subprocess.run(['docker', 'stop', 'job_recommender_mongo_express'], timeout=10)
        
        # Start Mongo Express with correct configuration
        subprocess.run([
            'docker', 'run', '-d',
            '--name', 'job_recommender_mongo_express_fixed',
            '--network', 'finalcode_job_recommender_network',
            '-p', '8081:8081',
            '-e', 'ME_CONFIG_MONGODB_URL=mongodb://job_recommender_mongodb:27017/job_recommender',
            '-e', 'ME_CONFIG_BASICAUTH_USERNAME=admin',
            '-e', 'ME_CONFIG_BASICAUTH_PASSWORD=admin123',
            'mongo-express:1.0.0'
        ], timeout=30)
        
        # Wait for it to start
        time.sleep(5)
        
        print("✅ Mongo Express restarted with correct configuration")
        return True
        
    except Exception as e:
        print(f"❌ Error restarting Mongo Express: {e}")
        return False

def show_mongo_express_urls():
    """Show correct URLs for Mongo Express"""
    print("\n🌐 Mongo Express Access URLs")
    print("=" * 50)
    print("Try these URLs in your browser:")
    print("")
    print("1. Main interface: http://localhost:8081")
    print("2. Database view: http://localhost:8081/db/job_recommender")
    print("3. Users collection: http://localhost:8081/db/job_recommender/users")
    print("")
    print("Login credentials:")
    print("Username: admin")
    print("Password: admin123")
    print("")
    print("💡 If you still see 'No documents found':")
    print("   1. Try refreshing the page")
    print("   2. Check if you're in the correct database (job_recommender)")
    print("   3. Make sure you're looking at the 'users' collection")

def create_test_user_in_mongo():
    """Create a test user directly in MongoDB"""
    try:
        print("\n🧪 Creating Test User in MongoDB")
        print("=" * 50)
        
        # Create a test user directly in MongoDB
        cmd = [
            'docker', 'exec', 'job_recommender_mongodb',
            'mongosh', 'job_recommender', '--eval', '''
            db.users.insertOne({
                firebase_uid: "test_mongo_express_user",
                email: "test@mongoexpress.com",
                display_name: "Mongo Express Test User",
                profile_complete: true,
                created_at: new Date(),
                last_login: new Date(),
                preferences: {
                    job_categories: ["Software Engineering"],
                    locations: ["Remote"],
                    salary_range: {min: 80000, max: 120000}
                },
                settings: {
                    profile_visibility: "public",
                    email_notifications: true
                }
            })
            '''
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Test user created successfully")
            print("You should now see this user in Mongo Express")
            return True
        else:
            print(f"❌ Failed to create test user: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        return False

def main():
    """Main function"""
    print("🔧 Fixing Mongo Express Connection")
    print("=" * 60)
    print("Diagnosing and fixing Mongo Express connection issues...")
    print("=" * 60)
    
    # Check MongoDB connection
    mongo_ok = check_mongodb_connection()
    
    # Check users collection
    users_ok = check_users_collection()
    
    # Create test user
    test_user_ok = create_test_user_in_mongo()
    
    # Show URLs
    show_mongo_express_urls()
    
    print("\n" + "=" * 60)
    print("📊 Results:")
    print(f"   MongoDB accessible: {'✅ Yes' if mongo_ok else '❌ No'}")
    print(f"   Users collection: {'✅ Yes' if users_ok else '❌ No'}")
    print(f"   Test user created: {'✅ Yes' if test_user_ok else '❌ No'}")
    
    if test_user_ok:
        print("\n🎉 Try refreshing Mongo Express now!")
        print("💡 Go to: http://localhost:8081/db/job_recommender/users")
    else:
        print("\n⚠️  There may be connection issues between Mongo Express and MongoDB")

if __name__ == "__main__":
    main()
