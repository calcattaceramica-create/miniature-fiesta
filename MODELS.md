# 🏗️ توثيق النماذج (Models Documentation)

## نظرة عامة

النماذج (Models) هي تمثيل للجداول في قاعدة البيانات باستخدام SQLAlchemy ORM.

---

## 📁 هيكل الملفات

```
app/
├── models.py                  # النماذج الأساسية (Users, Roles, Company, etc.)
├── models_inventory.py        # نماذج المخزون
├── models_sales.py           # نماذج المبيعات
├── models_purchases.py       # نماذج المشتريات
├── models_accounting.py      # نماذج المحاسبة
├── models_hr.py              # نماذج الموارد البشرية
└── models_pos.py             # نماذج نقاط البيع
```

---

## 🔧 النماذج الأساسية (models.py)

### User - المستخدم

```python
from app.models import User

# إنشاء مستخدم جديد
user = User(
    username='john',
    email='john@example.com',
    full_name='John Doe',
    is_active=True
)
user.set_password('password123')
db.session.add(user)
db.session.commit()

# التحقق من كلمة المرور
if user.check_password('password123'):
    print('Password correct!')

# الحصول على مستخدم
user = User.query.filter_by(username='john').first()
user = User.query.get(1)  # By ID
```

**الخصائص:**
- `id` - المعرف الفريد
- `username` - اسم المستخدم (فريد)
- `email` - البريد الإلكتروني (فريد)
- `password_hash` - كلمة المرور المشفرة
- `full_name` - الاسم الكامل
- `is_active` - نشط/غير نشط
- `is_admin` - مدير/مستخدم عادي
- `branch_id` - الفرع
- `role_id` - الدور

**الدوال:**
- `set_password(password)` - تعيين كلمة المرور
- `check_password(password)` - التحقق من كلمة المرور

---

### Role - الدور

```python
from app.models import Role

# إنشاء دور جديد
role = Role(
    name='manager',
    name_ar='مدير',
    description='Manager role'
)
db.session.add(role)
db.session.commit()
```

---

### Company - الشركة

```python
from app.models import Company

company = Company(
    name='شركتي',
    name_en='My Company',
    tax_number='123456789',
    phone='+966 12 345 6789',
    email='info@company.com'
)
db.session.add(company)
db.session.commit()
```

---

## 📦 نماذج المخزون (models_inventory.py)

### Product - المنتج

```python
from app.models_inventory import Product

# إنشاء منتج جديد
product = Product(
    name='لابتوب HP',
    name_en='HP Laptop',
    code='PROD-001',
    barcode='1234567890123',
    category_id=1,
    unit_id=1,
    cost_price=2000.00,
    selling_price=2500.00,
    track_inventory=True,
    min_stock_level=5
)
db.session.add(product)
db.session.commit()

# البحث عن منتج
product = Product.query.filter_by(code='PROD-001').first()
product = Product.query.filter_by(barcode='1234567890123').first()

# الحصول على جميع المنتجات النشطة
products = Product.query.filter_by(is_active=True).all()

# البحث بالاسم
products = Product.query.filter(Product.name.like('%لابتوب%')).all()
```

**الخصائص المهمة:**
- `code` - كود المنتج (فريد)
- `barcode` - الباركود (فريد)
- `cost_price` - سعر التكلفة
- `selling_price` - سعر البيع
- `track_inventory` - تتبع المخزون
- `min_stock_level` - الحد الأدنى للمخزون

---

### Category - التصنيف

```python
from app.models_inventory import Category

# إنشاء تصنيف رئيسي
category = Category(
    name='إلكترونيات',
    name_en='Electronics',
    code='ELEC'
)
db.session.add(category)
db.session.commit()

# إنشاء تصنيف فرعي
subcategory = Category(
    name='حواسيب',
    name_en='Computers',
    code='COMP',
    parent_id=category.id
)
db.session.add(subcategory)
db.session.commit()

# الحصول على التصنيفات الفرعية
children = category.children
```

---

### Stock - المخزون

```python
from app.models_inventory import Stock

# الحصول على مخزون منتج في مستودع
stock = Stock.query.filter_by(
    product_id=1,
    warehouse_id=1
).first()

# الكمية المتاحة
available = stock.available_quantity

# تحديث المخزون
stock.quantity += 10
db.session.commit()
```

---

### StockMovement - حركة المخزون

```python
from app.models_inventory import StockMovement

# تسجيل حركة مخزون
movement = StockMovement(
    product_id=1,
    warehouse_id=1,
    movement_type='in',  # in, out, transfer, adjustment
    quantity=10,
    reference_type='purchase_invoice',
    reference_id=1,
    notes='استلام بضاعة',
    created_by=current_user.id
)
db.session.add(movement)
db.session.commit()
```

---

## 💰 نماذج المبيعات (models_sales.py)

### Customer - العميل

```python
from app.models_sales import Customer

# إنشاء عميل جديد
customer = Customer(
    code='CUST-001',
    name='أحمد محمد',
    phone='+966 50 123 4567',
    email='ahmed@example.com',
    customer_type='individual',
    credit_limit=10000.00
)
db.session.add(customer)
db.session.commit()

# البحث عن عميل
customer = Customer.query.filter_by(code='CUST-001').first()
customers = Customer.query.filter(Customer.name.like('%أحمد%')).all()
```

---

### SalesInvoice - فاتورة البيع

