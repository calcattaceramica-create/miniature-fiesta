"""Test that the three cards are in Arabic"""
import os

print("="*80)
print("🔍 ARABIC TRANSLATION VERIFICATION")
print("="*80)

file_path = 'app/templates/reports/inventory.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find Summary Cards section
cards_start = content.find('<!-- Summary Cards -->')
cards_end = content.find('<!-- Inventory Table -->')
cards_section = content[cards_start:cards_end]

print("\n📊 CHECKING ARABIC TEXT IN CARDS:")
print("-" * 80)

arabic_checks = {
    '✅ إجمالي قيمة المخزون (Total Inventory Value)': 'إجمالي قيمة المخزون' in cards_section,
    '✅ إجمالي المنتجات (Total Products)': 'إجمالي المنتجات' in cards_section,
    '✅ متوسط القيمة (Average Value)': 'متوسط القيمة' in cards_section,
    '✅ منتج (Items)': 'منتج' in cards_section,
    '✅ لكل منتج (Per Item)': 'لكل منتج' in cards_section,
}

all_passed = True
for name, result in arabic_checks.items():
    if result:
        print(f"{name} ✓")
    else:
        print(f"❌ {name} FAILED")
        all_passed = False

# Check that English text is removed
print("\n📊 CHECKING ENGLISH TEXT REMOVED:")
print("-" * 80)

english_checks = {
    '✅ "Total Inventory Value" removed': 'Total Inventory Value' not in cards_section,
    '✅ "Total Products" removed': 'Total Products' not in cards_section,
    '✅ "Average Value" removed': 'Average Value' not in cards_section,
    '✅ "Items" removed': '"Items"' not in cards_section or 'Items' not in cards_section.replace('منتج', ''),
    '✅ "Per Item" removed': 'Per Item' not in cards_section,
}

for name, result in english_checks.items():
    if result:
        print(f"{name} ✓")
    else:
        print(f"❌ {name} FAILED")
        all_passed = False

print("\n" + "="*80)
if all_passed:
    print("🎉 ALL CHECKS PASSED! Cards are now in Arabic!")
    print("="*80)
    print("\n📋 NEXT STEPS:")
    print("1. Restart the server")
    print("2. Refresh the browser (Ctrl+F5)")
    print("3. You should see the cards in Arabic:")
    print("\n🎨 Expected Arabic text:")
    print("   • إجمالي قيمة المخزون (Purple card)")
    print("   • إجمالي المنتجات - منتج (Green card)")
    print("   • متوسط القيمة - لكل منتج (Blue card)")
else:
    print("❌ SOME CHECKS FAILED!")
    print("Please review the errors above.")

print("="*80)

