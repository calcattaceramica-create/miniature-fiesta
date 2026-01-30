"""Verify that the three cards are properly configured in inventory.html"""
import os
from datetime import datetime

print("="*80)
print("🔍 VERIFICATION SCRIPT - Three Summary Cards in Inventory Report")
print("="*80)

file_path = 'app/templates/reports/inventory.html'

# Check file exists
if not os.path.exists(file_path):
    print(f"❌ ERROR: File not found: {file_path}")
    exit(1)

print(f"✅ File found: {file_path}")

# Get file info
mod_time = os.path.getmtime(file_path)
mod_datetime = datetime.fromtimestamp(mod_time)
print(f"📅 Last modified: {mod_datetime.strftime('%Y-%m-%d %H:%M:%S')}")

# Read file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

print(f"📄 Total lines: {len(lines)}")

# Find Summary Cards section
summary_start = -1
summary_end = -1

for i, line in enumerate(lines):
    if '<!-- Summary Cards -->' in line:
        summary_start = i
    if '<!-- Inventory Table -->' in line:
        summary_end = i
        break

if summary_start == -1:
    print("❌ ERROR: '<!-- Summary Cards -->' comment not found!")
    exit(1)

if summary_end == -1:
    print("❌ ERROR: '<!-- Inventory Table -->' comment not found!")
    exit(1)

print(f"✅ Summary Cards section found: lines {summary_start+1} to {summary_end+1}")

# Extract section
section = '\n'.join(lines[summary_start:summary_end])

# Verify structure
print("\n" + "="*80)
print("📊 STRUCTURE VERIFICATION")
print("="*80)

checks = {
    'Three columns (col-md-4)': section.count('col-md-4') == 3,
    'Primary gradient (bg-gradient-primary)': 'bg-gradient-primary' in section,
    'Success gradient (bg-gradient-success)': 'bg-gradient-success' in section,
    'Info gradient (bg-gradient-info)': 'bg-gradient-info' in section,
    'Total Inventory Value card': 'Total Inventory Value' in section,
    'Total Products card': 'Total Products' in section,
    'Average Value card': 'Average Value' in section,
    'Warehouse icon (fa-warehouse)': 'fa-warehouse' in section,
    'Boxes icon (fa-boxes)': 'fa-boxes' in section,
    'Chart icon (fa-chart-line)': 'fa-chart-line' in section,
    'Large icons (fa-3x)': section.count('fa-3x') == 3,
    'Currency symbol variable': 'currency_symbol' in section,
    'Shadow effect (shadow-lg)': section.count('shadow-lg') == 3,
    'Flexbox layout (d-flex)': 'd-flex' in section,
    'Full height cards (h-100)': section.count('h-100') == 3,
}

passed = 0
failed = 0

for check, result in checks.items():
    if result:
        print(f"✅ {check}")
        passed += 1
    else:
        print(f"❌ {check}")
        failed += 1

# Check CSS
print("\n" + "="*80)
print("🎨 CSS VERIFICATION")
print("="*80)

css_checks = {
    'Primary gradient CSS': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' in content,
    'Success gradient CSS': 'linear-gradient(135deg, #56ab2f 0%, #a8e063 100%)' in content,
    'Info gradient CSS': 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)' in content,
}

for check, result in css_checks.items():
    if result:
        print(f"✅ {check}")
        passed += 1
    else:
        print(f"❌ {check}")
        failed += 1

# Summary
print("\n" + "="*80)
print("📊 SUMMARY")
print("="*80)
print(f"Total checks: {passed + failed}")
print(f"✅ Passed: {passed}")
print(f"❌ Failed: {failed}")

if failed == 0:
    print("\n" + "🎉"*20)
    print("✅ ALL CHECKS PASSED!")
    print("🎉"*20)
    print("\n📋 NEXT STEPS:")
    print("1. Run: restart_server.bat")
    print("2. Open browser in Incognito mode (Ctrl+Shift+N)")
    print("3. Go to: http://localhost:5000/reports/inventory")
    print("4. You should see THREE colored cards at the top!")
else:
    print("\n⚠️ SOME CHECKS FAILED!")
    print("Please review the errors above.")

print("="*80)

