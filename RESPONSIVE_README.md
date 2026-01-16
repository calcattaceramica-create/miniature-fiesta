# 📱 دليل التصميم المتجاوب - نظام DED ERP

## 📖 المحتويات
1. [نظرة عامة](#نظرة-عامة)
2. [الملفات المضافة](#الملفات-المضافة)
3. [كيفية الاستخدام](#كيفية-الاستخدام)
4. [الأنماط المتاحة](#الأنماط-المتاحة)
5. [أمثلة عملية](#أمثلة-عملية)
6. [الاختبار](#الاختبار)

---

## 🎯 نظرة عامة

تم تطبيق **التصميم المتجاوب (Responsive Design)** على جميع صفحات نظام DED ERP لضمان تجربة مستخدم مثالية على جميع الأجهزة.

### ✅ الأجهزة المدعومة:
- 📱 **الهواتف الذكية** (320px - 767px)
- 📱 **الأجهزة اللوحية** (768px - 991px)
- 💻 **الحواسيب** (992px وأكثر)

---

## 📁 الملفات المضافة

### 1. ملف CSS الرئيسي
```
app/static/css/responsive.css
```
- **الحجم:** 526 سطر
- **الوظيفة:** يحتوي على جميع أنماط التجاوب

### 2. ملفات التوثيق
```
RESPONSIVE_DESIGN_IMPLEMENTATION.md  # خطة التنفيذ
RESPONSIVE_DESIGN_COMPLETE.md        # التوثيق الكامل
RESPONSIVE_README.md                 # هذا الملف
test_responsive.html                 # صفحة اختبار
apply_responsive_design.py           # سكريبت التطبيق التلقائي
```

---

## 🚀 كيفية الاستخدام

### الخطوة 1: التأكد من تضمين ملف CSS

تأكد من أن ملف `responsive.css` مضمن في `base.html`:

```html
<!-- في قسم <head> -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/responsive.css') }}">
```

### الخطوة 2: استخدام الأنماط في الصفحات

#### مثال: Page Header متجاوب
```html
<div class="container-fluid">
    <div class="page-header mb-4">
        <div class="d-flex justify-content-between align-items-center flex-wrap">
            <div class="mb-2 mb-md-0">
                <h3><i class="fas fa-box"></i> {{ _('Products') }}</h3>
                <p class="text-muted mb-0">{{ _('Manage all products') }}</p>
            </div>
            <div class="action-buttons">
                <a href="#" class="btn btn-primary">
                    <i class="fas fa-plus"></i> 
                    <span class="d-none d-sm-inline">{{ _('Add Product') }}</span>
                </a>
            </div>
        </div>
    </div>
</div>
```

#### مثال: جدول متجاوب
```html
<div class="table-responsive">
    <table class="table table-hover mb-0">
        <thead>
            <tr>
                <th>{{ _('Product Name') }}</th>
                <th class="hide-on-mobile">{{ _('Code') }}</th>
                <th class="hide-on-mobile">{{ _('Category') }}</th>
                <th>{{ _('Price') }}</th>
                <th>{{ _('Actions') }}</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>
                    <strong>{{ product.name }}</strong>
                    <small class="text-muted show-on-mobile d-block">
                        {{ _('Code') }}: {{ product.code }} | 
                        {{ _('Category') }}: {{ product.category.name }}
                    </small>
                </td>
                <td class="hide-on-mobile">{{ product.code }}</td>
                <td class="hide-on-mobile">{{ product.category.name }}</td>
                <td><strong>{{ product.price }} {{ _('SAR') }}</strong></td>
                <td>
                    <div class="btn-group">
                        <a href="#" class="btn btn-sm btn-primary">
                            <i class="fas fa-edit"></i>
                        </a>
                    </div>
                </td>
            </tr>
        </tbody>
    </table>
</div>
```

#### مثال: نموذج متجاوب
```html
<form>
    <div class="row g-3">
        <div class="col-12 col-lg-6">
            <label class="form-label">{{ _('Product Name') }}</label>
            <input type="text" class="form-control" name="name">
        </div>
        <div class="col-12 col-lg-6">
            <label class="form-label">{{ _('Code') }}</label>
            <input type="text" class="form-control" name="code">
        </div>
    </div>
    
    <div class="d-flex justify-content-between flex-wrap gap-2 mt-4">
        <button type="button" class="btn btn-secondary">
            <i class="fas fa-times"></i> {{ _('Cancel') }}
        </button>
        <button type="submit" class="btn btn-primary">
            <i class="fas fa-save"></i> {{ _('Save') }}
        </button>
    </div>
</form>
```

---

## 🎨 الأنماط المتاحة

### 1. Utility Classes للإخفاء/الإظهار

```css
.hide-on-mobile      /* يخفي العنصر على الموبايل */
.show-on-mobile      /* يظهر العنصر فقط على الموبايل */
.hide-on-tablet      /* يخفي العنصر على التابلت */
.show-on-tablet      /* يظهر العنصر فقط على التابلت */
```

### 2. محاذاة النص

```css
.text-mobile-center  /* محاذاة للوسط على الموبايل */
.text-mobile-right   /* محاذاة لليمين على الموبايل */
.text-mobile-left    /* محاذاة لليسار على الموبايل */
```

### 3. المسافات

```css
.mb-mobile-2         /* margin-bottom على الموبايل */
.mb-mobile-3         /* margin-bottom أكبر على الموبايل */
.p-mobile-2          /* padding على الموبايل */
```

### 4. الأزرار

```css
.action-buttons      /* مجموعة أزرار متجاوبة */
.btn-group           /* مجموعة أزرار صغيرة */
```

---

## 📝 أمثلة عملية

### مثال 1: صفحة قائمة المنتجات
```html
{% extends "base.html" %}

{% block content %}
<div class="container-fluid">
    <!-- Page Header -->
    <div class="page-header mb-4">
        <div class="d-flex justify-content-between align-items-center flex-wrap">
            <div class="mb-2 mb-md-0">
                <h3><i class="fas fa-box"></i> {{ _('Products') }}</h3>
            </div>
            <div class="action-buttons">
                <a href="{{ url_for('inventory.add_product') }}" class="btn btn-primary">
                    <i class="fas fa-plus"></i> 
                    <span class="d-none d-sm-inline">{{ _('Add Product') }}</span>
                </a>
            </div>
        </div>
    </div>

    <!-- Filters -->
    <div class="card mb-3">
        <div class="card-body">
            <form method="GET">
                <div class="row g-2">
                    <div class="col-12 col-md-6">
                        <input type="text" class="form-control" name="search" 
                               placeholder="{{ _('Search...') }}">
                    </div>
                    <div class="col-12 col-md-4">
                        <select class="form-select" name="category">
                            <option value="">{{ _('All Categories') }}</option>
                        </select>
                    </div>
                    <div class="col-12 col-md-2">
                        <button class="btn btn-primary w-100" type="submit">
                            <i class="fas fa-search"></i> 
                            <span class="d-none d-sm-inline">{{ _('Search') }}</span>
                        </button>
                    </div>
                </div>
            </form>
        </div>
    </div>

    <!-- Table -->
    <div class="card">
        <div class="card-body p-0">
            <div class="table-responsive">
                <table class="table table-hover mb-0">
                    <!-- Table content here -->
                </table>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## 🧪 الاختبار

### 1. اختبار محلي
افتح ملف `test_responsive.html` في المتصفح:
```bash
# في المتصفح
file:///path/to/DED/test_responsive.html
```

### 2. اختبار على أجهزة حقيقية
- افتح النظام على هاتفك الذكي
- افتح النظام على جهاز لوحي
- قارن التجربة بين الأجهزة

### 3. اختبار في أدوات المطور
1. افتح Chrome DevTools (F12)
2. اضغط على أيقونة الجهاز المحمول (Ctrl+Shift+M)
3. جرب أحجام شاشات مختلفة

---

## 📊 نقاط التوقف (Breakpoints)

```css
/* Mobile (الهواتف الذكية) */
@media (max-width: 768px) {
    /* الأنماط هنا */
}

/* Tablet (الأجهزة اللوحية) */
@media (min-width: 769px) and (max-width: 992px) {
    /* الأنماط هنا */
}

/* Desktop (الحواسيب) */
@media (min-width: 993px) {
    /* الأنماط هنا */
}
```

---

## ✅ قائمة التحقق

عند إضافة صفحة جديدة، تأكد من:

- [ ] استخدام `container-fluid` للعرض الكامل
- [ ] إضافة `flex-wrap` للعناصر المتجاورة
- [ ] استخدام `col-12 col-md-*` للأعمدة
- [ ] إضافة `hide-on-mobile` للأعمدة الأقل أهمية
- [ ] استخدام `d-none d-sm-inline` لنصوص الأزرار
- [ ] إضافة `show-on-mobile` للمعلومات المدمجة
- [ ] استخدام `table-responsive` للجداول
- [ ] إضافة `g-2` أو `g-3` للمسافات بين الأعمدة

---

**تاريخ الإنشاء:** 2026-01-14  
**الإصدار:** 1.0  
**المطور:** DED Team

