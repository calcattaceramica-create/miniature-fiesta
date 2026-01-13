# 🔐 نظام المصادقة والصلاحيات (Authentication & Authorization)

## نظرة عامة

نظام المصادقة والصلاحيات في نظام إدارة المخزون المتكامل يوفر:
- ✅ تسجيل الدخول والخروج
- ✅ إدارة المستخدمين
- ✅ نظام الأدوار (Roles)
- ✅ نظام الصلاحيات (Permissions)
- ✅ التحكم في الوصول (Access Control)

---

## 🔑 المصادقة (Authentication)

### تسجيل الدخول

```python
# في app/auth/routes.py
@bp.route('/login', methods=['GET', 'POST'])
def login():
    # التحقق من بيانات المستخدم
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        login_user(user, remember=remember)
        # تحديث آخر دخول
        user.last_login = datetime.utcnow()
        db.session.commit()
```

### تسجيل الخروج

```python
@bp.route('/logout')
def logout():
    logout_user()
    flash('تم تسجيل الخروج بنجاح', 'info')
    return redirect(url_for('auth.login'))
```

---

## 👥 إدارة المستخدمين

### إضافة مستخدم جديد

```python
user = User(
    username='john',
    email='john@example.com',
    full_name='John Doe',
    role_id=2,  # Manager role
    branch_id=1,
    is_active=True
)
user.set_password('password123')
db.session.add(user)
db.session.commit()
```

### تعديل مستخدم

```python
user = User.query.get(user_id)
user.full_name = 'New Name'
user.email = 'newemail@example.com'
user.role_id = 3
db.session.commit()
```

### حذف مستخدم

```python
user = User.query.get(user_id)
db.session.delete(user)
db.session.commit()
```

---

## 🎭 نظام الأدوار (Roles)

### الأدوار الافتراضية

1. **مدير النظام (Admin)**
   - صلاحيات كاملة على النظام
   - `is_admin = True`

2. **مدير (Manager)**
   - صلاحيات إدارية محدودة
   - يمكنه إنشاء وتعديل معظم البيانات

3. **مستخدم (User)**
   - صلاحيات أساسية
   - يمكنه عرض البيانات وإنشاء بعض المستندات

### إنشاء دور جديد

```python
role = Role(
    name='sales_manager',
    name_ar='مدير المبيعات',
    description='Sales department manager'
)
db.session.add(role)
db.session.commit()
```

---

## 🔐 نظام الصلاحيات (Permissions)

### الصلاحيات المتوفرة

#### المخزون (Inventory)
- `inventory.view` - عرض المخزون
- `inventory.create` - إضافة منتجات
- `inventory.edit` - تعديل منتجات
- `inventory.delete` - حذف منتجات

#### المبيعات (Sales)
- `sales.view` - عرض المبيعات
- `sales.create` - إنشاء فواتير بيع
- `sales.edit` - تعديل فواتير بيع
- `sales.delete` - حذف فواتير بيع

#### المشتريات (Purchases)
- `purchases.view` - عرض المشتريات
- `purchases.create` - إنشاء فواتير شراء
- `purchases.edit` - تعديل فواتير شراء
- `purchases.delete` - حذف فواتير شراء

#### المحاسبة (Accounting)
- `accounting.view` - عرض الحسابات
- `accounting.create` - إنشاء قيود
- `accounting.edit` - تعديل قيود
- `accounting.delete` - حذف قيود

#### الموارد البشرية (HR)
- `hr.view` - عرض الموظفين
- `hr.create` - إضافة موظفين
- `hr.edit` - تعديل موظفين
- `hr.delete` - حذف موظفين

#### نقاط البيع (POS)
- `pos.view` - عرض نقاط البيع
- `pos.create` - إنشاء طلبات POS

#### التقارير (Reports)
- `reports.view` - عرض التقارير
- `reports.export` - تصدير التقارير

#### الإعدادات (Settings)
- `settings.view` - عرض الإعدادات
- `settings.edit` - تعديل الإعدادات
- `settings.users` - إدارة المستخدمين
- `settings.roles` - إدارة الأدوار

---

## 🛡️ استخدام Decorators

### التحقق من تسجيل الدخول

```python
from flask_login import login_required

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
```

### التحقق من صلاحية المدير

```python
from app.auth.decorators import admin_required

@bp.route('/admin/settings')
@login_required
@admin_required
def admin_settings():
    return render_template('admin/settings.html')
```

### التحقق من صلاحية محددة

```python
from app.auth.decorators import permission_required

@bp.route('/inventory/create')
@login_required
@permission_required('inventory.create')
def create_product():
    return render_template('inventory/create.html')
```

---

