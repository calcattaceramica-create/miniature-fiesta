# دليل تطبيق الصلاحيات على Routes

## كيفية تطبيق الصلاحيات

### 1. استيراد الـ decorators

في بداية كل ملف routes، أضف:

```python
from app.auth.decorators import permission_required, any_permission_required, all_permissions_required
```

### 2. تطبيق الصلاحيات على المبيعات (Sales)

```python
# عرض العملاء
@bp.route('/customers')
@login_required
@permission_required('customers.view')
def customers():
    ...

# إضافة عميل
@bp.route('/customers/add', methods=['GET', 'POST'])
@login_required
@permission_required('customers.create')
def add_customer():
    ...

# عرض الفواتير
@bp.route('/invoices')
@login_required
@permission_required('sales.view')
def invoices():
    ...

# إضافة فاتورة
@bp.route('/invoices/add', methods=['GET', 'POST'])
@login_required
@permission_required('sales.create')
def add_invoice():
    ...

# تعديل فاتورة
@bp.route('/invoices/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@permission_required('sales.edit')
def edit_invoice(id):
    ...

# حذف فاتورة
@bp.route('/invoices/<int:id>/delete', methods=['POST'])
@login_required
@permission_required('sales.delete')
def delete_invoice(id):
    ...

# عروض الأسعار
@bp.route('/quotations')
@login_required
@permission_required('sales.quotations')
def quotations():
    ...
```

### 3. تطبيق الصلاحيات على المشتريات (Purchases)

```python
# عرض الموردين
@bp.route('/suppliers')
@login_required
@permission_required('suppliers.view')
def suppliers():
    ...

# إضافة مورد
@bp.route('/suppliers/add', methods=['GET', 'POST'])
@login_required
@permission_required('suppliers.create')
def add_supplier():
    ...

# عرض فواتير المشتريات
@bp.route('/invoices')
@login_required
@permission_required('purchases.view')
def invoices():
    ...

# إضافة فاتورة مشتريات
@bp.route('/invoices/add', methods=['GET', 'POST'])
@login_required
@permission_required('purchases.create')
def add_invoice():
    ...
```

### 4. تطبيق الصلاحيات على المخزون (Inventory)

```python
# عرض المنتجات
@bp.route('/products')
@login_required
@permission_required('inventory.products.view')
def products():
    ...

# إضافة منتج
@bp.route('/products/add', methods=['GET', 'POST'])
@login_required
@permission_required('inventory.products.create')
def add_product():
    ...

# تعديل منتج
@bp.route('/products/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@permission_required('inventory.products.edit')
def edit_product(id):
    ...

# حذف منتج
@bp.route('/products/<int:id>/delete', methods=['POST'])
@login_required
@permission_required('inventory.products.delete')
def delete_product(id):
    ...

# عرض المخزون
@bp.route('/stock')
@login_required
@permission_required('inventory.stock.view')
def stock():
    ...

# تعديل المخزون
@bp.route('/stock/adjust', methods=['GET', 'POST'])
@login_required
@permission_required('inventory.stock.adjust')
def adjust_stock():
    ...
```

### 5. تطبيق الصلاحيات على الإعدادات (Settings)

```python
# عرض المستخدمين
@bp.route('/users')
@login_required
@permission_required('settings.users.view')
def users():
    ...

# إدارة المستخدمين
@bp.route('/users/add', methods=['GET', 'POST'])
@login_required
@permission_required('settings.users.manage')
def add_user():
    ...

# عرض الأدوار
@bp.route('/roles')
@login_required
@permission_required('settings.roles.view')
def roles():
    ...

# إدارة الأدوار
@bp.route('/roles/add', methods=['POST'])
@login_required
@permission_required('settings.roles.manage')
def add_role():
    ...
```

## ملاحظات مهمة

1. **الترتيب مهم**: يجب أن يكون `@login_required` قبل `@permission_required`
2. **Admin دائماً لديه صلاحيات**: المستخدمون الذين `is_admin=True` لديهم جميع الصلاحيات تلقائياً
3. **استخدم `any_permission_required`** عندما تريد أن يكون للمستخدم أي صلاحية من عدة صلاحيات
4. **استخدم `all_permissions_required`** عندما تريد أن يكون للمستخدم جميع الصلاحيات المحددة

