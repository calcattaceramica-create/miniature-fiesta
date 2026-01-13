# 📋 جميع الأوامر - All Commands Reference

## 🚀 DED Control Panel - دليل الأوامر الكامل

---

## 📌 1. إضافة اختصارات سطح المكتب - Add Desktop Shortcuts

### الطريقة 1: ملف BAT (الأسهل)
```bash
ADD_TO_DESKTOP.bat
```
**ماذا يفعل:**
- ينشئ اختصارين على سطح المكتب:
  - `DED Control Panel.lnk` - قائمة الأوامر الكاملة
  - `DED Panel (Direct).lnk` - تشغيل مباشر للوحة التحكم

### الطريقة 2: ملف PowerShell
```bash
powershell -ExecutionPolicy Bypass -File Create_Shortcut.ps1
```

### الطريقة 3: ملف التثبيت
```bash
Install_Desktop_Shortcut.bat
```

---

## 🎯 2. تشغيل لوحة التحكم - Launch Control Panel

### الطريقة 1: القائمة الكاملة (موصى بها)
```bash
DED_Control_Panel_Launcher.bat
```
**الميزات:**
- قائمة تفاعلية بجميع الأوامر
- 9 خيارات مختلفة
- واجهة ملونة وسهلة

### الطريقة 2: التشغيل المباشر
```bash
python DED_Control_Panel.pyw
```
أو
```bash
pythonw DED_Control_Panel.pyw
```

### الطريقة 3: ملف BAT القديم
```bash
run_control_panel.bat
```

---

## 🧪 3. إنشاء تراخيص تجريبية - Create Test Licenses

### تشغيل سكريبت الاختبار
```bash
python test_license_ui.py
```

**ماذا ينشئ:**
- 4 تراخيص تجريبية في `licenses_test.json`:
  - ✅ ترخيص نشط (100 يوم)
  - ⏸️ ترخيص معلق (50 يوم)
  - ❌ ترخيص منتهي (-10 يوم)
  - ⚠️ ترخيص قريب الانتهاء (5 أيام)

### نسخ التراخيص التجريبية للملف الفعلي
```bash
copy licenses_test.json licenses.json
```

---

## 📊 4. عرض الإحصائيات - Show Statistics

### من القائمة الرئيسية
```bash
DED_Control_Panel_Launcher.bat
# ثم اختر: 3
```

### مباشرة من Python
```bash
python -c "import json; data=json.load(open('licenses.json')); print(f'Total: {len(data)}')"
```

---

## 📁 5. إدارة الملفات - File Management

### فتح مجلد المشروع
```bash
explorer .
```
أو من القائمة:
```bash
DED_Control_Panel_Launcher.bat
# ثم اختر: 4
```

### عرض جميع ملفات المشروع
```bash
dir /b
```

---

## 📝 6. عرض التوثيق - View Documentation

### من القائمة الرئيسية
```bash
DED_Control_Panel_Launcher.bat
# ثم اختر: 5
```

### فتح ملف معين
```bash
notepad QUICK_START_GUIDE.md
notepad LICENSE_UI_FEATURES.md
notepad VERSION_2.0_CHANGELOG.md
notepad DELIVERY_SUMMARY.md
notepad UI_LAYOUT.txt
notepad ALL_COMMANDS.md
```

---

## 🌐 7. فتح معاينة HTML - Open HTML Preview

### من القائمة
```bash
DED_Control_Panel_Launcher.bat
# ثم اختر: 6
```

### مباشرة
```bash
start demo_preview.html
```

---

## 🔄 8. تحديث قاعدة البيانات - Update Database

### نسخ من ملف الاختبار
```bash
copy /y licenses_test.json licenses.json
```

### من القائمة
```bash
DED_Control_Panel_Launcher.bat
# ثم اختر: 7
```

---

## 🧹 9. تنظيف الملفات المؤقتة - Clean Temp Files

### من القائمة
```bash
DED_Control_Panel_Launcher.bat
# ثم اختر: 8
```

### يدوياً
```bash
rd /s /q __pycache__
del /q *.pyc
```

---

## ℹ️ 10. معلومات النظام - System Information

### من القائمة
```bash
DED_Control_Panel_Launcher.bat
# ثم اختر: 9
```

### التحقق من إصدار Python
```bash
python --version
```

### عرض معلومات المشروع
```bash
type VERSION_2.0_CHANGELOG.md
```

---

## 🎨 11. الميزات الجديدة - New Features

### أين تجدها؟
1. شغّل لوحة التحكم:
   ```bash
   python DED_Control_Panel.pyw
   ```

2. افتح تبويب **"📱 تشغيل التطبيق"**

3. انزل للأسفل - ستجد:
   - 📊 **4 بطاقات إحصائيات ملونة**
   - 📋 **قائمة آخر 5 تراخيص**
   - 🎯 **3 أزرار وصول سريع**

