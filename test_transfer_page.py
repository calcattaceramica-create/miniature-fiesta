"""Test the transfer page to see the exact error"""
from app import create_app
from app.models import User

app = create_app()

with app.app_context():
    # Login as admin
    admin = User.query.filter_by(username='admin').first()
    
    with app.test_client() as client:
        # Login
        client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        }, follow_redirects=True)
        
        # Try to access transfer page
        try:
            response = client.get('/inventory/transfer')
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 500:
                print("\n❌ Error 500 - Internal Server Error")
                print("\nResponse data:")
                print(response.data.decode('utf-8')[:500])
            elif response.status_code == 200:
                print("\n✅ Page loaded successfully!")
            else:
                print(f"\n⚠️ Unexpected status code: {response.status_code}")
                
        except Exception as e:
            print(f"\n❌ Exception occurred:")
            print(f"Type: {type(e).__name__}")
            print(f"Message: {str(e)}")
            
            import traceback
            print("\nFull traceback:")
            traceback.print_exc()

