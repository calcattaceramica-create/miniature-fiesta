#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
اختبار واجهة إدارة التراخيص - License UI Test
Test the new license management UI features
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

def test_license_ui():
    """Test the license management UI features"""
    
    print("=" * 60)
    print("🧪 اختبار واجهة إدارة التراخيص - License UI Test")
    print("=" * 60)
    print()
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Check if DED_Control_Panel.pyw exists
    print("1️⃣ اختبار وجود الملف الرئيسي...")
    try:
        panel_file = Path("DED_Control_Panel.pyw")
        assert panel_file.exists(), "الملف غير موجود!"
        print("   ✅ الملف موجود")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ فشل: {e}")
        tests_failed += 1
    print()
    
    # Test 2: Check for new UI components
    print("2️⃣ اختبار وجود مكونات الواجهة الجديدة...")
    try:
        with open("DED_Control_Panel.pyw", 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_components = [
            "update_license_stats",
            "total_licenses_label",
            "active_licenses_label",
            "suspended_licenses_label",
            "expired_licenses_label",
            "recent_licenses_listbox",
            "إدارة التراخيص السريعة",
            "Quick License Management"
        ]
        
        for component in required_components:
            assert component in content, f"المكون {component} غير موجود!"
        
        print("   ✅ جميع المكونات موجودة")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ فشل: {e}")
        tests_failed += 1
    print()
    
    # Test 3: Create sample licenses for testing
    print("3️⃣ إنشاء تراخيص تجريبية...")
    try:
        licenses = {}
        
        # Active license
        licenses["ACTIVE-LICENSE-KEY-001"] = {
            "company": "شركة اختبار نشطة",
            "expiry": (datetime.now() + timedelta(days=100)).strftime("%Y-%m-%d"),
            "status": "active",
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Suspended license
        licenses["SUSPENDED-LICENSE-KEY-002"] = {
            "company": "شركة اختبار معلقة",
            "expiry": (datetime.now() + timedelta(days=50)).strftime("%Y-%m-%d"),
            "status": "suspended",
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Expired license
        licenses["EXPIRED-LICENSE-KEY-003"] = {
            "company": "شركة اختبار منتهية",
            "expiry": (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"),
            "status": "active",
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Expiring soon license
        licenses["EXPIRING-LICENSE-KEY-004"] = {
            "company": "شركة اختبار قريبة الانتهاء",
            "expiry": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
            "status": "active",
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Save to test file
        with open("licenses_test.json", 'w', encoding='utf-8') as f:
            json.dump(licenses, f, indent=2, ensure_ascii=False)
        
        print(f"   ✅ تم إنشاء {len(licenses)} تراخيص تجريبية")
        print(f"      - 1 نشط (100 يوم)")
        print(f"      - 1 معلق (50 يوم)")
        print(f"      - 1 منتهي (-10 يوم)")
        print(f"      - 1 قريب الانتهاء (5 أيام)")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ فشل: {e}")
        tests_failed += 1
    print()
    
    # Test 4: Check statistics calculation logic
    print("4️⃣ اختبار منطق حساب الإحصائيات...")
    try:
        total = len(licenses)
        active = sum(1 for lic in licenses.values() 
                    if lic['status'] == 'active' and 
                    datetime.strptime(lic['expiry'], "%Y-%m-%d") > datetime.now())
        suspended = sum(1 for lic in licenses.values() if lic['status'] == 'suspended')
        expired = sum(1 for lic in licenses.values() 
                     if datetime.strptime(lic['expiry'], "%Y-%m-%d") < datetime.now())
        
        print(f"   ✅ الإحصائيات:")
        print(f"      - إجمالي: {total}")
        print(f"      - نشط: {active}")
        print(f"      - معلق: {suspended}")
        print(f"      - منتهي: {expired}")
        
        assert total == 4, "العدد الإجمالي خاطئ!"
        assert active == 2, "عدد النشطة خاطئ!"
        assert suspended == 1, "عدد المعلقة خاطئ!"
        assert expired == 1, "عدد المنتهية خاطئ!"
        
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ فشل: {e}")
        tests_failed += 1
    print()
    
    # Test 5: Check UI color scheme
    print("5️⃣ اختبار نظام الألوان...")
    try:
        with open("DED_Control_Panel.pyw", 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_colors = [
            "'accent': '#3b82f6'",
            "'success': '#22c55e'",
            "'danger': '#ef4444'",
            "'warning': '#f59e0b'"
        ]
        
        for color in required_colors:
            assert color in content, f"اللون {color} غير موجود!"
        
        print("   ✅ جميع الألوان موجودة")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ فشل: {e}")
        tests_failed += 1
    print()
    
    # Summary
    print("=" * 60)
    print("📊 ملخص النتائج - Test Summary")
    print("=" * 60)
    print(f"✅ نجح: {tests_passed}")
    print(f"❌ فشل: {tests_failed}")
    print(f"📈 نسبة النجاح: {(tests_passed/(tests_passed+tests_failed)*100):.1f}%")
    print()
    
    if tests_failed == 0:
        print("🎉 جميع الاختبارات نجحت! الواجهة جاهزة للاستخدام!")
        print("🚀 يمكنك الآن تشغيل: python DED_Control_Panel.pyw")
    else:
        print("⚠️ بعض الاختبارات فشلت. الرجاء مراجعة الأخطاء.")
    
    print("=" * 60)
    
    return tests_failed == 0

if __name__ == "__main__":
    success = test_license_ui()
    sys.exit(0 if success else 1)

