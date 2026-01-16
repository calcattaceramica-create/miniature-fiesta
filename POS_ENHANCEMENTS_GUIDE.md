# 🎯 دليل تحسينات نقطة البيع (POS Enhancements)

## 📋 نظرة عامة

تم تحسين نظام نقطة البيع (POS) بإضافة المميزات التالية:

1. ✅ **ربط نقطة البيع بالصلاحيات** - نظام صلاحيات متقدم
2. ✅ **ربط العملة الديناميكية** - دعم العملات المتعددة من الإعدادات
3. ✅ **إصدار الفاتورة تلقائياً** - عند إتمام البيع
4. ✅ **تنقيص المخزون تلقائياً** - مع حركة مخزون
5. ✅ **طباعة عرض الأسعار** - إنشاء وطباعة عروض الأسعار من POS

---

## 🔐 1. نظام الصلاحيات

### الصلاحيات المضافة:

| الصلاحية | الاسم بالعربية | الوصف |
|---------|----------------|-------|
| `pos.access` | الوصول إلى نقطة البيع | الدخول إلى واجهة نقطة البيع |
| `pos.session.manage` | إدارة جلسات نقطة البيع | فتح وإغلاق الورديات |
| `pos.sell` | البيع من نقطة البيع | إتمام عمليات البيع |
| `pos.quotation.create` | إنشاء عروض أسعار | إنشاء عروض أسعار من POS |
| `pos.reports.view` | عرض تقارير نقطة البيع | عرض تقارير الجلسات |

### كيفية تطبيق الصلاحيات:

#### 1️⃣ **تشغيل سكريبت SQL:**
```bash
sqlite3 instance/ded.db < add_pos_permissions.sql
```

#### 2️⃣ **أو استخدام Python:**
```bash
python -c "from app import create_app, db; from app.models import Permission; app = create_app(); app.app_context().push(); perms = [('pos.access', 'الوصول إلى نقطة البيع', 'pos'), ('pos.session.manage', 'إدارة جلسات نقطة البيع', 'pos'), ('pos.sell', 'البيع من نقطة البيع', 'pos'), ('pos.quotation.create', 'إنشاء عروض أسعار من نقطة البيع', 'pos'), ('pos.reports.view', 'عرض تقارير نقطة البيع', 'pos')]; [db.session.add(Permission(name=p[0], name_ar=p[1], module=p[2])) if not Permission.query.filter_by(name=p[0]).first() else None for p in perms]; db.session.commit(); print('✅ تم إضافة الصلاحيات بنجاح!')"
```

### الصلاحيات المطبقة على Routes:

```python
# app/pos/routes.py

@bp.route('/')
@login_required
@permission_required('pos.access')  # ✅ صلاحية الوصول
def index():
    ...

@bp.route('/open-session', methods=['GET', 'POST'])
@login_required
@permission_required('pos.session.manage')  # ✅ صلاحية إدارة الجلسات
def open_session():
    ...

@bp.route('/create-order', methods=['POST'])
@login_required
@permission_required('pos.sell')  # ✅ صلاحية البيع
def create_order():
    ...

@bp.route('/create-quotation', methods=['POST'])
@login_required
@permission_required('pos.quotation.create')  # ✅ صلاحية عروض الأسعار
def create_quotation():
    ...
```

---

## 💱 2. ربط العملة الديناميكية

### التعديلات المنفذة:

#### في `app/pos/routes.py`:
```python
from app.models import Company
from flask import current_app

# في دالة index():
company = Company.query.first()
currency_code = company.currency if company else current_app.config.get('DEFAULT_CURRENCY', 'SAR')
currency_symbol = current_app.config['CURRENCIES'].get(currency_code, {}).get('symbol', 'ر.س')

return render_template('pos/index.html',
                     session=open_session,
                     products=products,
                     customers=customers,
                     currency_code=currency_code,
                     currency_symbol=currency_symbol)
```

