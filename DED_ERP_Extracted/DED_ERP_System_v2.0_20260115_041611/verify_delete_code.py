#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
التحقق من كود حذف المنتج
"""

import os

def verify_delete_code():
    """Verify the delete product code"""
    print("\n" + "=" * 80)
    print("🔍 Verifying Delete Product Code")
    print("=" * 80)
    
    routes_file = "app/inventory/routes.py"
    
    if not os.path.exists(routes_file):
        print(f"\n❌ File not found: {routes_file}")
        return
    
    print(f"\n📁 Reading file: {routes_file}")
    
    with open(routes_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for the new delete function
    print("\n🔍 Checking for new delete function...")
    
    if 'def delete_product(id):' in content:
        print("   ✅ Function 'delete_product' found")
    else:
        print("   ❌ Function 'delete_product' NOT found")
    
    if 'Delete product permanently (hard delete)' in content:
        print("   ✅ Hard delete comment found")
    else:
        print("   ❌ Hard delete comment NOT found")
    
    if 'SalesInvoiceItem.query.filter_by(product_id=id).delete()' in content:
        print("   ✅ Deletes SalesInvoiceItem")
    else:
        print("   ❌ Does NOT delete SalesInvoiceItem")
    
    if 'Stock.query.filter_by(product_id=id).delete()' in content:
        print("   ✅ Deletes Stock")
    else:
        print("   ❌ Does NOT delete Stock")
    
    if 'StockMovement.query.filter_by(product_id=id).delete()' in content:
        print("   ✅ Deletes StockMovement")
    else:
        print("   ❌ Does NOT delete StockMovement")
    
    # Check for OLD code that checks relations
    print("\n🔍 Checking for OLD code (should NOT exist)...")
    
    if 'force_delete' in content:
        print("   ❌ WARNING: 'force_delete' found - OLD CODE EXISTS!")
    else:
        print("   ✅ 'force_delete' NOT found - Good!")
    
    if 'relations.append' in content:
        print("   ❌ WARNING: 'relations.append' found - OLD CODE EXISTS!")
    else:
        print("   ✅ 'relations.append' NOT found - Good!")
    
    if 'will be deactivated instead' in content:
        print("   ❌ WARNING: 'will be deactivated instead' found - OLD CODE EXISTS!")
    else:
        print("   ✅ 'will be deactivated instead' NOT found - Good!")
    
    # Find the delete_product function
    print("\n📋 Extracting delete_product function...")
    
    lines = content.split('\n')
    in_function = False
    function_lines = []
    
    for i, line in enumerate(lines, 1):
        if 'def delete_product(id):' in line:
            in_function = True
            start_line = i
        
        if in_function:
            function_lines.append(f"{i:4d}: {line}")
            
            # Stop at next function or route
            if len(function_lines) > 1 and (line.startswith('def ') or line.startswith('@bp.route')):
                function_lines = function_lines[:-1]  # Remove the last line
                break
    
    if function_lines:
        print(f"\n📄 Function found at line {start_line}:")
        print("-" * 80)
        for line in function_lines[:30]:  # Show first 30 lines
            print(line)
        if len(function_lines) > 30:
            print(f"... ({len(function_lines) - 30} more lines)")
        print("-" * 80)
    else:
        print("\n❌ Function NOT found!")
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 Summary")
    print("=" * 80)
    
    has_new_code = (
        'def delete_product(id):' in content and
        'Delete product permanently (hard delete)' in content and
        'SalesInvoiceItem.query.filter_by(product_id=id).delete()' in content
    )
    
    has_old_code = (
        'force_delete' in content or
        'relations.append' in content or
        'will be deactivated instead' in content
    )
    
    if has_new_code and not has_old_code:
        print("\n✅ CODE IS CORRECT!")
        print("   - New delete function exists")
        print("   - Deletes all related records")
        print("   - No old code that checks relations")
    elif has_new_code and has_old_code:
        print("\n⚠️  CODE IS MIXED!")
        print("   - New delete function exists")
        print("   - BUT old code also exists")
        print("   - You may be running the wrong version")
    else:
        print("\n❌ CODE IS WRONG!")
        print("   - New delete function NOT found")
        print("   - Please check the file")

def main():
    """Run the verification"""
    print("\n" + "=" * 80)
    print("🚀 Delete Product Code Verification")
    print("=" * 80)
    
    verify_delete_code()
    
    print("\n" + "=" * 80)
    print("✅ Verification Completed!")
    print("=" * 80 + "\n")

if __name__ == '__main__':
    main()