## 📋 أمثلة عملية

### مثال 1: إنشاء مستخدم مع صلاحيات

```python
# إنشاء دور جديد
sales_role = Role(
    name='sales_rep',
    name_ar='مندوب مبيعات',
    description='Sales representative'
)
db.session.add(sales_role)
db.session.flush()

# إضافة صلاحيات للدور
permissions = Permission.query.filter(
    Permission.name.in_([
        'sales.view',
        'sales.create',
        'inventory.view',
        'pos.view',
        'pos.create'
    ])
).all()

sales_role.permissions = permissions
db.session.commit()

# إنشاء مستخدم بهذا الدور
user = User(
    username='sales1',
    email='sales1@company.com',
    full_name='Sales Representative 1',
    role_id=sales_role.id,
    branch_id=1
)
user.set_password('password123')
db.session.add(user)
db.session.commit()
```

### مثال 2: التحقق من الصلاحيات في Template

```html
{% if current_user.has_permission('inventory.create') %}
<a href="{{ url_for('inventory.create') }}" class="btn btn-primary">
    <i class="fas fa-plus"></i> إضافة منتج
</a>
{% endif %}
```

### مثال 3: التحقق من الصلاحيات في Python

```python
if current_user.has_permission('sales.delete'):
    # حذف الفاتورة
    db.session.delete(invoice)
    db.session.commit()
    flash('تم حذف الفاتورة بنجاح', 'success')
else:
    flash('ليس لديك صلاحية لحذف الفواتير', 'error')
```

---

## 🔒 أفضل الممارسات

### 1. استخدام كلمات مرور قوية

```python
# في app/models/user.py
def set_password(self, password):
    # استخدام werkzeug.security لتشفير كلمة المرور
    self.password_hash = generate_password_hash(password)
```

### 2. تحديث آخر دخول

```python
# عند تسجيل الدخول
user.last_login = datetime.utcnow()
db.session.commit()
```

### 3. التحقق من نشاط المستخدم

```python
if not user.is_active:
    flash('حسابك غير نشط. يرجى الاتصال بالمدير', 'error')
    return redirect(url_for('auth.login'))
```

### 4. استخدام HTTPS في الإنتاج

```python
# في config.py
class ProductionConfig(Config):
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
```

---

## 📊 جداول قاعدة البيانات

### جدول المستخدمين (users)

| العمود | النوع | الوصف |
|--------|------|-------|
| id | Integer | المعرف الفريد |
| username | String(80) | اسم المستخدم |
| email | String(120) | البريد الإلكتروني |
| password_hash | String(255) | كلمة المرور المشفرة |
| full_name | String(120) | الاسم الكامل |
| phone | String(20) | رقم الهاتف |
| is_active | Boolean | نشط/غير نشط |
| is_admin | Boolean | مدير نظام |
| role_id | Integer | معرف الدور |
| branch_id | Integer | معرف الفرع |
| last_login | DateTime | آخر دخول |

### جدول الأدوار (roles)

| العمود | النوع | الوصف |
|--------|------|-------|
| id | Integer | المعرف الفريد |
| name | String(50) | اسم الدور |
| name_ar | String(50) | الاسم بالعربية |
| description | Text | الوصف |

### جدول الصلاحيات (permissions)

| العمود | النوع | الوصف |
|--------|------|-------|
| id | Integer | المعرف الفريد |
| name | String(100) | اسم الصلاحية |
| name_ar | String(100) | الاسم بالعربية |
| module | String(50) | الوحدة |

### جدول ربط الأدوار بالصلاحيات (role_permissions)

| العمود | النوع | الوصف |
|--------|------|-------|
| role_id | Integer | معرف الدور |
| permission_id | Integer | معرف الصلاحية |

---

## 🚀 الخطوات التالية

1. ✅ إضافة نظام تسجيل الأنشطة (Audit Log)
2. ✅ إضافة نظام إعادة تعيين كلمة المرور
3. ✅ إضافة نظام المصادقة الثنائية (2FA)
4. ✅ إضافة نظام الجلسات المتعددة
5. ✅ إضافة نظام تتبع محاولات تسجيل الدخول الفاشلة

---

## 📝 ملاحظات

- جميع كلمات المرور مشفرة باستخدام `werkzeug.security`
- يتم التحقق من الصلاحيات على مستوى الدور (Role-based)
- يمكن للمدير النظام (`is_admin=True`) الوصول لجميع الصفحات
- يتم تسجيل آخر دخول للمستخدم تلقائياً
- يمكن تعطيل المستخدم بدلاً من حذفه (`is_active=False`)

---

**تم التحديث:** 2026-01-10
**الإصدار:** 1.0.0

