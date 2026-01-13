# 🏭 نظام إدارة المستودعات (Warehouse Management System)

## نظرة عامة

نظام إدارة المستودعات في نظام إدارة المخزون المتكامل يوفر:
- ✅ إدارة المستودعات المتعددة
- ✅ تتبع المخزون لكل مستودع
- ✅ نقل المخزون بين المستودعات
- ✅ تقارير المخزون حسب المستودع
- ✅ إدارة مديري المستودعات
- ✅ ربط المستودعات بالفروع

---

## 📋 المميزات الرئيسية

### 1. إدارة المستودعات

#### إضافة مستودع جديد
```python
from app.models import Warehouse

warehouse = Warehouse(
    name='المستودع الرئيسي',
    name_en='Main Warehouse',
    code='WH-001',
    branch_id=1,
    address='الرياض، المملكة العربية السعودية',
    manager_id=2,
    is_active=True
)

db.session.add(warehouse)
db.session.commit()
```

#### تعديل مستودع
```python
warehouse = Warehouse.query.get(1)
warehouse.name = 'المستودع المركزي'
warehouse.address = 'عنوان جديد'
db.session.commit()
```

#### حذف مستودع
```python
warehouse = Warehouse.query.get(1)

# التحقق من عدم وجود مخزون
if not warehouse.stocks:
    db.session.delete(warehouse)
    db.session.commit()
else:
    print("لا يمكن حذف المستودع لأنه يحتوي على مخزون")
```

---

### 2. تتبع المخزون

#### عرض مخزون مستودع معين
```python
from app.models import Stock, Product

# الحصول على جميع المنتجات في مستودع
stocks = Stock.query.filter_by(warehouse_id=1).join(Product).all()

for stock in stocks:
    print(f"{stock.product.name}: {stock.quantity}")
```

#### الحصول على إحصائيات المستودع
```python
warehouse = Warehouse.query.get(1)

# عدد المنتجات
total_products = len(warehouse.stocks)

# القيمة الإجمالية
total_value = sum(
    stock.quantity * stock.product.cost_price 
    for stock in warehouse.stocks
)

# المنتجات المنخفضة
low_stock = sum(
    1 for stock in warehouse.stocks 
    if stock.quantity <= stock.product.min_stock_level
)
```

---

### 3. نقل المخزون بين المستودعات

#### نقل منتج من مستودع لآخر
```python
from app.models import Stock, StockMovement

# المعلومات الأساسية
product_id = 1
from_warehouse_id = 1
to_warehouse_id = 2
quantity = 10

# الحصول على المخزون المصدر
from_stock = Stock.query.filter_by(
    product_id=product_id,
    warehouse_id=from_warehouse_id
).first()

# التحقق من الكمية المتاحة
if from_stock.available_quantity >= quantity:
    # الحصول على أو إنشاء المخزون الوجهة
    to_stock = Stock.query.filter_by(
        product_id=product_id,
        warehouse_id=to_warehouse_id
    ).first()
    
    if not to_stock:
        to_stock = Stock(
            product_id=product_id,
            warehouse_id=to_warehouse_id,
            quantity=0,
            reserved_quantity=0,
            available_quantity=0
        )
        db.session.add(to_stock)
    
    # تحديث المخزون
    from_stock.quantity -= quantity
    from_stock.available_quantity -= quantity
    to_stock.quantity += quantity
    to_stock.available_quantity += quantity
    
    # تسجيل الحركات
    out_movement = StockMovement(
        product_id=product_id,
        warehouse_id=from_warehouse_id,
        movement_type='out',
        quantity=quantity,
        reference_type='transfer',
        notes='نقل إلى مستودع آخر',
        created_by=current_user.id
    )
    
    in_movement = StockMovement(
        product_id=product_id,
        warehouse_id=to_warehouse_id,
        movement_type='in',
        quantity=quantity,
        reference_type='transfer',
        notes='نقل من مستودع آخر',
        created_by=current_user.id
    )
    
    db.session.add(out_movement)
    db.session.add(in_movement)
    db.session.commit()
```

---

## 🎯 الواجهات (UI)

### صفحة إدارة المستودعات
**المسار:** `/inventory/warehouses`

