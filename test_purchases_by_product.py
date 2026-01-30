"""Test purchases by product report"""
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
        
        # Try to access purchases by product report
        print("\n=== Testing /reports/purchases-by-product ===")
        try:
            response = client.get('/reports/purchases-by-product')
            print("Status code:", response.status_code)
            if response.status_code == 200:
                print("✅ SUCCESS - Report is working!")
            else:
                print("❌ ERROR - Status code:", response.status_code)
                print("Response data:", response.data.decode('utf-8')[:500])
        except Exception as e:
            print("Exception occurred:")
            print(type(e).__name__, ":", str(e))
            import traceback
            traceback.print_exc()

