"""
Test License Route
اختبار route التراخيص
"""
from app import create_app, db
from flask import session
from app.models import User

app = create_app()

with app.app_context():
    with app.test_client() as client:
        # Try to access license page
        print("Testing /security/license route...")
        
        try:
            # First login
            response = client.post('/auth/login', data={
                'username': 'admin',
                'password': 'admin123',
                'license_key': 'CEC9-79EE-C42F-2DAD'
            }, follow_redirects=True)
            
            print(f"Login response status: {response.status_code}")
            
            # Then access license page
            response = client.get('/security/license')
            print(f"License page response status: {response.status_code}")
            
            if response.status_code == 500:
                print("ERROR 500!")
                print(response.data.decode('utf-8')[:500])
            else:
                print("SUCCESS!")
                
        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()

