"""
Integration testing script for PCA project.
Tests all major functionality and endpoints.
"""

import requests
import json
import time
import os
import sys

# Configuration
BASE_URL = "http://localhost:5000"
FRONTEND_URL = "http://localhost:3000"

def test_backend_health():
    """Test backend health endpoint."""
    print("Testing backend health...")
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is healthy")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend not accessible: {e}")
        return False

def test_authentication():
    """Test authentication endpoints."""
    print("\nTesting authentication...")
    
    # Test login
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/login",
            json=login_data,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'token' in data:
                print("✅ Login successful")
                return data['token']
            else:
                print("❌ Login failed: No token received")
                return None
        else:
            print(f"❌ Login failed: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Login request failed: {e}")
        return None

def test_session_creation(token):
    """Test session creation."""
    print("\nTesting session creation...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/session/create",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 201:
            data = response.json()
            if data.get('success') and 'session_id' in data:
                print("✅ Session created successfully")
                return data['session_id']
            else:
                print("❌ Session creation failed: Invalid response")
                return None
        else:
            print(f"❌ Session creation failed: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Session creation request failed: {e}")
        return None

def test_file_upload(token, session_id):
    """Test file upload functionality."""
    print("\nTesting file upload...")
    
    # Create a test CSV file
    test_csv_content = "col1,col2,col3\n1,2,3\n4,5,6\n7,8,9\n"
    test_file_path = "test_data.csv"
    
    try:
        with open(test_file_path, 'w') as f:
            f.write(test_csv_content)
        
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        files = {
            'file': ('test_data.csv', open(test_file_path, 'rb'), 'text/csv')
        }
        
        data = {
            'session_id': session_id
        }
        
        response = requests.post(
            f"{BASE_URL}/api/upload",
            headers=headers,
            files=files,
            data=data,
            timeout=10
        )
        
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get('success'):
                print("✅ File upload successful")
                return True
            else:
                print(f"❌ File upload failed: {response_data.get('error')}")
                return False
        else:
            print(f"❌ File upload failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ File upload test failed: {e}")
        return False
    finally:
        # Clean up test file
        if os.path.exists(test_file_path):
            os.remove(test_file_path)

def test_pca_processing(token, session_id):
    """Test PCA processing."""
    print("\nTesting PCA processing...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    pca_data = {
        "session_id": session_id,
        "filename": "test_data.csv",
        "k": 2
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/pca/run",
            headers=headers,
            json=pca_data,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ PCA processing successful")
                return True
            else:
                print(f"❌ PCA processing failed: {data.get('error')}")
                return False
        else:
            print(f"❌ PCA processing failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ PCA processing request failed: {e}")
        return False

def test_frontend_accessibility():
    """Test if frontend is accessible."""
    print("\nTesting frontend accessibility...")
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
            return True
        else:
            print(f"❌ Frontend not accessible: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Frontend not accessible: {e}")
        return False

def run_integration_tests():
    """Run all integration tests."""
    print("🚀 Starting PCA Project Integration Tests")
    print("=" * 50)
    
    # Test backend health
    if not test_backend_health():
        print("\n❌ Backend is not running. Please start the backend first.")
        return False
    
    # Test authentication
    token = test_authentication()
    if not token:
        print("\n❌ Authentication failed. Please check backend.")
        return False
    
    # Test session creation
    session_id = test_session_creation(token)
    if not session_id:
        print("\n❌ Session creation failed.")
        return False
    
    # Test file upload
    if not test_file_upload(token, session_id):
        print("\n❌ File upload failed.")
        return False
    
    # Test PCA processing
    if not test_pca_processing(token, session_id):
        print("\n❌ PCA processing failed.")
        return False
    
    # Test frontend
    if not test_frontend_accessibility():
        print("\n⚠️  Frontend is not accessible. Please start the frontend.")
    
    print("\n" + "=" * 50)
    print("✅ Integration tests completed successfully!")
    print("\n🎉 Your PCA project is working correctly!")
    print(f"🌐 Frontend: {FRONTEND_URL}")
    print(f"🔧 Backend: {BASE_URL}")
    print("\nYou can now use the application with the following credentials:")
    print("Username: admin, Password: admin123")
    
    return True

if __name__ == "__main__":
    print("PCA Project Integration Test Suite")
    print("Make sure both backend and frontend are running before starting tests.")
    print("\nTo start the project:")
    print("1. Run: setup_project.bat")
    print("2. Run: start_project.bat")
    print("\nPress Enter to continue with tests...")
    input()
    
    success = run_integration_tests()
    sys.exit(0 if success else 1)
