"""Test to verify the HTML file has the three cards"""
import os

file_path = 'app/templates/reports/inventory.html'

print("="*70)
print("Checking inventory.html file")
print("="*70)

# Check file exists
if os.path.exists(file_path):
    print(f"✅ File exists: {file_path}")
    
    # Get file modification time
    mod_time = os.path.getmtime(file_path)
    from datetime import datetime
    mod_datetime = datetime.fromtimestamp(mod_time)
    print(f"📅 Last modified: {mod_datetime}")
    
    # Read and check content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the summary cards section
    if '<!-- Summary Cards -->' in content:
        print("✅ Summary Cards section found")
        
        # Extract the section
        start = content.find('<!-- Summary Cards -->')
        end = content.find('<!-- Inventory Table -->')
        section = content[start:end]
        
        # Count cards
        card_count = section.count('col-md-4')
        print(f"📊 Number of cards (col-md-4): {card_count}")
        
        # Check gradients
        gradients = ['bg-gradient-primary', 'bg-gradient-success', 'bg-gradient-info']
        for grad in gradients:
            if grad in section:
                print(f"✅ {grad} found")
            else:
                print(f"❌ {grad} NOT found")
        
        # Check card titles
        titles = ['Total Inventory Value', 'Total Products', 'Average Value']
        for title in titles:
            if title in section:
                print(f"✅ '{title}' found")
            else:
                print(f"❌ '{title}' NOT found")
        
        # Print a snippet of the section
        print("\n" + "="*70)
        print("First 500 characters of Summary Cards section:")
        print("="*70)
        print(section[:500])
        
    else:
        print("❌ Summary Cards section NOT found")
else:
    print(f"❌ File NOT found: {file_path}")

print("\n" + "="*70)
print("INSTRUCTIONS TO FIX CACHE ISSUE:")
print("="*70)
print("1. Stop the server (Ctrl+C)")
print("2. Clear browser cache (Ctrl+Shift+Delete)")
print("3. Or open in incognito/private mode")
print("4. Or add ?v=2 to the URL: http://localhost:5000/reports/inventory?v=2")
print("5. Restart server: python run.py")
print("="*70)

