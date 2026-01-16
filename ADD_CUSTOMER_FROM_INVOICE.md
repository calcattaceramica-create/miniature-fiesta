# 👤 إضافة عميل جديد من صفحة الفاتورة

## 🎯 الهدف
تمكين المستخدم من إضافة عميل جديد مباشرة من صفحة الفاتورة دون الحاجة للانتقال إلى صفحة العملاء.

---

## ✅ التغييرات المنفذة

### 1️⃣ **إضافة Route جديد للـ AJAX**

تم إضافة route جديد في `app/sales/routes.py` لإضافة عميل عبر AJAX:

<augment_code_snippet path="app/sales/routes.py" mode="EXCERPT">
````python
@bp.route('/customers/add_ajax', methods=['POST'])
@login_required
def add_customer_ajax():
    """Add new customer via AJAX (for use in invoice forms)"""
    try:
        # Generate customer code
        last_customer = Customer.query.order_by(Customer.id.desc()).first()
        code = f'CUS{(last_customer.id + 1):05d}' if last_customer else 'CUS00001'
        
        customer = Customer(
            code=code,
            name=request.form.get('name'),
            # ... باقي الحقول
        )
        
        db.session.add(customer)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': _('Customer added successfully'),
            'customer': {
                'id': customer.id,
                'code': customer.code,
                'name': customer.name
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
````
</augment_code_snippet>

---

### 2️⃣ **إضافة زر "+" بجانب قائمة العملاء**

في `app/templates/sales/add_invoice.html`:

<augment_code_snippet path="app/templates/sales/add_invoice.html" mode="EXCERPT">
````html
<div class="input-group">
    <select class="form-select" name="customer_id" id="customer_id" required>
        <option value="">{{ _('Select Customer') }}</option>
        {% for customer in customers %}
        <option value="{{ customer.id }}">{{ customer.name }} ({{ customer.code }})</option>
        {% endfor %}
    </select>
    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addCustomerModal">
        <i class="fas fa-plus"></i>
    </button>
</div>
````
</augment_code_snippet>

---

### 3️⃣ **إضافة Modal لإضافة العميل**

تم إضافة نافذة منبثقة (Modal) تحتوي على نموذج إضافة عميل:

**الحقول المتاحة:**
- ✅ اسم العميل (عربي) - **إجباري**
- ✅ اسم العميل (إنجليزي)
- ✅ الجوال
- ✅ الهاتف
- ✅ البريد الإلكتروني
- ✅ الرقم الضريبي
- ✅ العنوان
- ✅ المدينة
- ✅ الدولة

---

### 4️⃣ **إضافة JavaScript للحفظ عبر AJAX**

<augment_code_snippet path="app/templates/sales/add_invoice.html" mode="EXCERPT">
````javascript
function saveCustomer() {
    const form = document.getElementById('addCustomerForm');
    const formData = new FormData(form);
    
    // Validate required fields
    const customerName = document.getElementById('customer_name').value.trim();
    if (!customerName) {
        alert('{{ _("Please enter customer name") }}');
        return;
    }
    
    // Send AJAX request
    fetch('{{ url_for("sales.add_customer_ajax") }}', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Add new customer to select dropdown
            const select = document.getElementById('customer_id');
            const option = document.createElement('option');
            option.value = data.customer.id;
            option.text = data.customer.name + ' (' + data.customer.code + ')';
            option.selected = true;
            select.add(option);
            
            // Close modal and reset form
            modal.hide();
            form.reset();
            alert(data.message);
        }
    });
}
````
</augment_code_snippet>

---

## 📊 الملفات المعدلة

| # | الملف | التعديل | السطور |
|---|-------|---------|--------|
| 1 | `app/sales/routes.py` | إضافة route للـ AJAX | 68-116 |
| 2 | `app/templates/sales/add_invoice.html` | إضافة زر + Modal + JS | متعدد |
| 3 | `app/templates/sales/add_quotation.html` | إضافة زر + Modal + JS | متعدد |

**المجموع:** 3 ملفات معدلة

---

## 🎬 كيفية الاستخدام

### **الطريقة 1: من صفحة الفاتورة**

1. **افتح صفحة إضافة فاتورة:**
   ```
   http://127.0.0.1:5000/sales/invoices/add
   ```

2. **اضغط زر "+" بجانب قائمة العملاء:**
   - ستظهر نافذة منبثقة

3. **املأ بيانات العميل:**
   - اسم العميل (إجباري)
   - باقي البيانات (اختياري)

4. **اضغط "حفظ العميل":**
   - ✅ سيتم حفظ العميل في قاعدة البيانات
   - ✅ سيظهر العميل الجديد في القائمة المنسدلة
   - ✅ سيتم اختياره تلقائياً
   - ✅ ستغلق النافذة المنبثقة

5. **أكمل الفاتورة:**
   - أضف المنتجات
   - احفظ الفاتورة

---

### **الطريقة 2: من صفحة عرض السعر**

نفس الخطوات السابقة، لكن من:
```
http://127.0.0.1:5000/sales/quotations/add
```

---

## 🔧 كيف يعمل النظام؟

### **1. المستخدم يضغط زر "+":**
```javascript
<button data-bs-toggle="modal" data-bs-target="#addCustomerModal">
    <i class="fas fa-plus"></i>
</button>
```

### **2. تظهر النافذة المنبثقة:**
```html
<div class="modal" id="addCustomerModal">
    <form id="addCustomerForm">
        <!-- حقول العميل -->
    </form>
</div>
```

### **3. المستخدم يملأ البيانات ويضغط "حفظ":**
```javascript
function saveCustomer() {
    // جمع البيانات
    const formData = new FormData(form);
    
    // إرسال AJAX
    fetch('/sales/customers/add_ajax', {
        method: 'POST',
        body: formData
    })
}
```

### **4. الخادم يحفظ العميل:**
```python
@bp.route('/customers/add_ajax', methods=['POST'])
def add_customer_ajax():
    customer = Customer(...)
    db.session.add(customer)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'customer': {...}
    })
```

### **5. JavaScript يضيف العميل للقائمة:**
```javascript
const option = document.createElement('option');
option.value = data.customer.id;
option.text = data.customer.name;
option.selected = true;
select.add(option);
```

---

## ✅ المميزات

- ✅ **سريع:** لا حاجة للانتقال لصفحة أخرى
- ✅ **سهل:** نافذة منبثقة بسيطة
- ✅ **تلقائي:** العميل يُضاف للقائمة ويُختار تلقائياً
- ✅ **آمن:** التحقق من البيانات في الخادم
- ✅ **متعدد:** يعمل في الفواتير وعروض الأسعار

---

**تاريخ التنفيذ:** 2026-01-14  
**الحالة:** ✅ **مكتمل وجاهز للاستخدام**