```python
from app.models_sales import SalesInvoice, SalesInvoiceItem

# إنشاء فاتورة بيع
invoice = SalesInvoice(
    invoice_number='INV-2024-001',
    invoice_date=datetime.now().date(),
    customer_id=1,
    warehouse_id=1,
    status='draft',
    created_by=current_user.id
)
db.session.add(invoice)
db.session.commit()

# إضافة منتجات للفاتورة
item = SalesInvoiceItem(
    invoice_id=invoice.id,
    product_id=1,
    quantity=2,
    unit_price=2500.00,
    discount_amount=100.00,
    tax_amount=72.00,
    total_amount=4972.00
)
db.session.add(item)
db.session.commit()

# حساب الإجماليات
invoice.calculate_totals()
db.session.commit()

# تأكيد الفاتورة
invoice.status = 'confirmed'
db.session.commit()
```

---

## 🛒 نماذج المشتريات (models_purchases.py)

### Supplier - المورد

```python
from app.models_purchases import Supplier

supplier = Supplier(
    code='SUPP-001',
    name='شركة التوريدات',
    phone='+966 11 234 5678',
    email='supplier@example.com',
    payment_terms=30  # 30 days
)
db.session.add(supplier)
db.session.commit()
```

---

### PurchaseInvoice - فاتورة الشراء

```python
from app.models_purchases import PurchaseInvoice, PurchaseInvoiceItem

# إنشاء فاتورة شراء
invoice = PurchaseInvoice(
    invoice_number='PINV-2024-001',
    invoice_date=datetime.now().date(),
    supplier_id=1,
    warehouse_id=1,
    status='draft',
    created_by=current_user.id
)
db.session.add(invoice)
db.session.commit()

# إضافة منتجات
item = PurchaseInvoiceItem(
    invoice_id=invoice.id,
    product_id=1,
    quantity=10,
    unit_price=2000.00,
    total_amount=20000.00
)
db.session.add(item)
db.session.commit()
```

---

## 💳 نماذج نقاط البيع (models_pos.py)

### POSSession - وردية نقطة البيع

```python
from app.models_pos import POSSession

# فتح وردية
session = POSSession(
    session_number='POS-2024-001',
    cashier_id=current_user.id,
    warehouse_id=1,
    opening_balance=1000.00,
    status='open'
)
db.session.add(session)
db.session.commit()

# إغلاق الوردية
session.closing_time = datetime.now()
session.closing_balance = 5000.00
session.status = 'closed'
db.session.commit()
```

---

### POSOrder - طلب نقطة البيع

```python
from app.models_pos import POSOrder, POSOrderItem

# إنشاء طلب
order = POSOrder(
    order_number='POS-ORD-001',
    session_id=session.id,
    payment_method='cash'
)
db.session.add(order)
db.session.commit()

# إضافة منتجات
item = POSOrderItem(
    order_id=order.id,
    product_id=1,
    quantity=1,
    unit_price=2500.00,
    total_amount=2500.00
)
db.session.add(item)
db.session.commit()
```

---

## 📊 نماذج المحاسبة (models_accounting.py)

### Account - الحساب

```python
from app.models_accounting import Account

# إنشاء حساب
account = Account(
    code='1110',
    name='النقدية',
    name_en='Cash',
    account_type='asset',
    is_system=True
)
db.session.add(account)
db.session.commit()
```

---

### JournalEntry - القيد اليومي

```python
from app.models_accounting import JournalEntry, JournalEntryLine

# إنشاء قيد
entry = JournalEntry(
    entry_number='JE-2024-001',
    entry_date=datetime.now().date(),
    entry_type='manual',
    description='قيد افتتاحي',
    created_by=current_user.id
)
db.session.add(entry)
db.session.commit()

# إضافة سطور القيد
# مدين
debit_line = JournalEntryLine(
    entry_id=entry.id,
    account_id=1,
    debit_amount=10000.00,
    credit_amount=0.00,
    description='رأس المال'
)
db.session.add(debit_line)

# دائن
credit_line = JournalEntryLine(
    entry_id=entry.id,
    account_id=2,
    debit_amount=0.00,
    credit_amount=10000.00,
    description='رأس المال'
)
db.session.add(credit_line)
db.session.commit()
```

---

## 🔍 استعلامات شائعة

### البحث والتصفية

```python
# البحث بالمعرف
product = Product.query.get(1)

# البحث بشرط
product = Product.query.filter_by(code='PROD-001').first()

# البحث بشروط متعددة
products = Product.query.filter_by(
    category_id=1,
    is_active=True
).all()

# البحث بـ LIKE
products = Product.query.filter(
    Product.name.like('%لابتوب%')
).all()

# الترتيب
products = Product.query.order_by(Product.name).all()

# التصفح (Pagination)
page = Product.query.paginate(page=1, per_page=20)
products = page.items
```

---

## ✅ أفضل الممارسات

1. **استخدم Transactions:**
```python
try:
    # عمليات متعددة
    db.session.add(obj1)
    db.session.add(obj2)
    db.session.commit()
except:
    db.session.rollback()
    raise
```

2. **تحقق من الوجود:**
```python
product = Product.query.filter_by(code='PROD-001').first()
if not product:
    # المنتج غير موجود
    pass
```

3. **استخدم Relationships:**
```python
# بدلاً من
category_id = product.category_id
category = Category.query.get(category_id)

# استخدم
category = product.category
```

---

**آخر تحديث:** 2026-01-10

