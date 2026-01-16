#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام تصدير DED ERP System
يقوم بإنشاء حزمة تصدير كاملة للنظام
"""

import os
import shutil
import zipfile
from datetime import datetime
import json

def create_export_package():
    """إنشاء حزمة تصدير كاملة"""
    
    # اسم الحزمة
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    export_name = f'DED_ERP_System_v2.0_{timestamp}'
    export_dir = export_name
    
    print(f"🚀 بدء عملية التصدير: {export_name}")
    print("=" * 60)
    
    # إنشاء مجلد التصدير
    if os.path.exists(export_dir):
        shutil.rmtree(export_dir)
    os.makedirs(export_dir)
    
    # قائمة المجلدات المطلوبة
    folders_to_copy = [
        'app',
        'migrations',
        'translations',
        'instance',
        'docs'
    ]
    
    # قائمة الملفات المطلوبة
    files_to_copy = [
        'config.py',
        'run.py',
        'requirements.txt',
        'babel.cfg',
        'README.md',
        'START_HERE.md',
        'INSTALLATION.md',
        'USER_GUIDE.md',
        'POS_INVOICE_INTEGRATION.md',
        'EXPORT_COMPLETE_GUIDE.md',
        'EXPORT_README.md',
        'LICENSE',
        'Dockerfile',
        'docker-compose.yml',
        'render.yaml',
        '.gitignore'
    ]
    
    # نسخ المجلدات
    print("\n📁 نسخ المجلدات...")
    for folder in folders_to_copy:
        if os.path.exists(folder):
            dest = os.path.join(export_dir, folder)
            print(f"  ✓ {folder}")
            shutil.copytree(folder, dest, 
                          ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '*.pyo', '.DS_Store'))
        else:
            print(f"  ⚠ {folder} (غير موجود)")
    
    # نسخ الملفات
    print("\n📄 نسخ الملفات...")
    for file in files_to_copy:
        if os.path.exists(file):
            print(f"  ✓ {file}")
            shutil.copy2(file, export_dir)
        else:
            print(f"  ⚠ {file} (غير موجود)")
    
    # إنشاء ملف معلومات التصدير
    print("\n📝 إنشاء ملف المعلومات...")
    export_info = {
        'name': 'DED ERP System',
        'version': '2.0.0',
        'export_date': datetime.now().isoformat(),
        'features': [
            'نظام نقاط البيع (POS)',
            'إدارة المخزون',
            'إدارة المبيعات',
            'إدارة المشتريات',
            'النظام المحاسبي',
            'إدارة الموارد البشرية',
            'إدارة علاقات العملاء (CRM)',
            'نظام التراخيص',
            'التقارير والإحصائيات',
            'دعم اللغة العربية',
            'تكامل POS مع فواتير المبيعات'
        ],
        'requirements': {
            'python': '3.8+',
            'database': 'SQLite / PostgreSQL',
            'web_server': 'Flask'
        }
    }
    
    with open(os.path.join(export_dir, 'EXPORT_INFO.json'), 'w', encoding='utf-8') as f:
        json.dump(export_info, f, ensure_ascii=False, indent=2)
    
    print("  ✓ EXPORT_INFO.json")
    
    # إنشاء ملف تعليمات التشغيل السريع
    quick_start = """# 🚀 تعليمات التشغيل السريع

## 1. التثبيت

```bash
# تثبيت المتطلبات
pip install -r requirements.txt

# تهيئة قاعدة البيانات
python run.py init-db

# إنشاء مستخدم مدير
python run.py create-admin
```

## 2. التشغيل

```bash
# تشغيل السيرفر
python run.py

# أو
flask run
```

## 3. الوصول للنظام

افتح المتصفح على: http://localhost:5000

- اسم المستخدم: admin
- كلمة المرور: (التي أدخلتها عند الإنشاء)

## 4. الميزات الجديدة

✅ تكامل نقطة البيع مع فواتير المبيعات
✅ إنشاء فاتورة تلقائياً عند إتمام البيع
✅ ربط كامل بين POS والمحاسبة

للمزيد من التفاصيل، راجع:
- START_HERE.md
- POS_INVOICE_INTEGRATION.md
- USER_GUIDE.md
"""
    
    with open(os.path.join(export_dir, 'QUICK_START.md'), 'w', encoding='utf-8') as f:
        f.write(quick_start)
    
    print("  ✓ QUICK_START.md")
    
    # ضغط الحزمة
    print(f"\n📦 ضغط الحزمة...")
    zip_filename = f'{export_name}.zip'
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(export_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, export_dir)
                zipf.write(file_path, os.path.join(export_name, arcname))
    
    # حساب حجم الملف
    zip_size = os.path.getsize(zip_filename) / (1024 * 1024)  # MB
    
    print(f"  ✓ {zip_filename} ({zip_size:.2f} MB)")
    
    # تنظيف المجلد المؤقت
    shutil.rmtree(export_dir)
    
    # طباعة الملخص
    print("\n" + "=" * 60)
    print("✅ تم التصدير بنجاح!")
    print("=" * 60)
    print(f"\n📦 اسم الملف: {zip_filename}")
    print(f"📊 الحجم: {zip_size:.2f} MB")
    print(f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n📍 الموقع: {os.path.abspath(zip_filename)}")
    print("\n" + "=" * 60)

if __name__ == '__main__':
    try:
        create_export_package()
    except Exception as e:
        print(f"\n❌ خطأ: {str(e)}")
        import traceback
        traceback.print_exc()