**المميزات:**
- عرض جميع المستودعات في بطاقات
- إضافة مستودع جديد (Modal)
- تعديل مستودع (Modal)
- حذف مستودع (Modal مع تأكيد)
- عرض معلومات كل مستودع:
  - الكود
  - الاسم بالعربية والإنجليزية
  - الفرع
  - العنوان
  - المدير
  - الحالة (نشط/غير نشط)
  - عدد المنتجات

### صفحة تفاصيل المستودع
**المسار:** `/inventory/warehouses/<id>`

**المميزات:**
- إحصائيات المستودع:
  - إجمالي المنتجات
  - قيمة المخزون
  - المنتجات المنخفضة
  - الحالة
- معلومات المستودع الكاملة
- جدول المخزون في المستودع:
  - اسم المنتج
  - الكود
  - التصنيف
  - الكمية (إجمالي، محجوز، متاح)
  - سعر التكلفة
  - القيمة الإجمالية
  - الحالة (منخفض/جيد/مرتفع)

### صفحة نقل المخزون
**المسار:** `/inventory/transfer`

**المميزات:**
- اختيار المنتج
- اختيار المستودع المصدر
- عرض الكمية المتاحة تلقائياً
- اختيار المستودع الوجهة
- إدخال الكمية المراد نقلها
- ملاحظات
- عرض آخر عمليات النقل

---

## 📊 قاعدة البيانات

### جدول المستودعات (warehouses)

| العمود | النوع | الوصف |
|--------|------|-------|
| id | Integer | المعرف الفريد |
| name | String(128) | اسم المستودع |
| name_en | String(128) | الاسم بالإنجليزية |
| code | String(20) | كود المستودع (فريد) |
| branch_id | Integer | معرف الفرع |
| address | Text | العنوان |
| manager_id | Integer | معرف المدير |
| is_active | Boolean | نشط/غير نشط |
| created_at | DateTime | تاريخ الإنشاء |

### العلاقات (Relationships)

```python
# في نموذج Warehouse
branch = db.relationship('Branch', backref='warehouses')
stocks = db.relationship('Stock', backref='warehouse')

# في نموذج Stock
warehouse = db.relationship('Warehouse', backref='stocks')
```

---

## 🔄 حركات المخزون (Stock Movements)

### أنواع الحركات

1. **in** - دخول (استلام بضاعة)
2. **out** - خروج (بيع أو صرف)
3. **transfer** - نقل بين مستودعات
4. **adjustment** - تسوية جرد

### تسجيل حركة مخزون

```python
movement = StockMovement(
    product_id=1,
    warehouse_id=1,
    movement_type='in',
    quantity=100,
    reference_type='purchase_invoice',
    reference_id=5,
    notes='استلام بضاعة من المورد',
    created_by=current_user.id
)

db.session.add(movement)
db.session.commit()
```

---

## 📈 التقارير

### تقرير المخزون حسب المستودع

```python
def warehouse_stock_report(warehouse_id):
    stocks = Stock.query.filter_by(warehouse_id=warehouse_id).all()
    
    report_data = []
    for stock in stocks:
        report_data.append({
            'product': stock.product.name,
            'code': stock.product.code,
            'quantity': stock.quantity,
            'available': stock.available_quantity,
            'value': stock.quantity * stock.product.cost_price
        })
    
    return report_data
```

---

## 🚀 أفضل الممارسات

### 1. التحقق من الكمية قبل النقل

```python
if from_stock.available_quantity < quantity:
    flash('الكمية المتاحة غير كافية', 'danger')
    return redirect(url_for('inventory.stock_transfer'))
```

### 2. تسجيل جميع الحركات

```python
# دائماً سجل حركة المخزون عند أي تغيير
movement = StockMovement(...)
db.session.add(movement)
```

### 3. استخدام Transactions

```python
try:
    # عمليات قاعدة البيانات
    db.session.commit()
except Exception as e:
    db.session.rollback()
    flash(f'حدث خطأ: {str(e)}', 'danger')
```

### 4. التحقق من المستودع قبل الحذف

```python
if warehouse.stocks:
    flash('لا يمكن حذف المستودع لأنه يحتوي على مخزون', 'danger')
```

---

## 🔒 الصلاحيات المطلوبة

- `inventory.view` - عرض المستودعات
- `inventory.create` - إضافة مستودع
- `inventory.edit` - تعديل مستودع
- `inventory.delete` - حذف مستودع

---

**تم التحديث:** 2026-01-10
**الإصدار:** 1.0.0

