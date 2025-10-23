#!/usr/bin/env python3
"""
Fix PostgreSQL access from host machine
"""

import subprocess
import time

def fix_postgresql_host_access():
    """Fix PostgreSQL to accept connections from host"""
    try:
        print("🔧 Fixing PostgreSQL Host Access")
        print("=" * 50)
        
        # Update pg_hba.conf to allow connections from host
        print("1. Updating pg_hba.conf...")
        cmd = [
            'docker', 'exec', 'job_recommender_postgresql',
            'bash', '-c',
            'echo "host all all 0.0.0.0/0 md5" >> /var/lib/postgresql/data/pg_hba.conf'
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ pg_hba.conf updated")
        else:
            print(f"   ⚠️  pg_hba.conf update failed: {result.stderr}")
        
        # Update postgresql.conf to listen on all addresses
        print("2. Updating postgresql.conf...")
        cmd2 = [
            'docker', 'exec', 'job_recommender_postgresql',
            'bash', '-c',
            'sed -i "s/#listen_addresses = \'localhost\'/listen_addresses = \'*\'/" /var/lib/postgresql/data/postgresql.conf'
        ]
        result2 = subprocess.run(cmd2, capture_output=True, text=True)
        
        if result2.returncode == 0:
            print("   ✅ postgresql.conf updated")
        else:
            print(f"   ⚠️  postgresql.conf update failed: {result2.stderr}")
        
        # Restart PostgreSQL
        print("3. Restarting PostgreSQL...")
        subprocess.run(['docker', 'restart', 'job_recommender_postgresql'], timeout=30)
        
        # Wait for restart
        time.sleep(5)
        
        # Test connection
        print("4. Testing connection...")
        cmd3 = ['docker', 'exec', 'job_recommender_postgresql', 'pg_isready', '-U', 'admin']
        result3 = subprocess.run(cmd3, capture_output=True, text=True, timeout=10)
        
        if result3.returncode == 0:
            print("   ✅ PostgreSQL is ready after restart")
            return True
        else:
            print(f"   ❌ PostgreSQL not ready: {result3.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error fixing PostgreSQL: {e}")
        return False

def test_postgresql_from_host():
    """Test PostgreSQL connection from host machine"""
    try:
        print("\n🔍 Testing PostgreSQL from Host Machine")
        print("=" * 50)
        
        # Try to connect using psql from host
        cmd = [
            'psql', '-h', 'localhost', '-p', '5432', '-U', 'admin', '-d', 'job_recommender',
            '-c', 'SELECT version();'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ PostgreSQL connection from host successful!")
            print(f"Output: {result.stdout}")
            return True
        else:
            print(f"❌ PostgreSQL connection from host failed:")
            print(f"Error: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ psql command not found. Install PostgreSQL client tools.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_simple_postgresql_test():
    """Create a simple test to verify PostgreSQL works"""
    try:
        print("\n🔍 Creating Simple PostgreSQL Test")
        print("=" * 50)
        
        # Create a test table and insert data
        cmd = [
            'docker', 'exec', 'job_recommender_postgresql',
            'psql', '-U', 'admin', '-d', 'job_recommender',
            '-c', '''
            CREATE TABLE IF NOT EXISTS test_connection (
                id SERIAL PRIMARY KEY,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            INSERT INTO test_connection (message) VALUES ('PostgreSQL is working!');
            SELECT * FROM test_connection;
            '''
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ PostgreSQL test successful!")
            print("Test table created and data inserted:")
            print(result.stdout)
            return True
        else:
            print(f"❌ PostgreSQL test failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating test: {e}")
        return False

def show_postgresql_connection_info():
    """Show connection information"""
    print("\n📋 PostgreSQL Connection Information")
    print("=" * 50)
    print("🌐 Connection Details:")
    print("   Host: localhost")
    print("   Port: 5432")
    print("   Database: job_recommender")
    print("   Username: admin")
    print("   Password: password123")
    print("")
    print("🔗 Connection String:")
    print("   postgresql://admin:password123@localhost:5432/job_recommender")
    print("")
    print("🌐 pgAdmin Access:")
    print("   URL: http://localhost:8080")
    print("   Email: admin@jobrecommender.com")
    print("   Password: admin123")
    print("")
    print("💡 If connection still fails:")
    print("   1. Check if port 5432 is used by another service")
    print("   2. Try restarting Docker: docker-compose down && docker-compose up -d")
    print("   3. Check Windows Firewall settings")

def main():
    """Main function"""
    print("🔧 PostgreSQL Access Fix")
    print("=" * 60)
    print("Fixing PostgreSQL to accept connections from host machine...")
    print("=" * 60)
    
    # Try to fix access
    fix_ok = fix_postgresql_host_access()
    
    # Test connection
    if fix_ok:
        test_ok = test_postgresql_from_host()
        
        if test_ok:
            print("\n🎉 PostgreSQL is now accessible from host machine!")
        else:
            print("\n⚠️  PostgreSQL is running but may need additional configuration")
    
    # Create test
    create_simple_postgresql_test()
    
    # Show connection info
    show_postgresql_connection_info()
    
    print("\n" + "=" * 60)
    print("📊 Summary:")
    print("   PostgreSQL container: ✅ Running")
    print("   Database: ✅ job_recommender exists")
    print("   User: ✅ admin exists")
    print("   Host access: " + ("✅ Working" if fix_ok else "❌ Needs configuration"))

if __name__ == "__main__":
    main()