#### في `app/templates/pos/index.html`:
```javascript
const CURRENCY_SYMBOL = '{{ currency_symbol }}';

// استخدام العملة في العرض:
<small class="text-muted">${item.price.toFixed(2)} ${CURRENCY_SYMBOL}</small>
<strong>${itemTotal.toFixed(2)} ${CURRENCY_SYMBOL}</strong>
```

### كيفية الاختبار:
1. اذهب إلى: **الإعدادات** → **بيانات الشركة**
2. غيّر العملة من `SAR` إلى `USD` أو `EUR`
3. احفظ التغييرات
4. افتح نقطة البيع
5. ستظهر العملة الجديدة تلقائياً! ✅

---

## 📄 3. إصدار الفاتورة تلقائياً

### الكود الحالي في `create_order()`:

```python
# ✅ Create Sales Invoice automatically
invoice_number = _generate_invoice_number()

# Get customer_id or use default walk-in customer
customer_id = data.get('customer_id')
if not customer_id:
    customer_id = _get_or_create_default_customer()

invoice = SalesInvoice(
    invoice_number=invoice_number,
    invoice_date=datetime.utcnow().date(),
    customer_id=customer_id,
    warehouse_id=session.warehouse_id,
    subtotal=data['subtotal'],
    discount_amount=data['discount_amount'],
    tax_amount=data['tax_amount'],
    total_amount=data['total_amount'],
    paid_amount=data['total_amount'],  # Fully paid in POS
    remaining_amount=0.0,  # No remaining amount
    notes=f'فاتورة من نقطة البيع - طلب {order_number}',
    pos_order_id=order.id,
    user_id=current_user.id,
    status='paid'  # Automatically mark as paid
)

db.session.add(invoice)
db.session.flush()

# Add invoice items
for item_data in data['items']:
    product = Product.query.get(item_data['productId'])
    item_total = item_data['price'] * item_data['quantity']
    
    invoice_item = SalesInvoiceItem(
        invoice_id=invoice.id,
        product_id=item_data['productId'],
        description=product.name if product else '',
        quantity=item_data['quantity'],
        unit_price=item_data['price'],
        tax_rate=tax_rate,
        tax_amount=item_tax,
        total=item_total + item_tax
    )
    db.session.add(invoice_item)
```

### المميزات:
- ✅ **إنشاء فاتورة تلقائياً** عند كل عملية بيع
- ✅ **رقم فاتورة فريد** بصيغة `INV202601XXXX`
- ✅ **حالة مدفوعة** تلقائياً (`status='paid'`)
- ✅ **ربط بطلب POS** عبر `pos_order_id`
- ✅ **عميل افتراضي** إذا لم يتم اختيار عميل

---

## 📦 4. تنقيص المخزون تلقائياً

### الكود الحالي في `create_order()`:

```python
# Update stock
stock = Stock.query.filter_by(
    product_id=item_data['productId'],
    warehouse_id=session.warehouse_id
).first()

if stock:
    stock.quantity -= item_data['quantity']  # ✅ تنقيص الكمية

    # Create stock movement
    movement = StockMovement(
        product_id=item_data['productId'],
        warehouse_id=session.warehouse_id,
        movement_type='out',  # ✅ حركة خروج
        quantity=item_data['quantity'],
        reference_type='pos_order',
        reference_id=order.id,
        notes=f'بيع من نقطة البيع - طلب {order_number}'
    )
    db.session.add(movement)
```

### المميزات:
- ✅ **تنقيص تلقائي** من المخزون
- ✅ **حركة مخزون** مسجلة لكل عملية بيع
- ✅ **ربط بالطلب** عبر `reference_id`
- ✅ **تتبع كامل** لحركة المخزون

---

## 🖨️ 5. طباعة عرض الأسعار (Quotation)

### الميزات الجديدة:

#### 1️⃣ **زر جديد في واجهة POS:**
```html
<button class="btn btn-info" onclick="createQuotation()" id="quotation-button" disabled>
    <i class="fas fa-file-invoice"></i> إنشاء عرض سعر
</button>
```

