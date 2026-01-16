# 🧾 تكامل نقطة البيع مع فواتير المبيعات

## 📋 نظرة عامة

تم إضافة خاصية إنشاء فاتورة مبيعات تلقائياً عند إتمام البيع في نقطة البيع (POS). هذا يضمن:

- ✅ تسجيل جميع المبيعات في نظام الفواتير
- ✅ ربط كل طلب POS بفاتورة مبيعات
- ✅ تحديث المخزون تلقائياً
- ✅ تتبع المدفوعات والمبالغ المستحقة

## 🔄 آلية العمل

### 1. عند إتمام البيع في POS

عندما يتم إتمام عملية بيع في نقطة البيع، يحدث التالي تلقائياً:

```python
# 1. إنشاء طلب POS
order = POSOrder(...)
db.session.add(order)

# 2. إنشاء فاتورة مبيعات مرتبطة
invoice = SalesInvoice(
    invoice_number=_generate_invoice_number(),
    pos_order_id=order.id,  # ربط الفاتورة بطلب POS
    status='paid',  # الفاتورة مدفوعة بالكامل
    ...
)
db.session.add(invoice)

# 3. إضافة عناصر الفاتورة
for item in order_items:
    invoice_item = SalesInvoiceItem(...)
    db.session.add(invoice_item)

# 4. تحديث المخزون
stock.quantity -= item.quantity
```

### 2. البيانات المنقولة

تنتقل البيانات التالية من طلب POS إلى فاتورة المبيعات:

| حقل POS | حقل الفاتورة | ملاحظات |
|---------|--------------|---------|
| `order_number` | `notes` | يتم تضمينه في الملاحظات |
| `customer_id` | `customer_id` | نفس العميل |
| `session.warehouse_id` | `warehouse_id` | نفس المستودع |
| `subtotal` | `subtotal` | المجموع الفرعي |
| `discount_amount` | `discount_amount` | الخصم |
| `tax_amount` | `tax_amount` | الضريبة |
| `total_amount` | `total_amount` | المجموع الكلي |
| `total_amount` | `paid_amount` | مدفوع بالكامل |
| - | `remaining_amount` | 0.0 (لا يوجد متبقي) |

### 3. حالة الفاتورة

جميع فواتير POS تُنشأ بالحالات التالية:

- **status**: `paid` (مدفوعة)
- **payment_status**: `paid` (مدفوعة بالكامل)
- **remaining_amount**: `0.0` (لا يوجد متبقي)

## 🔗 الربط بين الأنظمة

### قاعدة البيانات

تم إضافة حقل `pos_order_id` إلى جدول `sales_invoices`:

```sql
ALTER TABLE sales_invoices 
ADD COLUMN pos_order_id INTEGER 
REFERENCES pos_orders(id);
```

### الاستعلامات

```python
# الحصول على فاتورة من طلب POS
order = POSOrder.query.get(order_id)
invoice = SalesInvoice.query.filter_by(pos_order_id=order.id).first()

# الحصول على طلب POS من فاتورة
invoice = SalesInvoice.query.get(invoice_id)
if invoice.pos_order_id:
    order = POSOrder.query.get(invoice.pos_order_id)
```

## 📊 ترقيم الفواتير

يتم توليد رقم الفاتورة تلقائياً بالصيغة:

```
INV{YEAR}{MONTH}{SEQUENCE}
```

مثال: `INV202601001` (يناير 2026، الفاتورة رقم 1)

## 🧪 الاختبار

### اختبار إنشاء فاتورة من POS

```python
# 1. افتح وردية POS
session = POSSession(...)

# 2. أنشئ طلب بيع
order_data = {
    'session_id': session.id,
    'customer_id': customer.id,
    'items': [...],
    'subtotal': 100.0,
    'tax_amount': 15.0,
    'total_amount': 115.0,
    ...
}

# 3. أرسل الطلب
response = client.post('/pos/complete-order', json=order_data)

# 4. تحقق من النتيجة
assert response.json['success'] == True
assert 'invoice_id' in response.json
assert 'invoice_number' in response.json

# 5. تحقق من الفاتورة
invoice = SalesInvoice.query.get(response.json['invoice_id'])
assert invoice.status == 'paid'
assert invoice.pos_order_id == order.id
```

## 📝 ملاحظات مهمة

1. **الفواتير التلقائية**: جميع مبيعات POS تُنشئ فواتير تلقائياً
2. **لا يمكن التعديل**: فواتير POS مدفوعة ولا يمكن تعديلها
3. **المخزون**: يتم تحديث المخزون مرة واحدة فقط (من POS)
4. **التقارير**: يمكن عرض فواتير POS في تقارير المبيعات

## 🔧 الصيانة

### إضافة حقول جديدة

إذا أردت إضافة حقول جديدة للربط:

1. أضف الحقل إلى نموذج `SalesInvoice`
2. أنشئ migration جديد
3. عدّل دالة `complete_order` في `app/pos/routes.py`

### استكشاف الأخطاء

```python
# التحقق من الفواتير المفقودة
orders_without_invoices = POSOrder.query.filter(
    ~POSOrder.id.in_(
        db.session.query(SalesInvoice.pos_order_id)
        .filter(SalesInvoice.pos_order_id.isnot(None))
    )
).all()
```

## 📚 المراجع

- [نماذج POS](app/models_pos.py)
- [نماذج المبيعات](app/models_sales.py)
- [مسارات POS](app/pos/routes.py)
- [Migration](migrations/versions/b1ab24d9e06d_add_pos_order_id_to_sales_invoices.py)

