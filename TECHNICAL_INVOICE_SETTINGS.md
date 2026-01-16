# 🔧 التوثيق التقني لإعدادات الفواتير

## 📁 الملفات المعدّلة

### 1. **app/settings/routes.py**
```python
# التعديلات الرئيسية:
- إضافة import os و secure_filename
- تحسين معالجة رفع الشعار
- حفظ الملف في static/uploads/
- استخدام secure_filename لحماية أسماء الملفات
```

### 2. **app/templates/settings/company.html**
```html
<!-- التحسينات: -->
- إضافة badges "يظهر في الفواتير" للحقول المهمة
- إضافة أيقونات Font Awesome لكل حقل
- إضافة placeholders توضيحية
- إضافة قسم معاينة الفاتورة
- تحسين UX/UI
```

### 3. **app/templates/settings/index.html**
```html
<!-- التعديلات: -->
- إضافة بطاقة "إعدادات الفواتير" مع border-primary
- ربطها بصفحة بيانات الشركة
```

---

## 🗂️ هيكل المجلدات

```
DED/
├── app/
│   ├── static/
│   │   └── uploads/          # مجلد الشعارات (يُنشأ تلقائياً)
│   │       └── logo.png      # مثال
│   ├── templates/
│   │   └── settings/
│   │       ├── company.html  # صفحة إعدادات الشركة
│   │       └── index.html    # صفحة الإعدادات الرئيسية
│   └── settings/
│       └── routes.py         # معالجة رفع الشعار
└── INVOICE_SETTINGS_GUIDE.md # دليل المستخدم
```

---

## 🔐 الأمان

### معالجة رفع الملفات:
```python
from werkzeug.utils import secure_filename

# تأمين اسم الملف
filename = secure_filename(logo_file.filename)

# التحقق من نوع الملف
accept="image/png,image/jpeg,image/jpg,image/gif"

# إنشاء المجلد بشكل آمن
os.makedirs(upload_folder, exist_ok=True)
```

---

## 🎨 التصميم

### الألوان المستخدمة:
- **Primary (أزرق):** اسم الشركة، العنوان
- **Success (أخضر):** الرقم الضريبي
- **Warning (أصفر):** السجل التجاري
- **Info (سماوي):** الهاتف
- **Danger (أحمر):** البريد الإلكتروني

### الأيقونات:
```html
<i class="fas fa-building"></i>        <!-- اسم الشركة -->
<i class="fas fa-file-invoice"></i>    <!-- الرقم الضريبي -->
<i class="fas fa-certificate"></i>     <!-- السجل التجاري -->
<i class="fas fa-phone"></i>           <!-- الهاتف -->
<i class="fas fa-envelope"></i>        <!-- البريد -->
<i class="fas fa-map-marker-alt"></i>  <!-- العنوان -->
<i class="fas fa-image"></i>           <!-- الشعار -->
```

---

## 📊 قاعدة البيانات

### جدول Company:
```python
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    name_en = db.Column(db.String(200))
    tax_number = db.Column(db.String(50))
    commercial_register = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    logo = db.Column(db.String(200))  # اسم ملف الشعار
    currency = db.Column(db.String(10), default='SAR')
    tax_rate = db.Column(db.Float, default=15.0)
```

---

## 🔄 سير العمل (Workflow)

### 1. رفع الشعار:
```
المستخدم يختار الصورة
    ↓
POST /settings/company
    ↓
secure_filename() - تأمين الاسم
    ↓
إنشاء مجلد uploads/
    ↓
حفظ الملف
    ↓
تحديث company.logo في DB
    ↓
عرض رسالة نجاح
```

### 2. عرض الشعار في الفاتورة:
```
قراءة company.logo من DB
    ↓
بناء المسار: static/uploads/{logo}
    ↓
عرض الصورة في template
```

---

## 🧪 الاختبار

### اختبار رفع الشعار:
```python
# Test 1: رفع صورة صحيحة
- اختر صورة PNG
- تحقق من الحفظ في uploads/
- تحقق من تحديث DB

# Test 2: رفع صورة بحجم كبير
- اختر صورة > 5MB
- تحقق من رسالة الخطأ

# Test 3: رفع ملف غير صورة
- اختر ملف PDF
- تحقق من الرفض
```

---

## 🚀 التحسينات المستقبلية

### 1. **التحقق من حجم الملف:**
```python
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB

if logo_file.content_length > MAX_FILE_SIZE:
    flash('حجم الملف كبير جداً', 'error')
    return redirect(...)
```

### 2. **تغيير حجم الصورة تلقائياً:**
```python
from PIL import Image

img = Image.open(logo_file)
img.thumbnail((300, 100))
img.save(file_path)
```

### 3. **حذف الشعار القديم:**
```python
if company.logo and os.path.exists(old_logo_path):
    os.remove(old_logo_path)
```

### 4. **دعم QR Code:**
```python
import qrcode

# إنشاء QR Code للفاتورة
qr = qrcode.make(invoice_url)
qr.save('static/qr_codes/invoice_{id}.png')
```

---

## 📝 ملاحظات للمطورين

1. ✅ **استخدم secure_filename دائماً** عند رفع الملفات
2. ✅ **تحقق من نوع الملف** قبل الحفظ
3. ✅ **أنشئ المجلدات تلقائياً** باستخدام `os.makedirs(exist_ok=True)`
4. ✅ **احذف الملفات القديمة** عند رفع شعار جديد
5. ✅ **استخدم معالجة الأخطاء** (try-except)

---

## 🐛 معالجة الأخطاء

### مثال:
```python
try:
    logo_file.save(file_path)
    company.logo = filename
    db.session.commit()
    flash('تم رفع الشعار بنجاح', 'success')
except Exception as e:
    db.session.rollback()
    flash(f'خطأ في رفع الشعار: {str(e)}', 'error')
    app.logger.error(f'Logo upload error: {e}')
```

---

## 📚 المراجع

- [Flask File Uploads](https://flask.palletsprojects.com/en/2.3.x/patterns/fileuploads/)
- [Werkzeug secure_filename](https://werkzeug.palletsprojects.com/en/2.3.x/utils/#werkzeug.utils.secure_filename)
- [Bootstrap 5 Forms](https://getbootstrap.com/docs/5.0/forms/overview/)
- [Font Awesome Icons](https://fontawesome.com/icons)

---

**تم التوثيق بواسطة فريق تطوير DED ERP** 🚀

