# 📐 مخطط قاعدة البيانات (Database Schema)

## نظرة عامة

هذا المستند يوضح مخطط قاعدة البيانات الكامل للنظام.

---

## 🏗️ الهيكل العام

```
┌─────────────────────────────────────────────────────────┐
│                    ERP System Database                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Master     │  │  Inventory   │  │    Sales     │  │
│  │    Data      │  │              │  │              │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Purchases   │  │ Accounting   │  │      HR      │  │
│  │              │  │              │  │              │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                          │
│  ┌──────────────┐                                       │
│  │     POS      │                                       │
│  │              │                                       │
│  └──────────────┘                                       │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 العلاقات الرئيسية

### 1. Master Data Module

```
companies (1) ──────< (N) branches
    │
    └──────< (N) users
                │
                ├──────> (1) roles
                └──────> (1) branches
```

### 2. Inventory Module

```
categories (1) ──────< (N) products
    │                       │
    └──< (N) categories     ├──────> (1) units
         (self-ref)         │
                            └──────< (N) stock
                                        │
                                        └──────> (1) warehouses
```

### 3. Sales Module

```
customers (1) ──────< (N) sales_invoices
                            │
                            └──────< (N) sales_invoice_items
                                        │
                                        └──────> (1) products
```

### 4. Purchases Module

```
suppliers (1) ──────< (N) purchase_invoices
                            │
                            └──────< (N) purchase_invoice_items
                                        │
                                        └──────> (1) products
```

### 5. Accounting Module

```
accounts (1) ──────< (N) journal_entry_lines
    │                       │
    └──< (N) accounts       └──────> (1) journal_entries
         (self-ref)
```

### 6. HR Module

```
departments (1) ──────< (N) employees
                            │
positions (1) ──────────────┤
                            │
users (1) ──────────────────┘
```

### 7. POS Module

```
pos_sessions (1) ──────< (N) pos_orders
    │                           │
    ├──────> (1) users          └──────< (N) pos_order_items
    └──────> (1) warehouses                 │
                                            └──────> (1) products
