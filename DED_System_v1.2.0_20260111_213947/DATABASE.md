# 📊 توثيق قاعدة البيانات (Database Documentation)

## نظرة عامة

نظام إدارة المخزون المتكامل يستخدم قاعدة بيانات علائقية (Relational Database) مع دعم لـ:
- **SQLite** (افتراضي - للتطوير)
- **PostgreSQL** (موصى به للإنتاج)
- **MySQL** (مدعوم)

---

## 📋 جداول قاعدة البيانات

### 1. البيانات الأساسية (Master Data)

#### users - المستخدمون
```sql
- id (PK)
- username (UNIQUE)
- email (UNIQUE)
- password_hash
- full_name
- phone
- is_active
- is_admin
- language
- branch_id (FK → branches)
- role_id (FK → roles)
- created_at
- last_login
```

#### roles - الأدوار
```sql
- id (PK)
- name (UNIQUE)
- name_ar
- description
```

#### permissions - الصلاحيات
```sql
- id (PK)
- name (UNIQUE)
- name_ar
- module
- description
```

#### companies - الشركات
```sql
- id (PK)
- name
- name_en
- tax_number
- commercial_register
- phone, email, address
- city, country
- logo
- is_active
- created_at
```

#### branches - الفروع
```sql
- id (PK)
- company_id (FK → companies)
- name, name_en
- code (UNIQUE)
- phone, email, address
- city
- is_main
- is_active
- created_at
```

#### currencies - العملات
```sql
- id (PK)
- code (UNIQUE)
- name, name_en
- symbol
- exchange_rate
- is_default
- is_active
```

#### units - وحدات القياس
```sql
- id (PK)
- name, name_en
- symbol
- is_active
```

---

### 2. المخزون (Inventory)

#### categories - التصنيفات
```sql
- id (PK)
- name, name_en
- code (UNIQUE)
- parent_id (FK → categories) [Self-referential]
- description
- is_active
- created_at
```

#### products - المنتجات
```sql
- id (PK)
- name, name_en
- code (UNIQUE)
- barcode (UNIQUE)
- sku (UNIQUE)
- category_id (FK → categories)
- unit_id (FK → units)
- description
- image
- cost_price
- selling_price
- min_price
- tax_rate
- is_active
- track_inventory
- min_stock_level
- max_stock_level
- reorder_point
- created_at, updated_at
```

#### warehouses - المستودعات
```sql
- id (PK)
- name, name_en
- code (UNIQUE)
- branch_id (FK → branches)
- address
- manager_id (FK → users)
- is_active
- created_at
```

#### stock - المخزون
```sql
- id (PK)
- product_id (FK → products)
- warehouse_id (FK → warehouses)
- quantity
- reserved_quantity
- available_quantity
- last_updated
```

#### stock_movements - حركات المخزون
```sql
- id (PK)
- product_id (FK → products)
- warehouse_id (FK → warehouses)
- movement_type (in, out, transfer, adjustment)
- quantity
- reference_type
- reference_id
- notes
- created_by (FK → users)
- created_at
```

---

### 3. المبيعات (Sales)

#### customers - العملاء
```sql
- id (PK)
- code (UNIQUE)
- name, name_en
- email, phone, mobile
- address, city, country
- tax_number
- commercial_register
- customer_type (individual, company)
- credit_limit
- current_balance
- payment_terms
- category
- rating
- is_active
- notes
- created_at, updated_at
```

#### sales_invoices - فواتير البيع
```sql
- id (PK)
- invoice_number (UNIQUE)
- invoice_date
- customer_id (FK → customers)
- warehouse_id (FK → warehouses)
- subtotal
- discount_amount
- tax_amount
- total_amount
- paid_amount
- remaining_amount
- payment_status (unpaid, partial, paid)
- status (draft, confirmed, cancelled)
- notes
- created_by (FK → users)
- created_at, updated_at
```

#### sales_invoice_items - تفاصيل فواتير البيع
```sql
- id (PK)
- invoice_id (FK → sales_invoices)
- product_id (FK → products)
- quantity
- unit_price
- discount_amount
- tax_amount
- total_amount
```

#### sales_returns - مرتجعات البيع
```sql
- id (PK)
- return_number (UNIQUE)
- return_date
- invoice_id (FK → sales_invoices)
- customer_id (FK → customers)
- total_amount
- status
- reason
- created_at
```

---

### 4. المشتريات (Purchases)

#### suppliers - الموردون
```sql
- id (PK)
- code (UNIQUE)
- name, name_en
- email, phone, mobile
- address, city, country
- tax_number
- commercial_register
- credit_limit
- current_balance
- payment_terms
- category
- rating
- is_active
- notes
- created_at, updated_at
```

