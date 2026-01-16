# 💱 ربط العملة الديناميكية من الإعدادات إلى الفواتير

## 🎯 الهدف
ربط رمز العملة (€, $, ر.س، إلخ) من إعدادات الشركة لتظهر تلقائياً في جميع الفواتير وعروض الأسعار.

---

## ✅ التغييرات المنفذة

### 1️⃣ **إضافة المزيد من العملات في `config.py`**

<augment_code_snippet path="config.py" mode="EXCERPT">
````python
CURRENCIES = {
    'SAR': {'name': 'ريال سعودي', 'symbol': 'ر.س'},
    'USD': {'name': 'دولار أمريكي', 'symbol': '$'},
    'EUR': {'name': 'يورو', 'symbol': '€'},
    'AED': {'name': 'درهم إماراتي', 'symbol': 'د.إ'},
    'KWD': {'name': 'دينار كويتي', 'symbol': 'د.ك'},
    'BHD': {'name': 'دينار بحريني', 'symbol': 'د.ب'},
    'OMR': {'name': 'ريال عماني', 'symbol': 'ر.ع'},
    'QAR': {'name': 'ريال قطري', 'symbol': 'ر.ق'},
    'EGP': {'name': 'جنيه مصري', 'symbol': 'ج.م'},
}
````
</augment_code_snippet>

---

### 2️⃣ **تعديل Routes لإرسال العملة**

#### في `app/sales/routes.py` - فاتورة المبيعات:
<augment_code_snippet path="app/sales/routes.py" mode="EXCERPT">
````python
# Get company settings for currency
from app.models import Company
from flask import current_app
company = Company.query.first()
currency_code = company.currency if company else current_app.config.get('DEFAULT_CURRENCY', 'SAR')
currency_symbol = current_app.config['CURRENCIES'].get(currency_code, {}).get('symbol', 'ر.س')

return render_template('sales/add_invoice.html',
                     customers=customers,
                     warehouses=warehouses,
                     products=products,
                     today=today,
                     currency_code=currency_code,
                     currency_symbol=currency_symbol)
````
</augment_code_snippet>

#### نفس التعديل في:
- ✅ `app/sales/routes.py` - `add_quotation()` (عروض الأسعار)
- ✅ `app/purchases/routes.py` - `add_invoice()` (فواتير المشتريات)

---

### 3️⃣ **تعديل القوالب (Templates)**

#### في `app/templates/sales/add_invoice.html`:

**HTML - عرض العملة:**
```html
<td class="text-end"><strong id="subtotalDisplay">0.00 {{ currency_symbol }}</strong></td>
<td class="text-end"><strong id="taxDisplay">0.00 {{ currency_symbol }}</strong></td>
<td class="text-end"><strong id="totalDisplay">0.00 {{ currency_symbol }}</strong></td>
```

**JavaScript - استخدام العملة:**
```javascript
const currencySymbol = '{{ currency_symbol }}';

// في دالة updateTotals:
subtotalDisplay.textContent = subtotal.toFixed(2) + ' ' + currencySymbol;
taxDisplay.textContent = tax.toFixed(2) + ' ' + currencySymbol;
totalDisplay.textContent = total.toFixed(2) + ' ' + currencySymbol;
```

#### نفس التعديلات في:
- ✅ `app/templates/sales/add_quotation.html`
- ✅ `app/templates/purchases/add_invoice.html`

---

## 📊 الملفات المعدلة

| الملف | التعديل | السطور |
|-------|---------|--------|
| `config.py` | إضافة عملات جديدة | 57-69 |
| `app/sales/routes.py` | إضافة currency للفواتير | 175-205 |
| `app/sales/routes.py` | إضافة currency لعروض الأسعار | 471-499 |
| `app/purchases/routes.py` | إضافة currency لفواتير المشتريات | 128-144 |
| `app/templates/sales/add_invoice.html` | تحديث HTML & JS | متعدد |
| `app/templates/sales/add_quotation.html` | تحديث HTML & JS | متعدد |
| `app/templates/purchases/add_invoice.html` | تحديث HTML & JS | متعدد |

**المجموع:** 7 ملفات معدلة

---

## 🧪 كيفية الاختبار

### 1. **تغيير العملة من الإعدادات:**
```
1. افتح: http://127.0.0.1:5000/settings/company
2. غير العملة من SAR إلى EUR (يورو)
3. احفظ التغييرات
```

### 2. **اختبار فاتورة مبيعات:**
```
1. افتح: http://127.0.0.1:5000/sales/invoices/add
2. تحقق من أن العملة تظهر € بدلاً من ر.س ✅
3. أضف منتج وتحقق من الحسابات
```

### 3. **اختبار عرض أسعار:**
```
1. افتح: http://127.0.0.1:5000/sales/quotations/add
2. تحقق من أن العملة تظهر € ✅
```

### 4. **اختبار فاتورة مشتريات:**
```
1. افتح: http://127.0.0.1:5000/purchases/invoices/add
2. تحقق من أن العملة تظهر € ✅
```

---

## 💡 كيف يعمل النظام؟

### 1. **قراءة العملة من قاعدة البيانات:**
```python
company = Company.query.first()
currency_code = company.currency  # مثال: 'EUR'
```

### 2. **الحصول على رمز العملة:**
```python
currency_symbol = current_app.config['CURRENCIES'].get(currency_code, {}).get('symbol', 'ر.س')
# النتيجة: '€'
```

### 3. **إرسالها إلى القالب:**
```python
return render_template('sales/add_invoice.html',
                     currency_symbol=currency_symbol)
```

### 4. **استخدامها في JavaScript:**
```javascript
const currencySymbol = '{{ currency_symbol }}';  // '€'
totalDisplay.textContent = total.toFixed(2) + ' ' + currencySymbol;
// النتيجة: "1500.00 €"
```

---

## 🎨 العملات المدعومة

| الكود | الاسم | الرمز |
|------|-------|------|
| SAR | ريال سعودي | ر.س |
| USD | دولار أمريكي | $ |
| EUR | يورو | € |
| AED | درهم إماراتي | د.إ |
| KWD | دينار كويتي | د.ك |
| BHD | دينار بحريني | د.ب |
| OMR | ريال عماني | ر.ع |
| QAR | ريال قطري | ر.ق |
| EGP | جنيه مصري | ج.م |

---

## ✅ النتيجة النهائية

- ✅ **تغيير العملة من الإعدادات يؤثر على جميع الفواتير**
- ✅ **رمز العملة يظهر ديناميكياً (€, $, ر.س، إلخ)**
- ✅ **يعمل في فواتير المبيعات**
- ✅ **يعمل في عروض الأسعار**
- ✅ **يعمل في فواتير المشتريات**
- ✅ **سهل الإضافة لعملات جديدة**

---

**تاريخ التنفيذ:** 2026-01-14  
**الحالة:** ✅ **مكتمل وجاهز للاستخدام**

