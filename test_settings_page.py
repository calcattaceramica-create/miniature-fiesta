#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test the settings page to verify language card is present
"""

import requests
from bs4 import BeautifulSoup

def test_settings_page():
    """Test settings page after login"""
    
    base_url = 'http://localhost:5000'
    
    print("=" * 80)
    print("TESTING SETTINGS PAGE")
    print("=" * 80)
    
    # Create session
    session = requests.Session()
    
    # Step 1: Get login page to get CSRF token
    print("\n1. Getting login page...")
    login_page = session.get(f'{base_url}/auth/login')
    
    if login_page.status_code != 200:
        print(f"❌ Failed to get login page: {login_page.status_code}")
        return False
    
    print("✅ Login page loaded")
    
    # Step 2: Login
    print("\n2. Logging in as admin...")
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    login_response = session.post(f'{base_url}/auth/login', data=login_data, allow_redirects=True)
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        return False
    
    # Check if we're logged in (not redirected to login page)
    if 'login' in login_response.url:
        print("❌ Login failed - still on login page")
        print(f"Response URL: {login_response.url}")
        return False
    
    print("✅ Logged in successfully")
    
    # Step 3: Get settings page
    print("\n3. Getting settings page...")
    settings_response = session.get(f'{base_url}/settings/')
    
    if settings_response.status_code != 200:
        print(f"❌ Failed to get settings page: {settings_response.status_code}")
        return False
    
    print("✅ Settings page loaded")
    
    # Step 4: Parse HTML and look for language card
    print("\n4. Parsing HTML...")
    soup = BeautifulSoup(settings_response.text, 'html.parser')
    
    # Look for language-related elements
    checks = {
        'Language icon (fa-language)': soup.find('i', class_='fa-language'),
        'Language title': soup.find(string=lambda text: text and 'إعدادات اللغة' in text),
        'Language description': soup.find(string=lambda text: text and 'تغيير لغة التطبيق' in text),
        'Language button': soup.find(string=lambda text: text and 'تغيير اللغة' in text),
        'Language route': soup.find('a', href=lambda href: href and 'language' in href)
    }
    
    print("\n" + "=" * 80)
    print("RESULTS:")
    print("=" * 80)
    
    all_found = True
    for name, element in checks.items():
        found = element is not None
        status = "✅" if found else "❌"
        print(f"{status} {name}: {'Found' if found else 'NOT FOUND'}")
        if not found:
            all_found = False
    
    # Count all cards
    cards = soup.find_all('div', class_='card')
    print(f"\n📊 Total cards found: {len(cards)}")
    
    # List all card titles
    print("\n📋 Card titles found:")
    card_titles = soup.find_all('h5')
    for i, title in enumerate(card_titles, 1):
        print(f"   {i}. {title.get_text(strip=True)}")
    
    print("\n" + "=" * 80)
    
    if all_found:
        print("🎉 SUCCESS! Language settings card is present on the page!")
        print("\n✅ The card is visible in the HTML")
        print("✅ All elements are present")
        print("\n💡 If you don't see it in browser:")
        print("   1. Clear browser cache (Ctrl+Shift+Delete)")
        print("   2. Use Incognito/Private window (Ctrl+Shift+N)")
        print("   3. Hard refresh (Ctrl+Shift+R)")
        return True
    else:
        print("❌ FAILED! Language settings card is NOT complete")
        print("\n🔍 Saving HTML for inspection...")
        with open('settings_page_debug.html', 'w', encoding='utf-8') as f:
            f.write(settings_response.text)
        print("✅ Saved to: settings_page_debug.html")
        return False

if __name__ == '__main__':
    test_settings_page()

