# ✅ إصلاح خطأ JSON Serialization في الفواتير

## 🐛 المشكلة
```
TypeError: Object of type Product is not JSON serializable
when serializing list item 0
```

### 📍 مكان الخطأ:
- **الملف:** `app/sales/routes.py` (السطر 183)
- **الملف:** `app/sales/routes.py` (السطر 469 - عروض الأسعار)
- **السبب:** محاولة تحويل كائنات SQLAlchemy `Product` مباشرة إلى JSON

## 🔍 التفاصيل التقنية

### المشكلة الأصلية:
```python
# في app/sales/routes.py
products = Product.query.filter_by(is_active=True, is_sellable=True).all()

return render_template('sales/add_invoice.html',
                     products=products)  # ❌ كائنات SQLAlchemy
```

### في القالب:
```javascript
// في app/templates/sales/add_invoice.html
const products = {{ products|tojson }};  // ❌ فشل التحويل إلى JSON
```

### لماذا فشل؟
كائنات SQLAlchemy (مثل `Product`) تحتوي على:
- علاقات (relationships)
- خصائص داخلية (internal state)
- مراجع دائرية (circular references)

هذه العناصر لا يمكن تحويلها مباشرة إلى JSON.

## ✅ الحل المطبق

### 1. تحويل الكائنات إلى قواميس (Dictionaries)

#### في `app/sales/routes.py` - فواتير المبيعات:
```python
# الحصول على المنتجات من قاعدة البيانات
products_query = Product.query.filter_by(is_active=True, is_sellable=True).all()

# ✅ تحويل إلى قواميس بسيطة
products = [{
    'id': p.id,
    'name': p.name,
    'code': p.code,
    'selling_price': float(p.selling_price) if p.selling_price else 0,
    'tax_rate': float(p.tax_rate) if p.tax_rate else 15
} for p in products_query]

return render_template('sales/add_invoice.html',
                     products=products)  # ✅ قواميس قابلة للتحويل إلى JSON
```

#### في `app/sales/routes.py` - عروض الأسعار:
```python
# نفس الحل المطبق على add_quotation()
products_query = Product.query.filter_by(is_active=True, is_sellable=True).all()

products = [{
    'id': p.id,
    'name': p.name,
    'code': p.code,
    'selling_price': float(p.selling_price) if p.selling_price else 0,
    'tax_rate': float(p.tax_rate) if p.tax_rate else 15
} for p in products_query]
```

### 2. الحقول المضمنة في القاموس:
- **`id`**: معرف المنتج (لإرساله مع الفاتورة)
- **`name`**: اسم المنتج (للعرض في القائمة)
- **`code`**: كود المنتج (للعرض في القائمة)
- **`selling_price`**: سعر البيع (للملء التلقائي)
- **`tax_rate`**: نسبة الضريبة (لحساب الضريبة)

### 3. تحويل Decimal إلى float:
```python
'selling_price': float(p.selling_price) if p.selling_price else 0
```
هذا ضروري لأن `Decimal` أيضاً غير قابل للتحويل إلى JSON مباشرة.

## 📝 الملفات المعدلة
1. ✅ `app/sales/routes.py` - دالة `add_invoice()` (السطر 175-196)
2. ✅ `app/sales/routes.py` - دالة `add_quotation()` (السطر 462-481)

## 🧪 كيفية الاختبار

### 1. اختبار فاتورة مبيعات جديدة:
```bash
1. شغل التطبيق: python run.py
2. افتح: http://localhost:5000/sales/invoices/add
3. تحقق من: الصفحة تفتح بدون أخطاء ✅
4. افتح Console (F12)
5. تحقق من: لا توجد أخطاء JavaScript ✅
6. اضغط "إضافة منتج"
7. افتح قائمة المنتجات
8. تحقق من: المنتجات تظهر بشكل صحيح ✅
```

### 2. اختبار عرض أسعار جديد:
```bash
1. افتح: http://localhost:5000/sales/quotations/add
2. نفس الخطوات أعلاه
```

## 🎯 النتيجة المتوقعة
- ✅ الصفحة تفتح بدون أخطاء TypeError
- ✅ قائمة المنتجات تعمل بشكل صحيح
- ✅ السعر يتم ملؤه تلقائياً عند اختيار المنتج
- ✅ حساب الضريبة يعمل بشكل صحيح

## 💡 ملاحظات للمطورين

### متى تحتاج لهذا الحل؟
عندما تريد إرسال بيانات من SQLAlchemy إلى JavaScript عبر `tojson`:
```python
# ❌ خطأ
data = Model.query.all()
return render_template('page.html', data=data)

# ✅ صحيح
data = [{'id': item.id, 'name': item.name} for item in Model.query.all()]
return render_template('page.html', data=data)
```

### بدائل أخرى:
1. **استخدام API endpoint منفصل:**
```python
@bp.route('/api/products')
def get_products():
    products = Product.query.all()
    return jsonify([{'id': p.id, 'name': p.name} for p in products])
```

2. **استخدام مكتبة Marshmallow:**
```python
from marshmallow import Schema, fields

class ProductSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    selling_price = fields.Float()

products = ProductSchema(many=True).dump(Product.query.all())
```

3. **إضافة method للنموذج:**
```python
class Product(db.Model):
    # ...
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'selling_price': float(self.selling_price) if self.selling_price else 0
        }

# الاستخدام:
products = [p.to_dict() for p in Product.query.all()]
```

---
**تاريخ الإصلاح:** 2026-01-14
**الحالة:** ✅ تم الإصلاح بنجاح
**الأولوية:** 🔴 عالية (يمنع استخدام الفواتير)