---

## 🔧 12. أوامر متقدمة - Advanced Commands

### تشغيل Python في الخلفية
```bash
pythonw DED_Control_Panel.pyw
```

### التحقق من وجود الملفات
```bash
if exist DED_Control_Panel.pyw echo File exists
```

### عرض محتوى ملف JSON
```bash
type licenses.json
```

### البحث في الملفات
```bash
findstr "active" licenses.json
```

---

## 📦 13. الملفات المتاحة - Available Files

### ملفات التشغيل
- `DED_Control_Panel.pyw` - الملف الرئيسي
- `DED_Control_Panel_Launcher.bat` - القائمة الكاملة
- `run_control_panel.bat` - تشغيل بسيط
- `ADD_TO_DESKTOP.bat` - إضافة للسطح المكتب

### ملفات الاختبار
- `test_license_ui.py` - سكريبت الاختبار
- `licenses_test.json` - تراخيص تجريبية

### ملفات البيانات
- `licenses.json` - قاعدة بيانات التراخيص

### ملفات التوثيق
- `QUICK_START_GUIDE.md` - دليل البدء السريع
- `LICENSE_UI_FEATURES.md` - توثيق الميزات
- `VERSION_2.0_CHANGELOG.md` - سجل التغييرات
- `DELIVERY_SUMMARY.md` - ملخص التسليم
- `UI_LAYOUT.txt` - تصميم الواجهة
- `ALL_COMMANDS.md` - هذا الملف

### ملفات المعاينة
- `demo_preview.html` - معاينة HTML

### ملفات التثبيت
- `Create_Shortcut.ps1` - PowerShell
- `Install_Desktop_Shortcut.bat` - BAT
- `Create_Desktop_Shortcut.vbs` - VBScript

---

## 🎯 14. سيناريوهات الاستخدام - Usage Scenarios

### السيناريو 1: أول مرة استخدام
```bash
# 1. إضافة اختصار لسطح المكتب
ADD_TO_DESKTOP.bat

# 2. إنشاء تراخيص تجريبية
python test_license_ui.py

# 3. نسخها للملف الفعلي
copy licenses_test.json licenses.json

# 4. تشغيل لوحة التحكم
python DED_Control_Panel.pyw
```

### السيناريو 2: استخدام يومي
```bash
# انقر مرتين على اختصار سطح المكتب
# أو
DED_Control_Panel_Launcher.bat
```

### السيناريو 3: اختبار الميزات
```bash
# 1. إنشاء تراخيص جديدة
python test_license_ui.py

# 2. فتح المعاينة
start demo_preview.html

# 3. تشغيل لوحة التحكم
python DED_Control_Panel.pyw
```

---

## 💡 15. نصائح وحيل - Tips & Tricks

### نصيحة 1: الوصول السريع
أضف مجلد المشروع إلى PATH:
```bash
set PATH=%PATH%;C:\Users\DELL\DED
```

### نصيحة 2: تشغيل تلقائي
أضف اختصار إلى مجلد Startup:
```bash
copy "DED Panel (Direct).lnk" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\"
```

### نصيحة 3: نسخ احتياطي
```bash
copy licenses.json licenses_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%.json
```

---

## 🆘 16. حل المشاكل - Troubleshooting

### المشكلة: لا تظهر لوحة التحكم
**الحل:**
```bash
# تحقق من Python
python --version

# شغّل بوضع debug
python DED_Control_Panel.pyw
```

### المشكلة: الإحصائيات لا تظهر
**الحل:**
```bash
# تحقق من وجود الملف
dir licenses.json

# أنشئ تراخيص تجريبية
python test_license_ui.py
copy licenses_test.json licenses.json
```

### المشكلة: الاختصار لا يعمل
**الحل:**
```bash
# أعد إنشاء الاختصار
ADD_TO_DESKTOP.bat
```

---

## 📞 17. الدعم - Support

### الملفات المرجعية
- `QUICK_START_GUIDE.md` - للمبتدئين
- `LICENSE_UI_FEATURES.md` - للميزات التفصيلية
- `ALL_COMMANDS.md` - لجميع الأوامر

### معلومات الإصدار
- **الإصدار:** 2.0.0
- **التاريخ:** 2026-01-12
- **المطور:** DED Team + Augment AI

---

## ✨ 18. الخلاصة - Summary

### الأوامر الأساسية (يجب حفظها)
```bash
# 1. إضافة لسطح المكتب
ADD_TO_DESKTOP.bat

# 2. القائمة الكاملة
DED_Control_Panel_Launcher.bat

# 3. تشغيل مباشر
python DED_Control_Panel.pyw

# 4. اختبار
python test_license_ui.py

# 5. معاينة
start demo_preview.html
```

---

**Made with ❤️ by DED Team**

