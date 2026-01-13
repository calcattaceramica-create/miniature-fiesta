# دليل المطور - نظام المشتريات

## البنية التقنية

### 1. النماذج (Models)
الموجودة في `app/models.py`:

#### Supplier (المورد)
```python
- id: معرف فريد
- code: كود المورد (فريد)
- name: اسم المورد
- name_en: الاسم بالإنجليزية
- category: التصنيف
- email, phone, mobile: معلومات الاتصال
- address, city, country: العنوان
- tax_number: الرقم الضريبي
- commercial_register: السجل التجاري
- credit_limit: حد الائتمان
- payment_terms: شروط الدفع (أيام)
- current_balance: الرصيد الحالي
- is_active: نشط/غير نشط
- notes: ملاحظات
```

#### PurchaseInvoice (فاتورة الشراء)
```python
- id: معرف فريد
- invoice_number: رقم الفاتورة (فريد)
- invoice_date: تاريخ الفاتورة
- supplier_id: معرف المورد
- warehouse_id: معرف المستودع
- user_id: معرف المستخدم
- reference_number: رقم المرجع
- subtotal_amount: المجموع الفرعي
- discount_amount: الخصم
- tax_amount: الضريبة
- total_amount: الإجمالي
- paid_amount: المدفوع
- remaining_amount: المتبقي
- status: الحالة (draft, confirmed, paid, cancelled)
- payment_status: حالة الدفع (unpaid, partial, paid)
- notes: ملاحظات
```

#### PurchaseInvoiceItem (صنف الفاتورة)
```python
- id: معرف فريد
- invoice_id: معرف الفاتورة
- product_id: معرف المنتج
- quantity: الكمية
- unit_price: سعر الوحدة
- discount_percent: نسبة الخصم
- tax_percent: نسبة الضريبة
- total_price: الإجمالي
```

### 2. المسارات (Routes)
الموجودة في `app/purchases/routes.py`:

#### مسارات الموردين
```python
@bp.route('/suppliers')
- عرض قائمة الموردين
- البحث والترقيم
- GET فقط

@bp.route('/suppliers/add', methods=['GET', 'POST'])
- عرض نموذج إضافة مورد (GET)
- حفظ المورد الجديد (POST)
```

#### مسارات الفواتير
```python
@bp.route('/invoices')
- عرض قائمة الفواتير
- التصفية حسب الحالة
- GET فقط

@bp.route('/invoices/add', methods=['GET', 'POST'])
- عرض نموذج إضافة فاتورة (GET)
- حفظ الفاتورة الجديدة (POST)

@bp.route('/invoices/<int:id>')
- عرض تفاصيل الفاتورة
- GET فقط

@bp.route('/invoices/<int:id>/confirm', methods=['GET', 'POST'])
- عرض صفحة التأكيد (GET)
- تأكيد الفاتورة وإضافة المخزون (POST)

@bp.route('/invoices/<int:id>/cancel', methods=['GET', 'POST'])
- عرض صفحة الإلغاء (GET)
- إلغاء الفاتورة وخصم المخزون (POST)

@bp.route('/invoices/<int:id>/delete', methods=['GET', 'POST'])
- عرض صفحة الحذف (GET)
- حذف الفاتورة (POST) - مسودة فقط
```

### 3. العمليات الرئيسية

#### إضافة فاتورة شراء
```python
1. استقبال البيانات من النموذج
2. إنشاء كائن PurchaseInvoice
3. حساب المجاميع:
   - subtotal_amount
   - discount_amount
   - tax_amount
   - total_amount
4. إنشاء PurchaseInvoiceItem لكل صنف
5. حفظ في قاعدة البيانات
6. الحالة الافتراضية: draft
```

#### تأكيد الفاتورة
```python
1. التحقق من أن الحالة = draft
2. تحديث حالة الفاتورة إلى confirmed
3. لكل صنف في الفاتورة:
   a. البحث عن Stock أو إنشاء جديد
   b. إضافة الكمية
   c. إنشاء StockMovement (نوع: in)
4. تحديث رصيد المورد:
   supplier.current_balance += total_amount
5. حفظ التغييرات
```