```

---

## 📋 الجداول بالتفصيل

### Master Data Tables

#### users
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK | المعرف الفريد |
| username | VARCHAR(64) | UNIQUE, NOT NULL | اسم المستخدم |
| email | VARCHAR(120) | UNIQUE, NOT NULL | البريد الإلكتروني |
| password_hash | VARCHAR(256) | | كلمة المرور المشفرة |
| full_name | VARCHAR(128) | | الاسم الكامل |
| phone | VARCHAR(20) | | الهاتف |
| is_active | BOOLEAN | DEFAULT TRUE | نشط؟ |
| is_admin | BOOLEAN | DEFAULT FALSE | مدير؟ |
| language | VARCHAR(5) | DEFAULT 'ar' | اللغة |
| branch_id | INTEGER | FK(branches) | الفرع |
| role_id | INTEGER | FK(roles) | الدور |
| created_at | DATETIME | DEFAULT NOW | تاريخ الإنشاء |
| last_login | DATETIME | | آخر تسجيل دخول |

**Indexes:**
- `idx_users_username` ON (username)
- `idx_users_email` ON (email)

---

#### roles
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK | المعرف الفريد |
| name | VARCHAR(64) | UNIQUE, NOT NULL | الاسم |
| name_ar | VARCHAR(64) | | الاسم بالعربية |
| description | VARCHAR(256) | | الوصف |

---

#### companies
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK | المعرف الفريد |
| name | VARCHAR(256) | NOT NULL | الاسم |
| name_en | VARCHAR(256) | | الاسم بالإنجليزية |
| tax_number | VARCHAR(64) | | الرقم الضريبي |
| commercial_register | VARCHAR(64) | | السجل التجاري |
| phone | VARCHAR(20) | | الهاتف |
| email | VARCHAR(120) | | البريد الإلكتروني |
| address | TEXT | | العنوان |
| city | VARCHAR(64) | | المدينة |
| country | VARCHAR(64) | | الدولة |
| logo | VARCHAR(256) | | الشعار |
| is_active | BOOLEAN | DEFAULT TRUE | نشط؟ |
| created_at | DATETIME | DEFAULT NOW | تاريخ الإنشاء |

---

### Inventory Tables

#### products
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK | المعرف الفريد |
| name | VARCHAR(256) | NOT NULL | الاسم |
| name_en | VARCHAR(256) | | الاسم بالإنجليزية |
| code | VARCHAR(64) | UNIQUE, NOT NULL | الكود |
| barcode | VARCHAR(128) | UNIQUE | الباركود |
| sku | VARCHAR(64) | UNIQUE | SKU |
| category_id | INTEGER | FK(categories) | التصنيف |
| unit_id | INTEGER | FK(units) | الوحدة |
| description | TEXT | | الوصف |
| image | VARCHAR(256) | | الصورة |
| cost_price | FLOAT | DEFAULT 0.0 | سعر التكلفة |
| selling_price | FLOAT | DEFAULT 0.0 | سعر البيع |
| min_price | FLOAT | DEFAULT 0.0 | الحد الأدنى للسعر |
| tax_rate | FLOAT | DEFAULT 15.0 | نسبة الضريبة |
| is_active | BOOLEAN | DEFAULT TRUE | نشط؟ |
| track_inventory | BOOLEAN | DEFAULT TRUE | تتبع المخزون؟ |
| min_stock_level | FLOAT | DEFAULT 0.0 | الحد الأدنى للمخزون |
| max_stock_level | FLOAT | DEFAULT 0.0 | الحد الأقصى للمخزون |
| reorder_point | FLOAT | DEFAULT 0.0 | نقطة إعادة الطلب |
| created_at | DATETIME | DEFAULT NOW | تاريخ الإنشاء |
| updated_at | DATETIME | DEFAULT NOW | تاريخ التحديث |

**Indexes:**
- `idx_products_code` ON (code)
- `idx_products_barcode` ON (barcode)
- `idx_products_name` ON (name)

---

#### stock
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK | المعرف الفريد |
| product_id | INTEGER | FK(products) | المنتج |
| warehouse_id | INTEGER | FK(warehouses) | المستودع |
| quantity | FLOAT | DEFAULT 0.0 | الكمية |
| reserved_quantity | FLOAT | DEFAULT 0.0 | الكمية المحجوزة |
| available_quantity | FLOAT | DEFAULT 0.0 | الكمية المتاحة |
| last_updated | DATETIME | DEFAULT NOW | آخر تحديث |

**Unique Constraint:**
- `uq_stock_product_warehouse` ON (product_id, warehouse_id)

---

### Sales Tables

#### sales_invoices
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK | المعرف الفريد |
| invoice_number | VARCHAR(64) | UNIQUE, NOT NULL | رقم الفاتورة |
| invoice_date | DATE | NOT NULL | تاريخ الفاتورة |
| customer_id | INTEGER | FK(customers) | العميل |
| warehouse_id | INTEGER | FK(warehouses) | المستودع |
| subtotal | FLOAT | DEFAULT 0.0 | المجموع الفرعي |
| discount_amount | FLOAT | DEFAULT 0.0 | الخصم |
| tax_amount | FLOAT | DEFAULT 0.0 | الضريبة |
| total_amount | FLOAT | DEFAULT 0.0 | الإجمالي |
| paid_amount | FLOAT | DEFAULT 0.0 | المدفوع |
| remaining_amount | FLOAT | DEFAULT 0.0 | المتبقي |
| payment_status | VARCHAR(20) | DEFAULT 'unpaid' | حالة الدفع |
| status | VARCHAR(20) | DEFAULT 'draft' | الحالة |
| notes | TEXT | | ملاحظات |
| created_by | INTEGER | FK(users) | المنشئ |
| created_at | DATETIME | DEFAULT NOW | تاريخ الإنشاء |
| updated_at | DATETIME | DEFAULT NOW | تاريخ التحديث |

**Indexes:**
- `idx_sales_invoices_number` ON (invoice_number)
- `idx_sales_invoices_date` ON (invoice_date)

---

## 🔐 القيود والفهارس

### Primary Keys
جميع الجداول لها مفتاح أساسي `id` من نوع INTEGER AUTO_INCREMENT.

### Foreign Keys
جميع المفاتيح الأجنبية مع `ON DELETE RESTRICT` لمنع الحذف العرضي.

### Unique Constraints
- أكواد المنتجات والعملاء والموردين
- أرقام الفواتير
- أسماء المستخدمين والبريد الإلكتروني

### Indexes
فهارس على:
- جميع المفاتيح الأساسية والأجنبية
- حقول البحث الشائعة (الأسماء، الأكواد)
- حقول التواريخ

---

## 📊 إحصائيات متوقعة

| Table | Estimated Rows | Growth Rate |
|-------|---------------|-------------|
| users | 10-100 | Low |
| products | 1,000-10,000 | Medium |
| customers | 500-5,000 | Medium |
| sales_invoices | 10,000-100,000 | High |
| stock_movements | 50,000-500,000 | High |
| journal_entries | 20,000-200,000 | High |

---

**آخر تحديث:** 2026-01-10

