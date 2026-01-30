"""Test script to check reports error"""
import os
import sys

# Set the working directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from app import create_app

app = create_app()

with app.app_context():
    with app.test_client() as client:
        # Login first
        response = client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        }, follow_redirects=True)
        
        print("Login response status:", response.status_code)
        
        # Try to access reports page
        print("\n=== Testing /reports/ ===")
        try:
            response = client.get('/reports/')
            print("Status code:", response.status_code)
            if response.status_code == 500:
                print("ERROR 500 - Internal Server Error")
                print("Response data:", response.data.decode('utf-8')[:500])
        except Exception as e:
            print("Exception occurred:")
            print(type(e).__name__, ":", str(e))
            import traceback
            traceback.print_exc()

