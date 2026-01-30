"""Test script to verify supplier history report link is added and working"""
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User
from flask import url_for

def test_supplier_history_link():
    """Test that the supplier history link is present in the reports index"""
    app = create_app()
    
    with app.app_context():
        # Create a test client
        client = app.test_client()
        
        # Login as admin
        with client.session_transaction() as sess:
            sess['_user_id'] = '1'
            sess['_fresh'] = True
        
        print("📊 Testing Reports Index Page...")
        print("DEBUG: Request path: /reports")
        
        # Get the reports index page
        response = client.get('/reports')
        
        if response.status_code == 200:
            print(f"✅ Reports Index - Status: {response.status_code} OK")
            
            # Check if the supplier history link is present
            html = response.data.decode('utf-8')
            
            # Check for the history icon
            if 'fa-history' in html:
                print("✅ History icon found")
            else:
                print("❌ History icon NOT found")
            
            # Check for the link text (in English or Arabic)
            if 'Supplier History Report' in html or 'تقرير سجل الموردين' in html or 'تقرير تاريخ المورد' in html:
                print("✅ Supplier History Report link text found")
            else:
                print("❌ Supplier History Report link text NOT found")
            
            # Check for the URL
            if 'reports.suppliers_list' in html:
                print("✅ Link to suppliers list found (for accessing history)")
            else:
                print("❌ Link NOT found")
            
            # Count how many supplier report links we have
            supplier_links = html.count('list-group-item list-group-item-action')
            print(f"📋 Total links in page: {supplier_links}")
            
            # Check for all 4 supplier reports
            reports = [
                ('Supplier List', 'قائمة الموردين'),
                ('Top Suppliers Report', 'تقرير أفضل الموردين'),
                ('Supplier Balances Report', 'تقرير أرصدة الموردين'),
                ('Supplier History Report', 'تقرير سجل الموردين')
            ]
            
            print("\n📊 Checking all supplier reports:")
            for en, ar in reports:
                if en in html or ar in html:
                    print(f"  ✅ {en} ({ar})")
                else:
                    print(f"  ❌ {en} ({ar})")
            
        else:
            print(f"❌ Reports Index - Status: {response.status_code} FAILED")
            print(f"Response: {response.data.decode('utf-8')[:500]}")
        
        print("\n" + "="*70)
        print("✅ Test completed!")
        print("="*70)

if __name__ == '__main__':
    test_supplier_history_link()

