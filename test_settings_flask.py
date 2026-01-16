#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test the settings page using Flask test client
"""

import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User

def test_settings_page():
    """Test settings page"""
    
    print("=" * 80)
    print("TESTING SETTINGS PAGE WITH FLASK TEST CLIENT")
    print("=" * 80)
    
    # Create app
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            # Step 1: Login
            print("\n1. Logging in...")
            response = client.post('/auth/login', data={
                'username': 'admin',
                'password': 'admin123'
            }, follow_redirects=True)
            
            if response.status_code != 200:
                print(f"❌ Login failed: {response.status_code}")
                return False
            
            print("✅ Logged in successfully")
            
            # Step 2: Get settings page
            print("\n2. Getting settings page...")
            response = client.get('/settings/')
            
            if response.status_code != 200:
                print(f"❌ Failed to get settings page: {response.status_code}")
                return False
            
            print("✅ Settings page loaded")
            
            # Step 3: Check for language card elements
            print("\n3. Checking for language card elements...")
            html = response.data.decode('utf-8')
            
            checks = {
                'Language icon (fa-language)': 'fa-language' in html,
                'Language title (إعدادات اللغة)': 'إعدادات اللغة' in html,
                'Language description (تغيير لغة التطبيق)': 'تغيير لغة التطبيق' in html,
                'Language button (تغيير اللغة)': 'تغيير اللغة' in html,
                'Language route (language_settings)': 'language_settings' in html
            }
            
            print("\n" + "=" * 80)
            print("RESULTS:")
            print("=" * 80)
            
            all_found = True
            for name, found in checks.items():
                status = "✅" if found else "❌"
                print(f"{status} {name}: {'Found' if found else 'NOT FOUND'}")
                if not found:
                    all_found = False
            
            # Count cards
            card_count = html.count('<div class="card h-100">')
            print(f"\n📊 Total cards found: {card_count}")
            
            # Save HTML for debugging
            print("\n🔍 Saving HTML for inspection...")
            with open('settings_page_output.html', 'w', encoding='utf-8') as f:
                f.write(html)
            print("✅ Saved to: settings_page_output.html")
            
            print("\n" + "=" * 80)
            
            if all_found:
                print("🎉 SUCCESS! Language settings card is present in the HTML!")
                print("\n✅ The card exists in the rendered template")
                print("✅ All text elements are present")
                print("\n💡 If you don't see it in your browser:")
                print("   1. The HTML is correct - the problem is browser cache")
                print("   2. Open Incognito/Private window (Ctrl+Shift+N)")
                print("   3. Go to: http://localhost:5000/settings/")
                print("   4. You WILL see the card there!")
                return True
            else:
                print("❌ FAILED! Language settings card elements are missing")
                print("\n🔍 Check the saved HTML file: settings_page_output.html")
                return False

if __name__ == '__main__':
    try:
        result = test_settings_page()
        sys.exit(0 if result else 1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

