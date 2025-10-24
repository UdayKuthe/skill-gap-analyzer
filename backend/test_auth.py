#!/usr/bin/env python3
"""
Simple authentication test script for Skill Gap Analyzer
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"
TEST_USER = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPassword123",
    "confirm_password": "TestPassword123"
}

def test_auth_flow():
    """Test the complete authentication flow"""
    print("🧪 Testing Authentication Flow")
    print("=" * 50)
    
    # Test 1: Register a new user
    print("\n1️⃣ Testing User Registration...")
    try:
        response = requests.post(f"{API_BASE_URL}/auth/register", json=TEST_USER)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"   ✅ Registration successful!")
            print(f"   User ID: {data['user']['id']}")
            print(f"   Username: {data['user']['username']}")
            print(f"   Email: {data['user']['email']}")
            print(f"   Token Type: {data['token_type']}")
            print(f"   Expires In: {data['expires_in']} seconds")
            
            # Store token for further tests
            access_token = data['access_token']
            user_id = data['user']['id']
            
        else:
            print(f"   ❌ Registration failed: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Connection failed. Make sure the server is running on localhost:8000")
        return False
    except Exception as e:
        print(f"   ❌ Registration error: {e}")
        return False
    
    # Test 2: Login with the same user
    print("\n2️⃣ Testing User Login...")
    try:
        login_data = {
            "email": TEST_USER["email"],
            "password": TEST_USER["password"]
        }
        response = requests.post(f"{API_BASE_URL}/auth/login", json=login_data)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Login successful!")
            print(f"   User ID: {data['user']['id']}")
            print(f"   Username: {data['user']['username']}")
            print(f"   Email: {data['user']['email']}")
            
            # Update token
            access_token = data['access_token']
            
        else:
            print(f"   ❌ Login failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return False
    
    # Test 3: Get user profile (protected endpoint)
    print("\n3️⃣ Testing Protected Endpoint (Profile)...")
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{API_BASE_URL}/auth/profile", headers=headers)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Profile access successful!")
            print(f"   User ID: {data['id']}")
            print(f"   Username: {data['username']}")
            print(f"   Email: {data['email']}")
            print(f"   Created At: {data.get('created_at', 'N/A')}")
            
        else:
            print(f"   ❌ Profile access failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Profile error: {e}")
        return False
    
    # Test 4: Validate token
    print("\n4️⃣ Testing Token Validation...")
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.post(f"{API_BASE_URL}/auth/validate-token", headers=headers)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Token validation successful!")
            print(f"   User ID: {data['id']}")
            print(f"   Username: {data['username']}")
            print(f"   Email: {data['email']}")
            
        else:
            print(f"   ❌ Token validation failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Token validation error: {e}")
        return False
    
    # Test 5: Refresh token
    print("\n5️⃣ Testing Token Refresh...")
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.post(f"{API_BASE_URL}/auth/refresh-token", headers=headers)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Token refresh successful!")
            print(f"   New Token Type: {data['token_type']}")
            print(f"   Expires In: {data['expires_in']} seconds")
            
        else:
            print(f"   ❌ Token refresh failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Token refresh error: {e}")
        return False
    
    # Test 6: Test invalid credentials
    print("\n6️⃣ Testing Invalid Credentials...")
    try:
        invalid_login = {
            "email": TEST_USER["email"],
            "password": "wrongpassword"
        }
        response = requests.post(f"{API_BASE_URL}/auth/login", json=invalid_login)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 401:
            print(f"   ✅ Invalid credentials properly rejected!")
        else:
            print(f"   ❌ Invalid credentials not properly handled: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Invalid credentials test error: {e}")
    
    # Test 7: Test unauthorized access
    print("\n7️⃣ Testing Unauthorized Access...")
    try:
        response = requests.get(f"{API_BASE_URL}/auth/profile")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 401:
            print(f"   ✅ Unauthorized access properly rejected!")
        else:
            print(f"   ❌ Unauthorized access not properly handled: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Unauthorized access test error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Authentication flow test completed!")
    print("✅ All tests passed successfully!")
    return True

def test_health_check():
    """Test the health check endpoint"""
    print("\n🏥 Testing Health Check...")
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Health check successful!")
            print(f"   Status: {data['status']}")
            print(f"   Database Connected: {data['database_connected']}")
            print(f"   Services: {data['services_status']}")
        else:
            print(f"   ❌ Health check failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Health check error: {e}")

if __name__ == "__main__":
    print("🚀 Skill Gap Analyzer - Authentication Test")
    print(f"📅 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test health check first
    test_health_check()
    
    # Test authentication flow
    success = test_auth_flow()
    
    if success:
        print("\n🎯 All authentication tests passed!")
        sys.exit(0)
    else:
        print("\n💥 Some authentication tests failed!")
        sys.exit(1)

