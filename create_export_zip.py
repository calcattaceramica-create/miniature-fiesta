"""
سكريبت لإنشاء ملف ZIP للتصدير
يستبعد الملفات والمجلدات غير الضرورية
"""

import os
import zipfile
from datetime import datetime
from pathlib import Path

def should_exclude(path):
    """تحديد الملفات والمجلدات التي يجب استبعادها"""
    exclude_patterns = [
        'venv',
        '__pycache__',
        '.git',
        '.vscode',
        '.idea',
        'instance',
        '*.pyc',
        '*.pyo',
        '*.pyd',
        '.Python',
        'pip-log.txt',
        'pip-delete-this-directory.txt',
        '.env',
        '*.log',
        '*.db',
        '.DS_Store',
        'Thumbs.db',
        '*.swp',
        '*.swo',
        '*~',
        '.pytest_cache',
        '.coverage',
        'htmlcov',
        'dist',
        'build',
        '*.egg-info',
        'node_modules',
        '⚠️_',  # ملفات التحذيرات
    ]
    
    path_str = str(path)
    
    # تحقق من المجلدات
    for pattern in exclude_patterns:
        if pattern.startswith('*'):
            if path_str.endswith(pattern[1:]):
                return True
        else:
            if pattern in path_str:
                return True
    
    return False

def create_export_zip():
    """إنشاء ملف ZIP للتصدير"""
    
    # المجلد الحالي
    base_dir = Path.cwd()
    
    # اسم ملف ZIP
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    zip_filename = f'DED_System_v1.2.0_{timestamp}.zip'
    zip_path = base_dir / zip_filename
    
    print("=" * 60)
    print("🎯 إنشاء ملف ZIP للتصدير")
    print("=" * 60)
    print(f"📦 اسم الملف: {zip_filename}")
    print(f"📍 الموقع: {zip_path}")
    print("=" * 60)
    print()
    
    files_added = 0
    files_excluded = 0
    
    # إنشاء ملف ZIP
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # المرور على جميع الملفات
        for root, dirs, files in os.walk(base_dir):
            root_path = Path(root)
            
            # استبعاد المجلدات غير المرغوبة
            dirs[:] = [d for d in dirs if not should_exclude(root_path / d)]
            
            for file in files:
                file_path = root_path / file
                
                # تخطي ملف ZIP نفسه
                if file_path == zip_path:
                    continue
                
                # تحقق من الاستبعاد
                if should_exclude(file_path):
                    files_excluded += 1
                    continue
                
                # إضافة الملف إلى ZIP
                arcname = file_path.relative_to(base_dir)
                zipf.write(file_path, arcname)
                files_added += 1
                
                # طباعة التقدم كل 50 ملف
                if files_added % 50 == 0:
                    print(f"✅ تمت إضافة {files_added} ملف...")
    
    # حساب حجم الملف
    file_size = zip_path.stat().st_size
    file_size_mb = file_size / (1024 * 1024)
    
    print()
    print("=" * 60)
    print("✅ تم إنشاء ملف ZIP بنجاح!")
    print("=" * 60)
    print(f"📦 اسم الملف: {zip_filename}")
    print(f"📍 الموقع: {zip_path}")
    print(f"📊 الحجم: {file_size_mb:.2f} MB")
    print(f"✅ ملفات مضافة: {files_added}")
    print(f"⏭️ ملفات مستبعدة: {files_excluded}")
    print("=" * 60)
    print()
    print("🎉 المشروع جاهز للمشاركة!")
    print()
    print("📤 يمكنك الآن:")
    print("   1. مشاركة الملف عبر البريد الإلكتروني")
    print("   2. رفعه على Google Drive أو Dropbox")
    print("   3. مشاركته عبر USB")
    print("   4. رفعه على GitHub Releases")
    print()
    print("=" * 60)
    
    return zip_path

if __name__ == '__main__':
    try:
        zip_path = create_export_zip()
        print(f"\n✅ تم الحفظ في: {zip_path}")
    except Exception as e:
        print(f"\n❌ خطأ: {e}")
        import traceback
        traceback.print_exc()

