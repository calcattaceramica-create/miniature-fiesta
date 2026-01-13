# 💰 دليل نظام إدارة المبيعات - Sales Management System

## 📋 نظرة عامة

نظام إدارة المبيعات هو نظام متكامل لإدارة جميع عمليات البيع في الشركة، من إدارة العملاء إلى إصدار الفواتير وتتبع المدفوعات.

**التاريخ:** 2026-01-10  
**الإصدار:** 1.0.0  
**الحالة:** ✅ مكتمل وجاهز للاستخدام

---

## 🎯 المميزات الرئيسية

### ✨ إدارة العملاء
- ✅ إضافة وتعديل وحذف العملاء
- ✅ تصنيف العملاء (VIP، عادي، جملة)
- ✅ تتبع رصيد العميل
- ✅ حد الائتمان وشروط الدفع
- ✅ معلومات الاتصال الكاملة

### 📄 إدارة الفواتير
- ✅ إنشاء فواتير مبيعات جديدة
- ✅ إضافة منتجات متعددة للفاتورة
- ✅ حساب الضرائب والخصومات تلقائياً
- ✅ تأكيد الفاتورة وخصم المخزون
- ✅ إلغاء الفاتورة واسترجاع المخزون
- ✅ تتبع حالة الدفع

### 📊 التقارير والإحصائيات
- ✅ تقارير المبيعات التفصيلية
- ✅ تتبع المدفوعات
- ✅ رصيد العملاء
- ✅ حالة الفواتير

---

## 🗂️ هيكل النظام

### 📁 الملفات الرئيسية

```
app/
├── models_sales.py              # نماذج قاعدة البيانات
├── sales/
│   ├── __init__.py
│   └── routes.py                # مسارات المبيعات
└── templates/sales/
    ├── customers.html           # قائمة العملاء
    ├── add_customer.html        # إضافة عميل
    ├── invoices.html            # قائمة الفواتير
    ├── add_invoice.html         # إضافة فاتورة
    └── invoice_details.html     # تفاصيل الفاتورة
```

---

## 💾 قاعدة البيانات

### 1. جدول العملاء (customers)

<augment_code_snippet path="app/models_sales.py" mode="EXCERPT">
```python
class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False, index=True)
    name_en = db.Column(db.String(128))
    
    # Contact Info
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    address = db.Column(db.Text)
    city = db.Column(db.String(64))
    country = db.Column(db.String(64))
    
    # Business Info
    tax_number = db.Column(db.String(64))
    customer_type = db.Column(db.String(20), default='individual')
    
    # Financial
    credit_limit = db.Column(db.Float, default=0.0)
    current_balance = db.Column(db.Float, default=0.0)
    payment_terms = db.Column(db.Integer, default=0)
    
    # Classification
    category = db.Column(db.String(64))
    rating = db.Column(db.Integer, default=0)
    
    is_active = db.Column(db.Boolean, default=True)
```
</augment_code_snippet>

**الحقول الرئيسية:**
- `code`: كود العميل الفريد (مثل: CUS00001)
- `name`: اسم العميل بالعربية
- `customer_type`: نوع العميل (individual/company)
- `credit_limit`: حد الائتمان المسموح
- `current_balance`: الرصيد الحالي (المديونية)
- `payment_terms`: شروط الدفع بالأيام
- `category`: تصنيف العميل (VIP، عادي، جملة)

### 2. جدول فواتير المبيعات (sales_invoices)

<augment_code_snippet path="app/models_sales.py" mode="EXCERPT">
```python
class SalesInvoice(db.Model):
    __tablename__ = 'sales_invoices'
    
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(64), unique=True, nullable=False)
    invoice_date = db.Column(db.Date, nullable=False)
    
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'))
    
    # Amounts
    subtotal = db.Column(db.Float, default=0.0)
    discount_amount = db.Column(db.Float, default=0.0)
    tax_amount = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, default=0.0)
    paid_amount = db.Column(db.Float, default=0.0)
    remaining_amount = db.Column(db.Float, default=0.0)
    
    # Status
    status = db.Column(db.String(20), default='draft')
    payment_status = db.Column(db.String(20), default='unpaid')
```
</augment_code_snippet>

