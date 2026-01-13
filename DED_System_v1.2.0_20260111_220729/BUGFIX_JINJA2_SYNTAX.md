# إصلاح خطأ Jinja2 Syntax Error

## المشكلة

عند محاولة الوصول إلى صفحة الحسابات (`/accounting/accounts`)، ظهر الخطأ التالي:

```
jinja2.exceptions.TemplateSyntaxError: expected token 'end of statement block', got 'with'
```

## السبب

كان هناك استخدام خاطئ لـ `{% include %}` في ملف `app/templates/accounting/accounts.html`.

### الكود الخاطئ:

```jinja2
<!-- Assets -->
<div id="assets" class="tab-pane fade">
    {% include 'accounting/_account_table.html' with accounts=accounts_by_type.asset %}
</div>
```

### المشكلة:

في Jinja2، لا يمكن استخدام `with` بهذه الطريقة مع `{% include %}`. الصيغة الصحيحة تختلف عن Django templates.

## الحل

تم استبدال `{% include %}` بكتابة الكود مباشرة في كل تبويب (tab).

### الكود الصحيح:

```jinja2
<!-- Assets -->
<div id="assets" class="tab-pane fade">
    <div class="table-responsive">
        <table class="table table-hover table-striped">
            <thead class="table-dark">
                <tr>
                    <th>الرمز</th>
                    <th>اسم الحساب</th>
                    <th>رصيد مدين</th>
                    <th>رصيد دائن</th>
                    <th>الرصيد الحالي</th>
                    <th>الحالة</th>
                    <th>الإجراءات</th>
                </tr>
            </thead>
            <tbody>
                {% for account in accounts_by_type.asset %}
                <tr>
                    <td><strong>{{ account.code }}</strong></td>
                    <td>{{ account.name }}</td>
                    <td>{{ "{:,.2f}".format(account.debit_balance) }}</td>
                    <td>{{ "{:,.2f}".format(account.credit_balance) }}</td>
                    <td>{{ "{:,.2f}".format(account.current_balance) }}</td>
                    <td>
                        {% if account.is_active %}
                            <span class="badge bg-success">نشط</span>
                        {% else %}
                            <span class="badge bg-secondary">غير نشط</span>
                        {% endif %}
                    </td>
                    <td>
                        <a href="{{ url_for('accounting.account_details', id=account.id) }}" class="btn btn-sm btn-info">
                            <i class="fas fa-eye"></i>
                        </a>
                    </td>
                </tr>
                {% else %}
                <tr>
                    <td colspan="7" class="text-center text-muted">لا توجد حسابات</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
```

## البدائل الصحيحة في Jinja2

إذا أردت استخدام `{% include %}` في Jinja2، هناك عدة طرق:

### 1. استخدام `{% set %}` قبل `{% include %}`

```jinja2
{% set accounts = accounts_by_type.asset %}
{% include 'accounting/_account_table.html' %}
```

### 2. استخدام `{% with %}` block

```jinja2
{% with accounts=accounts_by_type.asset %}
    {% include 'accounting/_account_table.html' %}
{% endwith %}
```

### 3. تمرير المتغيرات مباشرة (Jinja2 2.10+)

```jinja2
{% include 'accounting/_account_table.html' with context %}
```

## الملفات المعدلة

- ✅ `app/templates/accounting/accounts.html` - تم إصلاح جميع التبويبات (5 تبويبات)

## التأثير

- ✅ تم حل المشكلة بالكامل
- ✅ صفحة الحسابات تعمل الآن بشكل صحيح
- ✅ جميع التبويبات (الأصول، الخصوم، حقوق الملكية، الإيرادات، المصروفات) تعمل

## الاختبار

للتأكد من أن المشكلة تم حلها:

```bash
# تشغيل التطبيق
python run.py

# الوصول إلى صفحة الحسابات
http://localhost:5000/accounting/accounts
```

## ملاحظات مهمة

1. **Jinja2 vs Django Templates**: Jinja2 له صيغة مختلفة عن Django templates
2. **استخدام `with`**: في Jinja2، `with` يستخدم كـ block وليس كـ parameter
3. **البدائل**: يمكن استخدام `{% set %}` أو `{% with %}` block كبديل

## الحالة

✅ **تم الحل** - المشكلة تم إصلاحها بنجاح

---

**تاريخ الإصلاح**: 2026-01-11  
**الملف المعدل**: `app/templates/accounting/accounts.html`  
**عدد الأسطر المعدلة**: ~230 سطر