#### إلغاء الفاتورة
```python
1. التحقق من أن الحالة = confirmed
2. تحديث حالة الفاتورة إلى cancelled
3. لكل صنف في الفاتورة:
   a. البحث عن Stock
   b. خصم الكمية
   c. إنشاء StockMovement (نوع: out)
4. تحديث رصيد المورد:
   supplier.current_balance -= total_amount
5. حفظ التغييرات
```

### 4. الحسابات

#### حساب سعر الصنف
```python
def calculate_item_total(quantity, unit_price, discount_percent, tax_percent):
    subtotal = quantity * unit_price
    discount = subtotal * (discount_percent / 100)
    after_discount = subtotal - discount
    tax = after_discount * (tax_percent / 100)
    total = after_discount + tax
    return total
```

#### حساب إجمالي الفاتورة
```python
def calculate_invoice_totals(items):
    subtotal = sum(item.quantity * item.unit_price for item in items)
    discount = sum(item.quantity * item.unit_price * item.discount_percent / 100 for item in items)
    after_discount = subtotal - discount
    tax = sum((item.quantity * item.unit_price * (1 - item.discount_percent/100)) * item.tax_percent / 100 for item in items)
    total = after_discount + tax
    return subtotal, discount, tax, total
```

## إضافة ميزات جديدة

### مثال: إضافة تعديل المورد

1. **إضافة المسار**:
```python
@bp.route('/suppliers/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    if request.method == 'POST':
        # تحديث البيانات
        supplier.name = request.form.get('name')
        # ... باقي الحقول
        db.session.commit()
        flash('تم تحديث بيانات المورد بنجاح', 'success')
        return redirect(url_for('purchases.suppliers'))
    return render_template('purchases/edit_supplier.html', supplier=supplier)
```

2. **إنشاء الواجهة**:
```html
<!-- app/templates/purchases/edit_supplier.html -->
{% extends "base.html" %}
{% block content %}
<!-- نموذج مشابه لـ add_supplier.html مع تعبئة البيانات -->
{% endblock %}
```

3. **تحديث القائمة**:
```html
<!-- في suppliers.html -->
<a href="{{ url_for('purchases.edit_supplier', id=supplier.id) }}" 
   class="btn btn-sm btn-warning">
    <i class="fas fa-edit"></i>
</a>
```

## الاختبار

### اختبار إضافة مورد
```python
def test_add_supplier():
    # تسجيل الدخول
    # الانتقال إلى /purchases/suppliers/add
    # ملء النموذج
    # إرسال POST
    # التحقق من الحفظ في قاعدة البيانات
```

### اختبار تأكيد الفاتورة
```python
def test_confirm_invoice():
    # إنشاء فاتورة مسودة
    # تأكيد الفاتورة
    # التحقق من:
    #   - تحديث حالة الفاتورة
    #   - إضافة الكميات للمخزون
    #   - تسجيل الحركات
    #   - تحديث رصيد المورد
```

## الأمان

### التحقق من الصلاحيات
```python
@login_required  # يتطلب تسجيل دخول
def protected_route():
    # يمكن إضافة فحص إضافي للصلاحيات
    if not current_user.has_permission('manage_purchases'):
        abort(403)
```

### التحقق من البيانات
```python
# التحقق من وجود السجل
invoice = PurchaseInvoice.query.get_or_404(id)

# التحقق من الحالة
if invoice.status != 'draft':
    flash('لا يمكن تأكيد هذه الفاتورة', 'error')
    return redirect(...)
```

## الأداء

### استعلامات محسّنة
```python
# استخدام eager loading
invoices = PurchaseInvoice.query\
    .options(db.joinedload('supplier'))\
    .options(db.joinedload('warehouse'))\
    .all()

# استخدام pagination
invoices = PurchaseInvoice.query.paginate(
    page=page, per_page=20, error_out=False
)
```

## التوثيق

عند إضافة ميزة جديدة:
1. أضف docstring للدالة
2. حدّث PURCHASES_DOCUMENTATION.md
3. أضف مثال في PURCHASES_README.md
4. اختبر الميزة جيداً

---

**للمزيد من المعلومات**:
- راجع `app/models.py` للنماذج
- راجع `app/purchases/routes.py` للمسارات
- راجع `PURCHASES_DOCUMENTATION.md` للتوثيق الكامل