#### purchase_invoices - فواتير الشراء
```sql
- id (PK)
- invoice_number (UNIQUE)
- invoice_date
- supplier_id (FK → suppliers)
- warehouse_id (FK → warehouses)
- subtotal
- discount_amount
- tax_amount
- total_amount
- paid_amount
- remaining_amount
- payment_status
- status
- notes
- created_by (FK → users)
- created_at, updated_at
```

---

### 5. نقاط البيع (POS)

#### pos_sessions - ورديات نقاط البيع
```sql
- id (PK)
- session_number (UNIQUE)
- cashier_id (FK → users)
- warehouse_id (FK → warehouses)
- opening_time
- closing_time
- opening_balance
- closing_balance
- total_sales
- total_cash
- total_card
- status (open, closed)
- notes
- created_at
```

#### pos_orders - طلبات نقاط البيع
```sql
- id (PK)
- order_number (UNIQUE)
- order_date
- session_id (FK → pos_sessions)
- customer_id (FK → customers)
- subtotal
- discount_amount
- tax_amount
- total_amount
- payment_method (cash, card, credit)
- status
- created_at
```

---

### 6. المحاسبة (Accounting)

#### accounts - دليل الحسابات
```sql
- id (PK)
- code (UNIQUE)
- name, name_en
- account_type (asset, liability, equity, revenue, expense)
- parent_id (FK → accounts) [Self-referential]
- debit_balance
- credit_balance
- current_balance
- is_active
- is_system
- description
- created_at
```

#### journal_entries - القيود اليومية
```sql
- id (PK)
- entry_number (UNIQUE)
- entry_date
- entry_type (manual, auto, opening, closing)
- reference_type
- reference_id
- description
- total_debit
- total_credit
- status (draft, posted, cancelled)
- created_by (FK → users)
- created_at
```

#### journal_entry_lines - سطور القيود
```sql
- id (PK)
- entry_id (FK → journal_entries)
- account_id (FK → accounts)
- debit_amount
- credit_amount
- description
```

---

### 7. الموارد البشرية (HR)

#### employees - الموظفون
```sql
- id (PK)
- employee_number (UNIQUE)
- user_id (FK → users)
- first_name, last_name
- national_id (UNIQUE)
- date_of_birth
- gender
- department_id (FK → departments)
- position_id (FK → positions)
- hire_date
- basic_salary
- is_active
- created_at, updated_at
```

#### departments - الأقسام
```sql
- id (PK)
- name, name_en
- code (UNIQUE)
- manager_id (FK → employees)
- is_active
```

#### attendance - الحضور
```sql
- id (PK)
- employee_id (FK → employees)
- date
- check_in
- check_out
- status (present, absent, late, leave)
```

---

## 🔗 العلاقات الرئيسية

### One-to-Many
- Company → Branches
- Branch → Users
- Category → Products
- Warehouse → Stock
- Customer → Sales Invoices
- Supplier → Purchase Invoices

### Many-to-Many
- Roles ↔ Permissions (via role_permissions)

### Self-Referential
- Category → Category (parent/child)
- Account → Account (parent/child)

---

## 📊 الفهارس (Indexes)

تم إنشاء فهارس على:
- جميع المفاتيح الأساسية (Primary Keys)
- جميع المفاتيح الأجنبية (Foreign Keys)
- الحقول الفريدة (UNIQUE)
- حقول البحث الشائعة (username, email, code, barcode)

---

## 🔐 القيود (Constraints)

- **Primary Keys:** على جميع الجداول
- **Foreign Keys:** للحفاظ على سلامة البيانات
- **UNIQUE:** على الأكواد والأرقام
- **NOT NULL:** على الحقول الإلزامية
- **DEFAULT:** قيم افتراضية للحقول

---

## 🚀 التهيئة

### إنشاء قاعدة البيانات

```bash
python init_db.py
```

هذا الأمر سيقوم بـ:
1. حذف الجداول القديمة (إن وجدت)
2. إنشاء جميع الجداول
3. إدخال البيانات الافتراضية:
   - مستخدم admin
   - الأدوار الأساسية
   - العملات
   - وحدات القياس
   - التصنيفات
   - دليل الحسابات

### بيانات الدخول الافتراضية

```
Username: admin
Password: admin123
```

⚠️ **مهم:** غيّر كلمة المرور فوراً!

---

## 📝 ملاحظات

- جميع التواريخ بصيغة UTC
- جميع المبالغ بصيغة Float
- الحقول النصية تدعم Unicode (العربية)
- الحقول المحذوفة تُعلّم بـ is_active=False (Soft Delete)

---

**آخر تحديث:** 2026-01-10

