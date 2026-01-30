"""Test script to verify the three summary cards in inventory report"""

# Simple file check
with open('app/templates/reports/inventory.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("="*70)
print("Testing Inventory Report - Three Summary Cards")
print("="*70)

# Check for gradient backgrounds
checks = [
    ('bg-gradient-primary', 'Primary gradient (Total Inventory Value)'),
    ('bg-gradient-success', 'Success gradient (Total Products)'),
    ('bg-gradient-info', 'Info gradient (Average Value)'),
    ('linear-gradient', 'CSS linear-gradient'),
]

for check, description in checks:
    if check in content:
        print(f"✅ {description}: Found")
    else:
        print(f"❌ {description}: NOT found")

# Check for card labels
labels = [
    ('Total Inventory Value', 'إجمالي قيمة المخزون'),
    ('Total Products', 'إجمالي المنتجات'),
    ('Average Value', 'متوسط القيمة'),
]

print("\n📊 Checking card labels:")
for en, ar in labels:
    if en in content:
        print(f"  ✅ {en} ({ar})")
    else:
        print(f"  ❌ {en} ({ar})")

# Check for icons
icons = [
    ('fa-warehouse', 'Warehouse icon'),
    ('fa-boxes', 'Boxes icon'),
    ('fa-chart-line', 'Chart line icon'),
]

print("\n🎨 Checking icons:")
for icon, description in icons:
    count = content.count(icon)
    if count > 0:
        print(f"  ✅ {description} ({icon}): Found {count} times")
    else:
        print(f"  ❌ {description} ({icon}): NOT found")

# Check for currency symbol
if 'currency_symbol' in content:
    print("\n✅ Currency symbol variable found")
else:
    print("\n❌ Currency symbol variable NOT found")

# Check for three cards in a row
if 'col-md-4' in content:
    count = content.count('col-md-4')
    print(f"✅ Three-column layout found ({count} col-md-4 instances)")
else:
    print("❌ Three-column layout NOT found")

# Check for d-flex layout
if 'd-flex' in content:
    print("✅ Flexbox layout found")
else:
    print("❌ Flexbox layout NOT found")

# Check for shadow
if 'shadow-lg' in content:
    count = content.count('shadow-lg')
    print(f"✅ Shadow effect found ({count} instances)")
else:
    print("❌ Shadow effect NOT found")

print("\n" + "="*70)
print("✅ Check completed!")
print("="*70)

