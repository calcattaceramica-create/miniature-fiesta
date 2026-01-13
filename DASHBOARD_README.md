# 📊 لوحة التحكم والتقارير - دليل المطور

## 🚀 البدء السريع

### تشغيل التطبيق
```bash
cd c:\Users\DELL\DED
flask run
```

### الوصول للوحة التحكم
```
http://localhost:5000/
```

### الوصول للتقارير
```
http://localhost:5000/reports
```

---

## 📁 هيكل الملفات

```
app/
├── main/
│   └── routes.py              # لوحة التحكم الرئيسية
├── reports/
│   └── routes.py              # جميع التقارير
└── templates/
    ├── main/
    │   └── index.html         # واجهة لوحة التحكم
    └── reports/
        ├── index.html         # مركز التقارير
        ├── low_stock.html     # تقرير المنتجات منخفضة المخزون
        ├── stock_movement.html # تقرير حركة المخزون
        ├── sales_by_product.html # تقرير المبيعات حسب المنتج
        └── sales_by_customer.html # تقرير المبيعات حسب العميل
```

---

## 🔧 الـ Routes

### لوحة التحكم
```python
@bp.route('/')
@bp.route('/index')
@login_required
def index():
    # عرض لوحة التحكم الرئيسية
```

### التقارير
```python
# مركز التقارير
@bp.route('/')
def index()

# تقرير المنتجات منخفضة المخزون
@bp.route('/low-stock')
def low_stock_report()

# تقرير حركة المخزون
@bp.route('/stock-movement')
def stock_movement_report()

# تقرير المبيعات حسب المنتج
@bp.route('/sales-by-product')
def sales_by_product()

# تقرير المبيعات حسب العميل
@bp.route('/sales-by-customer')
def sales_by_customer()
```

---

## 📊 البيانات المرسلة للقوالب

### لوحة التحكم (`index.html`)
```python
{
    'stats': {
        'total_products': int,
        'total_customers': int,
        'total_suppliers': int,
        'low_stock_products': int,
        'total_warehouses': int,
        'sales_this_month': float,
        'purchases_this_month': float,
        'profit_this_month': float,
        'inventory_value': float
    },
    'recent_sales': [SalesInvoice],
    'recent_purchases': [PurchaseInvoice],
    'sales_chart_data': [float],
    'purchases_chart_data': [float],
    'chart_labels': [str],
    'top_products': [(name, qty)]
}
```

### تقرير المنتجات منخفضة المخزون
```python
{
    'low_stock_products': [{
        'product': Product,
        'current_stock': float,
        'min_stock': float,
        'shortage': float
    }]
}
```

### تقرير حركة المخزون
```python
{
    'movements': [StockMovement],
    'products': [Product],
    'warehouses': [Warehouse],
    'start_date': str,
    'end_date': str,
    'selected_product_id': int,
    'selected_warehouse_id': int
}
```

### تقرير المبيعات حسب المنتج
```python
{
    'results': [(name, code, total_qty, total_amount)],
    'total_qty': float,
    'total_amount': float,
    'start_date': str,
    'end_date': str
}
```

### تقرير المبيعات حسب العميل
```python
{
    'results': [(name, code, invoice_count, total_amount)],
    'total_invoices': int,
    'total_amount': float,
    'start_date': str,
    'end_date': str
}
```

---

## 🎨 المكتبات المستخدمة

### Backend
- **Flask**: إطار العمل الرئيسي
- **SQLAlchemy**: ORM لقاعدة البيانات
- **Flask-Login**: إدارة الجلسات

### Frontend
- **Bootstrap 5**: إطار العمل للتصميم
- **Chart.js**: الرسوم البيانية
- **Font Awesome**: الأيقونات
- **jQuery**: التفاعل مع DOM

---

## 🔍 الاستعلامات الرئيسية

### حساب المنتجات منخفضة المخزون
```python
products = Product.query.filter_by(is_active=True, track_inventory=True).all()
for product in products:
    current_stock = product.get_stock()
    if current_stock <= product.min_stock:
        low_stock_products += 1
```

### حساب المبيعات الشهرية
```python
sales_this_month = db.session.query(func.sum(SalesInvoice.total_amount)).filter(
    SalesInvoice.invoice_date >= first_day,
    SalesInvoice.status != 'cancelled'
).scalar() or 0
```

### أفضل المنتجات مبيعاً
```python
top_products = db.session.query(
    Product.name,
    func.sum(SalesInvoiceItem.quantity).label('total_qty')
).join(SalesInvoiceItem).join(SalesInvoice).filter(
    SalesInvoice.status != 'cancelled',
    SalesInvoice.invoice_date >= first_day
).group_by(Product.id).order_by(func.sum(SalesInvoiceItem.quantity).desc()).limit(5).all()
```

---

## 🎨 التخصيص

### تغيير عدد الأشهر في الرسم البياني
في `app/main/routes.py`:
```python
# تغيير من 6 إلى 12 شهر
for i in range(11, -1, -1):  # كان 5
```

### تغيير عدد أفضل المنتجات
```python
.limit(10)  # بدلاً من 5
```

### تغيير الألوان
في `app/templates/main/index.html`:
```css
.bg-gradient-primary {
    background: linear-gradient(135deg, #YOUR_COLOR_1, #YOUR_COLOR_2);
}
```

---

## 🐛 استكشاف الأخطاء

### الرسم البياني لا يظهر
- تأكد من تحميل Chart.js
- تحقق من console في المتصفح
- تأكد من وجود بيانات

### البيانات غير صحيحة
- تحقق من حالة الفواتير (confirmed/cancelled)
- تحقق من التواريخ
- تحقق من الاستعلامات في routes.py

### خطأ في التقارير
- تأكد من وجود بيانات في قاعدة البيانات
- تحقق من الفلاتر
- راجع logs Flask

---

## 📝 ملاحظات للمطورين

1. **الأداء**: استخدم pagination للتقارير الكبيرة
2. **الأمان**: جميع الـ routes محمية بـ `@login_required`
3. **التوافق**: التصميم responsive ويعمل على جميع الأجهزة
4. **الطباعة**: جميع التقارير قابلة للطباعة
5. **التوسع**: يمكن إضافة تقارير جديدة بسهولة

---

## ✅ Checklist للتطوير

- [x] لوحة تحكم شاملة
- [x] رسوم بيانية تفاعلية
- [x] تقارير المخزون
- [x] تقارير المبيعات
- [x] فلاتر متقدمة
- [x] تصميم responsive
- [x] أزرار طباعة
- [ ] تصدير إلى Excel
- [ ] تصدير إلى PDF
- [ ] جدولة التقارير

---

**Happy Coding! 💻**

