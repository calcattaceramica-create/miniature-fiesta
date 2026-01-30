"""Simple check for supplier history link"""
with open('app/templates/reports/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("="*70)
print("Checking Supplier History Report Link")
print("="*70)

# Check for history icon
if 'fa-history' in content:
    print("✅ History icon (fa-history) found")
else:
    print("❌ History icon NOT found")

# Check for link text
if 'Supplier History Report' in content:
    print("✅ 'Supplier History Report' text found")
else:
    print("❌ 'Supplier History Report' text NOT found")

# Count supplier report links
supplier_count = content.count('reports.suppliers')
print(f"📊 Total supplier report links: {supplier_count}")

# List all supplier reports
print("\n📋 Supplier Reports Section:")
lines = content.split('\n')
in_supplier_section = False
for i, line in enumerate(lines):
    if 'Supplier Reports' in line:
        in_supplier_section = True
    if in_supplier_section:
        if 'list-group-item' in line and 'href' in line:
            # Extract the link text
            if i+1 < len(lines):
                next_line = lines[i+1].strip()
                print(f"  • {next_line}")
        if '</div>' in line and in_supplier_section:
            # Count closing divs
            if line.count('</div>') >= 2:
                break

print("\n" + "="*70)
print("✅ Check completed!")
print("="*70)

