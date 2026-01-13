# API Documentation

## نظرة عامة

هذا التوثيق يشرح كيفية استخدام API الخاص بنظام إدارة المخزون المتكامل.

**ملاحظة:** API قيد التطوير وسيتم إضافته في الإصدارات القادمة.

## المصادقة (Authentication)

سيتم استخدام JWT (JSON Web Tokens) للمصادقة.

### الحصول على Token

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "expires_in": 3600
}
```

### استخدام Token

```http
GET /api/v1/products
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

---

## Endpoints

### Products (المنتجات)

#### Get All Products
```http
GET /api/v1/products
```

**Query Parameters:**
- `page` (int): رقم الصفحة (افتراضي: 1)
- `per_page` (int): عدد العناصر في الصفحة (افتراضي: 20)
- `search` (string): البحث في الاسم أو الكود
- `category_id` (int): تصفية حسب التصنيف

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "code": "PRD001",
      "name": "منتج تجريبي",
      "name_en": "Sample Product",
      "category_id": 1,
      "unit_id": 1,
      "cost_price": 100.00,
      "selling_price": 150.00,
      "is_active": true
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "pages": 5
  }
}
```

#### Get Product by ID
```http
GET /api/v1/products/{id}
```

#### Create Product
```http
POST /api/v1/products
Content-Type: application/json

{
  "code": "PRD002",
  "name": "منتج جديد",
  "name_en": "New Product",
  "category_id": 1,
  "unit_id": 1,
  "cost_price": 100.00,
  "selling_price": 150.00
}
```

#### Update Product
```http
PUT /api/v1/products/{id}
Content-Type: application/json

{
  "name": "منتج محدث",
  "selling_price": 160.00
}
```

#### Delete Product
```http
DELETE /api/v1/products/{id}
```

---

### Customers (العملاء)

#### Get All Customers
```http
GET /api/v1/customers
```

#### Get Customer by ID
```http
GET /api/v1/customers/{id}
```

#### Create Customer
```http
POST /api/v1/customers
Content-Type: application/json

{
  "code": "CUST001",
  "name": "عميل جديد",
  "email": "customer@example.com",
  "phone": "0501234567"
}
```

---

### Sales Invoices (فواتير البيع)

#### Get All Invoices
```http
GET /api/v1/sales/invoices
```

#### Create Invoice
```http
POST /api/v1/sales/invoices
Content-Type: application/json

{
  "customer_id": 1,
  "invoice_date": "2026-01-10",
  "items": [
    {
      "product_id": 1,
      "quantity": 5,
      "unit_price": 150.00
    }
  ]
}
```

---

### Stock (المخزون)

#### Get Stock Levels
```http
GET /api/v1/stock
```

**Query Parameters:**
- `warehouse_id` (int): تصفية حسب المستودع
- `product_id` (int): تصفية حسب المنتج

---

### Reports (التقارير)

#### Sales Report
```http
GET /api/v1/reports/sales
```

**Query Parameters:**
- `start_date` (date): تاريخ البداية
- `end_date` (date): تاريخ النهاية
- `customer_id` (int): تصفية حسب العميل

---

## Error Handling

جميع الأخطاء تُرجع بالصيغة التالية:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "البيانات المدخلة غير صحيحة",
    "details": {
      "name": ["هذا الحقل مطلوب"]
    }
  }
}
```

### Error Codes

- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

---

## Rate Limiting

- **الحد الأقصى:** 100 طلب في الدقيقة
- **Headers:**
  - `X-RateLimit-Limit`: الحد الأقصى
  - `X-RateLimit-Remaining`: الطلبات المتبقية
  - `X-RateLimit-Reset`: وقت إعادة التعيين

---

## Webhooks (قيد التطوير)

سيتم دعم Webhooks للأحداث التالية:
- إنشاء فاتورة جديدة
- تحديث المخزون
- إضافة عميل جديد

---

**ملاحظة:** هذا التوثيق قيد التطوير وسيتم تحديثه مع إضافة ميزات جديدة.