#### 2️⃣ **دالة JavaScript لإنشاء عرض السعر:**
```javascript
async function createQuotation() {
    if (cart.length === 0) {
        alert('السلة فارغة!');
        return;
    }

    const response = await fetch('/pos/create-quotation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            session_id: SESSION_ID,
            customer_id: customerId || null,
            items: cart,
            subtotal: totals.subtotal,
            discount_amount: totals.discount,
            tax_amount: totals.tax,
            total_amount: totals.total
        })
    });

    const result = await response.json();
    
    if (result.success) {
        alert('تم إنشاء عرض السعر بنجاح!');
        
        // طباعة عرض السعر
        if (confirm('هل تريد طباعة عرض السعر؟')) {
            window.open('/pos/print-quotation/' + result.quotation_id, '_blank');
        }
        
        clearCart();
    }
}
```

#### 3️⃣ **Route جديد في `app/pos/routes.py`:**
```python
@bp.route('/create-quotation', methods=['POST'])
@login_required
@permission_required('pos.quotation.create')
def create_quotation():
    """Create quotation from POS cart"""
    # ... الكود الكامل في الملف
```

#### 4️⃣ **قالب طباعة احترافي:**
- ملف: `app/templates/pos/quotation.html`
- تصميم احترافي مع شعار الشركة
- جدول المنتجات
- الإجماليات والضرائب
- ملاحظات وتاريخ الصلاحية

---

## 🧪 كيفية الاختبار الشامل

### 1️⃣ **اختبار الصلاحيات:**
```
1. سجّل الدخول كـ admin
2. اذهب إلى نقطة البيع
3. يجب أن تعمل جميع الأزرار ✅
```

### 2️⃣ **اختبار العملة:**
```
1. غيّر العملة من الإعدادات إلى USD
2. افتح نقطة البيع
3. يجب أن تظهر $ بدلاً من ر.س ✅
```

### 3️⃣ **اختبار الفاتورة:**
```
1. أضف منتج pg1111 إلى السلة
2. اضغط "إتمام البيع"
3. اذهب إلى: المبيعات → الفواتير
4. يجب أن تجد فاتورة جديدة بحالة "مدفوعة" ✅
```

### 4️⃣ **اختبار المخزون:**
```
1. تحقق من كمية المنتج قبل البيع
2. قم بعملية بيع
3. تحقق من كمية المنتج بعد البيع
4. يجب أن تكون الكمية قد نقصت ✅
5. اذهب إلى: المخزون → حركات المخزون
6. يجب أن تجد حركة خروج جديدة ✅
```

### 5️⃣ **اختبار عرض الأسعار:**
```
1. أضف منتجات إلى السلة
2. اضغط "إنشاء عرض سعر"
3. اختر طباعة
4. يجب أن تفتح صفحة طباعة احترافية ✅
```

---

## 📊 الملفات المعدلة

| الملف | التعديلات |
|------|-----------|
| `app/pos/routes.py` | إضافة صلاحيات، عملة، route عرض السعر |
| `app/templates/pos/index.html` | زر عرض السعر، دالة JavaScript، عملة ديناميكية |
| `app/templates/pos/quotation.html` | قالب طباعة عرض السعر (جديد) |
| `add_pos_permissions.sql` | سكريبت إضافة الصلاحيات (جديد) |

---

## ✅ الخلاصة

تم تحسين نظام نقطة البيع بنجاح بإضافة:

1. ✅ **نظام صلاحيات متقدم** - 5 صلاحيات جديدة
2. ✅ **دعم العملات المتعددة** - ديناميكي من الإعدادات
3. ✅ **إصدار فواتير تلقائي** - مع كل عملية بيع
4. ✅ **تنقيص مخزون تلقائي** - مع حركات مخزون
5. ✅ **طباعة عروض أسعار** - من داخل POS

**النظام جاهز للاستخدام! 🚀**

---

📅 **تاريخ التحديث:** 2026-01-15  
👨‍💻 **الإصدار:** 2.1.0

