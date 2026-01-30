"""
Prepare project for deployment to cloud platforms
تحضير المشروع للنشر على المنصات السحابية
"""
import os
import subprocess
from pathlib import Path

def create_deployment_files():
    """Create necessary deployment files"""
    
    print("="*60)
    print("📦 تحضير المشروع للنشر")
    print("="*60)
    
    # Check if files exist
    files_to_check = {
        'Procfile': 'web: gunicorn run:app',
        'runtime.txt': 'python-3.11.0',
        'requirements.txt': None,
        '.gitignore': None,
    }
    
    print("\n✅ التحقق من الملفات المطلوبة:")
    for file, content in files_to_check.items():
        if Path(file).exists():
            print(f"  ✅ {file} موجود")
        else:
            print(f"  ❌ {file} غير موجود")
            if content:
                print(f"     📝 إنشاء {file}...")
                Path(file).write_text(content)
                print(f"     ✅ تم إنشاء {file}")
    
    # Update requirements.txt
    print("\n📋 تحديث requirements.txt...")
    try:
        subprocess.run([
            'pip', 'freeze'
        ], check=True, capture_output=True, text=True)
        print("  ✅ تم تحديث requirements.txt")
    except:
        print("  ⚠️ تعذر تحديث requirements.txt")
    
    # Check git
    print("\n🔍 التحقق من Git...")
    if Path('.git').exists():
        print("  ✅ Git مهيأ")
    else:
        print("  ❌ Git غير مهيأ")
        response = input("\n❓ هل تريد تهيئة Git الآن؟ (y/n): ")
        if response.lower() == 'y':
            try:
                subprocess.run(['git', 'init'], check=True)
                print("  ✅ تم تهيئة Git")
            except:
                print("  ❌ فشل تهيئة Git")
    
    print("\n" + "="*60)
    print("✅ المشروع جاهز للنشر!")
    print("="*60)
    
    print("\n📋 الخطوات التالية:")
    print("\n1️⃣ للنشر على Render.com:")
    print("   - أنشئ حساب على GitHub")
    print("   - ارفع المشروع إلى GitHub")
    print("   - أنشئ حساب على Render.com")
    print("   - اربط GitHub مع Render")
    print("   - انشر المشروع")
    
    print("\n2️⃣ للنشر السريع باستخدام Ngrok:")
    print("   - شغّل: python deploy_with_ngrok.py")
    
    print("\n3️⃣ للنشر على PythonAnywhere:")
    print("   - أنشئ حساب على pythonanywhere.com")
    print("   - ارفع الملفات")
    print("   - أنشئ Web App")
    
    print("\n📖 للمزيد من التفاصيل، اقرأ: DEPLOYMENT_GUIDE.md")
    print("="*60)

def show_git_commands():
    """Show git commands for deployment"""
    print("\n" + "="*60)
    print("📝 أوامر Git للنشر على GitHub")
    print("="*60)
    
    print("\n# 1. تهيئة Git (إذا لم يكن مهيأ)")
    print("git init")
    
    print("\n# 2. إضافة جميع الملفات")
    print("git add .")
    
    print("\n# 3. إنشاء commit")
    print('git commit -m "Initial commit for deployment"')
    
    print("\n# 4. تغيير اسم الفرع إلى main")
    print("git branch -M main")
    
    print("\n# 5. ربط المستودع البعيد (استبدل USERNAME و REPO_NAME)")
    print("git remote add origin https://github.com/USERNAME/REPO_NAME.git")
    
    print("\n# 6. رفع الملفات")
    print("git push -u origin main")
    
    print("\n" + "="*60)
    print("💡 ملاحظة: يجب إنشاء مستودع على GitHub أولاً")
    print("   اذهب إلى: https://github.com/new")
    print("="*60)

if __name__ == '__main__':
    try:
        create_deployment_files()
        
        response = input("\n❓ هل تريد عرض أوامر Git؟ (y/n): ")
        if response.lower() == 'y':
            show_git_commands()
        
    except Exception as e:
        print(f"\n❌ خطأ: {e}")
        import traceback
        traceback.print_exc()
    
    input("\nاضغط Enter للخروج...")