**الحقول الرئيسية:**
- `invoice_number`: رقم الفاتورة (مثل: INV202601001)
- `status`: حالة الفاتورة (draft/confirmed/paid/cancelled)
- `payment_status`: حالة الدفع (unpaid/partial/paid)
- `subtotal`: الإجمالي قبل الضريبة
- `tax_amount`: قيمة الضريبة
- `total_amount`: الإجمالي النهائي
- `remaining_amount`: المبلغ المتبقي

### 3. جدول بنود الفاتورة (sales_invoice_items)

<augment_code_snippet path="app/models_sales.py" mode="EXCERPT">
```python
class SalesInvoiceItem(db.Model):
    __tablename__ = 'sales_invoice_items'
    
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('sales_invoices.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    
    quantity = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    discount_percentage = db.Column(db.Float, default=0.0)
    discount_amount = db.Column(db.Float, default=0.0)
    tax_rate = db.Column(db.Float, default=15.0)
    tax_amount = db.Column(db.Float, default=0.0)
    total = db.Column(db.Float, default=0.0)
```
</augment_code_snippet>

---

## 🛣️ المسارات (Routes)

### 1. إدارة العملاء

#### عرض جميع العملاء
```
GET /sales/customers
```

#### إضافة عميل جديد
```
GET/POST /sales/customers/add
```

### 2. إدارة الفواتير

#### عرض جميع الفواتير
```
GET /sales/invoices
```

#### إضافة فاتورة جديدة
```
GET/POST /sales/invoices/add
```

#### عرض تفاصيل الفاتورة
```
GET /sales/invoices/<id>
```

#### تأكيد الفاتورة
```
GET/POST /sales/invoices/<id>/confirm
```

#### حذف الفاتورة
```
GET/POST /sales/invoices/<id>/delete
```

#### إلغاء الفاتورة
```
GET/POST /sales/invoices/<id>/cancel
```

---

## 💻 أمثلة برمجية

### 1. إنشاء عميل جديد

```python
from app.models_sales import Customer
from app import db

# إنشاء عميل
customer = Customer(
    code='CUS00001',
    name='أحمد محمد',
    name_en='Ahmed Mohammed',
    email='ahmed@example.com',
    phone='+966 50 123 4567',
    customer_type='individual',
    credit_limit=10000.00,
    payment_terms=30,
    category='VIP',
    is_active=True
)

db.session.add(customer)
db.session.commit()
```

### 2. إنشاء فاتورة مبيعات

```python
from app.models_sales import SalesInvoice, SalesInvoiceItem
from datetime import datetime

# إنشاء الفاتورة
invoice = SalesInvoice(
    invoice_number='INV202601001',
    invoice_date=datetime.now().date(),
    customer_id=1,
    warehouse_id=1,
    status='draft',
    user_id=current_user.id
)

db.session.add(invoice)
db.session.flush()  # للحصول على ID الفاتورة

# إضافة بنود الفاتورة
item = SalesInvoiceItem(
    invoice_id=invoice.id,
    product_id=1,
    quantity=2,
    unit_price=1000.00,
    discount_percentage=5,
    tax_rate=15
)

# حساب المبالغ
line_total = item.quantity * item.unit_price
item.discount_amount = line_total * (item.discount_percentage / 100)
subtotal = line_total - item.discount_amount
item.tax_amount = subtotal * (item.tax_rate / 100)
item.total = subtotal + item.tax_amount

db.session.add(item)

# تحديث إجماليات الفاتورة
invoice.subtotal = subtotal
invoice.tax_amount = item.tax_amount
invoice.total_amount = item.total
invoice.remaining_amount = invoice.total_amount

db.session.commit()
```

### 3. تأكيد الفاتورة وخصم المخزون

```python
from app.models_inventory import Stock, StockMovement

# تحديث حالة الفاتورة
invoice.status = 'confirmed'

# خصم المخزون لكل منتج
for item in invoice.items:
    # الحصول على المخزون
    stock = Stock.query.filter_by(
        product_id=item.product_id,
        warehouse_id=invoice.warehouse_id
    ).first()
    
    # التحقق من الكمية المتاحة
    if stock.quantity < item.quantity:
        raise ValueError(f'الكمية المتاحة غير كافية')
    
    # خصم الكمية
    stock.quantity -= item.quantity
    
    # تسجيل الحركة
    movement = StockMovement(
        product_id=item.product_id,
        warehouse_id=invoice.warehouse_id,
        movement_type='out',
        quantity=item.quantity,
        reference_type='sales_invoice',
        reference_id=invoice.id,
        notes=f'بيع - فاتورة رقم {invoice.invoice_number}'
    )
    db.session.add(movement)

# تحديث رصيد العميل
invoice.customer.current_balance += invoice.total_amount

db.session.commit()
```

### 4. إلغاء الفاتورة واسترجاع المخزون

```python
# إرجاع المخزون
for item in invoice.items:
    stock = Stock.query.filter_by(
        product_id=item.product_id,
        warehouse_id=invoice.warehouse_id
    ).first()
    
    stock.quantity += item.quantity
    
    # تسجيل الحركة
    movement = StockMovement(
        product_id=item.product_id,
        warehouse_id=invoice.warehouse_id,
        movement_type='in',
        quantity=item.quantity,
        reference_type='sales_invoice_cancel',
        reference_id=invoice.id,
        notes=f'إلغاء بيع - فاتورة رقم {invoice.invoice_number}'
    )
    db.session.add(movement)

# تحديث رصيد العميل
invoice.customer.current_balance -= invoice.total_amount

# تحديث حالة الفاتورة
invoice.status = 'cancelled'
invoice.payment_status = 'unpaid'

db.session.commit()
```

---

## 🔒 الأمان والتحققات

### 1. التحقق من الكمية المتاحة
```python
if stock.quantity < item.quantity:
    flash(f'الكمية المتاحة من {item.product.name} غير كافية', 'error')
    return redirect(url_for('sales.invoice_details', id=id))
```

### 2. منع حذف فاتورة مؤكدة
```python
if invoice.status != 'draft':
    flash('لا يمكن حذف فاتورة مؤكدة', 'error')
    return redirect(url_for('sales.invoice_details', id=id))
```

### 3. استخدام Transactions
```python
try:
    # العمليات
    db.session.commit()
except Exception as e:
    db.session.rollback()
    flash(f'حدث خطأ: {str(e)}', 'error')
```

---

## 📊 حالات الفاتورة

### حالة الفاتورة (status)
- **draft**: مسودة - يمكن التعديل والحذف
- **confirmed**: مؤكدة - تم خصم المخزون
- **paid**: مدفوعة - تم الدفع بالكامل
- **cancelled**: ملغاة - تم إلغاء الفاتورة

### حالة الدفع (payment_status)
- **unpaid**: غير مدفوعة
- **partial**: مدفوعة جزئياً
- **paid**: مدفوعة بالكامل

---

## 🎨 الواجهات

### 1. قائمة الفواتير (invoices.html)
- عرض جميع الفواتير في جدول
- فلترة حسب الحالة
- بحث برقم الفاتورة
- أزرار الإجراءات (عرض، تأكيد، حذف، طباعة)

### 2. إضافة فاتورة (add_invoice.html)
- نموذج إدخال بيانات الفاتورة
- إضافة منتجات ديناميكياً
- حساب الإجماليات تلقائياً
- JavaScript للتفاعل

### 3. تفاصيل الفاتورة (invoice_details.html)
- عرض معلومات الفاتورة الكاملة
- جدول المنتجات
- الإجماليات والمدفوعات
- أزرار الإجراءات

---

## 🚀 الاستخدام

### للمستخدمين:
```
القائمة → المبيعات → فواتير المبيعات
```

### للمطورين:
راجع الأمثلة البرمجية أعلاه

---

**آخر تحديث:** 2026-01-10  
**الإصدار:** 1.0.0

